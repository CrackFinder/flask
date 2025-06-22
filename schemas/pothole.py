from flask_restx import fields

def create_pothole_schemas(api):
    """PotHole 관련 스키마들을 생성"""
    
    # 기본 PotHole 모델
    pothole_model = api.model('PotHole', {
        'id': fields.Integer(readonly=True, description='PotHole ID'),
        'image_path': fields.String(required=True, description='이미지 파일 경로'),
        'address': fields.String(required=True, description='주소'),
        'latitude': fields.Float(required=True, description='GPS 위도'),
        'longitude': fields.Float(required=True, description='GPS 경도'),
        'raspberry_id': fields.Integer(required=True, description='Raspberry ID'),
        'created_at': fields.String(readonly=True, description='생성일시')
    })
    
    # PotHole 생성 모델 (이미지 + 위치 정보)
    pothole_create_model = api.model('PotHoleCreate', {
        'address': fields.String(required=True, description='주소'),
        'latitude': fields.Float(required=True, description='GPS 위도'),
        'longitude': fields.Float(required=True, description='GPS 경도'),
    })
    
    # PotHole 수정 모델 (선택적 필드)
    pothole_update_model = api.model('PotHoleUpdate', {
        'address': fields.String(description='주소'),
        'latitude': fields.Float(description='GPS 위도'),
        'longitude': fields.Float(description='GPS 경도'),
    })
    
    # PotHole 목록 응답 모델
    pothole_list_model = api.model('PotHoleList', {
        'potholes': fields.List(fields.Nested(pothole_model), description='PotHole 목록'),
        'total': fields.Integer(description='총 개수')
    })
    
    # PotHole 생성/수정 응답 모델
    pothole_response_model = api.model('PotHoleResponse', {
        'message': fields.String(description='응답 메시지'),
        'pothole': fields.Nested(pothole_model, description='PotHole 정보'),
        'image_info': fields.Raw(description='이미지 정보 (파일명, 크기 등)')
    })
    
    return {
        'pothole_model': pothole_model,
        'pothole_create_model': pothole_create_model,
        'pothole_update_model': pothole_update_model,
        'pothole_list_model': pothole_list_model,
        'pothole_response_model': pothole_response_model
    } 