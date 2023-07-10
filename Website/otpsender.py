import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random

def otp_generator():
    otp = ''
    for _ in range(6):
        otp += str(random.randint(0, 9))
    return otp    

def send_otp_email(email):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587 
    smtp_username = 'shri.ai.codegen@gmail.com'
    smtp_password = 'oqomnmejovkllbdh'
    sender_email = 'shri.ai.codegen@gmail.com'
    subject = 'Verification Code for Password Reset - Shri AI'
    html_file_path = 'templates/otp.html'
    
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

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, email, msg.as_string())

        return otp_sent
    except Exception:
        return False
