from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_restx import Api, Resource, fields
import bcrypt
from db import db, User
from schemas import create_all_schemas
from routes.auth import create_auth_routes
from routes.user import create_user_routes
from routes.raspberry import create_raspberry_routes
import os
from datetime import timedelta

app = Flask(__name__)
CORS(app)

# Flask-RESTX 설정
api = Api(app, version='1.0', title='Flask API', description='Flask API 문서')

# 네임스페이스 생성
ns = api.namespace('api', description='API 엔드포인트')

# 스키마 생성
schemas = create_all_schemas(api)

# 라우트 생성
create_auth_routes(ns, schemas)
create_user_routes(ns, schemas)
create_raspberry_routes(ns, schemas)

# 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your-secret-key')  # 실제 운영시에는 환경변수로 관리
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

# 초기화
db.init_app(app)
jwt = JWTManager(app)

# 데이터베이스 생성
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
