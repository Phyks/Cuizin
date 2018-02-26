from __future__ import absolute_import, print_function, unicode_literals
import json
import sys

from weboob.core.ouiboube import WebNip
from weboob.tools.json import WeboobEncoder

BACKENDS = ['750g', 'allrecipes', 'cuisineaz', 'marmiton', 'supertoinette']


def __main__(url, modules_path=None):
    webnip = WebNip(modules_path=modules_path)

    backends = [
        webnip.load_backend(
            module,
            module,
            params={}
        )
        for module in BACKENDS
    ]

    for backend in backends:
        browser = backend.browser
        if url.startswith(browser.BASEURL):
            browser.location(url)
            recipe = browser.page.get_recipe()
            print(json.dumps(recipe, cls=WeboobEncoder))
            break


if __name__ == "__main__":
    __main__(sys.argv[1])
