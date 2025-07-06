from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restx import Api
from flask_apscheduler import APScheduler
import os
from datetime import timedelta
from core.db import db

# 도메인별 모듈 import
from auth import init_auth_routes, create_auth_schemas
from user import init_user_routes, create_user_schemas
from raspberry import init_raspberry_routes, create_raspberry_schemas
from pothole import init_pothole_routes, create_pothole_schemas

# 도메인별 모델 import (side-effect용)
from auth.models import User
from raspberry.models import Raspberry, RaspberryStatus
from pothole.models import PotHole

app = Flask(__name__)
CORS(app)

# Flask-RESTX 설정
api = Api(app, version='1.0', title='라즈베리파이 Pothole API', description='Pothole API 문서')

# 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your-secret-key')  # 실제 운영시에는 환경변수로 관리
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

# 스케줄러 설정
app.config['SCHEDULER_API_ENABLED'] = True
app.config['SCHEDULER_TIMEZONE'] = 'Asia/Seoul'

# 초기화
db.init_app(app)
jwt = JWTManager(app)
scheduler = APScheduler()
scheduler.init_app(app)

# 스키마 생성 및 라우트 초기화
def init_app():
    from copy import deepcopy
    """앱 초기화"""
    # 모든 스키마 생성
    auth_schemas = {}
    auth_schemas.update(create_auth_schemas(api))
    auth_schemas.update(create_user_schemas(api))
    auth_schemas.update(create_raspberry_schemas(api))
    
    # 도메인별 라우트 초기화
    init_auth_routes(api, auth_schemas)
    init_user_routes(api, auth_schemas)
    init_raspberry_routes(api, auth_schemas)
    
    all_schemas = deepcopy(auth_schemas)
    all_schemas.update(create_pothole_schemas(api))
    init_pothole_routes(api, all_schemas)
    
    # 스케줄러 초기화
    from raspberry.scheduler import init_scheduler
    init_scheduler(scheduler)

# 앱 초기화
init_app()

# 데이터베이스 생성
with app.app_context():
    db.create_all()

# 스케줄러 시작
scheduler.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
