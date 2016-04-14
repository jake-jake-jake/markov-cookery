#!/usr/bin/env python3

# std lib
from contextlib import closing
import json
from os import path, listdir, environ
import random
from string import punctuation

# Markov Chain, flickrapi
import flickrapi
from wordchainer import WordChainer

# Flask and database services
from flask import Flask, request, session, g, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy

# configuration
# DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = environ['SECRET_KEY']
USERNAME = environ['USERNAME']
PASSWORD = environ['PASSWORD']
BRITISH_LIB_UID = '12403504@N02'
SQLALCHEMY_DATABASE_URI = 'sqlite+pysqlite:///test.db'

# CREATE ZEE APPLICATION
app = Flask(__name__, static_folder='static')
app.config.from_object(__name__)
db = SQLAlchemy(app)

@app.route('/')
def make_recipe():
    title = titles.sentence()[:-1]
    recipe = ' '.join([recipes.sentence() for _ in range(3)])
    pic = image_from_title(title) or get_default_img()
    return render_template('make_recipe.html', pic=pic, title=title, recipe=recipe)

@app.route('/<int:id>')
def saved_recipe(id):
    recipe = db.session.query(Recipe).get(id)
    return render_template('make_recipe.html', pic=recipe.img_url, 
                           title=recipe.title, recipe=recipe.text)


@app.route('/save', methods=['POST'])
def save_recipe():
    recipe = Recipe(img_url=request.form['img_url'], title=request.form['title'], text=request.form['recipe'])
    db.session.add(recipe)
    db.session.commit()
    return redirect('/' + str(recipe.id))


@app.route('/images/<filename>')
def img_url(filename): pass


# Flickr functions (for getting images)
def get_secret(setting):
    ''' Return secret value from loaded JSON file.'''
    try:
        return environ[setting]
    except KeyError:
        error_message = 'Unable to load {} variable.'.format(setting)
        raise AttributeError(error_message)


def make_flickr_api(secrets_filename, format='json'):
    ''' Return instance of FlickrAPI using credentials from secrets file.'''
    flickr_api_key = environ['FLICKR_API_KEY']
    flickr_api_secret = environ['FLICKR_API_SECRET']
    return flickrapi.FlickrAPI(flickr_api_key, flickr_api_secret,
                               format=format)


def get_img_url(flickr_api, tag=''):
    ''' Return a list of URLs to query for images.'''
    flickr = flickr_api
    resp = flickr.photos.search(tags=tag, user_id=BRITISH_LIB_UID)
    resp = json.loads(str(resp, 'utf8'))
    print(resp)
    if resp['stat'] == 'ok' and resp['photos']['photo']:
        # get total number of photos and then mod that by 100
        total = int(resp['photos']['total']) % 100
        photo = resp['photos']['photo'][random.randrange(total)]
        photo_id, secret, owner = photo['id'], photo['secret'], photo['owner']
        farm, server = photo['farm'], photo['server']
        return 'https://farm{}.staticflickr.com/{}/{}_{}_c.jpg'.format(farm,
            server, photo_id, secret)
    else:
        return

def get_default_img():
    ''' If the Flickr query returns nothing good, choose a default image.'''
    file_name = random.choice(listdir(path.join('static', 'images')))
    return path.join('static', 'images', file_name)


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
        return None


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img_url = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    text = db.Column(db.String, nullable=False)



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
    app.run()
