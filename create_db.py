### create_db.py
import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()

# 테이블이 존재하면 삭제
c.execute("DROP TABLE IF EXISTS sessions")

# 새로운 테이블을 생성
c.execute('''CREATE TABLE sessions
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              email TEXT NOT NULL UNIQUE,
              token TEXT NOT NULL,
              created_time DATETIME NOT NULL);''')

conn.commit()
conn.close()
