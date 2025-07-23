from app import app
from core.db import db
from auth.models import User
from raspberry.models import Raspberry
from pothole.models import PotHole
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
        
        # 초기 라즈베리파이 기기 생성 (데이터베이스가 비어있을 경우)
        if Raspberry.query.count() == 0:
            # 사용자 ID 가져오기 (첫 번째 사용자)
            user = User.query.first()
            if user:
                initial_raspberry = Raspberry(
                    id='raspberry_001',
                    name='Test Raspberry Pi',
                    ip='8.8.8.8',
                    port=1234,
                    user_id=user.id,
                    status='offline'
                )
                
                db.session.add(initial_raspberry)
                db.session.commit()
                print("초기 라즈베리파이 기기가 생성되었습니다: 8.8.8.8:1234")
            else:
                print("사용자가 없어서 라즈베리파이 기기를 생성할 수 없습니다.")
        else:
            print("이미 라즈베리파이 기기가 존재합니다. 초기 기기를 생성하지 않습니다.")
        
        # 초기 포트홀 생성 (데이터베이스가 비어있을 경우)
        if PotHole.query.count() == 0:
            # 사용자와 라즈베리파이 ID 가져오기
            user = User.query.first()
            raspberry = Raspberry.query.first()
            
            if user and raspberry:
                # 포트홀 1 생성
                pothole1 = PotHole(
                    video_path='uploads/potholes/sample_pothole_1.png',
                    address='서울특별시 강남구 테헤란로 123',
                    latitude=37.5665,
                    longitude=126.9780,
                    raspberry_id=raspberry.id
                )
                
                # 포트홀 2 생성
                pothole2 = PotHole(
                    video_path='uploads/potholes/sample_pothole_2.png',
                    address='서울특별시 서초구 서초대로 456',
                    latitude=37.5013,
                    longitude=127.0246,
                    raspberry_id=raspberry.id
                )
                
                db.session.add(pothole1)
                db.session.add(pothole2)
                db.session.commit()
                
                print("초기 포트홀 2개가 생성되었습니다:")
                print(f"- 포트홀 1: {pothole1.address} (위도: {pothole1.latitude}, 경도: {pothole1.longitude})")
                print(f"- 포트홀 2: {pothole2.address} (위도: {pothole2.latitude}, 경도: {pothole2.longitude})")
            else:
                print("사용자 또는 라즈베리파이 기기가 없어서 포트홀을 생성할 수 없습니다.")
        else:
            print("이미 포트홀이 존재합니다. 초기 포트홀을 생성하지 않습니다.")

if __name__ == '__main__':
    init_database() 