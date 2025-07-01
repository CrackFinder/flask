from app import app
from core.db import db
from auth.models import User
import bcrypt

def init_database():
    """데이터베이스 초기화 및 초기 데이터 생성"""
    with app.app_context():
        # 테이블 생성
        db.create_all()
        
        # 초기 사용자 생성 (데이터베이스가 비어있을 경우)
        if User.query.count() == 0:
            hashed_password = bcrypt.hashpw('12341234'.encode('utf-8'), bcrypt.gensalt())
            
            initial_user = User(
                username='test',
                email='test@test.com',
                password=hashed_password.decode('utf-8')
            )
            
            db.session.add(initial_user)
            db.session.commit()
            print("초기 사용자가 생성되었습니다: test@test.com / 12341234")
        else:
            print("이미 사용자가 존재합니다. 초기 사용자를 생성하지 않습니다.")

if __name__ == '__main__':
    init_database() 