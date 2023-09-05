### email_service.py
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

class EmailService:
    def __init__(self):
        self.email = os.environ.get("EMAIL")
        self.password = os.environ.get("PASSWORD")


    def send_email(self, to_email, token):
        try:
            smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtp.login(self.email, self.password)
            msg = MIMEMultipart()
            msg["From"] = self.email
            msg["To"] = to_email
            msg["Subject"] = "로그인 확인"
            content = f"로그인 확인 링크: http://127.0.0.1:5000/verify_login?token={token}"
            content_part = MIMEText(content, "plain")
            msg.attach(content_part)
            smtp.sendmail(self.email, to_email, msg.as_string())
            smtp.quit()
        except Exception as e:
            print(f"이메일 전송 실패: {e}")
            raise e