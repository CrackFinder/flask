from datetime import datetime
from core.db import db

class PotHole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_path = db.Column(db.String(500), nullable=False)
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
            'video_path': self.video_path,
            'address': self.address,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'raspberry_id': self.raspberry_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 