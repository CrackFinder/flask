from flask_restx import fields

def create_raspberry_schemas(api):
    """라즈베리파이 관련 스키마들을 생성"""

    # 라즈베리파이 모델 ( 수정될 수 있음 )
    raspberry_model = api.model('Raspberry', {
        'id': fields.Integer(readonly=True, description='라즈베리파이 ID'),
        'name': fields.String(required=True, description='라즈베리파이 이름'),
        'ip': fields.String(required=True, description='라즈베리파이 IP 주소'),
        'port': fields.Integer(required=True, description='라즈베리파이 포트 번호'),
    })

    return {'raspberry_model': raspberry_model}