### database.py
import pymysql
from datetime import datetime

class Database:
    def __init__(self, db_config):
        self.db_config = db_config

    def connect(self):
        return pymysql.connect(**self.db_config, cursorclass=pymysql.cursors.DictCursor)

    def check_duplicate_token(self, token):
        conn = self.connect()
        c = conn.cursor()
        c.execute("SELECT * FROM sessions WHERE token = %s", (token,))
        result = bool(c.fetchone())
        conn.close()
        return result

    # 중복 이메일을 확인하는 메소드입니다.
    def check_duplicate_email(self, email):
        conn = self.connect()
        c = conn.cursor()
        c.execute("SELECT * FROM sessions WHERE email = %s", (email,))
        result = bool(c.fetchone())
        conn.close()
        return result

    # 세션을 업데이트하는 메소드입니다.
    def update_session(self, email, new_token):
        conn = self.connect()
        c = conn.cursor()
        current_time = datetime.now()
        c.execute("UPDATE sessions SET token = %s, created_time = %s WHERE email = %s", (new_token, current_time, email))
        conn.commit()
        conn.close()

    # 새 세션을 생성하는 메소드입니다.
    def create_session(self, email, token):
        conn = self.connect()
        created_time = datetime.now()
        c = conn.cursor()
        c.execute("INSERT INTO sessions (email, token, created_time) VALUES (%s, %s, %s)", (email, token, created_time))
        conn.commit()
        conn.close()

    # 특정 토큰에 해당하는 세션 정보를 가져오는 메소드입니다.
    def get_session(self, token):
        conn = self.connect()
        c = conn.cursor()
        c.execute("SELECT * FROM sessions WHERE token = %s", (token,))
        session_data = c.fetchone()
        conn.close()
        return session_data
    
    # 세션을 삭제하는 메소드입니다.
    def delete_session(self, token):
        conn = self.connect()
        c = conn.cursor()
        c.execute("DELETE FROM sessions WHERE token = %s", (token,))
        conn.commit()
        conn.close()