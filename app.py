import os
import secrets
from datetime import datetime, UTC
from functools import wraps

from dateutil import parser
from dotenv import load_dotenv
from flask import Flask, render_template, request, session, redirect, url_for, flash
from jinja2 import Environment, FileSystemLoader, select_autoescape
from sqlalchemy import select, or_, and_, delete, func, update

import database
import email_worker
import models

load_dotenv()
SECRET_KEY = os.environ.get("SECRET_KEY")

app = Flask(__name__)
app.secret_key = SECRET_KEY

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    autoescape=select_autoescape(['html', 'xml']))


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get('user_id'):
            return f(*args, **kwargs)
        else:
            return redirect(url_for('user_login'))

    return wrapper


def current_user_data():
    user_session = session.get('logged_in', False)
    user_id = session.get('user_id')
    username = None
    database.init_db()
    if user_session and user_id:
        stmt = select(models.User).where(models.User.id == user_id)
        user = database.db_session().execute(stmt).scalars().first()
        if user:
            username = user.login
    return user_session, username


@app.route('/')
def main_page():
    user_session, username = current_user_data()
    database.init_db()
    stmt = select(models.Film).order_by(models.Film.added_at.desc()).limit(15)
    film = database.db_session().execute(stmt).scalars().all()
    return render_template('index.html', user_session=user_session, username=username, films=film)


def create_and_save_confirmation_code(user):
    token = secrets.token_urlsafe(32)
    user.token = token
    db_session = database.db_session()
    db_session.commit()
    return token


def build_message_body_for_confirmation(token, first_name):
    confirm_url = url_for('confirm_email', token=token, _external=True)

    return jinja_env.get_template("confirm_registration.html").render(
        first_name=first_name,
        confirm_url=confirm_url
    )


@app.route('/confirm_email/<token>')
def confirm_email(token):
    db_session = database.db_session()
    user = db_session.query(models.User).filter_by(token=token).first()

    if not user:
        return "Invalid or expired token", 400

    user.active = True
    user.token = None
    db_session.commit()

    return render_template("email_confirmed.html", first_name=user.first_name)


