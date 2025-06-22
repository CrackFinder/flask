from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_restx import Api, Resource, fields
import bcrypt
from db import db, User
from schemas import create_all_schemas
import os
from datetime import timedelta

app = Flask(__name__)
CORS(app)

# Flask-RESTX 설정
api = Api(app, version='1.0', title='Flask API', description='Flask API 문서')

# 네임스페이스 생성
ns = api.namespace('api', description='API 엔드포인트')

# 스키마 생성
schemas = create_all_schemas(api)

# 개별 스키마 추출
user_model = schemas['user_model']
register_model = schemas['register_model']
login_model = schemas['login_model']
login_response_model = schemas['login_response_model']
response_model = schemas['response_model']

# 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your-secret-key')  # 실제 운영시에는 환경변수로 관리
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

# 초기화
db.init_app(app)
jwt = JWTManager(app)

# 데이터베이스 생성
with app.app_context():
    db.create_all()

@ns.route('/register')
class Register(Resource):
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

@ns.route('/login')
class Login(Resource):
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

@ns.route('/user')
class UserInfo(Resource):
    @ns.doc('사용자 정보 조회', security='Bearer')
    @ns.response(200, '사용자 정보 조회 성공', user_model)
    @ns.response(401, '인증 실패', response_model)
    @ns.response(404, '사용자를 찾을 수 없음', response_model)
    @jwt_required()
    def get(self):
        """사용자 정보 조회 API"""
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return {'error': '사용자를 찾을 수 없습니다'}, 404
        
        return user.to_dict(), 200

if __name__ == '__main__':
    app.run(debug=True)
