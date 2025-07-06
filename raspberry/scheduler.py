import requests
import time
from datetime import datetime
from flask import current_app
from core.db import db
from .models import Raspberry, RaspberryStatus

class RaspberryHealthChecker:
    """라즈베리파이 상태 체크 클래스"""
    
    def __init__(self):
        self.timeout = 5  # 5초 타임아웃
        self.max_retries = 4  # 최대 4회 시도
    
    def ping_raspberry(self, ip, port):
        """라즈베리파이에 ping 요청"""
        url = f"http://{ip}:{port}/health"
        success_count = 0
        total_response_time = 0
        error_message = None
        
        for attempt in range(self.max_retries):
            try:
                start_time = time.time()
                response = requests.get(url, timeout=self.timeout)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    success_count += 1
                    total_response_time += response_time
                else:
                    error_message = f"HTTP {response.status_code}"
                    
            except requests.exceptions.Timeout:
                error_message = "Timeout"
            except requests.exceptions.ConnectionError:
                error_message = "Connection Error"
            except requests.exceptions.RequestException as e:
                error_message = str(e)
            except Exception as e:
                error_message = f"Unexpected error: {str(e)}"
        
        # 평균 응답 시간 계산
        avg_response_time = total_response_time / success_count if success_count > 0 else None
        
        # 50% 이상 성공하면 온라인으로 판단
        is_online = success_count >= (self.max_retries // 2)
        
        return {
            'is_online': is_online,
            'success_count': success_count,
            'response_time': avg_response_time,
            'error_message': error_message if success_count == 0 else None
        }
    
    def check_all_raspberries(self):
        """모든 라즈베리파이 상태 체크"""
        try:
            # Flask 앱 인스턴스 가져오기
            from app import app
            
            with app.app_context():
                raspberries = Raspberry.query.all()
                
                for raspberry in raspberries:
                    print(f"Checking {raspberry.name} ({raspberry.ip}:{raspberry.port})")
                    
                    # 상태 체크 수행
                    result = self.ping_raspberry(raspberry.ip, raspberry.port)
                    
                    # 상태 체크 결과 저장
                    status_check = RaspberryStatus(
                        raspberry_id=raspberry.id,
                        is_online=result['is_online'],
                        response_time=result['response_time'],
                        success_count=result['success_count'],
                        error_message=result['error_message']
                    )
                    print('상태체크 결과:', status_check)
                    db.session.add(status_check)
                    
                    # 라즈베리파이 상태 업데이트
                    raspberry.status = 'online' if result['is_online'] else 'offline'
                    
                    print(f"  - Status: {raspberry.status}")
                    if result['response_time']:
                        print(f"  - Response time: {result['response_time']:.3f}s")
                    if result['error_message']:
                        print(f"  - Error: {result['error_message']}")
                
                db.session.commit()
                print(f"Status check completed for {len(raspberries)} raspberries at {datetime.now()}")
                
        except Exception as e:
            print(f"Error during status check: {str(e)}")
            # 애플리케이션 컨텍스트 내에서만 rollback 시도
            try:
                from app import app
                with app.app_context():
                    db.session.rollback()
            except:
                pass

def init_scheduler(scheduler):
    """스케줄러 초기화"""
    checker = RaspberryHealthChecker()
    
    print('작업등록')
    # 1분마다 상태 체크 작업 등록
    scheduler.add_job(
        id='raspberry_health_check',
        func=checker.check_all_raspberries,
        trigger='interval',
        seconds=5,
        replace_existing=True
    )
    
    print("Raspberry health check scheduler initialized - running every 1 minute") 