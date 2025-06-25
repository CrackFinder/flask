#!/usr/bin/env python3
"""
데이터베이스 마이그레이션 스크립트
image_path 컬럼을 video_path로 변경
"""

import sqlite3
import os
from pathlib import Path

def migrate_database():
    """데이터베이스 마이그레이션 실행"""
    db_path = 'instance/users.db'
    
    if not os.path.exists(db_path):
        print(f"데이터베이스 파일을 찾을 수 없습니다: {db_path}")
        return
    
    try:
        # 데이터베이스 연결
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 현재 테이블 구조 확인
        cursor.execute("PRAGMA table_info(pothole)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        print(f"현재 컬럼: {column_names}")
        
        if 'image_path' in column_names and 'video_path' not in column_names:
            print("마이그레이션을 시작합니다...")
            
            # 임시 테이블 생성 (video_path 컬럼 포함)
            cursor.execute("""
                CREATE TABLE pothole_new (
                    id INTEGER PRIMARY KEY,
                    video_path VARCHAR(500) NOT NULL,
                    address VARCHAR(200) NOT NULL,
                    latitude FLOAT NOT NULL,
                    longitude FLOAT NOT NULL,
                    created_at DATETIME,
                    updated_at DATETIME,
                    raspberry_id INTEGER NOT NULL,
                    FOREIGN KEY (raspberry_id) REFERENCES raspberry (id)
                )
            """)
            
            # 기존 데이터 복사 (image_path → video_path)
            cursor.execute("""
                INSERT INTO pothole_new (id, video_path, address, latitude, longitude, 
                                       created_at, updated_at, raspberry_id)
                SELECT id, image_path, address, latitude, longitude, 
                       created_at, updated_at, raspberry_id
                FROM pothole
            """)
            
            # 기존 테이블 삭제
            cursor.execute("DROP TABLE pothole")
            
            # 새 테이블 이름 변경
            cursor.execute("ALTER TABLE pothole_new RENAME TO pothole")
            
            # 변경사항 저장
            conn.commit()
            
            print("마이그레이션이 성공적으로 완료되었습니다!")
            print("- image_path 컬럼이 video_path로 변경되었습니다.")
            
        elif 'video_path' in column_names:
            print("이미 video_path 컬럼이 존재합니다. 마이그레이션이 필요하지 않습니다.")
            
        else:
            print("예상치 못한 테이블 구조입니다. 수동 확인이 필요합니다.")
            
    except Exception as e:
        print(f"마이그레이션 중 오류가 발생했습니다: {e}")
        conn.rollback()
        
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database() 