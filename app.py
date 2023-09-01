### app.py
from flask import Flask, session, request, render_template, redirect, url_for
from database import Database
from email_service import EmailService
from session_manager import SessionManager
import os
from dotenv import load_dotenv

load_dotenv()

# Flask 앱 초기화, 시크릿 키 설정
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

# 데이터베이스, 이메일 서비스, 세션 매니저 초기화
db = Database()
email_service = EmailService()
session_manager = SessionManager(db)

# 첫 요청 전에 세션을 초기화
@app.before_first_request
def initialize_session():
    pass

# 메인 페이지 라우트
@app.route('/')
def index():
    is_logged_in = session_manager.is_logged_in(session)
    if is_logged_in:
        return render_template('index.html', logged_in=True, email=session['email'])
    return render_template('index.html', logged_in=False)

# 로그인 상태를 확인하는 라우트
@app.route('/check_login_status')
def check_login_status():
    if session_manager.is_logged_in(session):
        return "로그인 상태: True"
    else:
        return "로그인 상태: False"

# 로그인 처리를 위한 라우트
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        
        if not session_manager.is_logged_in(session):
            session_manager.create_session(email, session)
            email_service.send_email(email, session['token'])
            return redirect(url_for('login_verification'))
        else:
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/login_verification')
def login_verification():
    email = session.get('email', 'unknown@example.com')
    domain = email.split('@')[1] if '@' in email else 'example.com'
    return render_template('login_verification.html', email_domain=domain)

# 로그인 토큰을 검증하는 라우트
@app.route('/verify_login')
def verify_login():
    token = request.args.get('token')
    if session_manager.verify_token(token, session):
        return redirect(url_for('index'))
    return render_template('verification_success.html', message="로그인 실패: 사용자를 찾을 수 없습니다.")

# 로그아웃 처리를 위한 라우트
@app.route('/logout')
def logout():
    session_manager.logout(session)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)