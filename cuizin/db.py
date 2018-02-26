import base64

import requests
from peewee import (
    Model, SqliteDatabase,
    BlobField, CharField, IntegerField, TextField
)
from playhouse.shortcuts import model_to_dict


database = SqliteDatabase('recipes.db')


class Recipe(Model):
    title = CharField()
    author = CharField(null=True)
    picture = BlobField(null=True)
    short_description = TextField(null=True)
    nb_person = None  # TODO
    preparation_time = IntegerField(null=True)  # In minutes
    cooking_time = IntegerField(null=True)  # In minutes
    ingredients = None  # TODO
    instructions = TextField()
    comments = None  # TODO

    class Meta:
        database = database

    @staticmethod
    def from_weboob(obj):
        recipe = Recipe()
        for field in ['title', 'author', 'picture_url', 'short_description',
                      'preparation_time', 'cooking_time', 'instructions']:
            value = getattr(obj, field)
            if value:
                setattr(recipe, field, value)
        recipe.picture = requests.get(obj.picture_url).content
        return recipe

    def to_dict(self):
        serialized = model_to_dict(self)
        serialized['picture'] = base64.b64encode(
            serialized['picture']
        ).decode('utf-8')
        return serialized
