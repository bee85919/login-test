### create_db.py
import os
import pymysql
from dotenv import load_dotenv


# .env 파일에서 환경 변수를 불러옵니다.
load_dotenv()


# 환경 변수나 설정 파일로부터 데이터베이스 설정을 가져옵니다.
db_config = {
    "host": os.environ.get("DB_HOST", "127.0.0.1"),
    "port": int(os.environ.get("DB_PORT", 3306)),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", ""),
    "db": os.environ.get("DB_NAME", "your_db_name"),
    "charset": "utf8"
}


conn = None
cursor = None


try:
    # 데이터베이스 선택을 제외한 연결 설정
    conn = pymysql.connect(
        host=db_config['host'],
        port=db_config['port'],
        user=db_config['user'],
        password=db_config['password'],
        charset=db_config['charset']
    )
    cursor = conn.cursor()


    # 'TEST' 데이터베이스 생성
    cursor.execute("CREATE DATABASE IF NOT EXISTS `Basic_info`")
    conn.commit()


    # 'TEST' 데이터베이스 사용 설정
    conn.select_db('Basic_info')


    # 테이블이 존재하면 삭제
    cursor.execute("DROP TABLE IF EXISTS TEST")


    # 새로운 테이블을 생성
    cursor.execute('''
        CREATE TABLE TEST (
            ID INTEGER PRIMARY KEY AUTO_INCREMENT,
            USER_EMAIL VARCHAR(255) NOT NULL UNIQUE,
            TOKEN_CD VARCHAR(255) NOT NULL,
            CREATE_DATE DATETIME NOT NULL
        );
    ''')
    conn.commit()


except pymysql.MySQLError as e:
    print(f"An error occurred: {e}")


finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
