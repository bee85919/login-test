from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3
import smtplib
import random
import string
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "your_fallback_secret_key")

# 이메일 전송 함수
def send_email(email, token, purpose):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(os.environ.get("EMAIL", "your_fallback_email@gmail.com"), os.environ.get("PASSWORD", "your_fallback_password"))
    if purpose == 'signup':
        message = f"회원가입 확인 링크: http://127.0.0.1:5000/verify_signup?token={token}"
    else:
        message = f"로그인 확인 링크: http://127.0.0.1:5000/verify_login?token={token}"
    server.sendmail(os.environ.get("EMAIL", "your_fallback_email@gmail.com"), email, message)
    server.quit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    send_email(email, token, 'signup')
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (email, token, verified) VALUES (?, ?, 0)", (email, token))
    conn.commit()
    conn.close()
    return render_template('signup_verification.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    send_email(email, token, 'login')
    return render_template('login_verification.html')

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
    if user:
        session['user_id'] = user[0]
        session['logged_in'] = True
        return render_template('verification_success.html', message="로그인 성공!")
    return render_template('verification_success.html', message="로그인 실패.")

if __name__ == '__main__':
    app.run(debug=True)
