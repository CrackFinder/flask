# schemas 패키지 
from .user import create_user_schemas
from .common import create_common_schemas

def create_all_schemas(api):
    """모든 스키마를 생성하고 반환"""
    
    # 사용자 스키마 생성
    user_schemas = create_user_schemas(api)
    
    # 공통 스키마 생성
    common_schemas = create_common_schemas(api)
    
    # 모든 스키마 통합
    all_schemas = {**user_schemas, **common_schemas}
    
    return all_schemas 