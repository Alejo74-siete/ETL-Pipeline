# src/notifier.py
import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")


def send_email_report(body: str, subject: str = "ETL QC Report"):
    if not EMAIL_SENDER or not EMAIL_PASSWORD or not EMAIL_RECIPIENT:
        print("Email not configured, skipping send.")
        return

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECIPIENT

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, [EMAIL_RECIPIENT], msg.as_string())

    print("Email sent.")
