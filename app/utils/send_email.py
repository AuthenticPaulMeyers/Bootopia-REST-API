# This module contains utility functions for generating and sending password reset tokens.
from flask_mail import Message
from app import mail 
from flask import current_app as app
from flask import url_for
def send_email(subject, sender, recipients, text_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    # Send the email using Flask-Mail
    mail.send(msg)

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    link = url_for('auth.reset_password', token=token, _external=True)

    send_email('Password reset request',
    sender=app.config['MAIL_USERNAME'],
    recipients=[user.email],
    text_body=f"Hello { user.username }, To reset your password please click on the following link: {link}. If you have not requested a password reset simply ignore this message. Sincerely, The Bootopia Support Team")
