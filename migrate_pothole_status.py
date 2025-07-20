#!/usr/bin/env python3
"""
PotHole 테이블에 status 컬럼 추가 마이그레이션 스크립트
"""

from app import app
from core.db import db
from sqlalchemy import text

def migrate_pothole_status():
    """PotHole 테이블에 status 컬럼 추가"""
    with app.app_context():
        try:
            # status 컬럼이 이미 존재하는지 확인
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'pot_hole' 
                AND column_name = 'status'
            """))
            
            if result.fetchone():
                print("status 컬럼이 이미 존재합니다.")
                return
            
            # status 컬럼 추가
            db.session.execute(text("""
                ALTER TABLE pot_hole 
                ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT '미처리'
            """))
            
            db.session.commit()
            print("PotHole 테이블에 status 컬럼이 성공적으로 추가되었습니다.")
            
        except Exception as e:
            db.session.rollback()
            print(f"마이그레이션 중 오류 발생: {str(e)}")
            raise

if __name__ == "__main__":
    migrate_pothole_status() 