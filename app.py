from flask import Flask, request, render_template, session, redirect
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

def send_email(email, token, purpose):
    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp.login(os.environ.get("EMAIL"), os.environ.get("PASSWORD"))
    
    msg = MIMEMultipart()
    msg["From"] = os.environ.get("EMAIL")
    msg["To"] = email

    if purpose == 'signup':
        msg["Subject"] = "회원가입 확인"
        content = f"회원가입 확인 링크: http://127.0.0.1:5000/verify_signup?token={token}"
    else:
        msg["Subject"] = "로그인 확인"
        content = f"로그인 확인 링크: http://127.0.0.1:5000/verify_login?token={token}"

    content_part = MIMEText(content, "plain")
    msg.attach(content_part)

    smtp.sendmail(os.environ.get("EMAIL"), email, msg.as_string())
    smtp.quit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        send_email(email, token, 'signup')

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (email, token, verified) VALUES (?, ?, 0)", (email, token))
        conn.commit()
        conn.close()

        return render_template('signup_verification.html')
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = c.fetchone()

        if user:
            if user[3]:  # user[3] is the 'verified' column
                token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
                send_email(email, token, 'login')
                c.execute("UPDATE users SET token = ? WHERE email = ?", (token, email))
                conn.commit()
                conn.close()
                return render_template('login_verification.html')
            else:
                conn.close()
                return render_template('verification_success.html', message="로그인 실패: 이메일이 인증되지 않았습니다.")
        else:
            conn.close()
            return render_template('verification_success.html', message="로그인 실패: 사용자를 찾을 수 없습니다.")
    return render_template('login.html')


@app.route('/verify_signup')
def verify_signup():
    token = request.args.get('token')

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("UPDATE users SET verified = 1 WHERE token = ?", (token,))
    conn.commit()
    conn.close()

    return render_template('verification_success.html', message="회원가입 완료!")

@app.route('/verify_login')
def verify_login():
    token = request.args.get('token')

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE token = ?", (token,))
    user = c.fetchone()
    conn.close()

    if user and user[3]:  # user[3] is the 'verified' column
        session['user_id'] = user[0]
        session['logged_in'] = True
        return render_template('hello_world.html')
    return render_template('verification_success.html', message="로그인 실패: 사용자를 찾을 수 없습니다.")

if __name__ == '__main__':
    app.run(debug=True)
