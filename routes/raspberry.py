from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import Raspberry, db

def create_raspberry_routes(ns, schemas):
    """라즈베리 파이용 라우트 생성"""
    
    raspberry_model = schemas['raspberry_model']
    response_model = schemas['response_model']
    
    @ns.route('/raspberry')
    class RaspberryInfo(Resource):
        @ns.doc('라즈베리파이 정보 조회', security='Bearer')
        @ns.response(200, '라즈베리파이 정보 조회 성공', raspberry_model)
        @ns.response(401, '인증 실패', response_model)
        @ns.response(404, '라즈베리파이를 찾을 수 없음', response_model)
        @jwt_required()
        def get(self):
            """라즈베리파이 정보 조회 API"""
            data = request.get_json()
            raspberry = Raspberry.query.get(data['id'])
            
            if not raspberry:
                return {'error': '라즈베리파이를 찾을 수 없습니다'}, 404
            
            return raspberry.to_dict(), 200
        
        @ns.expect(raspberry_model)
        @ns.response(201, '라즈베리파이 정보 추가 성공', response_model)
        @ns.response(400, '잘못된 요청', response_model)
        def post(self):
            """라즈베리파이 정보 추가 API"""
            data = request.get_json()
            raspberry = Raspberry(**data)
            db.session.add(raspberry)
            db.session.commit()
            return {'message': '라즈베리파이 정보가 추가되었습니다'}, 201
        
    return RaspberryInfo
    
    