import smtplib
import uuid
import random
from email.mime.text import MIMEText
from datetime import datetime, timedelta

def generate_token():
    return str(uuid.uuid4())

def generate_otp():
    return str(random.randint(100000, 999999))

def send_email(to_email: str, subject: str, body: str):
    sender_email = "krunalgadher250@gmail.com"
    sender_password = "tjiz omjp pokw zjvw"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())

