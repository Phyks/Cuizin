import os

from cuizin import web


app = application = web.app

if __name__ == '__main__':
    HOST = os.environ.get('CUIZIN_HOST', 'localhost')
    PORT = os.environ.get('CUIZIN_PORT', '8080')
    DEBUG = os.environ.get('CUIZIN_DEBUG', False)
    app.run(host=HOST, port=PORT, debug=DEBUG)
