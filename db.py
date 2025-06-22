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

class PotHole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(500), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Raspberry 외래키
    raspberry_id = db.Column(db.Integer, db.ForeignKey('raspberry.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'image_path': self.image_path,
            'address': self.address,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'raspberry_id': self.raspberry_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
