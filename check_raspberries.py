from app import app
from core.db import db
from auth.models import User
from raspberry.models import Raspberry

with app.app_context():
    print("\n=== 등록된 사용자 목록 ===")
    users = User.query.all()
    for user in users:
        print(f"\nID: {user.id}")
        print(f"사용자명: {user.username}")
        print(f"이메일: {user.email}")
        print(f"가입일: {user.created_at}")
        print("-" * 30)
    
    print("\n=== 등록된 라즈베리파이 기기 목록 ===")
    raspberries = Raspberry.query.all()
    for raspberry in raspberries:
        print(f"\nID: {raspberry.id}")
        print(f"이름: {raspberry.name}")
        print(f"IP: {raspberry.ip}")
        print(f"포트: {raspberry.port}")
        print(f"상태: {raspberry.status}")
        print(f"사용자 ID: {raspberry.user_id}")
        print(f"생성일: {raspberry.created_at}")
        print("-" * 30)
    
    print(f"\n총 사용자 수: {len(users)}")
    print(f"총 라즈베리파이 기기 수: {len(raspberries)}")
