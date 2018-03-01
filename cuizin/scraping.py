"""
Scraping code, to fetch and add a recipe.

This code wraps around [Web Outside Of Browsers](http://weboob.org/).
"""
from __future__ import absolute_import, print_function, unicode_literals

import os

from weboob.core.ouiboube import WebNip

from cuizin import db

# List of backends with recipe abilities in Weboob
BACKENDS = ['750g', 'allrecipes', 'cuisineaz', 'marmiton', 'supertoinette']


def add_recipe(url):
    """
    Add a recipe, trying to scrape from a given URL.

    :param url: URL of the recipe.
    :return: A ``cuizin.db.Recipe`` model.
    """
    # Eventually load modules from a local clone
    MODULES_PATH = os.environ.get('WEBOOB_MODULES_PATH', None)

    # Get all backends with recipe abilities
    webnip = WebNip(modules_path=MODULES_PATH)
    backends = [
        webnip.load_backend(
            module,
            module,
            params={}
        )
        for module in BACKENDS
    ]

    # Try to fetch the recipe with a Weboob backend
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
