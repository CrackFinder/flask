# schemas 패키지 
from .user import create_user_schemas
from .common import create_common_schemas
from .raspberry import create_raspberry_schemas

def create_all_schemas(api):
    """모든 스키마를 생성하고 반환"""
    
    # 사용자 스키마 생성
    user_schemas = create_user_schemas(api)

    # 라즈베리파이 스키마 생성
    raspberry_schemas = create_raspberry_schemas(api)
    
    # 공통 스키마 생성
    common_schemas = create_common_schemas(api)
    
    # 모든 스키마 통합
    all_schemas = {**user_schemas, **common_schemas, **raspberry_schemas}
    
    return all_schemas 