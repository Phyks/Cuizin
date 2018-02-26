import bottle

from cuizin import db


bottle.Bottle()


@app.get('/api/v1')
def api_v1_index():
    return {
        'recipes': '/api/v1/recipes'
    }


@app.get('/api/v1/recipes')
def api_v1_recipes():
    return {
        'recipes': [
            recipe.to_dict() for recipe in db.Recipe.select()
        ]
    }


@app.get('/api/v1/recipe/:id')
def api_v1_recipe(id):
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
    return bottle.static_file(filename, root=)
