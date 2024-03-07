from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from database.db import db


def delete_expired_signup_tokens():
    signup_tokens = db.get_signup_tokens()
    format = "%Y-%m-%d %H:%M:%S"
    current_time = datetime.utcnow()

    for token in signup_tokens:
        if datetime.strptime(token.get("expires_at"), format) < current_time:
            print("DELETED", token.get("id"))
            db.delete_signup_token(token.get("id"))


scheduler = BackgroundScheduler()

scheduler.add_job(delete_expired_signup_tokens, "interval", hours=12)
