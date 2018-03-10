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
    # Name of the recipe
    title = CharField(null=True)
    # URL, should be unique
    url = CharField(null=True, unique=True)
    # Author
    author = CharField(null=True)
    # Picture as a binary blob
    picture = BlobField(null=True)
    # Short description
    short_description = TextField(null=True)
    # Number of persons as text, as it can be either "N persons" or "N parts"
    nb_person = TextField(null=True)
    # Preparation and cooking times
    preparation_time = IntegerField(null=True)  # In minutes
    cooking_time = IntegerField(null=True)  # In minutes
    # List of ingredients
    ingredients = JSONField(null=True)
    # Instructions
    instructions = TextField(null=True)

    class Meta:
        database = database

    def update_from_dict(self, d):
        """
        Update field taking values from a dict of values.
        """
        # Set fields
        for field in ['title', 'url', 'author', 'picture_url',
                      'short_description', 'preparation_time', 'cooking_time',
                      'ingredients', 'instructions', 'nb_person']:
            value = d.get(field, None)
            if value:
                setattr(self, field, value)
        # Download picture and save it as a blob
        if d.get('picture_url', None):
            self.picture = requests.get(d['picture_url']).content

    def update_from_weboob(self, weboob_obj):
        """
        Update fields taking values from the Weboob object.
        """
        weboob_dict = dict(weboob_obj.iter_fields())
        if weboob_dict.get('nb_person', None):
            weboob_dict['nb_person'] = '-'.join(
                str(num) for num in weboob_dict['nb_person']
            )
        self.update_from_dict(weboob_dict)

    def to_dict(self):
        """
        Dict conversion function, for serialization in the API.
        """
        serialized = model_to_dict(self)
        # Dump picture as a base64 string, compatible with HTML `src` attribute
        # for images.
        if serialized['picture']:
            picture_mime = (
            'data:%s;base64' % magic.from_buffer(serialized['picture'],
                                                 mime=True)
            )
            serialized['picture'] = '%s,%s' % (
                picture_mime,
                base64.b64encode(serialized['picture']).decode('utf-8')
            )
        return serialized
