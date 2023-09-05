### session_manager.py
from datetime import datetime, timedelta
from dateutil import parser
import random
import string

class SessionManager:
    def __init__(self, db):
        self.db = db


    def create_session(self, email, session):
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

        while self.db.check_duplicate_token(token):
            token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

        if self.db.check_duplicate_email(email):
            self.db.update_session(email, token)
        else:
            self.db.create_session(email, token)

        # 세션 데이터 생성
        session_data = {
            'email': email,
            'token': token,
            'created_time': datetime.now().isoformat()
        }
        session['user_data'] = session_data


    # 로그인 상태를 확인하는 메소드입니다.
    def is_logged_in(self, session):
        try:
            session_data = session.get('user_data')
            
            if not session_data:
                return False

            created_time = session_data.get('created_time', None)
            if not created_time:
                return False

            # 이미 datetime 객체인 경우 문자열로 변환하지 않음
            if isinstance(created_time, datetime):
                current_time = datetime.now()

                # 세션 유효 시간 검사
                if (current_time - created_time).total_seconds() > 60:
                    return False

                return True
        except Exception as e:
            print(f"Debug: is_logged_in 메소드에서 에러 발생 - {e}")
            return False


    # 토큰을 검증하는 메소드입니다.
    def verify_token(self, token, session):
        session_data = self.db.get_session(token)
        if session_data:
            stored_token = session.get('user_data', {}).get('token', None)
            if stored_token == session_data['token']:
                return True
        return False
    
    
    # 로그아웃 처리를 하는 메소드입니다.
    def logout(self, session):
        session_data = session.get('user_data', {})
        if 'token' in session_data:
            self.db.delete_session(session_data['token'])
        session.pop('user_data', None)
