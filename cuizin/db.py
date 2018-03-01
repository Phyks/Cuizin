"""
Database definition
"""
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
    """
    A Peewee database field with transparent JSON dump/load.
    """
    def db_value(self, value):
        return json.dumps(value)

    def python_value(self, value):
        if value is not None:
            return json.loads(value)


class Recipe(Model):
    """
    Our base model for a recipe.
    """
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
        # Set fields
        for field in ['title', 'url', 'author', 'picture_url',
                      'short_description', 'preparation_time', 'cooking_time',
                      'ingredients', 'instructions']:
            value = getattr(obj, field)
            if value:
                setattr(recipe, field, value)
        # Serialize number of person
        recipe.nb_person = '-'.join(str(num) for num in obj.nb_person)
        # Download picture and save it as a blob
        recipe.picture = requests.get(obj.picture_url).content
        return recipe

    def to_dict(self):
        """
        Dict conversion function, for serialization in the API.
        """
        serialized = model_to_dict(self)
        # Dump picture as a base64 string, compatible with HTML `src` attribute
        # for images.
        picture_mime = (
          'data:%s;base64' % magic.from_buffer(serialized['picture'],
                                               mime=True)
        )
        serialized['picture'] = '%s,%s' % (
            picture_mime,
            base64.b64encode(serialized['picture']).decode('utf-8')
        )
        return serialized
