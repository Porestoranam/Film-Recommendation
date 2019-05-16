import argparse
import requests


# parser does hot work. Use defaults
parser = argparse.ArgumentParser()
subs = parser.add_subparsers()

set_parser = subs.add_parser('set', description='Enter your port and host for connection')
set_parser.add_argument('--port', default=50000, help='Enter your port for connection')
set_parser.add_argument('--host', default='localhost', help='Enter your host')

args = set_parser.parse_args()


while True:
    print("Hello, it's a service can help you choose a film and special drink for you")
    print("If you want to exit, please type exit")
    print("Dou you want to register or you have an account? register/log in")

    reg = input()

    if reg == 'register':
        while True:
            print("Enter your login for registration:")
            user_login = input()
            if user_login == 'exit':
                break
            print("Enter your password for registration:")
            user_password = input()
            if requests.post('http://127.0.0.1:50000/register', json={'nick': user_login, 'password': user_password}).status_code == 400:
                print("This login is already exist")
            else:
                print("Registration is completed. Log in")
                reg = 'log in'
                break

    if reg == 'log in':
        while True:
            print("Enter your login for log in:")
            user_login = input()
            if user_login == 'exit':
                break
            print("Enter your password:")
            user_password = input()
            r = requests.post('http://127.0.0.1:50000/check_log', json={'login': user_login, 'password': user_password})
            if r.status_code == 400:
                print("The user does not exist or you enter wrong password")
            else:
                print("Connection successful")
                requests.post('http://127.0.0.1:50000/add_session_of_user', json={'nick': user_login})
                while True:
                    print("You can try some options:")
                    print("mood\ncompany\ngenres\nage\nget film\nget cocktail\ngenres")
                    print("To select one of this, type, for example, mood or film")
                    print("Choose option...")
                    option = input()
                    if option == 'exit':
                        requests.post('http://127.0.0.1:50000/end_session', json={'nick': user_login})
                        break
                    elif option == 'genres':
                        while True:
                            print("Please enter your favorite genres through the gap from next below:")
                            print("\"action\", \"adventure\", \"comedy\", \"thriller\", \"drama\", \"historical\"")
                            print(" \"horror\", \"musicals\", \"science fiction\", \"war\", \"western\"")
                            genres = input()
                            if genres == 'back':
                                break
                            if requests.post('http://127.0.0.1:50000/add_genres', json={'genres': genres, 'nick':user_login}).status_code == 400:
                                print("Please, enter correct")
                            else:
                                break
                            print("To go back type 'back'")
                    elif option == 'age':
                        while True:
                            print("Please enter your age:")
                            age_ = input()
                            if age_ == 'back':
                                break
                            if requests.post('http://127.0.0.1:50000/add_age', json={'age': age_, 'nick':user_login}).status_code == 400:
                                print("Please, enter correct")
                            else:
                                break
                            print("To go back type 'back'")
                    elif option == 'mood':
                        while True:
                            print("Please enter your mood from 1 to 10:")
                            mood_ = input()
                            if mood_ == 'back':
                                break
                            if requests.post('http://127.0.0.1:50000/add_mood', json={'mood': mood_, 'nick': user_login}).status_code == 400:
                                print("Please, enter correct")
                            else:
                                break
                            print("To go back type 'back'")
                    elif option == 'company':
                        while True:
                            print("Please enter your company:")
                            company_ = input()
                            if company_ == 'back':
                                break
                            elif company_ == 'friends' or company_ == 'family':
                                print("How many people are going to go with you?")
                                num_people = input()
                                if requests.post('http://127.0.0.1:50000/add_company', json={'company': company_, 'people': num_people, 'nick': user_login}).status_code == 400:
                                    print("Please, enter correct")
                                else:
                                    break
                            elif requests.post('http://127.0.0.1:50000/add_company', json={'company': company_, 'people': '1', 'nick': user_login}).status_code == 400:
                                print("Please, enter correct")
                            else:
                                break
                            print("To go back type 'back'")
                    elif option == 'film':
                        r = requests.get('http://127.0.0.1:50000/get_film', json={'nick': user_login})
                        if r.status_code == 400:
                            print("You should enter all options: mood/age/company")
                            continue
                        else:
                            print(r.json())
                    elif option == 'drink':
                        r = requests.get('http://127.0.0.1:50000/get_drink', json={'nick': user_login})
                        if r.status_code == 400:
                            print("You should enter all options: mood/age/company")
                            continue
                        else:
                            print(r.json())
                    else:
                        print("Please, enter correct key word:)")
    elif reg == 'exit':
        break
