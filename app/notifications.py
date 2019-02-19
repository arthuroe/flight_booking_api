import logging

from flask_mail import Message
from threading import Thread

from app import app, mail


def send_async_email(app, msg):
    with app.app_context():
        app.update
        mail.send(msg)


def send_email(subject, recipients, text_body, html_body):
    """
    Helper function for sending email
    """
    try:
        msg = Message(subject, recipients=recipients)
        msg.sender = os.getenv("DEFAULT_EMAIL_SENDER")
        msg.body = text_body
        msg.html = html_body
        thr = Thread(target=send_async_email, args=[app, msg])
        thr.start()
    except Exception as e:
        logging.error(f"An error has occurred  {e}")
        return e
