Cuizin
======

Cuizin is a tool wrapping around [Web Outside Of Browsers](http://weboob.org/)
to help you sort and organize recipes you find online. You can also manually
add new recipes.


## Installation

```
$ git clone …  # Clone this repository
$ pip install -r requirements.txt  # Install Python dependencies
$ npm install  # Install JS dependencies for the frontend
$ npm run build  # Build the JS dependencies
```

Ideally, Python dependencies should be installed in a virtual environment.

If you serve the app from a subdirectory (and not the root of your domain),
you might want to run `URL_PREFIX=/subdir/ npm run build` instead of `npm run
build` to use the correct path to call the API. Note that the trailing slash
is important.


## Usage

Run `python -m cuizin` to run the built-in webserver. Conversely, you can use
WSGI to serve the application directly (`application` variable is exported in
`cuizin/__main__.py`).

You can customize the behavior of the app by passing environment variables:
* `CUIZIN_HOST` to set the host on which the webserver should listen to
  (defaults to `localhost` only). Use `HOST=0.0.0.0` to make it
  world-accessible.
* `CUIZIN_PORT` to set the port on which the webserver should listen. Defaults
  to `8080`.
* `CUIZIN_DEBUG` to enable or disable the debug from Bottle (defaults to
  `False`).
* `WEBOOB_MODULES_PATH` to set the path to the local clone of the Weboob
  modules. Default to using the `weboob-modules` package installed by `pip`
  (and which you should regularly update with `pip install --upgrade
  weboob-modules`).

If you serve the app with a reverse proxy, you should serve the content of
`cuizin/dist` (static frontend files) directly, without passing it down to the
Bottle webserver.


## Contributing

All contributions are welcome, feel free to open a MR. Just in case, if you
plan on working on some major new feature, please open an issue before to get
some feedbacks.

All the code lies under `cuizin` directory. Frontend code lies under
`cuizin/js_src`. `build` and `config` folders at the root of this repository
are used for the frontend build.

Additionnally, you can use `make dev` to spawn a development webserver to
serve the JS frontend and auto-update/auto-reload when you make changes. The
spawned JS server will be set up at `localhost:8081` and you should start the
backend Python server at `localhost:8080` with `python -m cuizin` along it.
You can simply open the app at `localhost:8081` and start developping, it will
automatically call the API from the `python -m cuizin` process, on port
`8080`.


## License

This software is released under an MIT License.
