### database.py
import sqlite3
from datetime import datetime

# 결과를 딕셔너리 형태로 반환하는 함수입니다.
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# Database 클래스 정의
class Database:
    # 생성자에서 데이터베이스 경로를 설정합니다.
    def __init__(self, db_path='users.db'):
        self.db_path = db_path

    # 데이터베이스에 연결하는 메소드입니다.
    def connect(self):
        return sqlite3.connect(self.db_path)
        
    # 중복 토큰을 확인하는 메소드입니다.
    def check_duplicate_token(self, token):
        conn = self.connect()
        c = conn.cursor()
        c.execute("SELECT * FROM sessions WHERE token = ?", (token,))
        result = bool(c.fetchone())
        conn.close()
        return result

    # 중복 이메일을 확인하는 메소드입니다.
    def check_duplicate_email(self, email):
        conn = self.connect()
        c = conn.cursor()
        c.execute("SELECT * FROM sessions WHERE email = ?", (email,))
        result = bool(c.fetchone())
        conn.close()
        return result

    # 세션을 업데이트하는 메소드입니다.
    def update_session(self, email, new_token):
        conn = self.connect()
        c = conn.cursor()
        current_time = datetime.now()
        c.execute("UPDATE sessions SET token = ?, created_time = ? WHERE email = ?", (new_token, current_time, email))
        conn.commit()
        conn.close()

    # 새 세션을 생성하는 메소드입니다.
    def create_session(self, email, token):
        conn = self.connect()
        created_time = datetime.now()
        c = conn.cursor()
        c.execute("INSERT INTO sessions (email, token, created_time) VALUES (?, ?, ?)", (email, token, created_time))
        conn.commit()
        conn.close()

    # 특정 토큰에 해당하는 세션 정보를 가져오는 메소드입니다.
    def get_session(self, token):
        conn = self.connect()
        conn.row_factory = dict_factory
        c = conn.cursor()
        c.execute("SELECT * FROM sessions WHERE token = ?", (token,))
        session_data = c.fetchone()
        conn.close()
        return session_data
    
    # 세션을 삭제하는 메소드입니다.
    def delete_session(self, token):
        conn = self.connect()
        c = conn.cursor()
        c.execute("DELETE FROM sessions WHERE token = ?", (token,))
        conn.commit()
        conn.close()