import os
from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from datetime import datetime
from core.db import db
from auth.models import User
from raspberry.models import Raspberry
from pothole.models import PotHole
import json

# 스키마는 나중에 주입받을 예정
pothole_model = None
pothole_create_model = None
pothole_update_model = None
pothole_list_model = None
pothole_response_model = None
response_model = None

def init_pothole_schemas(schemas):
    """스키마 초기화"""
    global pothole_model, pothole_create_model, pothole_update_model, pothole_list_model, pothole_response_model, response_model
    pothole_model = schemas['pothole_model']
    pothole_create_model = schemas['pothole_create_model']
    pothole_update_model = schemas['pothole_update_model']
    pothole_list_model = schemas['pothole_list_model']
    pothole_response_model = schemas['pothole_response_model']
    response_model = schemas['response_model']

# 동영상 업로드 설정
UPLOAD_FOLDER = 'uploads/potholes'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv', 'flv', 'webm', 'mkv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 업로드 폴더 생성
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class PotHoleList(Resource):
    @staticmethod
    def init(ns):
        @ns.route('/potholes')
        class PotHoleListRoute(PotHoleList):
            @ns.doc('사용자의 PotHole 목록 조회', security='Bearer')
            @ns.response(200, '조회 성공', pothole_list_model)
            @ns.response(401, '인증 실패', response_model)
            @jwt_required()
            def get(self):
                """사용자의 PotHole 목록 조회"""
                current_user_id = get_jwt_identity()
                
                # 사용자의 모든 Raspberry의 PotHole 조회
                potholes = db.session.query(PotHole).join(Raspberry).filter(Raspberry.user_id == current_user_id).all()
                
                return {
                    'potholes': [pothole.to_dict() for pothole in potholes],
                    'total': len(potholes)
                }, 200

