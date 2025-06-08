import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.smtp_port = int(os.getenv("SMTP_PORT"))
        self.smtp_username = os.getenv("SMTP_USERNAME")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.email_from = os.getenv("EMAIL_FROM")

    def send_email(self, to_email: str, subject: str, body: str) -> bool:
        msg = MIMEMultipart()
        msg['From'] = self.email_from
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
                return True
        except smtplib.SMTPException as e:
            print(f"SMTP error occurred while sending email: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error occurred while sending email: {e}")
            return False

email_service = EmailService()