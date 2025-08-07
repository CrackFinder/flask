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
                    video_path='uploads/potholes/pothole_1.webp',
                    address='부산광역시 해운대구 센텀남대로 76',
                    latitude=35.173220,
                    longitude=129.129040,
                    raspberry_id=raspberry.id
                )
                
                # 포트홀 2 생성
                pothole2 = PotHole(
                    video_path='uploads/potholes/pothole_2.webp',
                    address='부산광역시 해운대구 센텀남대로 76 부산지하철 센텀시티역',
                    latitude=35.171760,
                    longitude=129.130371,
                    raspberry_id=raspberry.id
                )

                pothole3 = PotHole(
                    video_path='uploads/potholes/pothole_3.webp',
                    address='부산광역시 해운대구 재송동 920-14',
                    latitude=35.190735,
                    longitude=129.120342,
                    raspberry_id=raspberry.id
                )

                pothole4 = PotHole(
                    video_path='uploads/potholes/pothole_4.webp',
                    address='부산광역시 해운대구 반여동 산158-9',
                    latitude=35.192960,
                    longitude=129.118946,
                    raspberry_id=raspberry.id
                )

                pothole5 = PotHole(
                    video_path='uploads/potholes/pothole_5.webp',
                    address='부산광역시 사상구 삼락동 29-2',
                    latitude=35.164215,
                    longitude=128.975354,
                    raspberry_id=raspberry.id
                )

                pothole6 = PotHole(
                    video_path='uploads/potholes/pothole_6.webp',
                    address='부산광역시 남구 감만동 511-122',
                    latitude=35.111299,
                    longitude=129.077812,
                    raspberry_id=raspberry.id
                )

                pothole7 = PotHole(
                    video_path='uploads/potholes/pothole_7.webp',
                    address='부산광역시 남구 감만동 418-5',
                    latitude=35.115983,
                    longitude=129.075394,
                    raspberry_id=raspberry.id
                )

                pothole8 = PotHole(
                    video_path='uploads/potholes/pothole_8.webp',
                    address='부산광역시 남구 우암동 103-18',
                    latitude=35.127738,
                    longitude=129.082751,
                    raspberry_id=raspberry.id
                )

                pothole9 = PotHole(
                    video_path='uploads/potholes/pothole_9.webp',
                    address='부산광역시 남구 대연동 329-4',
                    latitude=35.135387,
                    longitude=129.094148,
                    raspberry_id=raspberry.id
                )

                pothole10 = PotHole(
                    video_path='uploads/potholes/pothole_10.webp',
                    address='부산광역시 남구 대연동 267-2',
                    latitude=35.148530,
                    longitude=129.093321,
                    raspberry_id=raspberry.id
                )

                potholes = [pothole1, pothole2, pothole3, pothole4, pothole5, pothole6, pothole7, pothole8, pothole9, pothole10]
                for pothole in potholes:
                    db.session.add(pothole)
                db.session.commit()
                
                print(f"초기 포트홀 {len(potholes)}개가 생성되었습니다:")
                for pothole in potholes:
                    print(f"- 포트홀 {pothole.id}: {pothole.address} (위도: {pothole.latitude}, 경도: {pothole.longitude})")
            else:
                print("사용자 또는 라즈베리파이 기기가 없어서 포트홀을 생성할 수 없습니다.")
        else:
            print("이미 포트홀이 존재합니다. 초기 포트홀을 생성하지 않습니다.")

if __name__ == '__main__':
    init_database() 