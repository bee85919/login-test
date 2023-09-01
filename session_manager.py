### session_manager.py
from datetime import datetime, timedelta
import random
import string

# SessionManager 클래스 정의
class SessionManager:
    # 생성자에서 Database 객체를 초기화합니다.
    def __init__(self, db):
        self.db = db

    # 새 세션을 생성하는 메소드입니다.
    def create_session(self, email, session):
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        
        while self.db.check_duplicate_token(token):
            token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

        if self.db.check_duplicate_email(email):
            self.db.update_session(email, token)
        else:
            self.db.create_session(email, token)
        
        session['email'] = email
        session['token'] = token
        session['created_time'] = datetime.now()

    # 로그인 상태를 확인하는 메소드입니다.
    def is_logged_in(self, session):
        if 'token' in session:
            session_data = self.db.get_session(session['token'])
            if session_data and 'created_time' in session_data:
                if datetime.now() - datetime.fromisoformat(session_data['created_time']) < timedelta(minutes=1):
                    return True
        return False

    # 토큰을 검증하는 메소드입니다.
    def verify_token(self, token, session):
        session_data = self.db.get_session(token)
        if session_data:
            if 'token' in session and session_data['token'] == session['token']:
                return True
        return False
    
    # 로그아웃 처리를 하는 메소드입니다.
    def logout(self, session):
        session.pop('email', None)
        session.pop('token', None)
        session.pop('created_time', None)
        if 'token' in session:
            self.db.delete_session(session['token'])