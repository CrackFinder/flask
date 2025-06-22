from flask_restx import fields

def create_user_schemas(api):
    """사용자 관련 스키마들을 생성"""
    
    # 기본 사용자 모델
    user_model = api.model('User', {
        'id': fields.Integer(readonly=True, description='사용자 ID'),
        'username': fields.String(required=True, description='사용자명'),
        'email': fields.String(required=True, description='이메일 주소'),
        'created_at': fields.String(readonly=True, description='생성일시')
    })
    
    # 일반 응답 모델
    response_model = api.model('Response', {
        'message': fields.String(description='응답 메시지'),
        'error': fields.String(description='에러 메시지')
    })
    
    return {
        'user_model': user_model,
        'response_model': response_model
    } 