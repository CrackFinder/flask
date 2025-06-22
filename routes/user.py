from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import User

def create_user_routes(ns, schemas):
    """사용자 관련 라우트 생성"""
    
    # 스키마 추출
    user_model = schemas['user_model']
    response_model = schemas['response_model']
    
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
    
    return UserInfo 