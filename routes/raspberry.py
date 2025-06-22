from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db, User, Raspberry

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
                current_user_id = get_jwt_identity()
                data = request.get_json()
                
                # 필수 필드 확인
                if not all(k in data for k in ['name', 'ip', 'port']):
                    return {'error': '모든 필드를 입력해주세요'}, 400
                
                # 같은 사용자의 중복 이름 확인
                if Raspberry.query.filter_by(user_id=current_user_id, name=data['name']).first():
                    return {'error': '이미 존재하는 이름입니다'}, 400
                
                # 새 Raspberry 생성
                new_raspberry = Raspberry(
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
        @ns.route('/raspberry/<int:raspberry_id>')
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
    
    