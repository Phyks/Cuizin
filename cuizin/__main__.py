import os

import peewee

from cuizin import db
from cuizin import web


app = application = web.app

if __name__ == '__main__':
    HOST = os.environ.get('CUIZIN_HOST', 'localhost')
    PORT = os.environ.get('CUIZIN_PORT', '8080')
    DEBUG = os.environ.get('CUIZIN_DEBUG', False)

    try:
        db.database.create_tables([db.Recipe])
    except peewee.OperationalError:
        pass

    app.run(host=HOST, port=PORT, debug=DEBUG)
