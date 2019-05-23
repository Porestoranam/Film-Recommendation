from constants import *


def correct_people(num_people):
    return num_people.isdigit()


def correct_company(_company):
    if _company not in companies:
        return False
    else:
        return True


def correct_age(_age):
    if not _age.isdigit():
        return False
    elif not min_age <= int(_age) <= max_age:
        return False
    else:
        return True


def correct_mood(_mood):
    if not _mood.isdigit():
        return False
    elif not 1 <= int(_mood) <= 10:
        return False
    else:
        return True


def correct_genre(_genres):
    for cur_genre in _genres.split(' '):
        if cur_genre not in all_genres:
            return False
    return True


fruits = ['apple', 'piece of pineapple', 'slice of orange', 'slice of lemon', 'cubes of ice', 'half of banana',
          'small kiwi', 'little piece of lime', 'grape branch']

companies = ['alone', 'family', 'friends', 'girlfriend']

genres_valuates = {}

all_genres = ["action", "adventure", "comedy", "thriller", "drama", "historical", "horror",
              "musicals", "science_fiction", "war", "western"]

genres_valuates[('action', 'action')] = 1
genres_valuates[('action', 'comedy')] = 0.6
genres_valuates[('action', 'adventure')] = 0.2
genres_valuates[('action', 'thriller')] = 0.4
genres_valuates[('action', 'drama')] = 0.2
genres_valuates[('action', 'historical')] = 0.4
genres_valuates[('action', 'horror')] = 0.2
genres_valuates[('action', 'musicals')] = 0.1
genres_valuates[('action', 'science_fiction')] = 0.2
genres_valuates[('action', 'war')] = 0.8
genres_valuates[('action', 'western')] = 0.6

genres_valuates[('adventure', 'action')] = 0.3
genres_valuates[('adventure', 'adventure')] = 1
genres_valuates[('adventure', 'thriller')] = 0.1
genres_valuates[('adventure', 'drama')] = 0.3
genres_valuates[('adventure', 'historical')] = 0.5
genres_valuates[('adventure', 'horror')] = 0.1
genres_valuates[('adventure', 'musicals')] = 0.1
genres_valuates[('adventure', 'science_fiction')] = 0.3
genres_valuates[('adventure', 'war')] = 0.2
genres_valuates[('adventure', 'western')] = 0.6
genres_valuates[('adventure', 'comedy')] = 0.6

genres_valuates[('comedy', 'action')] = 0.6
genres_valuates[('comedy', 'adventure')] = 0.6
genres_valuates[('comedy', 'thriller')] = 0.2
genres_valuates[('comedy', 'drama')] = 0.1
genres_valuates[('comedy', 'historical')] = 0.1
genres_valuates[('comedy', 'horror')] = 0.1
genres_valuates[('comedy', 'musicals')] = 0.1
genres_valuates[('comedy', 'science_fiction')] = 0.3
genres_valuates[('comedy', 'war')] = 0.1
genres_valuates[('comedy', 'western')] = 0.2
genres_valuates[('comedy', 'comedy')] = 1

genres_valuates[('thriller', 'action')] = 0.4
genres_valuates[('thriller', 'adventure')] = 0.1
genres_valuates[('thriller', 'comedy')] = 0.2
genres_valuates[('thriller', 'thriller')] = 1
genres_valuates[('thriller', 'drama')] = 0.5
genres_valuates[('thriller', 'historical')] = 0.1
genres_valuates[('thriller', 'horror')] = 0.6
genres_valuates[('thriller', 'musicals')] = 0.1
genres_valuates[('thriller', 'science_fiction')] = 0.1
genres_valuates[('thriller', 'war')] = 0.3
genres_valuates[('thriller', 'western')] = 0.5

genres_valuates[('drama', 'action')] = 0.2
genres_valuates[('drama', 'adventure')] = 0.3
genres_valuates[('drama', 'comedy')] = 0.1
genres_valuates[('drama', 'thriller')] = 0.5
genres_valuates[('drama', 'drama')] = 1
genres_valuates[('drama', 'historical')] = 0.3
genres_valuates[('drama', 'horror')] = 0.1
genres_valuates[('drama', 'musicals')] = 0.4
genres_valuates[('drama', 'science_fiction')] = 0.2
genres_valuates[('drama', 'war')] = 0.8
genres_valuates[('drama', 'western')] = 0.2

