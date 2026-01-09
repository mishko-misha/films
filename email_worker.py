from celery import Celery
from celery.schedules import crontab
from flask import render_template
from sqlalchemy import select

import database
import models
import os
import smtplib

app = Celery('tasks', broker='pyamqp://guest@localhost//')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=8, minute=0),
        build_and_send_daily_emails.s(),
        name='Film digest every day at 8am'
    )


@app.task
def send_email(recipient, subject, new_films):
    FROM = os.environ.get("FROM_EMAIL")
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = "Film Notification"
    TEXT = render_template("email_template.html", new_films=new_films)

    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login('user@gmail.com', 'xxxx xxxx xxxx xxxx')# user and password as mask
        server.sendmail(FROM, TO, message)
        server.close()
        print('successfully sent the mail')
    except Exception as e:
        print("failed to send mail:", e)


@app.task
def build_and_send_daily_emails():
    session = database.db_session()
    try:
        stmt = select(models.Film).order_by(models.Film.added_at.desc()).limit(15)
        new_films = session.execute(stmt).scalars().all()
        if not new_films:
            return

        email_users = session.query(models.User).filter(models.User.email.isnot(None)).all()

        for user in email_users:
            send_email.delay(user.email, "Newest Films Just Added", new_films)
    finally:
        session.close()
