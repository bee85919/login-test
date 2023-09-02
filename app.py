### app.py
from flask import Flask, session, request, render_template, redirect, url_for
import os
from dotenv import load_dotenv
import pymysql
from database import Database
from email_service import EmailService
from session_manager import SessionManager

# 환경 변수 로딩
load_dotenv()

# Flask 설정 클래스
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DB_HOST = os.environ.get("DB_HOST")
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_NAME = os.environ.get("DB_NAME")
    DB_PORT = os.environ.get("DB_PORT", 3306)  # .env 파일에서 없으면 3306으로 설정

# Flask 앱 초기화와 설정 로딩
app = Flask(__name__)
app.config.from_object(Config)

# 데이터베이스 설정
db_config = {
    "host": app.config["DB_HOST"],
    "port": int(app.config["DB_PORT"]),  # 문자열을 정수로 변환
    "user": app.config["DB_USER"],
    "password": app.config["DB_PASSWORD"],
    "db": app.config["DB_NAME"],
    "charset": "utf8"
}

print("DB Config:", db_config)

# pymysql을 이용해 DB 연결
db = pymysql.connect(**db_config)

# 클래스 인스턴스 생성
db_instance = Database(db_config)  # db_config 딕셔너리를 인자로 넘김
email_service = EmailService()
session_manager = SessionManager(db_instance)

# 메인 페이지 라우트
@app.route('/')
def index():
    is_logged_in = session_manager.is_logged_in(session)
    user_data = session.get('user_data', {})
    if is_logged_in:
        return render_template('index.html', logged_in=True, email=user_data.get('email'))
    return render_template('index.html', logged_in=False)

# 로그인 상태 확인 라우트
@app.route("/check_login_status")
def check_login_status():
    try:
        if session_manager.is_logged_in(session):
            return "Logged in"
        else:
            return "Not logged in"
    except Exception as e:
        # 에러 발생 시 디버깅
        print(f"Debug: check_login_status에서 에러 발생 - {e}")
        return "Error"

# 로그인 페이지 라우트
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        
        if not session_manager.is_logged_in(session):
            session_manager.create_session(email, session)
            return redirect(url_for('login_verification'))
        else:
            return redirect(url_for('index'))
    return render_template('login.html')

# 이메일 인증 페이지 라우트
@app.route('/login_verification')
def login_verification():
    user_data = session.get('user_data', {})
    email = user_data.get('email', 'unknown@example.com')
    domain = email.split('@')[1] if '@' in email else 'example.com'
    return render_template('login_verification.html', email_domain=domain)

# 이메일 토큰 확인 라우트
@app.route('/verify_login')
def verify_login():
    token = request.args.get('token')
    if session_manager.verify_token(token, session):
        return redirect(url_for('index'))
    return render_template('verification_success.html', message="로그인 실패: 사용자를 찾을 수 없습니다.")

# 로그아웃 라우트
@app.route('/logout')
def logout():
    session_manager.logout(session)
    return redirect(url_for('index'))

# 앱 실행
if __name__ == '__main__':
    app.run(debug=True, port=5000)