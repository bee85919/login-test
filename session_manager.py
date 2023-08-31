from datetime import datetime, timedelta
import random
import string
from flask import redirect, url_for

class SessionManager:
    def __init__(self, db):
        # Database 객체를 받아서 초기화
        self.db = db

    def create_session(self, email, session):
        # 랜덤 토큰 생성
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        
        # 중복 토큰 확인
        while self.db.check_duplicate_token(token):
            print("토큰 중복, 재생성합니다.")
            token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

        # 데이터베이스에 세션 정보 저장
        if self.db.check_duplicate_email(email):
            print(f"{email}은(는) 이미 사용 중인 이메일입니다. 세션을 업데이트합니다.")
            self.db.update_session(email, token)  # update_session은 새로 만들어야 하는 메서드입니다.
        else:
            self.db.create_session(email, token)
        
        # 세션 변수 설정
        session['email'] = email
        session['token'] = token
        session['created_time'] = datetime.now()

    def is_logged_in(self, session):
        if 'token' in session:
            session_data = self.db.get_session(session['token'])
            
            if session_data and 'created_time' in session_data:
                if datetime.now() - session_data['created_time'] < timedelta(minutes=15):
                    return True
        return False
    
    def get_email_redirect(self):
        return redirect(url_for('index'))

    def verify_token(self, token, session):
        # 토큰 검증
        session_data = self.db.get_session(token)
        if session_data:
            # 세션 정보와 전달된 토큰 비교
            if session_data['token'] == session['token']:
                return True
        return False
