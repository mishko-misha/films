from celery import Celery
from celery.schedules import crontab
from jinja2 import Environment, FileSystemLoader, select_autoescape
from sqlalchemy import select
from email.mime.text import MIMEText

import database
import models
import os
import smtplib

app = Celery('tasks', broker='pyamqp://guest@localhost//')

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    autoescape=select_autoescape(['html', 'xml'])
)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute=1),
        build_and_send_daily_emails.s(),
        name='Film digest every day at 12am'
    )


# @app.task
# def send_email(recipient, subject, new_films):
#     FROM = os.environ.get("FROM_EMAIL")
#     TO = recipient if isinstance(recipient, list) else [recipient]
#
#     TEXT = jinja_env.get_template("digest.html").render(new_films=new_films)
#
#     msg = MIMEText(TEXT, "html", "utf-8")
#     msg["From"] = "myapp@example.com"
#     msg["To"] = ["misha.polunin@gmail.com"]
#     msg["Subject"] = subject
#
#     try:
#         server = smtplib.SMTP("smtp.gmail.com", 587)
#         server.ehlo()
#         server.starttls()
#         server.login('polunin1986@gmail.com', 'mxyh bkas gbgw bhkz')
#         server.sendmail(FROM, TO, msg.as_string())
#         server.close()
#         print('successfully sent the mail')
#     except Exception as e:
#         print("failed to send mail:", e)

@app.task
def send_email(recipient, subject, html_body):
    FROM = os.environ.get("FROM_EMAIL")
    print("FROM_EMAIL =", FROM)
    TO = recipient if isinstance(recipient, list) else [recipient]

    msg = MIMEText(html_body, "html", "utf-8")
    msg["From"] = FROM
    msg["To"] = ", ".join(TO)
    msg["Subject"] = subject

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login('polunin1986@gmail.com', 'mxyh bkas gbgw bhkz')
        server.sendmail(FROM, TO, msg.as_string())
        server.quit()
    except Exception as e:
        print("failed to send mail:", e)


# @app.task
# def build_and_send_daily_emails():
#     session = database.db_session()
#     try:
#         stmt = select(models.Film).order_by(models.Film.added_at.desc()).limit(15)
#         new_films = session.execute(stmt).scalars().all()
#         if not new_films:
#             return
#         # Celery works with dict, list, str, int, bool, float, None, JSON-like
#         # So we need to convert our Film objects to dict
#         # ORM does not support serialization
#         films_data = []
#         for film in new_films:
#             added_at = film.added_at
#             if isinstance(added_at, int):
#                 from datetime import datetime
#                 added_at = datetime.fromtimestamp(added_at)
#             films_data.append({
#                 'title': film.name,
#                 'description': film.description,
#                 'added_at': added_at.isoformat() if hasattr(added_at, 'isoformat') else str(added_at)
#             })
#
#         email_users = session.query(models.User).filter(models.User.email.isnot(None)).all()
#         for user in email_users:
#             send_email.delay(user.email, "Newest Films", films_data)
#     finally:
#         session.close()

@app.task
def build_and_send_daily_emails():
    session = database.db_session()
    try:
        stmt = select(models.Film).order_by(models.Film.added_at.desc()).limit(15)
        new_films = session.execute(stmt).scalars().all()
        if not new_films:
            return

        email_users = session.query(models.User).filter(
            models.User.email.isnot(None)
        ).all()

        for user in email_users:
            html_body = jinja_env.get_template("digest.html").render(new_films=new_films)

            send_email.delay(
                user.email,
                "Newest Films",
                html_body
            )
    finally:
        session.close()
