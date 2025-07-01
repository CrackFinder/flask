from flask_restx import fields

def create_raspberry_schemas(api):
    """Raspberry 관련 스키마들을 생성"""
    
    # 기본 Raspberry 모델
    raspberry_model = api.model('Raspberry', {
        'id': fields.String(readonly=True, description='Raspberry ID'),
        'name': fields.String(required=True, description='Raspberry 이름'),
        'ip': fields.String(required=True, description='IP 주소'),
        'port': fields.Integer(required=True, description='포트 번호'),
        'status': fields.String(description='상태 (online/offline)'),
        'user_id': fields.Integer(required=True, description='소유자 ID'),
        'created_at': fields.String(readonly=True, description='생성일시')
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
        'response_model': response_model
    } 