import base64
import os

import magic

from peewee import TextField
from playhouse.migrate import (
    SqliteDatabase, SqliteMigrator, migrate
)
SCRIPT_DIR = os.path.dirname(__file__)


def update_picture(picture):
    if not picture:
        return picture

    picture_mime = (
        'data:%s;base64' % magic.from_buffer(picture,
                                             mime=True)
    )
    return '%s,%s' % (
        picture_mime,
        base64.b64encode(picture).decode('utf-8')
    )


def run_migration():
    recipes_db = SqliteDatabase(os.path.join(SCRIPT_DIR, '../recipes.db'))
    migrator = SqliteMigrator(recipes_db)

    new_picture_field = TextField(null=True)
    updated_pictures = [
        (recipe_id, update_picture(picture))
        for (recipe_id, picture) in recipes_db.execute_sql(
            'SELECT id, picture FROM recipe'
        )
    ]

    migrate(
        migrator.drop_column('recipe', 'picture'),
        migrator.add_column('recipe', 'picture', new_picture_field),
    )

    for (recipe_id, picture) in updated_pictures:
        if picture:
            recipes_db.execute_sql('UPDATE recipe SET picture=? WHERE id=?',
                                   (picture, recipe_id))


if __name__ == "__main__":
    run_migration()
