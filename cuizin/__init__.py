from __future__ import absolute_import, print_function, unicode_literals
import json
import sys

from weboob.core.ouiboube import WebNip
from weboob.tools.json import WeboobEncoder

from cuizin import db

BACKENDS = ['750g', 'allrecipes', 'cuisineaz', 'marmiton', 'supertoinette']


def add_recipe(url, modules_path=None):
    webnip = WebNip(modules_path=modules_path)

    backends = [
        webnip.load_backend(
            module,
            module,
            params={}
        )
        for module in BACKENDS
    ]

    recipe = None
    for backend in backends:
        browser = backend.browser
        if url.startswith(browser.BASEURL):
            browser.location(url)
            recipe = db.Recipe.from_weboob(browser.page.get_recipe())
            # Ensure URL is set
            recipe.url = url
            break

    if not recipe:
        # TODO
        recipe = db.Recipe()
        recipe.url = url

    recipe.save()
    return recipe
