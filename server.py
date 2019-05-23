import flask
import json
import argparse
from tools import correct_mood, correct_age, correct_company, correct_genre, correct_people, all_genres, genres_valuates
from films import smart_function, cfilm
from drinks import drink_smart_function
from mini_script import just

import psycopg2

app = flask.Flask("Film_recomendation")

params = dict(dbname="postgres", user="postgres", password="8246", host="localhost")

with psycopg2.connect(**params) as conn:
    cur = conn.cursor()

    cur.execute('DROP TABLE IF EXISTS bd_films CASCADE')
    cur.execute('DROP TABLE IF EXISTS user_session CASCADE')
    cur.execute('DROP TABLE IF EXISTS login CASCADE')
    cur.execute('DROP TABLE IF EXISTS genres_valuates CASCADE')

    cur.execute('''
        CREATE TABLE bd_films (
            name VARCHAR(255) PRIMARY KEY,
            genre VARCHAR(255),
            mood integer,
            company VARCHAR(255),
            age integer,
            age_rating integer
        )
    ''')
    cur.execute('''
            CREATE TABLE login (
                nick VARCHAR(255) PRIMARY KEY,
                password VARCHAR(255)
            )
        ''')
    cur.execute('''
            CREATE TABLE user_session(
                nick VARCHAR(255) PRIMARY KEY,
                mood integer,
                company VARCHAR(255),
                people integer,
                age integer,
                genres VARCHAR(255),
                FOREIGN KEY(nick) REFERENCES login(nick)
            )
        ''')

    cur.execute('''
    CREATE TABLE genres_valuates(
    first_genre VARCHAR(255),
    second_genre VARCHAR(255),
    value double precision,
    PRIMARY KEY(first_genre, second_genre)
    )
    ''')



def add_user_login(cur_cursor, cur_nick, cur_password):
    cur_cursor.execute("INSERT INTO login (nick, password) VALUES ('{}', '{}')".format(cur_nick, cur_password))


def add_user_session_mood(cur_cursor, cur_nick, cur_mood):
    cur_cursor.execute("UPDATE user_session SET mood = {} WHERE nick = '{}'". format(cur_mood, cur_nick))


def add_user_session_company(cur_cursor, cur_nick, cur_company, cur_people):
    cur_cursor.execute("UPDATE user_session SET company = '{}', people = '{}' WHERE nick = '{}'". format(cur_company, cur_people, cur_nick))


def add_user_session_age(cur_cursor, cur_nick, cur_age):
    cur_cursor.execute("UPDATE user_session SET age = '{}' WHERE nick = '{}'". format(cur_age, cur_nick))


def add_user_session_genres(cur_cursor, cur_nick, cur_genres):
        cur_cursor.execute("UPDATE user_session SET genres = '{}' WHERE nick = '{}'". format(cur_genres, cur_nick))


def add_film_info(cur_cursor, cur_film_name, cur_genre, cur_mood, cur_company, cur_age, cur_age_rating):
    cur_cursor.execute("INSERT INTO bd_films (name, genre, mood, company, age, age_rating)"
                       " VALUES ('{}', '{}', '{}', '{}', '{}', '{}')"
                       .format(cur_film_name, cur_genre, cur_mood, cur_company, cur_age, cur_age_rating))


def add_genres_valuate(cur_cursor, first_genre, second_genre, genres_value):
    cur_cursor.execute("INSERT INTO genres_valuates (first_genre, second_genre, value)"
                       " VALUES ('{}', '{}', '{}')".format(first_genre, second_genre, genres_value))


def check_nick(cur_cursor, cur_nick):     # do not know
    q = "SELECT * FROM login WHERE nick = '{}'".format(cur_nick)
    cur_cursor.execute(q)
    for row in cur_cursor:          # i dont know how can i check null query, is None doesnt work
        return True
    return False


def check_all_param(cur_cursor, cur_nick):
    q = "SELECT mood, company, people, age, genres FROM user_session where nick = '{}'".format(cur_nick)
    cur_cursor.execute(q)
    row = cur_cursor.fetchone()
    if row[0] is None or row[1] is None or row[3] is None:
        return None
    dct_param = {'mood': row[0], 'company': row[1], 'people': row[2], 'age': row[3]}
    if row[4] is not None:
        dct_param['genres'] = row[4].split(' ')
    return dct_param


def choose_film(cur_intrests):
    if 'genres' not in cur_intrests:
        cur_intrests['genres'] = all_genres
    name_film = None
    value = -100
    with psycopg2.connect(**params) as conn:
        cur_cursor = conn.cursor()
        q = "SELECT name, genre, mood, company, age, age_rating FROM bd_films"
        cur_cursor.execute(q)
        for f in cur_cursor:
            name, genre, mood, company, age, age_rating = f
            cur_dct = {'name': name, 'mood': mood, 'company': company, 'age': age, 'age_rating': age_rating, 'genre': genre}
            cur_film = cfilm(cur_dct)
            if smart_function(cur_film, cur_intrests) > value:
                value = smart_function(cur_film, cur_intrests)
                name_film = cur_film.name
        return name_film


