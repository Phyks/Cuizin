import base64
import mimetypes

import requests
from peewee import (
    Model, SqliteDatabase,
    BlobField, CharField, IntegerField, TextField
)
from playhouse.shortcuts import model_to_dict


database = SqliteDatabase('recipes.db', threadlocals=True)
database.connect()


class Recipe(Model):
    title = CharField()
    url = CharField(null=True, unique=True)
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
        for field in ['title', 'url', 'author', 'picture_url', 'short_description',
                      'preparation_time', 'cooking_time', 'instructions']:
            value = getattr(obj, field)
            if value:
                setattr(recipe, field, value)
        recipe.picture = requests.get(obj.picture_url).content
        return recipe

    def to_dict(self):
        serialized = model_to_dict(self)
        prepend_info = (
          'data:%s;base64' % mimetypes.guess_type(serialized['picture'])[0]
        )
        serialized['picture'] = '%s,%s' % (
            prepend_info,
            base64.b64encode(serialized['picture']).decode('utf-8')
        )
        return serialized
