from flask_restx import fields

def create_user_schemas(api):
    """사용자 관련 스키마들을 생성"""
    
    # 기본 사용자 모델
    user_model = api.model('User', {
        'id': fields.Integer(readonly=True, description='사용자 ID'),
        'username': fields.String(required=True, description='사용자명'),
        'email': fields.String(required=True, description='이메일 주소')
    })
    
    # 회원가입 모델
    register_model = api.model('Register', {
        'username': fields.String(required=True, description='사용자명'),
        'email': fields.String(required=True, description='이메일 주소'),
        'password': fields.String(required=True, description='비밀번호')
    })
    
    # 로그인 모델
    login_model = api.model('Login', {
        'email': fields.String(required=True, description='이메일 주소'),
        'password': fields.String(required=True, description='비밀번호')
    })
    
    # 로그인 응답 모델
    login_response_model = api.model('LoginResponse', {
        'access_token': fields.String(description='JWT 토큰'),
        'user': fields.Nested(user_model, description='사용자 정보')
    })
    
    return {
        'user_model': user_model,
        'register_model': register_model,
        'login_model': login_model,
        'login_response_model': login_response_model
    } 