import os
import datetime
import psycopg2
from dotenv import load_dotenv

load_dotenv()

CREATE_MOVIE_TABLE = "CREATE TABLE IF NOT EXISTS movies (id SERIAL PRIMARY KEY, title TEXT,release_timestamp REAL);"

CREATE_USER_TABLE = "CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY);"

CREATE_WATCH_LIST_TABLE = """ CREATE TABLE IF NOT EXISTS watched (
    user_username TEXT,
    movie_id INTEGER,
    FOREIGN KEY(user_username) REFERENCES users (username),
    FOREIGN KEY(movie_id) REFERENCES movies (id));
"""

INSERT_MOVIES = "INSERT INTO movies (title,release_timestamp) VALUES (%s,%s);"
SELECT_ALL_MOVIES = "SELECT * FROM movies;"
SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > %s;"
INSERT_USER = "INSERT INTO users(username) VALUES (%s);"
SELECT_WATCHED_MOVIES = "SELECT movies.* FROM watched " \
                        "JOIN movies ON movies.id = watched.movie_id " \
                        "JOIN users ON watched.user_username=users.username WHERE users.username = %s;"
INSERT_MOVIES_WATCHED = "INSERT INTO watched VALUES (%s,%s);"
DELETE_MOVIE = "DELETE FROM movies WHERE title = %s;"
SEARCH_MOVIE = "SELECT * FROM movies WHERE title LIKE %s;"
RELEASE_INDEX = "CREATE INDEX IF NOT EXISTS inx_release_timestamp ON movies(release_timestamp);"


connection = psycopg2.connect(os.environ["DATABASE_URL"])


def create_table():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_MOVIE_TABLE)
            cursor.execute(CREATE_USER_TABLE)
            cursor.execute(CREATE_WATCH_LIST_TABLE)
            cursor.execute(RELEASE_INDEX)

def add_user(username):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_USER,(username,))


def add_movie(title, release_timestamp):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_MOVIES, (title, release_timestamp))


def get_movies(upcoming=False):
    with connection:
        with connection.cursor() as cursor:
            if upcoming:
                right_now = datetime.datetime.today().timestamp()
                cursor.execute(SELECT_UPCOMING_MOVIES, (right_now,))
            else:
                cursor.execute(SELECT_ALL_MOVIES)

            return cursor.fetchall()

def search_movie(search_term):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SEARCH_MOVIE,(f"%{search_term}%",))
            return cursor.fetchall()



def watch_movie(watcher, movie_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_MOVIES_WATCHED, (watcher, movie_id))


def get_watched_movies(watcher):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_WATCHED_MOVIES, (watcher,))
            return cursor.fetchall()
