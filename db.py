from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # User와 Raspberry의 1:N 관계
    raspberries = db.relationship('Raspberry', backref='user', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }

class Raspberry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    ip = db.Column(db.String(120), nullable=False)
    port = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='offline')  # online, offline
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # User 외래키
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'ip': self.ip,
            'port': self.port,
            'status': self.status,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat()
        }
