from flask import Flask, request, render_template, session, redirect, url_for
import sqlite3
import smtplib
import random
import string
from dotenv import load_dotenv
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

# 이메일 전송 함수
def send_email(email, token):
    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp.login(os.environ.get("EMAIL"), os.environ.get("PASSWORD"))

    msg = MIMEMultipart()
    msg["From"] = os.environ.get("EMAIL")
    msg["To"] = email
    msg["Subject"] = "로그인 확인"
    content = f"로그인 확인 링크: http://127.0.0.1:5000/verify_login?token={token}"

    content_part = MIMEText(content, "plain")
    msg.attach(content_part)

    smtp.sendmail(os.environ.get("EMAIL"), email, msg.as_string())
    smtp.quit()
    
@app.before_first_request
def initialize_session():
    session['logged_in'] = False


@app.route('/')
def index():
    print(f"Session logged_in value: {session.get('logged_in')}")
    if session.get('logged_in'):
        return "Hello World"
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        send_email(email, token)

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
        return render_template('login_verification.html')
    return render_template('login.html')

@app.route('/verify_login')
def verify_login():
    token = request.args.get('token')

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE token = ?", (token,))
    user = c.fetchone()
    conn.close()

    if user:
        session['logged_in'] = True
        return redirect(url_for('index'))
    return render_template('verification_success.html', message="로그인 실패: 사용자를 찾을 수 없습니다.")

if __name__ == '__main__':
    app.run(debug=True)
