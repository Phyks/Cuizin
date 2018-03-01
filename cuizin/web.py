import json
import os

import bottle

from cuizin import db
from cuizin.scraping import add_recipe

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))


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
    """
    API index route
    """
    return {
        'recipes': '/api/v1/recipes',
        'recipe': '/api/v1/recipe/:id'
    }


@app.route('/api/v1/recipes', ['GET', 'OPTIONS'])
def api_v1_recipes():
    """
    List all recipes
    """
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
    """
    Create a new recipe from URL
    """
    data = json.load(bottle.request.body)
    if 'url' not in data:
        return {
            'error': 'No URL provided'
        }

    recipes = []
    try:
        recipe = db.Recipe.select().where(
            db.Recipe.url == data['url']
        ).first()
        assert recipe
        recipes = [recipe.to_dict()]
    except AssertionError:
        recipes = [add_recipe(data['url']).to_dict()]

    return {
        'recipes': recipes
    }


@app.route('/api/v1/recipe/:id', ['GET', 'OPTIONS'])
def api_v1_recipe(id):
    """
    Get a given recipe from db
    """
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


@app.delete('/api/v1/recipe/:id', ['DELETE', 'OPTIONS'])
def api_v1_recipe_delete(id):
    """
    Delete a given recipe from db
    """
    # CORS
    if bottle.request.method == 'OPTIONS':
        return ''

    db.Recipe.delete().where(
        db.Recipe.id == id
    ).execute()

    return {
        'status': 'OK'
    }


@app.get('/')
def index():
    """
    Return built index.html file
    """
    return bottle.static_file('index.html',
                              root=os.path.join(MODULE_DIR, 'dist'))


@app.get('/static/<filename:path>')
def get_static_files(filename):
    """
    Get Static files
    """
    return bottle.static_file(filename,
                              root=os.path.join(MODULE_DIR, 'dist', 'static'))
