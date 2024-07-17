import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os



otp_storage = {}

def send_otp_via_email(receiver_email: str, otp: str):
    sender_email = os.getenv("sender_email")
    password = os.getenv("password")
    subject = "Your OTP Code"
    message_text = f"Your OTP is {otp} which is valid for 5 minute"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(message_text, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Mail sent successfully")
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")