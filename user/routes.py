from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import User

# 스키마는 나중에 주입받을 예정
user_model = None
response_model = None

def init_user_schemas(schemas):
    """스키마 초기화"""
    global user_model, response_model
    user_model = schemas['user_model']
    response_model = schemas['response_model']

class UserInfo(Resource):
    @staticmethod
    def init(ns):
        @ns.route('/user')
        class UserInfoRoute(UserInfo):
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

def init_user_routes(api, schemas):
    """User 라우트 초기화"""
    init_user_schemas(schemas)
    
    # User 네임스페이스 생성
    user_ns = api.namespace('user', description='사용자 관련 API')
    
    # 라우트 등록
    UserInfo.init(user_ns) 