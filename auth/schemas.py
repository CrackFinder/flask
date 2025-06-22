from flask_restx import fields

def create_auth_schemas(api):
    """Auth 관련 스키마들을 생성"""
    
    # 회원가입 모델
    register_model = api.model('Register', {
        'username': fields.String(required=True, description='사용자명'),
        'email': fields.String(required=True, description='이메일'),
        'password': fields.String(required=True, description='비밀번호')
    })
    
    # 로그인 모델
    login_model = api.model('Login', {
        'email': fields.String(required=True, description='이메일'),
        'password': fields.String(required=True, description='비밀번호')
    })
    
    # 로그인 응답 모델
    login_response_model = api.model('LoginResponse', {
        'access_token': fields.String(description='JWT 액세스 토큰'),
        'user': fields.Raw(description='사용자 정보')
    })
    
    # 일반 응답 모델
    response_model = api.model('Response', {
        'message': fields.String(description='응답 메시지'),
        'error': fields.String(description='에러 메시지')
    })
    
    return {
        'register_model': register_model,
        'login_model': login_model,
        'login_response_model': login_response_model,
        'response_model': response_model
    } 