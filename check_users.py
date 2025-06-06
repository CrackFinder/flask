from app import app
from db import db, User

with app.app_context():
    users = User.query.all()
    print("\n=== 등록된 사용자 목록 ===")
    for user in users:
        print(f"\nID: {user.id}")
        print(f"사용자명: {user.username}")
        print(f"이메일: {user.email}")
        print(f"가입일: {user.created_at}")
        print("-" * 30) 