## db_handler.py
import pymysql
from datetime import datetime

class DBHandler:
    def __init__(self, db_config):
        self.db_config = db_config


    def connect(self):
        return pymysql.connect(**self.db_config, cursorclass=pymysql.cursors.DictCursor)


    def execute_query(self, query, params, fetch=False):
        conn = self.connect()
        c = conn.cursor()
        c.execute(query, params)
        result = None
        if fetch:
            result = c.fetchone()
        conn.commit()
        conn.close()
        return result
    
    
    def get_user_id_by_email(self, email):
        query = "SELECT USER_ID FROM USER_TB WHERE USER_EMAIL = %s"
        params = (email,)
        result = self.execute_query(query, params, fetch=True)
        print(f"Debug: 쿼리 실행 결과는 {result}")  # 디버깅 로그
        if result:
            return result['USER_ID']
        else:
            return None


    def check_duplicate(self, table, column, value):
        query = f"SELECT * FROM {table} WHERE {column} = %s"
        params = (value,)
        result = self.execute_query(query, params, fetch=True)
        return bool(result)


    def create_user(self, user_id, email):
        CREATE_TIME = datetime.now()
        query = """INSERT INTO USER_TB (USER_ID, USER_EMAIL, CREATE_TIME) VALUES (%s, %s, %s)"""
        params = (user_id, email, CREATE_TIME)
        self.execute_query(query, params)


    def create_session(self, user_id, TOKEN_CD):
        UPDATE_TIME = datetime.now()
        query = """INSERT INTO SESSION_TB (USER_ID, TOKEN_CD, UPDATE_TIME) VALUES (%s, %s, %s)"""
        params = (user_id, TOKEN_CD, UPDATE_TIME)
        self.execute_query(query, params)
        

    def update_session(self, user_id, TOKEN_CD):
        UPDATE_TIME = datetime.now()
        query = """UPDATE SESSION_TB SET TOKEN_CD = %s, UPDATE_TIME = %s WHERE USER_ID = %s"""
        params = (TOKEN_CD, UPDATE_TIME, user_id)
        self.execute_query(query, params)


    def create_or_update_session(self, USER_ID, email, TOKEN_CD):
        if self.check_duplicate("USER_TB", "USER_EMAIL", email):
            self.update_session(USER_ID, TOKEN_CD)
        else:
            self.create_session(email, TOKEN_CD)
        
        
    def get_session(self, token):
        query = "SELECT * FROM SESSION_TB WHERE TOKEN_CD = %s"
        params = (token,)
        return self.execute_query(query, params, fetch=True)
