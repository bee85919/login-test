import sqlite3
from datetime import datetime

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class Database:
    def __init__(self):
        self.connect()
        c = self.conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                token TEXT NOT NULL,
                created_time DATETIME NOT NULL
            );
        """)
        self.conn.commit()
        self.close()
        
    def connect(self):
        self.conn = sqlite3.connect('users.db')
        
    def close(self):
        if self.conn:
            self.conn.close()
    
    def create_session(self, email, token):
        # 세션 생성 시간을 현재 시간으로 설정
        created_time = datetime.now()
        
        # DB 연결 열기
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        
        try:
            c.execute("INSERT INTO sessions (email, token, created_time) VALUES (?, ?, ?)", (email, token, created_time))
            conn.commit()
        finally:
            # DB 연결 닫기
            conn.close()

    def get_session(self, token):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        
        try:
            c.execute("SELECT * FROM sessions WHERE token = ?", (token,))
            return c.fetchone()
        finally:
            conn.close()

    def delete_session(self, token):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        
        try:
            c.execute("DELETE FROM sessions WHERE token = ?", (token,))
            conn.commit()
        finally:
            conn.close()
        
    # 중복 이메일 확인
    def check_duplicate_email(self, email):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        
        try:
            c.execute("SELECT * FROM sessions WHERE email = ?", (email,))
            return bool(c.fetchone())
        finally:
            conn.close()

    # 중복 토큰 확인
    def check_duplicate_token(self, token):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        
        try:
            c.execute("SELECT * FROM sessions WHERE token = ?", (token,))
            return bool(c.fetchone())
        finally:
            conn.close()
            
    # 세션 업데이트
    def update_session(self, email, new_token):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        try:
            c.execute("UPDATE sessions SET token = ? WHERE email = ?", (new_token, email))
            conn.commit()
        finally:
            conn.close()
