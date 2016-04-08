#!usr/bin/env python3

# std lib
from contextlib import closing
from os import path

# Markov Chain
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


# CREATE ZEE APPLICATION
app = Flask(__name__)
app.config.from_object(__name__)

# title and recipe Markov chains
titles = WordChainer()
recipes = WordChainer()
p = path.join('texts', '1600s')
recipes.add_words(path.join(p, 'accomplisht_cook_STRIPPED.txt'))
recipes.add_words(path.join(p, 'closet_of_sir_digby_STRIPPED.txt'))
recipes.add_words(path.join(p, 'eales_receipts_STRIPPED.txt'))
titles.add_words(path.join(p, '1600s_titles.txt'))


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
    pic = 'https://c3.staticflickr.com/3/2845/11128080714_1f998fd022_n.jpg'
    title = titles.sentence()
    recipe = ' '.join([recipes.sentence() for _ in range(3)])
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


if __name__ == '__main__':
    app.run()
