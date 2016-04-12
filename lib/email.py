# from flask_mail import Mail, Message
# import constants
#
#
# MAIL_SERVER = 'smtp.googlemail.com'
# MAIL_PORT = 465
# MAIL_USE_TLS = False
# MAIL_USE_SSL = True
# MAIL_USERNAME = 'swimautomail'
# MAIL_PASSWORD = 'projectpass110'
#
#
# def send_email(subject, sender, recipients, text_body, html_body,app):
#     mail = Mail(app)
#     # msg = Message(subject = "Test", sender=constants.DEFAULT_SENDER, recipients=constants.RECIPIENTS)
#     # msg.body = text_body
#     # msg.html = html_body
#     mail.send(msg)


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
