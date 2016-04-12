#!usr/bin/env python3

# std lib
from contextlib import closing
from os import path
import json
from string import punctuation

# Markov Chain, flickrapi
import flickrapi
from wordchainer import WordChainer

# Flask and database services
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

# configuration
# DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
BRITISH_LIB_UID = '12403504@N02'


# CREATE ZEE APPLICATION
app = Flask(__name__)
app.config.from_object(__name__)

# Functions for initializing and connecting to database
# def connect_db():
#     return sqlite3.connect(app.config['DATABASE'])


# def init_db():
#     with closing(connect_db()) as db:
#         with app.open_resource('schema.sql', mode='r') as f:
#             db.cursor().executescript(f.read())
#         db.commit()


# # Request handling functions; `g` is a special Flask object.
# @app.before_request
# def before_request():
#     g.db = connect_db()


# @app.teardown_request
# def teardown_request(exception):
#     db = getattr(g, 'db', None)
#     if db is not None:
#         db.close()


@app.route('/')
def make_recipe():
    title = titles.sentence()
    recipe = ' '.join([recipes.sentence() for _ in range(3)])
    pic = image_from_title(title)
    return render_template('make_recipe.html', pic=pic, title=title, recipe=recipe)


# @app.route('/add', methods=['POST'])
# def add_entry():
#     if not session.get('logged_in'):
#         abort(401)
#     g.db.execute('insert into entries (title, text) values (?, ?)',
#                  [request.form['title'], request.form['text']])
#     g.db.commit()
#     flash('New entry was successfully posted')
#     return redirect(url_for('show_entries'))


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if request.form['username'] != app.config['USERNAME']:
#             error = 'Invalid username'
#         elif request.form['password'] != app.config['PASSWORD']:
#             error = 'Invalid password'
#         else:
#             session['logged_in'] = True
#             flash('You were logged in')
#             return redirect(url_for('show_entries'))
#     return render_template('login.html', error=error)


# @app.route('/logout')
# def logout():
#     session.pop('logged_in', None)
#     flash('You were logged out')
#     return redirect(url_for('show_entries'))


# Flickr functions (for getting images)
def get_secret(setting, json_obj):
    ''' Return secret value from loaded JSON file.'''
    try:
        return json_obj[setting]
    except KeyError:
        error_message = 'Unable to load {} variable.'.format(setting)
        raise AttributeError(error_message)


def make_flickr_api(secrets_filename, format='json'):
    ''' Return instance of FlickrAPI using credentials from secrets file.'''
    with open(secrets_filename) as f:
        secrets = json.loads(f.read())
    flickr_api_key = get_secret('flickr_api_key', secrets)
    flickr_api_secret = get_secret('flicker_api_secret', secrets)
    return flickrapi.FlickrAPI(flickr_api_key, flickr_api_secret,
                               format=format)


def get_img_url(flickr_api, tag=''):
    ''' Return a list of URLs to query for images.'''
    flickr = flickr_api
    resp = flickr.photos.search(tags=tag, user_id=BRITISH_LIB_UID)
    resp = json.loads(str(resp, 'utf8'))
    print(resp)
    if resp['stat'] == 'ok' and resp['photos']['photo']:
        photo = resp['photos']['photo'][0]
        photo_id, secret, owner = photo['id'], photo['secret'], photo['owner']
        farm, server = photo['farm'], photo['server']
        return 'https://farm{}.staticflickr.com/{}/{}_{}_c.jpg'.format(farm,
            server, photo_id, secret)
    else:
        return False


def image_from_title(title):
    ''' Given string, try each word and return images.'''
    title_words = [word.strip(punctuation) for word in title.split()]
    while title_words:
        t = title_words.pop()
        if len(t) < 4:
            continue
        url = get_img_url(flickr, tag=t)
        if url:
            return url
    else:
        return 'DEFAULT IMAGE'




# title and recipe Markov chains
titles = WordChainer()
recipes = WordChainer()
p = path.join('texts', '1600s')
recipes.add_words(path.join(p, 'accomplisht_cook_STRIPPED.txt'))
recipes.add_words(path.join(p, 'closet_of_sir_digby_STRIPPED.txt'))
recipes.add_words(path.join(p, 'eales_receipts_STRIPPED.txt'))
recipes.add_words(path.join(p, 'queen_like_closet_STRIPPED.txt'))
titles.add_words(path.join(p, '1600s_titles.txt'))
flickr = make_flickr_api('secrets.json')


if __name__ == '__main__':
    print('length of title dict:', len(titles.links))
    print('length of recipe dict:', len(recipes.links))
    app.run()
