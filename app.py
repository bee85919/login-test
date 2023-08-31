from flask import Flask, request, render_template, session, redirect, url_for
import sqlite3
import smtplib
import random
import string
from dotenv import load_dotenv
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# 환경 변수 로딩
load_dotenv()

app = Flask(__name__)
# 앱의 비밀 키 설정
app.secret_key = os.environ.get('SECRET_KEY')

# 이메일 전송 함수 정의
def send_email(email, token):
    # SMTP 설정
    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp.login(os.environ.get("EMAIL"), os.environ.get("PASSWORD"))

    # 이메일 메시지 구성
    msg = MIMEMultipart()
    msg["From"] = os.environ.get("EMAIL")
    msg["To"] = email
    msg["Subject"] = "로그인 확인"
    content = f"로그인 확인 링크: http://127.0.0.1:5000/verify_login?token={token}"

    content_part = MIMEText(content, "plain")
    msg.attach(content_part)

    # 이메일 전송
    smtp.sendmail(os.environ.get("EMAIL"), email, msg.as_string())
    smtp.quit()

# 첫 요청 전에 세션 초기화
@app.before_first_request
def initialize_session():
    session['logged_in'] = False

# 메인 페이지 라우트
@app.route('/')
def index():
    print(f"Session logged_in value: {session.get('logged_in')}")
    if session.get('logged_in'):
        return "로그인 성공"
    return render_template('index.html')

from urllib.parse import urlparse

# 로그인 페이지 라우트
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        send_email(email, token)

        # 이메일 도메인 추출
        email_domain = email.split('@')[1]

        # 도메인별 리다이렉션 URL 설정
        redirect_url = {
            'gmail.com': 'https://mail.google.com',
            'yahoo.com': 'https://mail.yahoo.com',
            # 여기에 더 많은 도메인과 URL을 추가할 수 있습니다.
        }.get(email_domain, '/')  # 해당 도메인이 없으면 메인 페이지('/')로 리다이렉션

        # DB 연결 및 토큰 저장
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = c.fetchone()
        if user:
            c.execute("UPDATE users SET token = ? WHERE email = ?", (token, email))
        else:
            c.execute("INSERT INTO users (email, token) VALUES (?, ?)", (email, token))
        conn.commit()
        conn.close()

        return redirect(redirect_url)
    return render_template('login.html')

# 로그인 확인 라우트
@app.route('/verify_login')
def verify_login():
    token = request.args.get('token')

    # DB 연결
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE token = ?", (token,))
    user = c.fetchone()
    conn.close()

    # 사용자 확인 후 세션 설정
    if user:
        session['logged_in'] = True
        return redirect(url_for('index'))
    return render_template('verification_success.html', message="로그인 실패: 사용자를 찾을 수 없습니다.")

if __name__ == '__main__':
    app.run(debug=True)