@app.route('/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        first_name = request.form['username']
        last_name = request.form['lname']
        login = request.form['login']
        email = request.form['email']
        password = request.form['password']
        birth_date = parser.parse(request.form['birth_date'])

        database.init_db()
        db_session = database.db_session()
        new_user = models.User(
            first_name=first_name,
            last_name=last_name,
            login=login,
            email=email,
            password=password,
            birth_date=birth_date
        )
        new_user.active = False

        db_session.add(new_user)
        db_session.commit()

        token = create_and_save_confirmation_code(new_user)
        html_body = build_message_body_for_confirmation(token, new_user.first_name)
        email_worker.send_email.delay(new_user.email, "Confirm your registration", html_body)

        return render_template('confirm_check_email.html', first_name=new_user.first_name)
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        database.init_db()
        db_session = database.db_session()
        stmt = select(models.User).where(and_(models.User.login == login, models.User.password == password))
        user = db_session.execute(stmt).scalars().first()
        if user:
            user.last_login = datetime.now(UTC)
            db_session.commit()
            session['logged_in'] = True
            session['user_id'] = user.id
            return redirect(url_for('main_page'))
    return render_template('login.html')


@app.route('/logout', methods=['GET'])
def user_logout():
    session.clear()
    return redirect(url_for('main_page'))


@app.route('/films', methods=['GET'])
def films():
    user_session, username = current_user_data()
    films_query = select(models.Film)
    for key, value in request.args.items():
        if value:
            if key == 'name':
                films_query = films_query.where(models.Film.name.like(f'%{value}%'))
            elif key == 'rating':
                value = float(value)
                films_query = films_query.where(models.Film.rating == value)
            elif key == 'country':
                films_query = films_query.where(models.Film.country == value)
            elif key == 'year':
                films_query = films_query.where(models.Film.year == int(value))
            elif key == 'actor':
                films_query = films_query.join(models.ActorFilm, models.Film.id == models.ActorFilm.film_id) \
                    .join(models.Actor, models.Actor.id == models.ActorFilm.actor_id) \
                    .where(or_(
                    models.Actor.first_name.ilike(f'%{value}%'),
                    models.Actor.last_name.ilike(f'%{value}%')
                )
                )
            elif key == 'genre':
                films_query = films_query.join(models.GenreFilm, models.Film.id == models.GenreFilm.film_id) \
                    .where(models.GenreFilm.genre_id == value)

    films_query = films_query.order_by(models.Film.added_at.desc())
    result_films = database.db_session.execute(films_query).scalars().all()
    country_query = select(models.Country)
    countries = database.db_session.execute(country_query).scalars().all()
    genres_query = select(models.Genre)
    genres = database.db_session.execute(genres_query).scalars().all()
    return render_template('films.html', films=result_films, genres=genres, countries=countries,
                           user_session=user_session, username=username)


@app.route('/films/new', methods=['GET', 'POST'])
@login_required
def film_create():
    database.init_db()
    db_session = database.db_session()

    genres = db_session.execute(select(models.Genre)).scalars().all()
    countries_list = db_session.execute(select(models.Country)).scalars().all()

    if request.method == 'POST':
        name = request.form['name']
        year = int(request.form['year'])
        poster = request.form['poster_url']
        description = request.form['description']
        rating = float(request.form['rating'])
        duration = int(request.form['duration'])
        country_name = request.form['country']

        new_film = models.Film(
            name=name,
            year=year,
            poster=poster,
            description=description,
            country=country_name,
            rating=rating,
            duration=duration,
            added_at=datetime.now(UTC)
        )
        db_session.add(new_film)
        db_session.flush()

        selected_genres = request.form.getlist('genres')
        for genre_id in selected_genres:
            db_session.add(models.GenreFilm(
                film_id=new_film.id,
                genre_id=genre_id
            ))

        actors_text = request.form.get('actors', '').strip()
        if actors_text:
            for line in actors_text.splitlines():
                line = line.strip()
                if not line:
                    continue
                parts = line.split(maxsplit=1)
                first_name = parts[0]
                last_name = parts[1] if len(parts) > 1 else ''
                actor = models.Actor(first_name=first_name, last_name=last_name)
                db_session.add(actor)
                db_session.flush()  # чтобы получить actor.id
                db_session.add(models.ActorFilm(
                    film_id=new_film.id,
                    actor_id=actor.id
                ))

        db_session.commit()
        return redirect(url_for('films'))

    return render_template('film_create.html', genres=genres, countries=countries_list)


@app.route('/films/<int:film_id>', methods=['GET'])
def film_detail(film_id):
    user_session, username = current_user_data()
    database.init_db()
    db_session = database.db_session()

    film_by_id = select(models.Film).where(models.Film.id == film_id)
    result = db_session.execute(film_by_id).scalar_one()

    actors_query = select(models.Actor).join(models.ActorFilm, models.Actor.id == models.ActorFilm.actor_id).where(
        models.ActorFilm.film_id == film_id)
    actors = db_session.execute(actors_query).scalars()

    genres_query = select(models.Genre).join(models.GenreFilm, models.Genre.genre == models.GenreFilm.genre_id).where(
        models.GenreFilm.film_id == film_id)
    genres = db_session.execute(genres_query).scalars()

    all_feedbacks = db_session.execute(
        select(models.Feedback).where(models.Feedback.film == film_id)
    ).scalars().all()

    user_feedback = None
    if 'user_id' in session:
        user_feedback = db_session.execute(
            select(models.Feedback).where(
                models.Feedback.film == film_id,
                models.Feedback.user == session['user_id']
            )
        ).scalars().first()
    grade_query = (
        select(func.avg(models.Feedback.grade).label('average'),
               func.count(models.Feedback.id).label('rating_count'))
        .where(models.Feedback.film == film_id)
    )
    grade = database.db_session().execute(grade_query).fetchone()
    return render_template('film_detail.html', film=result, actors=actors, genres=genres, all_feedbacks=all_feedbacks,
                           user_feedback=user_feedback, average_rating=grade.average, rating_count=grade.rating_count,
                           user_session=user_session, username=username)


@app.route('/films/<int:film_id>/delete', methods=['GET', 'POST'])
@login_required
def film_delete(film_id):
    database.init_db()
    db_session = database.db_session()
    if request.method == 'POST':
        db_session.query(models.GenreFilm).filter(models.GenreFilm.film_id == film_id).delete()
        db_session.query(models.ActorFilm).filter(models.ActorFilm.film_id == film_id).delete()
        db_session.query(models.Film).filter(models.Film.id == film_id).delete()
        db_session.commit()
        return redirect(url_for('films'))
    film_stmt = select(models.Film).where(models.Film.id == film_id)
    film = db_session.execute(film_stmt).scalars().first()
    return render_template('confirm_film_delete.html', film=film)


@app.route('/films/<int:film_id>/rating', methods=['GET'])
def film_rating(film_id):
    user_session, username = current_user_data()
    database.init_db()

    ratings_query = select(models.Feedback).where(models.Feedback.film == film_id)
    ratings = database.db_session().execute(ratings_query).scalars().all()

    grades_query = (select(func.avg(models.Feedback.grade).label('average'),
                           func.count(models.Feedback.id).label('rating_count')).where(models.Feedback.film == film_id))
    grade = database.db_session().execute(grades_query).fetchone()
    return render_template(
        'film_rating.html',
        user_session=user_session,
        username=username,
        film_id=film_id,
        average_rating=grade.average,
        rating_count=grade.rating_count,
        ratings=ratings
    )


@app.route('/films/<film_id>/rating/<feedback_id>', methods=['GET', 'POST'])
@login_required
def film_feedback(film_id, feedback_id):
    database.init_db()
    db_session = database.db_session()
    if request.method == 'POST':
        grade = request.form['grade']
        description = request.form['description']
        stmt = update(models.Feedback).where(models.Feedback.id == feedback_id).values(
            grade=grade,
            description=description
        )
        db_session.execute(stmt)
        db_session.commit()
        return redirect(url_for('film_rating', film_id=film_id))
    else:
        feedback_query = select(models.Feedback).where(and_(
            models.Feedback.film == film_id,
            models.Feedback.id == feedback_id
        ))
        feedback = db_session.execute(feedback_query).scalars().first()
        return render_template('film_feedback.html', film_id=film_id, feedback_id=feedback_id, feedback=feedback)


@app.route('/films/<int:film_id>/feedback/new', methods=['GET', 'POST'])
@login_required
def film_feedback_new(film_id):
    database.init_db()
    db_session = database.db_session()

    if request.method == 'POST':
        grade = request.form['grade']
        description = request.form['description']

        new_feedback = models.Feedback(
            user=session['user_id'],
            film=film_id,
            grade=grade,
            description=description
        )
        db_session.add(new_feedback)
        db_session.commit()

        return redirect(url_for('film_detail', film_id=film_id))

    return render_template('film_feedback.html', film_id=film_id, feedback=None)


@app.route('/films/<int:film_id>/feedback/<int:feedback_id>/delete', methods=['GET', 'POST'])
def film_feedback_delete(film_id, feedback_id):
    database.init_db()
    db_session = database.db_session()
    if request.method == 'POST':
        stmt = delete(models.Feedback).where(models.Feedback.id == feedback_id)
        db_session.execute(stmt)
        db_session.commit()
        return redirect(url_for('film_detail', film_id=film_id))
    feedback_stmt = select(models.Feedback).where(models.Feedback.id == feedback_id)
    feedback = db_session.execute(feedback_stmt).scalars().first()
    return render_template('confirm_feedback_delete.html', feedback=feedback, film_id=film_id)


@app.route('/users/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user_profile(user_id):
    session_user_id = session['user_id']
    database.init_db()

    if request.method == 'POST':
        if user_id != session_user_id:
            return 'Unauthorized', 403

        first_name = request.form['username']
        last_name = request.form['lname']
        password = request.form['password']
        email = request.form['email']
        phone_number = request.form['phone_number']
        birth_date = request.form['birth_date']
        photo = request.form['photo']
        additional_info = request.form['additional_info']

        stmt = update(models.User).where(models.User.id == user_id).values(
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email,
            phone_number=phone_number,
            birth_date=parser.parse(birth_date),
            photo=photo,
            additional_info=additional_info
        )
        database.db_session().execute(stmt)
        database.db_session().commit()
        return redirect(url_for('user_profile', user_id=user_id))

    else:
        stmt = select(models.User).where(models.User.id == user_id)
        user = database.db_session().execute(stmt).scalars().first()
        stmt_session = select(models.User).where(models.User.id == session_user_id)
        user_session = database.db_session().execute(stmt_session).scalars().first()
        return render_template('user_profile.html', user=user, user_session=user_session)


@app.route('/users/<int:user_id>/delete', methods=['GET', 'POST'])
@login_required
def user_delete(user_id):
    database.init_db()
    db_session = database.db_session()
    if request.method == 'POST':
        stmt = delete(models.User).where(models.User.id == user_id)
        db_session.execute(stmt)
        db_session.commit()
        db_session.close()

        session.clear()

        return redirect(url_for('main_page'))
    user_stmt = select(models.User).where(models.User.id == user_id)
    user = db_session.execute(user_stmt).scalars().first()
    return render_template('confirm_user_delete.html', user=user)


@app.route('/users/<user_id>/lists', methods=['GET', 'POST'])
@login_required
def user_lists(user_id):
    database.init_db()
    db_session = database.db_session()
    user = db_session.execute(
        select(models.User).where(models.User.id == user_id)
    ).scalars().first()
    if request.method == 'POST':
        list_name = request.form['list_name']
        new_list = models.List(
            user_id=user_id,
            name=list_name
        )
        db_session.add(new_list)
        db_session.commit()
        return redirect(url_for('user_lists', user_id=user_id))
    else:
        stmt = select(models.List).where(models.List.user_id == user_id)
        lists = db_session.execute(stmt).scalars().all()
        return render_template('user_lists.html', user_id=user.id, user=user, lists=lists)


@app.route('/users/<user_id>/lists/<list_id>/delete',
           methods=['GET', 'POST'])  # Remove list not films from list!!!! work with List model
@login_required
def user_list_detail(user_id, list_id):
    database.init_db()
    db_session = database.db_session()
    if request.method == 'POST':
        stmt = delete(models.List).where(models.List.id == list_id)
        db_session.execute(stmt)
        db_session.commit()
        return redirect(url_for('user_lists', user_id=user_id))
    list_stmt = select(models.List).where(models.List.id == list_id)
    user_list = db_session.execute(list_stmt).scalars().first()
    return render_template('confirm_list_delete.html', user_list=user_list, list_id=list_id, user_id=user_id)


@app.route('/users/<user_id>/lists/<list_id>', methods=['GET', 'POST'])
@login_required
def user_watch_later_list(user_id, list_id):
    database.init_db()
    db_session = database.db_session()
    user = db_session.execute(
        select(models.User).where(models.User.id == user_id)
    ).scalars().first()

    if request.method == 'POST':
        film_name = request.form['film_name']

        film = db_session.execute(
            select(models.Film).where(models.Film.name.ilike(f'%{film_name}%'))
        ).scalars().first()

        if not film:
            return redirect(url_for('user_watch_later_list', user_id=user.id, list_id=list_id))

        existing_film_in_list = db_session.execute(
            select(models.FilmList).where(models.FilmList.list_id == list_id, models.FilmList.film_id == film.id)
        ).scalars().first()

        if existing_film_in_list:
            flash('Film already in the list.')
        else:
            new_film_in_list = models.FilmList(
                list_id=list_id,
                film_id=film.id
            )
            db_session.add(new_film_in_list)
            db_session.commit()
        return redirect(url_for('user_watch_later_list', user_id=user.id, list_id=list_id))
    stmt = select(models.Film).join(models.FilmList, models.Film.id == models.FilmList.film_id).where(
        models.FilmList.list_id == list_id)
    films_result = db_session.execute(stmt).scalars().all()
    return render_template('user_watch_later_list.html', user=user, user_id=user_id, list_id=list_id,
                           films=films_result)


@app.route('/users/<user_id>/lists/<list_id>/<film_id>/delete', methods=['GET', 'POST'])
@login_required
def remove_film_from_list(user_id, list_id, film_id):
    database.init_db()
    db_session = database.db_session()
    if request.method == 'POST':
        stmt = delete(models.FilmList).where(
            and_(
                models.FilmList.list_id == list_id,
                models.FilmList.film_id == film_id
            )
        )
        db_session.execute(stmt)
        db_session.commit()
        return redirect(url_for('user_watch_later_list', user_id=user_id, list_id=list_id))
    return render_template('user_watch_later_list.html', user_id=user_id, list_id=list_id, film_id=film_id)


@app.teardown_appcontext
def shutdown_session(exception=None):
    database.db_session.remove()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
