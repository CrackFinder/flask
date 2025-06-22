from flask_restx import fields

def create_common_schemas(api):
    """공통 응답 스키마들을 생성"""
    
    # 일반 응답 모델
    response_model = api.model('Response', {
        'message': fields.String(description='응답 메시지'),
        'error': fields.String(description='에러 메시지')
    })
    
    # 성공 응답 모델
    success_model = api.model('Success', {
        'message': fields.String(description='성공 메시지'),
        'data': fields.Raw(description='응답 데이터')
    })
    
    # 에러 응답 모델
    error_model = api.model('Error', {
        'error': fields.String(description='에러 메시지'),
        'code': fields.String(description='에러 코드')
    })
    
    return {
        'response_model': response_model,
        'success_model': success_model,
        'error_model': error_model
    } 