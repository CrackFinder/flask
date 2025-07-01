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