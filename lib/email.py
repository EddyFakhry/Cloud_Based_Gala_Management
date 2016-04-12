
import os
from flask_mail import Mail, Message

_EMAIL_CONFIG = {
    'MAIL_SERVER': 'smtp.gmail.com',
    'MAIL_PORT': 465,
    'MAIL_USE_TLS': False,
    'MAIL_USE_SSL': True,
    'MAIL_USERNAME': 'swimautomail@gmail.com',
    'MAIL_PASSWORD': 'projectpass110'
}


class Mailer:
    def __init__(self, app):
        app.config.update(_EMAIL_CONFIG)
        self.app = app
        self.mail = Mail(app)

    def send_mail(self, recipient, subject, body, html=None):
        msg = Message(subject, sender="confirm@gmail.com", recipients=[recipient])
        msg.body = body
        if html is not None:
            msg.html = html
        with self.app.app_context():
            self.mail.send(msg)