genres_valuates[('historical', 'action')] = 0.4
genres_valuates[('historical', 'adventure')] = 0.5
genres_valuates[('historical', 'comedy')] = 0.1
genres_valuates[('historical', 'thriller')] = 0.1
genres_valuates[('historical', 'drama')] = 0.3
genres_valuates[('historical', 'historical')] = 1
genres_valuates[('historical', 'horror')] = 0.1
genres_valuates[('historical', 'musicals')] = 0.2
genres_valuates[('historical', 'science_fiction')] = 0.3
genres_valuates[('historical', 'war')] = 0.9
genres_valuates[('historical', 'western')] = 0.7

genres_valuates[('horror', 'action')] = 0.2
genres_valuates[('horror', 'adventure')] = 0.1
genres_valuates[('horror', 'comedy')] = 0.1
genres_valuates[('horror', 'thriller')] = 0.6
genres_valuates[('horror', 'drama')] = 0.1
genres_valuates[('horror', 'historical')] = 0.1
genres_valuates[('horror', 'horror')] = 1
genres_valuates[('horror', 'musicals')] = 0
genres_valuates[('horror', 'science_fiction')] = 0.3
genres_valuates[('horror', 'war')] = 0.3
genres_valuates[('horror', 'western')] = 0

genres_valuates[('musicals', 'action')] = 0.1
genres_valuates[('musicals', 'adventure')] = 0.1
genres_valuates[('musicals', 'comedy')] = 0.1
genres_valuates[('musicals', 'thriller')] = 0.1
genres_valuates[('musicals', 'drama')] = 0.4
genres_valuates[('musicals', 'historical')] = 0.2
genres_valuates[('musicals', 'horror')] = 0
genres_valuates[('musicals', 'musicals')] = 1
genres_valuates[('musicals', 'science_fiction')] = 0.1
genres_valuates[('musicals', 'war')] = 0.1
genres_valuates[('musicals', 'western')] = 0

genres_valuates[('science_fiction', 'action')] = 0.2
genres_valuates[('science_fiction', 'adventure')] = 0.3
genres_valuates[('science_fiction', 'comedy')] = 0.3
genres_valuates[('science_fiction', 'thriller')] = 0.1
genres_valuates[('science_fiction', 'drama')] = 0.2
genres_valuates[('science_fiction', 'historical')] = 0.3
genres_valuates[('science_fiction', 'horror')] = 0.3
genres_valuates[('science_fiction', 'musicals')] = 0.1
genres_valuates[('science_fiction', 'science_fiction')] = 1
genres_valuates[('science_fiction', 'war')] = 0.1
genres_valuates[('science_fiction', 'western')] = 0.1

genres_valuates[('war', 'action')] = 0.8
genres_valuates[('war', 'adventure')] = 0.2
genres_valuates[('war', 'comedy')] = 0.1
genres_valuates[('war', 'thriller')] = 0.3
genres_valuates[('war', 'drama')] = 0.8
genres_valuates[('war', 'historical')] = 0.9
genres_valuates[('war', 'horror')] = 0.3
genres_valuates[('war', 'musicals')] = 0.1
genres_valuates[('war', 'science_fiction')] = 0.1
genres_valuates[('war', 'war')] = 1
genres_valuates[('war', 'western')] = 0.6

genres_valuates[('western', 'action')] = 0.6
genres_valuates[('western', 'adventure')] = 0.6
genres_valuates[('western', 'comedy')] = 0.2
genres_valuates[('western', 'thriller')] = 0.5
genres_valuates[('western', 'drama')] = 0.2
genres_valuates[('western', 'historical')] = 0.7
genres_valuates[('western', 'horror')] = 0
genres_valuates[('western', 'musicals')] = 0
genres_valuates[('western', 'science_fiction')] = 0.1
genres_valuates[('western', 'war')] = 0.6
genres_valuates[('western', 'western')] = 1
