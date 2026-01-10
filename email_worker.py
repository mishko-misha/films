from celery import Celery
from celery.schedules import crontab
from flask import render_template
from sqlalchemy import select
from email.mime.text import MIMEText

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

    TEXT = render_template("digest.html", new_films=new_films)

    msg = MIMEText(TEXT, "html", "utf-8")
    msg["From"] = FROM
    msg["To"] = ", ".join(TO)
    msg["Subject"] = subject

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login('user@gmail.com', 'xxxx xxxx xxxx xxxx')# user and password as mask
        server.sendmail(FROM, TO, msg.as_string())
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
        # Celery works with dict, list, str, int, bool, float, None, JSON-like
        # So we need to convert our Film objects to dict
        # ORM does not support serialization
        films_data = [{
            'title': film.title,
            'description': film.description,
            'added_at': film.added_at.isoformat()
        } for film in new_films]

        email_users = session.query(models.User).filter(models.User.email.isnot(None)).all()

        for user in email_users:
            send_email.delay(user.email, "Newest Films", films_data)
    finally:
        session.close()
