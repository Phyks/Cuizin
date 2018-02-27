import json

import bottle
import peewee

from cuizin import add_recipe
from cuizin import db


app = bottle.Bottle()

@app.hook('after_request')
def enable_cors():
    """
    Add CORS headers at each request.
    """
    # The str() call is required as we import unicode_literal and WSGI
    # headers list should have plain str type.
    bottle.response.headers[str('Access-Control-Allow-Origin')] = str('*')
    bottle.response.headers[str('Access-Control-Allow-Methods')] = str(
        'PUT, GET, POST, DELETE, OPTIONS, PATCH'
    )
    bottle.response.headers[str('Access-Control-Allow-Headers')] = str(
        'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    )


@app.route('/api/v1', ['GET', 'OPTIONS'])
def api_v1_index():
    return {
        'recipes': '/api/v1/recipes'
    }


@app.route('/api/v1/recipes', ['GET', 'OPTIONS'])
def api_v1_recipes():
    # CORS
    if bottle.request.method == 'OPTIONS':
        return ''

    return {
        'recipes': [
            recipe.to_dict() for recipe in db.Recipe.select()
        ]
    }


@app.post('/api/v1/recipes')
def api_v1_recipes_post():
    data = json.load(bottle.request.body)
    if 'url' not in data:
        return {
            'error': 'No URL provided'
        }

    recipes = []
    try:
        recipes = [add_recipe(data['url']).to_dict()]
    except peewee.IntegrityError:
        recipes = [db.Recipe.select().where(
            db.Recipe.url == data['url']
        ).first().to_dict()]

    return {
        'recipes': recipes
    }


@app.route('/api/v1/recipe/:id', ['GET', 'OPTIONS'])
def api_v1_recipe(id):
    # CORS
    if bottle.request.method == 'OPTIONS':
        return ''

    return {
        'recipes': [
            recipe.to_dict() for recipe in db.Recipe.select().where(
                db.Recipe.id == id
            )
        ]
    }


@app.get('/static/<filename:path>')
def get_static_files(filename):
    """Get Static files"""
    return bottle.static_file(filename)  # TODO: root=
