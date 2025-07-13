from flask_restx import fields
from pothole.schemas import create_pothole_schemas

def create_raspberry_schemas(api):
    """Raspberry 관련 스키마들을 생성"""

    pothole_model = create_pothole_schemas(api)['pothole_model']
    
    # 기본 Raspberry 모델
    raspberry_model = api.model('Raspberry', {
        'id': fields.String(readonly=True, description='Raspberry ID'),
        'name': fields.String(required=True, description='Raspberry 이름'),
        'ip': fields.String(required=True, description='IP 주소'),
        'port': fields.Integer(required=True, description='포트 번호'),
        'status': fields.String(description='상태 (online/offline)'),
        'user_id': fields.Integer(required=True, description='소유자 ID'),
        'created_at': fields.String(readonly=True, description='생성일시'),
        'potholes': fields.List(fields.Nested(pothole_model), description='PotHole 목록')
    })
    
    # Raspberry 생성 모델
    raspberry_create_model = api.model('RaspberryCreate', {
        'id': fields.String(required=True, description='Raspberry ID'),
        'name': fields.String(required=True, description='Raspberry 이름'),
        'ip': fields.String(required=True, description='IP 주소'),
        'port': fields.Integer(required=True, description='포트 번호')
    })
    
    # Raspberry 수정 모델
    raspberry_update_model = api.model('RaspberryUpdate', {
        'name': fields.String(description='Raspberry 이름'),
        'ip': fields.String(description='IP 주소'),
        'port': fields.Integer(description='포트 번호'),
        'status': fields.String(description='상태 (online/offline)')
    })
    
    # Raspberry 목록 응답 모델
    raspberry_list_model = api.model('RaspberryList', {
        'raspberries': fields.List(fields.Nested(raspberry_model), description='Raspberry 목록'),
        'total': fields.Integer(description='총 개수')
    })
    
    # Raspberry 상태 체크 모델
    raspberry_status_model = api.model('RaspberryStatus', {
        'id': fields.Integer(readonly=True, description='상태 체크 ID'),
        'raspberry_id': fields.String(required=True, description='Raspberry ID'),
        'is_online': fields.Boolean(required=True, description='온라인 여부'),
        'response_time': fields.Float(description='응답 시간 (초)'),
        'success_count': fields.Integer(description='성공한 ping 횟수'),
        'total_attempts': fields.Integer(description='총 시도 횟수'),
        'error_message': fields.String(description='에러 메시지'),
        'checked_at': fields.String(readonly=True, description='체크 일시')
    })
    
    # Raspberry 상태 체크 목록 모델
    raspberry_status_list_model = api.model('RaspberryStatusList', {
        'raspberry_id': fields.String(description='Raspberry ID'),
        'raspberry_name': fields.String(description='Raspberry 이름'),
        'status_checks': fields.List(fields.Nested(raspberry_status_model), description='상태 체크 이력'),
        'total': fields.Integer(description='총 개수')
    })
    
    # 일반 응답 모델
    response_model = api.model('Response', {
        'message': fields.String(description='응답 메시지'),
        'error': fields.String(description='에러 메시지')
    })
    
    return {
        'raspberry_model': raspberry_model,
        'raspberry_create_model': raspberry_create_model,
        'raspberry_update_model': raspberry_update_model,
        'raspberry_list_model': raspberry_list_model,
        'raspberry_status_model': raspberry_status_model,
        'raspberry_status_list_model': raspberry_status_list_model,
        'response_model': response_model
    } 