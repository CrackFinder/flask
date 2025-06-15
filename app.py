from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import bcrypt
from db import db, User
import os
from datetime import timedelta

app = Flask(__name__)
CORS(app)

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

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # 필수 필드 확인
    if not all(k in data for k in ['username', 'email', 'password']):
        return jsonify({'error': '모든 필드를 입력해주세요'}), 400
    
    # 이메일 중복 확인
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': '이미 등록된 이메일입니다'}), 400
    
    # 사용자명 중복 확인
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': '이미 사용중인 사용자명입니다'}), 400
    
    # 비밀번호 해싱
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    
    # 새 사용자 생성
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password.decode('utf-8')
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': '회원가입이 완료되었습니다'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not all(k in data for k in ['email', 'password']):
        return jsonify({'error': '이메일과 비밀번호를 입력해주세요'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
        return jsonify({'error': '이메일 또는 비밀번호가 올바르지 않습니다'}), 401
    
    # JWT 토큰 생성
    print(f'userid {user.id} {type(user.id)}')
    access_token = create_access_token(identity=f'{user.id}')
    
    return jsonify({
        'access_token': access_token,
        'user': user.to_dict()
    }), 200

@app.route('/api/user', methods=['GET'])
@jwt_required()
def get_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': '사용자를 찾을 수 없습니다'}), 404
    
    return jsonify(user.to_dict()), 200

if __name__ == '__main__':
    app.run(debug=True)
