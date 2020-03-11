import random
import io
from tools import all_genres


def just():
    companies = ['friends', 'alone', 'girlfriend', 'family']
    ages = ['16', '18']
    age_rating = ['16', '30', '40', '20', '25']

    films_and_other = []
    with io.open('title_films.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.replace('\'', ' ')
            films_and_other.append({'film': line[:-1]})

    with io.open('mood_films.txt', 'r', encoding='utf-8') as f:
        i = 0
        for line in f.readlines():
            if len(line) > 2:
                films_and_other[i]['mood'] = line[1]
            elif len(line) > 1:
                films_and_other[i]['mood'] = line[0]
            else:
                films_and_other[i]['mood'] = '1'
            i += 1

    for j in range(0, len(films_and_other)):
        films_and_other[j]['company'] = companies[random.randint(0, 3)]
        films_and_other[j]['age'] = ages[random.randint(0, 1)]
        films_and_other[j]['age_rating'] = age_rating[random.randint(0, 4)]

    with open('genres_film.txt', 'r') as f:
        j = 0
        for line in f.readlines():
            for gen in all_genres:
                if gen in line.lower():
                    films_and_other[j]['genre'] = gen
                    break
            if 'genre' not in films_and_other[j]:
                films_and_other[j]['genre'] = all_genres[random.randint(0, 10)]
            j += 1
    return films_and_other



