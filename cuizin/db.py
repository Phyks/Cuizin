import base64
import json

import magic
import requests
from peewee import (
    Model, SqliteDatabase,
    BlobField, CharField, IntegerField, TextField
)
from playhouse.shortcuts import model_to_dict


database = SqliteDatabase('recipes.db')
database.connect()


class JSONField(TextField):
    def db_value(self, value):
        return json.dumps(value)

    def python_value(self, value):
        if value is not None:
            return json.loads(value)


class Recipe(Model):
    title = CharField()
    url = CharField(null=True, unique=True)
    author = CharField(null=True)
    picture = BlobField(null=True)
    short_description = TextField(null=True)
    nb_person = TextField(null=True)
    preparation_time = IntegerField(null=True)  # In minutes
    cooking_time = IntegerField(null=True)  # In minutes
    ingredients = JSONField(null=True)
    instructions = TextField()

    class Meta:
        database = database

    @staticmethod
    def from_weboob(obj):
        recipe = Recipe()
        for field in ['title', 'url', 'author', 'picture_url',
                      'short_description', 'preparation_time', 'cooking_time',
                      'ingredients', 'instructions']:
            value = getattr(obj, field)
            if value:
                setattr(recipe, field, value)

        recipe.nb_person = '-'.join(str(num) for num in obj.nb_person)
        recipe.picture = requests.get(obj.picture_url).content
        return recipe

    def to_dict(self):
        serialized = model_to_dict(self)
        prepend_info = (
          'data:%s;base64' % magic.from_buffer(serialized['picture'],
                                               mime=True)
        )
        serialized['picture'] = '%s,%s' % (
            prepend_info,
            base64.b64encode(serialized['picture']).decode('utf-8')
        )
        return serialized
