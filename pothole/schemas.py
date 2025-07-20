from flask_restx import fields

def create_pothole_schemas(api):
    """PotHole 관련 스키마들을 생성"""

    # 기본 PotHole 모델
    pothole_model = api.model('PotHole', {
        'id': fields.Integer(readonly=True, description='PotHole ID'),
        'video_path': fields.String(required=True, description='동영상 파일 경로'),
        'address': fields.String(required=True, description='주소'),
        'latitude': fields.Float(required=True, description='GPS 위도'),
        'longitude': fields.Float(required=True, description='GPS 경도'),
        'status': fields.String(required=True, description='처리 상태 (처리완료/미처리)'),
        'raspberry_id': fields.String(required=True, description='Raspberry ID'),
        'created_at': fields.String(readonly=True, description='생성일시'),
        'updated_at': fields.String(readonly=True, description='수정일시')
    })

    # PotHole 생성 모델 (동영상 + 위치 정보). 라즈베리파이에서 포트홀 비디오 하나나를 추가할때 사용
    pothole_create_model = api.model('PotHoleCreate', {
        'video': fields.Raw(required=True, description='동영상 파일 (multipart/form-data)'),
        'raspberry_id': fields.String(required=True, description='Raspberry ID'),
        'address': fields.String(required=True, description='주소'),
        'latitude': fields.Float(required=True, description='GPS 위도'),
        'longitude': fields.Float(required=True, description='GPS 경도')
    })

    # PotHole 수정 모델 (선택적 필드)
    pothole_update_model = api.model('PotHoleUpdate', {
        'video': fields.Raw(description='동영상 파일 (multipart/form-data, 선택사항)'),
        'address': fields.String(description='주소'),
        'latitude': fields.Float(description='GPS 위도'),
        'longitude': fields.Float(description='GPS 경도')
    })

    # PotHole 상태 업데이트 모델
    pothole_status_update_model = api.model('PotHoleStatusUpdate', {
        'status': fields.String(required=True, enum=['처리완료', '미처리'], description='처리 상태')
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
        'video_info': fields.Raw(description='동영상 정보 (파일명, 크기 등)')
    })

    # 일반 응답 모델
    response_model = api.model('Response', {
        'message': fields.String(description='응답 메시지'),
        'error': fields.String(description='에러 메시지')
    })

    return {
        'pothole_model': pothole_model,
        'pothole_create_model': pothole_create_model,
        'pothole_update_model': pothole_update_model,
        'pothole_status_update_model': pothole_status_update_model,
        'pothole_list_model': pothole_list_model,
        'pothole_response_model': pothole_response_model,
        'response_model': response_model
    } 