class PotHoleCreate(Resource):
    @staticmethod
    def init(ns):
        @ns.route('/potholes')
        class PotHoleCreateRoute(PotHoleCreate):
            @ns.doc('PotHole 생성 (동영상 + 위치 정보)', security='Bearer')
            @ns.expect(pothole_create_model)
            @ns.response(201, '생성 성공', pothole_response_model)
            @ns.response(400, '잘못된 요청', response_model)
            @ns.response(401, '인증 실패', response_model)
            @ns.response(404, 'Raspberry를 찾을 수 없음', response_model)
            def post(self):
                
                """PotHole 생성 (동영상 파일 + 위치 정보)"""

                # 폼 데이터에서 정보 추출
                json_data = json.loads(request.form.get('json'))
                raspberry_id = json_data['raspberry_id']
                address = json_data['address']
                latitude = json_data['latitude']
                longitude = json_data['longitude']

                # 필수 필드 확인
                if not all([raspberry_id, address, latitude, longitude]):
                    return {'error': 'raspberry_id, address, latitude, longitude는 필수입니다'}, 400
                
                # 동영상 파일 확인
                if 'video' not in request.files:
                    return {'error': '동영상 파일이 필요합니다'}, 400
                
                video_file = request.files['video']
                if video_file.filename == '':
                    return {'error': '선택된 파일이 없습니다'}, 400
                
                if not allowed_file(video_file.filename):
                    return {'error': '허용되지 않는 파일 형식입니다 (mp4, avi, mov, wmv, flv, webm, mkv만 가능)'}, 400
                
                # Raspberry가 사용자의 것인지 확인

                # 새 PotHole 생성
                new_pothole = PotHole(
                    address=address,
                    latitude=float(latitude),
                    longitude=float(longitude),
                    raspberry_id=raspberry_id
                )
                
                db.session.add(new_pothole)
                db.session.flush()  # ID 생성을 위해 flush
                
                # 동영상 파일 저장
                filename = secure_filename(video_file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                new_filename = f"pothole_{new_pothole.id}_{timestamp}_{filename}"
                file_path = os.path.join(UPLOAD_FOLDER, new_filename)
                
                video_file.save(file_path)
                
                # 동영상 경로 업데이트
                new_pothole.video_path = file_path
                db.session.commit()
                
                return {
                    'message': 'PotHole이 성공적으로 생성되었습니다',
                    'pothole': new_pothole.to_dict(),
                    'video_info': {
                        'filename': filename,
                        'file_size': os.path.getsize(file_path),
                        'uploaded_at': datetime.now().isoformat()
                    }
                }, 201

class PotHoleDetail(Resource):
    @staticmethod
    def init(ns):
        @ns.route('/potholes/<int:pothole_id>')
        class PotHoleDetailRoute(PotHoleDetail):
            @ns.doc('PotHole 상세 조회', security='Bearer')
            @ns.response(200, '조회 성공', pothole_model)
            @ns.response(401, '인증 실패', response_model)
            @ns.response(404, 'PotHole을 찾을 수 없음', response_model)
            @jwt_required()
            def get(self, pothole_id):
                """PotHole 상세 조회"""
                current_user_id = get_jwt_identity()
                
                pothole = db.session.query(PotHole).join(Raspberry).filter(
                    PotHole.id == pothole_id,
                    Raspberry.user_id == current_user_id
                ).first()
                
                if not pothole:
                    return {'error': 'PotHole을 찾을 수 없습니다'}, 404
                
                return pothole.to_dict(), 200
            
            @ns.doc('PotHole 수정 (선택적 필드)', security='Bearer')
            @ns.response(200, '수정 성공', pothole_response_model)
            @ns.response(400, '잘못된 요청', response_model)
            @ns.response(401, '인증 실패', response_model)
            @ns.response(404, 'PotHole을 찾을 수 없음', response_model)
            @jwt_required()
            def put(self, pothole_id):
                """PotHole 수정 (동영상, 위치 정보 선택적 제공)"""
                current_user_id = get_jwt_identity()
                
                pothole = db.session.query(PotHole).join(Raspberry).filter(
                    PotHole.id == pothole_id,
                    Raspberry.user_id == current_user_id
                ).first()
                
                if not pothole:
                    return {'error': 'PotHole을 찾을 수 없습니다'}, 404
                
                video_info = None
                
                # 동영상 파일이 제공된 경우
                if 'video' in request.files:
                    file = request.files['video']
                    if file.filename != '':
                        if not allowed_file(file.filename):
                            return {'error': '허용되지 않는 파일 형식입니다 (mp4, avi, mov, wmv, flv, webm, mkv만 가능)'}, 400
                        
                        # 기존 동영상 파일 삭제
                        if pothole.video_path and os.path.exists(pothole.video_path):
                            os.remove(pothole.video_path)
                        
                        # 새 동영상 파일 저장
                        filename = secure_filename(file.filename)
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        new_filename = f"pothole_{pothole_id}_{timestamp}_{filename}"
                        file_path = os.path.join(UPLOAD_FOLDER, new_filename)
                        
                        file.save(file_path)
                        pothole.video_path = file_path
                        
                        video_info = {
                            'filename': filename,
                            'file_size': os.path.getsize(file_path),
                            'uploaded_at': datetime.now().isoformat()
                        }
                
                # 폼 데이터에서 위치 정보 업데이트
                if 'address' in request.form:
                    pothole.address = request.form['address']
                
                if 'latitude' in request.form:
                    pothole.latitude = float(request.form['latitude'])
                
                if 'longitude' in request.form:
                    pothole.longitude = float(request.form['longitude'])
                
                db.session.commit()
                
                return {
                    'message': 'PotHole이 성공적으로 수정되었습니다',
                    'pothole': pothole.to_dict(),
                    'video_info': video_info
                }, 200
            
            @ns.doc('PotHole 삭제', security='Bearer')
            @ns.response(200, '삭제 성공', response_model)
            @ns.response(401, '인증 실패', response_model)
            @ns.response(404, 'PotHole을 찾을 수 없음', response_model)
            @jwt_required()
            def delete(self, pothole_id):
                """PotHole 삭제"""
                current_user_id = get_jwt_identity()
                
                pothole = db.session.query(PotHole).join(Raspberry).filter(
                    PotHole.id == pothole_id,
                    Raspberry.user_id == current_user_id
                ).first()
                
                if not pothole:
                    return {'error': 'PotHole을 찾을 수 없습니다'}, 404
                
                # 동영상 파일 삭제
                if pothole.video_path and os.path.exists(pothole.video_path):
                    os.remove(pothole.video_path)
                
                # 데이터베이스에서 삭제
                db.session.delete(pothole)
                db.session.commit()
                
                return {'message': 'PotHole이 성공적으로 삭제되었습니다'}, 200

def init_pothole_routes(api, schemas):
    """PotHole 라우트 초기화"""
    init_pothole_schemas(schemas)
    
    # PotHole 네임스페이스 생성
    pothole_ns = api.namespace('pothole', description='PotHole 관련 API')
    
    # 라우트 등록
    PotHoleList.init(pothole_ns)
    PotHoleCreate.init(pothole_ns)
    PotHoleDetail.init(pothole_ns) 