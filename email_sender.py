import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv_read import EMAIL_USER, EMAIL_PASS

def send_result_email(recipient_email, original_subject, body_text):
    subject = f"Найкоротший маршрут: {original_subject}"

    message = MIMEMultipart()
    message["From"] = EMAIL_USER
    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(MIMEText(body_text, "plain"))

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(EMAIL_USER, EMAIL_PASS)
    server.send_message(message)
    server.quit()

    print(f"📤 Відповідь надіслано на {recipient_email} з темою: '{subject}'")
