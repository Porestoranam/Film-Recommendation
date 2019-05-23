import flask
import json
import argparse
from tools import correct_mood, correct_age, correct_company, correct_genre, correct_people, all_genres, genres_valuates
from films import smart_function, cfilm, companies_valuate
from drinks import drink_smart_function
from mini_script import just

import psycopg2

app = flask.Flask("Film_recomendation")

params = dict(dbname="postgres", user="postgres", password="8246", host="localhost")


def create_data_base(dbname_="postgres", user_="postgres", password_="8246", host_="localhost"):
    params = dict(dbname=dbname_, user=user_, password=password_, host=host_)
    with psycopg2.connect(**params) as conn:
        cur = conn.cursor()
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

        cur.execute('''
        CREATE TABLE companies_valuates(
        first_company VARCHAR(255),
        second_company VARCHAR(255),
        value DOUBLE PRECISION,
        PRIMARY KEY (first_company, second_company)
        )
        ''')
        cur.commit()

    with psycopg2.connect(**params) as conn:
        film_info = just()
        add_cur = conn.cursor()
        for cur_film in film_info:
            add_film_info(add_cur, cur_film['film'], cur_film['genre'], cur_film['mood'], cur_film['company'],
                          cur_film['age'], cur_film['age_rating'])

        for ((f_genre, s_genre), g_value) in genres_valuates.items():
            add_genres_valuate(add_cur, f_genre, s_genre, g_value)

        for((f_c, s_c), c_v) in companies_valuate.items():
            add_companies_valuate(add_cur, f_c, s_c, c_v)

        conn.commit()

    return params


def add_user_login(cur_cursor, cur_nick, cur_password):
    cur_cursor.execute("INSERT INTO login (nick, password) VALUES (%s, %s)", (cur_nick, cur_password, ))


def add_user_session_mood(cur_cursor, cur_nick, cur_mood):
    cur_cursor.execute("UPDATE user_session SET mood = %s WHERE nick = %s", (cur_mood, cur_nick, ))


def add_user_session_company(cur_cursor, cur_nick, cur_company, cur_people):
    cur_cursor.execute("UPDATE user_session SET company = %s, people = %s WHERE nick = %s",
                       (cur_company, cur_people, cur_nick, ))


def add_user_session_age(cur_cursor, cur_nick, cur_age):
    cur_cursor.execute("UPDATE user_session SET age = %s WHERE nick = %s", (cur_age, cur_nick, ))


def add_user_session_genres(cur_cursor, cur_nick, cur_genres):
        cur_cursor.execute("UPDATE user_session SET genres = %s WHERE nick = %s", (cur_genres, cur_nick, ))


def add_film_info(cur_cursor, cur_film_name, cur_genre, cur_mood, cur_company, cur_age, cur_age_rating):
    cur_cursor.execute("INSERT INTO bd_films (name, genre, mood, company, age, age_rating)"
                       " VALUES (%s, %s, %s, %s, %s, %s)"
                       , (cur_film_name, cur_genre, cur_mood, cur_company, cur_age, cur_age_rating, ))


def add_genres_valuate(cur_cursor, first_genre, second_genre, genres_value):
    cur_cursor.execute("INSERT INTO genres_valuates (first_genre, second_genre, value)"
                       " VALUES (%s, %s, %s)", (first_genre, second_genre, genres_value, ))


def add_companies_valuate(cur_cursor, first_company, second_company, company_value):
    cur_cursor.execute("INSERT INTO companies_valuates (first_company, second_company, value)"
                       " VALUES (%s, %s, %s)", (first_company, second_company, company_value, ))


def check_nick(cur_cursor, cur_nick):
        cur_cursor.execute("SELECT * FROM login WHERE nick = %s", (cur_nick, ))
        for row in cur_cursor:          # i dont know how can i check null query, is None doesnt work
            return True
        return False


def check_all_param(cur_cursor, cur_nick):
    cur_cursor.execute("SELECT mood, company, people, age, genres FROM user_session WHERE nick = %s", (cur_nick, ))
    row = cur_cursor.fetchone()
    dct_param = {'mood': row[0], 'company': row[1], 'people': row[2], 'age': row[3]}
    if row[4] is not None:
        dct_param['genres'] = row[4].split(' ')
    return dct_param