with psycopg2.connect(**params) as conn:
    film_info = just()
    add_cur = conn.cursor()
    for cur_film in film_info:
        add_film_info(add_cur, cur_film['film'], cur_film['genre'], cur_film['mood'], cur_film['company'], cur_film['age'], cur_film['age_rating'])

    for ((f_genre, s_genre), g_value) in genres_valuates.items():
        add_genres_valuate(add_cur, f_genre, s_genre, g_value)

    conn.commit()


@app.route('/register', methods=['POST'])
def register():
    with psycopg2.connect(**params) as conn:
        cur_cursor = conn.cursor()
        if check_nick(cur_cursor, flask.request.json['nick']):
            flask.abort(400)
        else:
            add_user_login(cur_cursor, flask.request.json['nick'], flask.request.json['password'])
            conn.commit()
            return 'ok'


@app.route('/check_log', methods=['POST'])
def check_login():
    cur_nick = flask.request.json['login']
    cur_password = flask.request.json['password']
    with psycopg2.connect(**params) as conn:
        cur = conn.cursor()
        cur.execute("SELECT nick, password FROM login")  # too much time
        for row in cur:
            if (cur_nick, cur_password) == row:
                return 'ok'
    return flask.abort(400)


@app.route('/add_session_of_user', methods=['POST'])
def add_session_of_user():
    with psycopg2.connect(**params) as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO user_session (nick) VALUES ('{}')".format(flask.request.json['nick']))             # МОЖЕТ ПРОИЗОЙТИ ФИГНЯ, ЕСЛИ ПОД ОДНИМ НИКОМ АКТИВНО НЕСКОЛЬКО СЕССИЙ
        conn.commit()                                                                                               # ОПЯТЬ ЖЕ ИЗОЛИР ТРАНЗАКЦИЙ
    return 'ok'


@app.route('/add_mood', methods=['POST'])
def add_mood():
    if not correct_mood(flask.request.json['mood']):
        flask.abort(400)
    else:
        with psycopg2.connect(**params) as conn:
            cur = conn.cursor()
            add_user_session_mood(cur, flask.request.json['nick'], flask.request.json['mood'])
            conn.commit()
            return 'ok'


@app.route('/add_genres', methods=['POST'])
def add_genres():
    if not correct_genre(flask.request.json['genres']):
        return flask.abort(400)
    else:
        with psycopg2.connect(**params) as conn:
            cur = conn.cursor()
            add_user_session_genres(cur, flask.request.json['nick'], flask.request.json['genres'])
            conn.commit()
        return 'ok'


@app.route('/end_session', methods=['POST'])
def end_session():
    with psycopg2.connect(**params) as conn:
        cur = conn.cursor()
        q = "DELETE FROM user_session WHERE nick = '{}'".format(flask.request.json['nick'])
        cur.execute(q)
        conn.commit()
    return 'ok'


@app.route('/add_age', methods=['POST'])
def add_age():
    if not correct_age(flask.request.json['age']):
        flask.abort(400)
    else:
        with psycopg2.connect(**params) as conn:
            cur = conn.cursor()
            add_user_session_age(cur, flask.request.json['nick'], flask.request.json['age'])
            conn.commit()
        return 'ok'


@app.route('/add_company', methods=['POST'])
def add_company():
    if not correct_company(flask.request.json['company']) or not correct_people(flask.request.json['people']):
        flask.abort(400)
    else:
        with psycopg2.connect(**params) as conn:
            cur = conn.cursor()
            add_user_session_company(cur, flask.request.json['nick'], flask.request.json['company'], flask.request.json['people'])
            conn.commit()
        return 'ok'


@app.route('/get_film', methods=['GET'])
def get_film():
    with psycopg2.connect(**params) as conn:
        cur_cursor = conn.cursor()
        param_user = check_all_param(cur_cursor, flask.request.json['nick'])
        if param_user is not None:
            return json.dumps(choose_film(param_user))
        else:
            flask.abort(400)


@app.route('/get_drink', methods=['GET'])
def get_drink():
    with psycopg2.connect(**params) as conn:
        cur_cursor = conn.cursor()
        param_film = check_all_param(cur_cursor, flask.request.json['nick'])
        if param_film is not None:
            return json.dumps(drink_smart_function(param_film))
        else:
            flask.abort(400)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=50000, type=int)
    args = parser.parse_args()
    app.run('localhost', args.port, debug=True, threaded=True)


if __name__ == '__main__':
    main()
