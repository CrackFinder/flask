from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from core.db import db
from auth.models import User
from raspberry.models import Raspberry

# 스키마는 나중에 주입받을 예정
raspberry_model = None
raspberry_create_model = None
raspberry_update_model = None
raspberry_list_model = None
response_model = None

def init_raspberry_schemas(schemas):
    """스키마 초기화"""
    global raspberry_model, raspberry_create_model, raspberry_update_model, raspberry_list_model, response_model
    raspberry_model = schemas['raspberry_model']
    raspberry_create_model = schemas['raspberry_create_model']
    raspberry_update_model = schemas['raspberry_update_model']
    raspberry_list_model = schemas['raspberry_list_model']
    response_model = schemas['response_model']

class RaspberryCreate(Resource):
    @staticmethod
    def init(ns):
        @ns.route('/raspberry')
        class RaspberryCreateRoute(RaspberryCreate):
            @ns.doc('Raspberry 생성', security='Bearer')
            @ns.expect(raspberry_create_model)
            @ns.response(201, '생성 성공', raspberry_model)
            @ns.response(400, '잘못된 요청', response_model)
            @ns.response(401, '인증 실패', response_model)
            @jwt_required()
            def post(self):
                """Raspberry 생성"""
                current_user_id = int(get_jwt_identity())
                data = request.get_json()
                
                # 필수 필드 확인
                if not all(k in data for k in ['id', 'name', 'ip', 'port']):
                    return {'error': 'id, name, ip, port는 필수입니다'}, 400
                
                # ID 중복 확인
                if Raspberry.query.filter_by(id=data['id']).first():
                    return {'error': '이미 존재하는 ID입니다'}, 400
                
                # 같은 사용자의 중복 이름 확인
                if Raspberry.query.filter_by(user_id=current_user_id, name=data['name']).first():
                    return {'error': '이미 존재하는 이름입니다'}, 400
                
                # 새 Raspberry 생성
                new_raspberry = Raspberry(
                    id=data['id'],
                    name=data['name'],
                    ip=data['ip'],
                    port=data['port'],
                    user_id=current_user_id
                )
                
                db.session.add(new_raspberry)
                db.session.commit()
                
                return new_raspberry.to_dict(), 201
            
            @ns.doc('사용자의 Raspberry 목록 조회', security='Bearer')
            @ns.expect(raspberry_list_model)
            @ns.response(200, '조회 성공', raspberry_list_model)
            @ns.response(401, '인증 실패', response_model)
            @jwt_required()
            def get(self):
                """사용자의 Raspberry 목록 조회"""
                current_user_id = get_jwt_identity()
                
                raspberries = Raspberry.query.filter_by(user_id=current_user_id).all()
                
                return {
                    'raspberries': [raspberry.to_dict() for raspberry in raspberries],
                    'total': len(raspberries)
                }, 200

class RaspberryDetail(Resource):
    @staticmethod
    def init(ns):
        @ns.route('/raspberry/<string:raspberry_id>')
        class RaspberryDetailRoute(RaspberryDetail):
            @ns.doc('Raspberry 상세 조회', security='Bearer')
            @ns.response(200, '조회 성공', raspberry_model)
            @ns.response(401, '인증 실패', response_model)
            @ns.response(404, 'Raspberry를 찾을 수 없음', response_model)
            @jwt_required()
            def get(self, raspberry_id):
                """Raspberry 상세 조회"""
                current_user_id = get_jwt_identity()
                
                raspberry = Raspberry.query.filter_by(id=raspberry_id, user_id=current_user_id).first()
                
                if not raspberry:
                    return {'error': 'Raspberry를 찾을 수 없습니다'}, 404
                
                return raspberry.to_dict(), 200
            
            @ns.doc('Raspberry 수정', security='Bearer')
            @ns.expect(raspberry_update_model)
            @ns.response(200, '수정 성공', raspberry_model)
            @ns.response(400, '잘못된 요청', response_model)
            @ns.response(401, '인증 실패', response_model)
            @ns.response(404, 'Raspberry를 찾을 수 없음', response_model)
            @jwt_required()
            def put(self, raspberry_id):
                """Raspberry 수정"""
                current_user_id = get_jwt_identity()
                data = request.get_json()
                
                raspberry = Raspberry.query.filter_by(id=raspberry_id, user_id=current_user_id).first()
                
                if not raspberry:
                    return {'error': 'Raspberry를 찾을 수 없습니다'}, 404
                
                # 수정할 필드 업데이트
                if 'name' in data:
                    # 같은 사용자의 중복 이름 확인 (자신 제외)
                    existing = Raspberry.query.filter_by(user_id=current_user_id, name=data['name']).first()
                    if existing and existing.id != raspberry_id:
                        return {'error': '이미 존재하는 이름입니다'}, 400
                    raspberry.name = data['name']
                
                if 'ip' in data:
                    raspberry.ip = data['ip']
                
                if 'port' in data:
                    raspberry.port = data['port']
                
                if 'status' in data:
                    raspberry.status = data['status']
                
                db.session.commit()
                
                return raspberry.to_dict(), 200
            
            @ns.doc('Raspberry 삭제', security='Bearer')
            @ns.response(200, '삭제 성공', response_model)
            @ns.response(401, '인증 실패', response_model)
            @ns.response(404, 'Raspberry를 찾을 수 없음', response_model)
            @jwt_required()
            def delete(self, raspberry_id):
                """Raspberry 삭제"""
                current_user_id = get_jwt_identity()
                
                raspberry = Raspberry.query.filter_by(id=raspberry_id, user_id=current_user_id).first()
                
                if not raspberry:
                    return {'error': 'Raspberry를 찾을 수 없습니다'}, 404
                
                db.session.delete(raspberry)
                db.session.commit()
                
                return {'message': 'Raspberry가 삭제되었습니다'}, 200

def init_raspberry_routes(api, schemas):
    """Raspberry 라우트 초기화"""
    init_raspberry_schemas(schemas)
    
    # Raspberry 네임스페이스 생성
    raspberry_ns = api.namespace('raspberry', description='Raspberry 관련 API')
    
    # 라우트 등록
    RaspberryCreate.init(raspberry_ns)
    RaspberryDetail.init(raspberry_ns) 