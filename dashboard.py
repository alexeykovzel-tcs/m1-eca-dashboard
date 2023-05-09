import textwrap
from datetime import datetime

from eca import *
import json

import random
import dataconverter


# You might have to update the root path to point to the correct path
# (by default, it points to <rules>_static)
from eca.generators import start_offline_tweets

# root path for static content
root_content_path = 'dashboard_static'

# global variables
emerg_calls_per_city = {}
emerg_codes = {}


# binds the 'setup' function as the action for the 'init' event
# the action will be called with the context and the event
@event('init')
def setup(ctx, e):
    ctx.count = 0
    # start the offline tweet stream
    start_offline_tweets('p2000-tweets.txt', event_name='tweet',
                         aux_name='tweeter', time_factor=1000, arff_file=None)

    with open('cities-population.json', 'r') as f:
        cities_by_population = f.read()

    # we take top 16 cities by population to display on the barchart
    top_cities_by_population = json.loads(cities_by_population)[:16]
    for city in top_cities_by_population:
        city_name = city['name']
        emerg_calls_per_city[city_name] = 0

    # the rest of cities are sorted in 'other' category
    emerg_calls_per_city['other'] = 0


# event for adding new tweets into the tweet list
# and calling barchart & piechart events for updating
@event('tweet')
def generate_tweets(ctx, e):
    emit('tweet', e.data)

     # retrieves data from a tweet
    tweet = json.loads(json.dumps(e.data))
    city = tweet['place']['name']
    text = tweet['text']
    emerg_code = dataconverter.get_emergency_code(text)

    # updating barchart & piechart
    fire('barchart', {'city': city})
    fire('piechart', {'code': emerg_code})


# define a normal Python function
def clip(lower, value, upper):
    return max(lower, min(value, upper))


# event for updating barchart values
@event('barchart')
def update_barchart(ctx, e):
    # logging
    ctx.count += 1
    if ctx.count % 50 == 0:
        emit('debug', {'text': 'Log message #'+str(ctx.count)+'!'})

    # adds a new city occurrence into the global variable
    city = e.data['city']
    if(city in emerg_calls_per_city):
        emerg_calls_per_city[city] += 1
    else:
        emerg_calls_per_city['other'] += 1

    # sets all city values into the barchart
    emit('barlistener', {
        'action': 'setFull',
        'serie': 'serie1',  # series supposed to be pre-defined at dashboard_static/index.html
        'dataFull': emerg_calls_per_city
    })


# event for updating piechart values
@event('piechart')
def update_piechart(ctx, e):
    # logging
    ctx.count += 1
    if ctx.count % 50 == 0:
        emit('debug', {'text': 'Log message #' + str(ctx.count) + '!'})

    # retrieves an emergency code data from a tweet
    tweet = e.data
    code = tweet['code']

    # adds a new emergency code and takes the top values again
    emerg_codes[code] = emerg_codes[code] + \
        1 if code in emerg_codes else 1
    top_codes = dataconverter.get_dict_top(6, emerg_codes)

    # formattes codes for the website view
    output_codes = {}
    for c in top_codes:
        formatted_code = c[0].upper() + c[1:] if c == 'other' else c.upper()
        output_codes[formatted_code] = top_codes[c]

    # emits changes for the piechart
    emit('pielistener', {'action': 'reset'})
    emit('pielistener', {
        'action': 'setFull',
        'dataFull': output_codes
    })
