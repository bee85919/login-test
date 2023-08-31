# 필요한 모듈과 클래스를 임포트
from flask import Flask, session, request, render_template, redirect, url_for
from database import Database
from email_service import EmailService
from session_manager import SessionManager
import os
from dotenv import load_dotenv

# 환경 변수를 로드
load_dotenv()

# Flask 앱을 초기화
app = Flask(__name__)
# 앱의 비밀 키를 설정
app.secret_key = os.environ.get('SECRET_KEY')

# 데이터베이스와 이메일 서비스, 세션 관리자 객체를 생성
db = Database()
email_service = EmailService()
session_manager = SessionManager(db)

# 첫 요청 전에 세션을 초기화
@app.before_first_request
def initialize_session():
    session['logged_in'] = False

# 메인 페이지 라우트
@app.route('/')
def index():
    # 로그인 상태를 확인하여 적절한 메시지 또는 페이지를 반환
    if session_manager.is_logged_in(session):
        return "로그인 성공"
    return render_template('index.html')

# 로그인 페이지 라우트
@app.route('/login', methods=['GET', 'POST'])
def login():
    # POST 요청인 경우 로그인 처리를 수행
    if request.method == 'POST':
        email = request.form['email']
        # 세션을 생성하고 이메일을 전송
        session_manager.create_session(email, session)
        return session_manager.get_email_redirect(email)
    return render_template('login.html')

# 로그인 확인 라우트
@app.route('/verify_login')
def verify_login():
    # 전달된 토큰을 확인
    token = request.args.get('token')
    if session_manager.verify_token(token, session):
        return redirect(url_for('index'))
    return render_template('verification_success.html', message="로그인 실패: 사용자를 찾을 수 없습니다.")

# 앱을 실행
if __name__ == '__main__':
    app.run(debug=True)
