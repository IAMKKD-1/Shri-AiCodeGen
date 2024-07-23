import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import os
from dotenv import load_dotenv

load_dotenv()

smtp_server = os.environ.get('SMTP_SERVER')
smtp_port = os.environ.get('SMTP_PORT')
smtp_username = os.environ.get('SMTP_USERNAME')
smtp_password = os.environ.get('SMTP_PASSWORD')
sender_email = os.environ.get('SENDER_EMAIL')


def otp_generator():
    otp = ''
    for _ in range(6):
        otp += str(random.randint(0, 9))
    return otp    


def send_otp_email(email):
    subject = 'Verification Code for Password Reset - Shri AI'
    html_file_path = 'ShriWebsite/templates/otp.html'
    
    with open(html_file_path, 'r') as f:
        html_content = f.read()
    otp_sent = otp_generator()
    html_content = html_content.replace('{otp}', otp_sent)

    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = subject

        msg.attach(MIMEText(html_content, 'html'))

        with smtplib.SMTP(smtp_server, int(smtp_port)) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, email, msg.as_string())
            server.close()
        return otp_sent
    except Exception as e:
        print(e)
        return False
