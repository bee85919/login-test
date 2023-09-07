### session_manager.py
from datetime import datetime, timedelta
from dateutil import parser
import random
import string

class SessionManager:
    def __init__(self, db):
        self.db = db


    def create_session(self, email, session):
        TOKEN_CD = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

        while self.db.check_duplicate_TOKEN_CD(TOKEN_CD):
            TOKEN_CD = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

        if self.db.check_duplicate_email(email):
            self.db.update_session(email, TOKEN_CD)
        else:
            self.db.create_session(email, TOKEN_CD)

        # 세션 데이터 생성
        session_data = {
            'USER_EMAIL': email,
            'TOKEN_CD': TOKEN_CD,
            'CREATE_DATE': datetime.now().isoformat()
        }
        session['user_data'] = session_data


    # 로그인 상태를 확인하는 메소드입니다.
    def is_logged_in(self, session):        
        try:
            session_data = session.get('user_data')
            
            if not session_data:
                return False

            create_time = parser.parse(session_data.get('CREATE_DATE', ''))
            if not create_time:
                return False

            # 이미 datetime 객체인 경우 문자열로 변환하지 않음
            if isinstance(create_time, datetime):
                current_time = datetime.now()
                temp = current_time - create_time
                
                # 세션 유효 시간 검사
                if (temp).total_seconds() > 60:
                    return False
                
                return True
            
        except Exception as e:
            print(f"Debug: is_logged_in 메소드에서 에러 발생 - {e}")
            return False


    # 토큰을 검증하는 메소드입니다.
    def verify_token(self, token, session):
        session_data = self.db.get_session(token)
        if session_data:
            stored_token = session.get('user_data', {}).get('TOKEN_CD', None)
            if stored_token == session_data['TOKEN_CD']:
                return True
        return False
    
    
    # 로그아웃 처리를 하는 메소드입니다.
    def logout(self, session):
        session_data = session.get('user_data', {})
        if 'TOKEN_CD' in session_data:
            self.db.delete_session(session_data['TOKEN_CD'])
        session.pop('user_data', None)