def check_main_param_user(client_dct):
    if client_dct['age'] is None or client_dct['company'] is None or client_dct['mood'] is None:
        return False
    return True


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


def choose_film2(cur_intrests):
    if 'genres' not in cur_intrests:
        cur_intrests['genres'] = all_genres

    with psycopg2.connect(**params) as conn:
        cur = conn.cursor()
        cur.execute("WITH main_films AS ( "
                    "SELECT name, company, MAX(t1.value) as max_genre,"
                    " 1 - CAST(ABS(%s - mood) AS NUMERIC(6,1))/10 as mood_value,"
                    " 1 - (CAST(ABS(age_rating - %s) AS NUMERIC(6,2)))/100 as age_value"
                    " from (bd_films INNER JOIN genres_valuates on"
                    " bd_films.genre = genres_valuates.first_genre) t1"
                    " WHERE t1.second_genre = ANY(%s)"
                    " GROUP BY name )"
                    " SELECT name, max_genre + mood_value + age_value + MAX(t1.value)"
                    " as final_value from"
                    " (main_films join companies_valuates on main_films.company = companies_valuates.first_company) t1"
                    " WHERE t1.second_company = %s"
                    " GROUP BY name, max_genre, mood_value, age_value"
                    " ORDER BY final_value DESC LIMIT 10"
                    "", (cur_intrests['mood'], cur_intrests['age'], cur_intrests['genres'], cur_intrests['company'],))
        vec = []
        for row in cur:
            vec.append(row[0])
        return vec


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
        cur.execute("SELECT nick, password FROM login WHERE nick = %s and password = %s", (cur_nick, cur_password,))  # here
        for row in cur:
            return 'ok'
    return flask.abort(400)


@app.route('/add_session_of_user', methods=['POST'])
def add_session_of_user():
    with psycopg2.connect(**params) as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO user_session (nick) VALUES (%s)", (flask.request.json['nick'], ))
        conn.commit()
    return 'ok'


@app.route('/prev_param', methods=['POST'])
def prev_param():
    with psycopg2.connect(**params) as conn:
        cur = conn.cursor()
        cur.execute("SELECT mood, age, company, people FROM user_session WHERE nick = %s", (flask.request.json['nick'], ))      # here
        row = cur.fetchone()
        return json.dumps({'age': row[1], 'mood': row[0], 'company': row[2], 'people': row[3]})      # and here


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
        cur.execute("DELETE FROM user_session WHERE nick = %s", (flask.request.json['nick'], ))
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
            add_user_session_company(cur, flask.request.json['nick'], flask.request.json['company'],
                                     flask.request.json['people'])
            conn.commit()
        return 'ok'


@app.route('/get_film', methods=['GET'])
def get_film():
    with psycopg2.connect(**params) as conn:
        cur_cursor = conn.cursor()
        param_user = check_all_param(cur_cursor, flask.request.json['nick'])
        if check_main_param_user(param_user):
            return json.dumps(choose_film2(param_user))
        else:
            flask.abort(400)


@app.route('/get_drink', methods=['GET'])
def get_drink():
    with psycopg2.connect(**params) as conn:
        cur_cursor = conn.cursor()
        param_user = check_all_param(cur_cursor, flask.request.json['nick'])
        if check_main_param_user(param_user):
            return json.dumps(drink_smart_function(param_user))
        else:
            flask.abort(400)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers()

    create_parser = subs.add_parser('create_data')
    create_parser.set_defaults(method='create_data')

    main_parser = subs.add_parser('main')
    main_parser.set_defaults(method='main')

    main_parser.add_argument('--host', default='localhost')
    main_parser.add_argument('--port', default='50000')
    main_parser.add_argument('--dbname')
    main_parser.add_argument('--user')
    main_parser.add_argument('--password')

    args = parser.parse_args()
    if args.method == 'create_data':
        create_data_base()
    else:
        app.run(args.host, args.port, debug=True, threaded=True)
