import os
import smtplib
from email.message import EmailMessage

SMTP_PASSWORD = os.environ["SMTP_PASSWORD"]
SMTP_EMAIL = os.environ["SMTP_EMAIL"]


def send_email(receiver_email, token):
    text = (
    "Hello,\n\nWe received a request for a password change on your team-finder-404.web.app account."
    " You can reset your password by clicking this link:"
    f" https://team-finder-404.web.app/newpassword/{token}\n\n"
    "This link will expire in 12 hours. After that, you'll need to submit a new request in order"
    " to reset your password. If you don't want to reset it, simply disregard this email.\n\n"
    "(Please don't reply to this message; it's automated)\n\nThanks,\nTeam Finder"
    )

    message = EmailMessage()
    message["Subject"] = "Password reset request"
    message["From"] = SMTP_EMAIL
    message["To"] = receiver_email
    message.set_content(text, subtype="plain", charset='us-ascii')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(SMTP_EMAIL, SMTP_PASSWORD)
        smtp_server.sendmail(SMTP_EMAIL, receiver_email, message.as_string())
