import imaplib
from dotenv_read import EMAIL_PASS, EMAIL_USER, IMAP_SERVER

def connect_to_mail():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_USER, EMAIL_PASS)
    mail.select("inbox")
    return mail