### email_service.py
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# 환경 변수를 로드합니다.
load_dotenv()

# EmailService 클래스 정의
class EmailService:
    # 생성자에서 환경 변수로부터 이메일과 비밀번호를 불러옵니다.
    def __init__(self):
        self.email = os.environ.get("EMAIL")
        self.password = os.environ.get("PASSWORD")

    # 이메일을 발송하는 메소드입니다.
    def send_email(self, to_email, token):
        try:
            # SMTP 설정과 로그인을 수행합니다.
            smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtp.login(self.email, self.password)

            # 이메일 메시지를 구성합니다.
            msg = MIMEMultipart()
            msg["From"] = self.email
            msg["To"] = to_email
            msg["Subject"] = "로그인 확인"
            content = f"로그인 확인 링크: http://127.0.0.1:5000/verify_login?token={token}"

            content_part = MIMEText(content, "plain")
            msg.attach(content_part)

            # 이메일을 발송합니다.
            smtp.sendmail(self.email, to_email, msg.as_string())
            smtp.quit()
            print("이메일 성공적으로 발송")
        except Exception as e:
            print(f"이메일 전송 실패: {e}")
