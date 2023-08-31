import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        # 데이터베이스에 연결
        self.conn = sqlite3.connect('users.db')
        self.c = self.conn.cursor()

    def create_session(self, email, token):
        # 세션 생성 시간을 현재 시간으로 설정
        created_time = datetime.now()
        self.c.execute("INSERT INTO sessions (email, token, created_time) VALUES (?, ?, ?)", (email, token, created_time))
        self.conn.commit()

    def get_session(self, token):
        # 토큰으로 세션 정보 조회
        self.c.execute("SELECT * FROM sessions WHERE token = ?", (token,))
        return self.c.fetchone()

    def delete_session(self, token):
        # 토큰으로 세션 정보 삭제
        self.c.execute("DELETE FROM sessions WHERE token = ?", (token,))
        self.conn.commit()
