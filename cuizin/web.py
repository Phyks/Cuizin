import json
import os

import bottle
import peewee

from cuizin import db
from cuizin.scraping import fetch_recipe

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))


app = bottle.Bottle()

@app.hook('before_request')
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
            recipe.to_dict()
            for recipe in db.Recipe.select().order_by(db.Recipe.id.desc())
        ]
    }


@app.post('/api/v1/recipes/by_url')
def api_v1_recipes_post_by_url():
    """
    Create a new recipe from URL
    """
    data = json.loads(bottle.request.body.read().decode('utf-8'))
    if 'url' not in data:
        return {
            'error': 'No URL provided'
        }

    try:
        # Try to add
        return {
            'recipes': [fetch_recipe(data['url']).to_dict()]
        }
    except peewee.IntegrityError:
        # Redirect to pre-existing recipe if already there
        recipe = db.Recipe.select().where(
            db.Recipe.url == data['url']
        ).first()
        bottle.redirect('/api/v1/recipe/%s' % recipe.id, 301)


@app.post('/api/v1/recipes/manually')
def api_v1_recipes_post_manual():
    """
    Create a new recipe manually
    """
    data = json.loads(bottle.request.body.read().decode('utf-8'))

    try:
        # Try to add
        recipe = db.Recipe()
        recipe.update_from_dict(data)
        recipe.save()
        return {
            'recipes': [recipe.to_dict()]
        }
    except peewee.IntegrityError:
        return {
            'error': 'Duplicate recipe.'
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


@app.route('/api/v1/recipe/:id/refetch', ['GET', 'OPTIONS'])
def api_v1_recipe_refetch(id):
    """
    Refetch a given recipe.
    """
    # CORS
    if bottle.request.method == 'OPTIONS':
        return ''

    recipe = db.Recipe.select().where(
        db.Recipe.id == id
    ).first()
    if not recipe:
        return bottle.abort(400, 'No recipe with id %s.' % id)

    recipe = fetch_recipe(recipe.url, recipe=recipe)

    return {
        'recipes': [
            recipe.to_dict()
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
