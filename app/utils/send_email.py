# This module contains utility functions for generating and sending password reset tokens.
from flask import url_for, current_app
from flask_mail import Message
from app import mail 

def send_reset_email(user):
    token = user.get_reset_token() # Generate the token

    # Construct the reset link.
    reset_link = url_for('auth.reset_token', token=token, _external=True)

    # Create the email message
    msg = Message('Password Reset Request',
                  sender=current_app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link: {reset_link} If you did not make this request, please ignore this email.
'''
    # try to send the email
    try:
        mail.send(msg)
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to send password reset email to {user.email}: {e}")
        return False