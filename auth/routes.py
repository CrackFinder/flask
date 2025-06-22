from flask import request
from flask_restx import Resource
from flask_jwt_extended import create_access_token
import bcrypt
from db import db, User

# 스키마는 나중에 주입받을 예정
register_model = None
login_model = None
login_response_model = None
response_model = None

def init_auth_schemas(schemas):
    """스키마 초기화"""
    global register_model, login_model, login_response_model, response_model
    register_model = schemas['register_model']
    login_model = schemas['login_model']
    login_response_model = schemas['login_response_model']
    response_model = schemas['response_model']

class Register(Resource):
    @staticmethod
    def init(ns):
        @ns.route('/register')
        class RegisterRoute(Register):
            @ns.doc('회원가입')
            @ns.expect(register_model)
            @ns.response(201, '회원가입 성공', response_model)
            @ns.response(400, '잘못된 요청', response_model)
            def post(self):
                """회원가입 API"""
                data = request.get_json()
                
                # 필수 필드 확인
                if not all(k in data for k in ['username', 'email', 'password']):
                    return {'error': '모든 필드를 입력해주세요'}, 400
                
                # 이메일 중복 확인
                if User.query.filter_by(email=data['email']).first():
                    return {'error': '이미 등록된 이메일입니다'}, 400
                
                # 사용자명 중복 확인
                if User.query.filter_by(username=data['username']).first():
                    return {'error': '이미 사용중인 사용자명입니다'}, 400
                
                # 비밀번호 해싱
                hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
                
                # 새 사용자 생성
                new_user = User(
                    username=data['username'],
                    email=data['email'],
                    password=hashed_password.decode('utf-8')
                )
                
                db.session.add(new_user)
                db.session.commit()
                
                return {'message': '회원가입이 완료되었습니다'}, 201

class Login(Resource):
    @staticmethod
    def init(ns):
        @ns.route('/login')
        class LoginRoute(Login):
            @ns.doc('로그인')
            @ns.expect(login_model)
            @ns.response(200, '로그인 성공', login_response_model)
            @ns.response(400, '잘못된 요청', response_model)
            @ns.response(401, '인증 실패', response_model)
            def post(self):
                """로그인 API"""
                data = request.get_json()
                
                if not all(k in data for k in ['email', 'password']):
                    return {'error': '이메일과 비밀번호를 입력해주세요'}, 400
                
                user = User.query.filter_by(email=data['email']).first()
                
                if not user or not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                    return {'error': '이메일 또는 비밀번호가 올바르지 않습니다'}, 401
                
                # JWT 토큰 생성
                print(f'userid {user.id} {type(user.id)}')
                access_token = create_access_token(identity=f'{user.id}')
                print(f'토큰 : {access_token}')
                
                return {
                    'access_token': access_token,
                    'user': user.to_dict()
                }, 200

def init_auth_routes(api, schemas):
    """Auth 라우트 초기화"""
    init_auth_schemas(schemas)
    
    # Auth 네임스페이스 생성
    auth_ns = api.namespace('auth', description='인증 관련 API')
    
    # 라우트 등록
    Register.init(auth_ns)
    Login.init(auth_ns) 