from sqlalchemy import Column, Integer, String, Date, ForeignKey
from database import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)
    login = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone_number = Column(String(20), unique=True)
    birth_date = Column(Date)
    photo = Column(String(200))
    additional_info = Column(String(500))
    last_login = Column(Date)
    created_at = Column(Date)

class Actor(Base):
    __tablename__ = 'actor'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    birth_date = Column(Date)
    death_date = Column(Date)
    description = Column(String(1000))


class ActorFilm(Base):
    __tablename__ = 'actor_film'
    id = Column(Integer, primary_key=True)
    actor_id = Column(Integer, ForeignKey("actor.id"), nullable=False)
    film_id = Column(Integer, ForeignKey("film.id"), nullable=False)


class Country(Base):
    __tablename__ = 'country'
    country_name = Column(String(100), primary_key=True, unique=True, nullable=False)


class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey('user.id'))
    film = Column(Integer, ForeignKey("film.id"))
    grade = Column(Integer)
    description = Column(String(1000))


class Film(Base):
    __tablename__ = 'film'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    year = Column(Integer, nullable=False)
    poster = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=False)
    rating = Column(Integer)
    duration = Column(Integer, nullable=False)
    country = Column(String(100), nullable=False)
    added_at = Column(Integer, nullable=False)


class FilmList(Base):
    __tablename__ = 'film_list'
    id = Column(Integer, primary_key=True)
    film_id = Column(Integer, ForeignKey('film.id'))
    list_id = Column(Integer, nullable=False)


class Genre(Base):
    __tablename__ = 'genre'
    genre = Column(String(100), primary_key=True, unique=True, nullable=False)


class GenreFilm(Base):
    __tablename__ = 'genre_film'
    id = Column(Integer, primary_key=True)
    genre_id = Column(String(100),ForeignKey('genre.genre'))
    film_id = Column(Integer, ForeignKey('film.id'))


class List(Base):
    __tablename__ = 'list'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
