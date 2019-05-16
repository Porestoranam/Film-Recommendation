import random
import math
import collections
from tools import fruits


def value_drink_mood(_mood):
    return math.sqrt(11 - _mood)


def value_drink_age(age):
    return 1 + math.log2(math.fabs(age - 16.5))


def drink_smart_function(cur_intrests):
    c = round(value_drink_age(cur_intrests['age']) * cur_intrests['people']
              + value_drink_mood(cur_intrests['mood']))
    my_counter = collections.Counter()
    list_of_fruits = []
    for i in range(0, c):
        my_counter[fruits[random.randint(0, 8)]] += 1
    for cur_fruit in my_counter.keys():
        list_of_fruits.append('{} {}, '.format(my_counter[cur_fruit], cur_fruit))
    return 'Our waiters will make a special cocktail for you, which consist of' + ' '.join(list_of_fruits)

