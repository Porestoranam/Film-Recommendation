import random
import math
from tools import companies, genres_valuates

companies_valuate = {}

for i in range(0, 4):
    for j in range(0, 4):
        if i == j:
            companies_valuate[(companies[i], companies[j])] = 1
        else:
            companies_valuate[(companies[i], companies[j])] = random.random()     # it will be fill independently later


def value_of_company(company, film_company):            # max 1
    return companies_valuate[(company, film_company)]


def value_of_mood(mood, film_mood):                     # max 1
    return 1 - math.fabs(int(mood) - film_mood)/10


def value_of_age(age, film_age, film_age_rating):       # max 1
    if int(age) < film_age:
        return -3
    else:
        return 1 - math.fabs(film_age_rating - int(age))/100


def value_of_genres(genres, film_genre):
    max_value = 0
    for cur_genre in genres:
        if genres_valuates[(cur_genre, film_genre)] > max_value:
            max_value = genres_valuates[(cur_genre, film_genre)]
    return max_value


class cfilm:
    def __init__(self, d):
        self.name = d['name']
        self.mood = d['mood']
        self.age = d['age']
        self.age_rating = d['age_rating']
        self.company = d['company']
        self.genre = d['genre']


def smart_function(cfilm, person_intrests):
    return value_of_company(person_intrests['company'], cfilm.company)\
           + value_of_age(person_intrests['age'], cfilm.age, cfilm.age_rating)\
           + value_of_mood(person_intrests['mood'], cfilm.mood)\
           + value_of_genres(person_intrests['genres'], cfilm.genre)


