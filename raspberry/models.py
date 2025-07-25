from datetime import datetime
from core.db import db

class Raspberry(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    ip = db.Column(db.String(120), nullable=False)
    port = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='offline')  # online, offline
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # User 외래키
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Raspberry와 PotHole의 1:N 관계
    potholes = db.relationship('PotHole', backref='raspberry', lazy=True, cascade='all, delete-orphan')
    
    # Raspberry와 RaspberryStatus의 1:N 관계
    status_checks = db.relationship('RaspberryStatus', backref='raspberry', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'ip': self.ip,
            'port': self.port,
            'status': self.status,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'potholes': [pothole.to_dict() for pothole in self.potholes]
        }

class RaspberryStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    raspberry_id = db.Column(db.String(50), db.ForeignKey('raspberry.id'), nullable=False)
    is_online = db.Column(db.Boolean, nullable=False)
    response_time = db.Column(db.Float, nullable=True)  # 응답 시간 (초)
    success_count = db.Column(db.Integer, default=0)  # 성공한 ping 횟수 (0-4)
    total_attempts = db.Column(db.Integer, default=4)  # 총 시도 횟수
    error_message = db.Column(db.String(200), nullable=True)  # 에러 메시지
    checked_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'raspberry_id': self.raspberry_id,
            'is_online': self.is_online,
            'response_time': self.response_time,
            'success_count': self.success_count,
            'total_attempts': self.total_attempts,
            'error_message': self.error_message,
            'checked_at': self.checked_at.isoformat()
        } 