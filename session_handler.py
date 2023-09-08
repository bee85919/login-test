## session_handler.py
from datetime import datetime
from dateutil import parser
import random
import string


class SessionHandler:
    def __init__(self, db):
        self.db = db


    def create_random_string(self, length=16):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


    def create_token_cd(self):
        TOKEN_CD = self.create_random_string()
        while self.db.check_duplicate('SESSION_TB', 'TOKEN_CD', TOKEN_CD):
            TOKEN_CD = self.create_random_string()
        return TOKEN_CD


    def update_session(self, email, TOKEN_CD):
        self.db.update_session(email, TOKEN_CD)


    def create_session_data(self, user_id, email, TOKEN_CD):
        return {
            'USER_ID': user_id,
            'USER_EMAIL': email,
            'TOKEN_CD': TOKEN_CD,
            'CREATE_DATE': datetime.now().isoformat()
        }


    def set_session_data(self, session, session_data):
        session['user_data'] = session_data


    def manage_session(self, email, session):
        TOKEN_CD = self.create_token_cd()

        if self.db.check_duplicate("USER_TB", "USER_EMAIL", email):
            user_id = self.db.get_user_id_by_email(email)
            
            if self.db.check_duplicate("SESSION_TB", "USER_ID", user_id):
                self.db.update_session(user_id, TOKEN_CD)
            else:
                self.db.create_session(user_id, TOKEN_CD)
        else:
            user_id = self.create_unique_id()
            self.db.create_user(user_id, email)
            self.db.create_session(user_id, TOKEN_CD)

        session_data = self.create_session_data(user_id, email, TOKEN_CD)
        self.set_session_data(session, session_data)

    
    def create_unique_id(self):
        return self.create_token_cd()


    def get_session_data(self, session):
        return session.get('user_data')


    def is_session_expired(self, create_time, current_time):
        return (current_time - create_time).total_seconds() > 60


    def is_logged_in(self, session):        
        try:
            session_data = self.get_session_data(session)
            if not session_data:
                return False, {}

            create_time_str = session_data.get('CREATE_DATE', '')
            create_time = parser.parse(create_time_str)
            if not create_time:
                return False, {}

            current_time = datetime.now()
            if self.is_session_expired(create_time, current_time):
                return False, {}

            return True, session_data

        except Exception as e:
            print(f"Debug: is_logged_in 메소드에서 에러 발생 - {e}")
            return False, {}


    def verify_token(self, token, session):
        db_session_data = self.db.get_session(token)  # 이 부분이 딕셔너리를 반환해야 합니다.
        db_token = db_session_data.get('TOKEN_CD', None)  # 이렇게 수정하면 db_token은 문자열이 됩니다.

        if db_token:
            session_token = session.get('user_data', {}).get('TOKEN_CD', None)
            if session_token == db_token:  # 여기서 비교할 때 문자열과 문자열을 비교하게 됩니다.
                return True
        return False


    def logout(self, session):
        session_data = session.get('user_data', {})
        if 'TOKEN_CD' in session_data:
            self.db.delete_session(session_data['TOKEN_CD'])
        session.pop('user_data', None)