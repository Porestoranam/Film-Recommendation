import argparse
import requests
from constants import *

# parser does hot work. Use defaults
parser = argparse.ArgumentParser()
subs = parser.add_subparsers()

set_parser = subs.add_parser('set', description='Enter your port and host for connection')
set_parser.add_argument('--port', default=50000, help='Enter your port for connection')
set_parser.add_argument('--host', default='localhost', help='Enter your host')

args = set_parser.parse_args()
# address = 'http://localhost:50000/'
address = 'http://{}:{}/'.format(args.host, args.port)


def register_func():
    while True:
        # print("To go back type 'back'")
        print("Enter your login for registration:")

        user_login = input()
        if user_login == 'exit':
            raise SystemExit

        print("Enter your password for registration:")
        user_password = input()

        if requests.post(address + 'register',
                         json={'nick': user_login, 'password': user_password}).status_code == 400:
            print("This login is already exist")
        else:
            print("Registration is completed.")
            return log_in_func()


def log_in_func():
    while True:
        print("To go back type 'back'")
        print("Enter your login for log in:")
        user_login = input()
        if user_login == 'exit':
            raise SystemExit

        if user_login == 'back':
            return register_func()

        print("Enter your password:")
        user_password = input()

        r = requests.post(address + 'check_log', json={'login': user_login, 'password': user_password})
        if r.status_code == 400:
            print("The user does not exist or you enter wrong password")
        else:
            print("Connection successful")
            requests.post(address + 'add_session_of_user', json={'nick': user_login})
            return client_choose_fun(user_login)


def client_choose_fun(user_login):
    while True:
        print("You can try some options:")
        print("mood/company/genres/age/get film/get cocktail/genres")
        print("To select one of this, type, for example, mood or film")
        print("Choose option...")
        option = input()
        option = option.strip(' ')
        if option == 'exit':
            requests.post(address + 'end_session', json={'nick': user_login})
            raise SystemExit
        elif option == 'genres':
            genres_func(user_login)

        elif option == 'age':
            age_func(user_login)

        elif option == 'mood':
            mood_func(user_login)

        elif option == 'company':
            company_func(user_login)

        elif option == 'get film':
            return film_func(user_login)

        elif option == 'get cocktail':
            return drink_func(user_login)

        elif option == 'back':
            requests.post(address + 'end_session', json={'nick': user_login})
            return log_in_func()
        else:
            print("Please, enter correct")


def drink_func(user_login):
    r = requests.get(address + 'get_drink', json={'nick': user_login})
    if r.status_code == 400:
        print("You should enter all options: mood/age/company")
        return client_choose_fun(user_login)
    else:
        print("#" * num_of_brackets)
        print(r.json())
        print("#" * num_of_brackets)
        return client_choose_fun(user_login)


def film_func(user_login):
    r = requests.get(address + 'get_film', json={'nick': user_login})
    if r.status_code == 400:
        print("You should enter all options: mood/age/company")
        return client_choose_fun(user_login)
    else:
        vec_films = r.json()
        for i in vec_films:
            print("To go back type back")
            print("Type get film!")
            client_request = input()
            client_request = client_request.strip(' ')
            if client_request == "get film":
                print("#" * num_of_brackets)
                print(i)
                print("#" * num_of_brackets)
            elif client_request == "back":
                return client_choose_fun(user_login)
            else:
                print("Enter correct!")
        print("Enough!")
        return client_choose_fun(user_login)


def company_func(user_login):
    while True:
        print("To go back type 'back'")
        print("Please enter your company: alone/friends/family/girlfriend")
        client_company = input()
        client_company = client_company.strip(' ')
        if client_company == 'back':
            return client_choose_fun(user_login)

        elif client_company == 'friends' or client_company == 'family':
            print("How many people are going to go with you?")
            num_people = input()
            num_people = num_people.strip(' ')
            if requests.post(address + 'add_company',
                             json={'company': client_company, 'people': num_people, 'nick': user_login}).status_code == 400:
                print("Please, enter correct")
            else:
                return client_choose_fun(user_login)
        elif requests.post(address + 'add_company',
                           json={'company': client_company, 'people': '1', 'nick': user_login}).status_code == 400:
            print("Please, enter correct")
        else:
            return client_choose_fun(user_login)


def mood_func(user_login):
    while True:
        print("To go back type 'back'")
        print("Please enter your mood from 1 to 10:")
        client_mood = input()
        client_mood = client_mood.strip(' ')
        if client_mood == 'back':
            return client_choose_fun(user_login)
        if requests.post(address + 'add_mood',
                         json={'mood': client_mood, 'nick': user_login}).status_code == 400:
            print("Please, enter correct")
        else:
            return client_choose_fun(user_login)


def age_func(user_login):
    while True:
        print("To go back type 'back'")
        # print(requests.post(address + 'prev_param', json={'nick': user_login}).request)
        print("Please enter your age from 10 to 100:")
        client_age = input()
        client_age = client_age.strip(' ')
        if client_age == '':
            return client_choose_fun(user_login)
        if client_age == 'back':
            return client_choose_fun(user_login)

        elif requests.post(address + 'add_age',
                           json={'age': client_age, 'nick': user_login}).status_code == 400:
            print("Please, enter correct")

        else:
            return client_choose_fun(user_login)


def genres_func(user_login):
    while True:
        print("Please enter your favorite genres through the gap from next below:")
        print("\"action\", \"adventure\", \"comedy\", \"thriller\", \"drama\", \"historical\"")
        print(" \"horror\", \"musicals\", \"science_fiction\", \"war\", \"western\"")
        print("Type all if it doesn't matter")
        print("To go back type 'back'")
        client_genres = input()
        client_genres = client_genres.strip(' ')
        if client_genres == 'all':
            return client_choose_fun(user_login)
        elif client_genres == 'back':
            return client_choose_fun(user_login)
        elif client_genres == 'exit':
            raise SystemExit

        elif requests.post(address + 'add_genres',
                           json={'genres': client_genres, 'nick': user_login}).status_code == 400:
            print("Please, enter correct")
        else:
            return client_choose_fun(user_login)


while True:
    print("Hello, it's a service that can help you choose a film and special drink for you")
    print("If you want to exit, please type exit")
    print("Dou you want to register or you have an account? register/log in")

    reg = input()
    reg = reg.strip(' ')

    if reg == 'register':
        register_func()

    elif reg == 'log in':
        log_in_func()

    elif reg == 'exit':
        raise SystemExit

    else:
        print("Please, enter correct!")
