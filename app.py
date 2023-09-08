## app.py
from flask import Flask, session, request, render_template, redirect, url_for
import os
from dotenv import load_dotenv
from db_handler import DBHandler
from email_sender import EmailSender  # 이메일 발송 클래스는 예시로 적어둠
from session_handler import SessionHandler


load_dotenv()
app = Flask(__name__)


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DB_HOST = os.environ.get("DB_HOST")
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_NAME = os.environ.get("DB_NAME")
    DB_PORT = os.environ.get("DB_PORT", 3306)


app.config.from_object(Config)


db_config = {
    "host": app.config["DB_HOST"],
    "port": int(app.config["DB_PORT"]),
    "user": app.config["DB_USER"],
    "password": app.config["DB_PASSWORD"],
    "db": app.config["DB_NAME"],
    "charset": "utf8"
}


db_handler = DBHandler(db_config)
email_sender = EmailSender()  
session_handler = SessionHandler(db_handler)


@app.route('/')
def index():
    is_logged_in, user_data = session_handler.is_logged_in(session)
    email = user_data.get('USER_EMAIL') if is_logged_in else None
    return render_template('index.html', logged_in=is_logged_in, email=email)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        session_handler.manage_session(email, session)
        email_sender.send_email(email, session['user_data']['TOKEN_CD'])
        return redirect(url_for('login_verification'))        
    return render_template('login.html')


@app.route('/login_verification')
def login_verification():
    user_data = session.get('user_data', {})
    email = user_data.get('USER_EMAIL', 'unknown@example.com')
    domain = email.split('@')[1] if '@' in email else 'example.com'
    return render_template('login_verification.html', email_domain=domain)


@app.route('/verify_login')
def verify_login():
    token = request.args.get('token')
    if session_handler.verify_token(token, session):
        return redirect(url_for('index'))
    return render_template('verification_failed.html', message="로그인 실패: 사용자를 찾을 수 없습니다.")


@app.route('/logout')
def logout():
    session_handler.logout(session)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)