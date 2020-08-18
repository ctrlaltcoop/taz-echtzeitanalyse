# tazboard

This is a real time analytics tool for managing the taz website.
It is meant for internal usage by the taz website editorial team.

## Structure

tazboard's backend is written in `django` and the frontend in `vue.js`.
`frontend` contains the frontend of the project
`tazboard` contains the settings urls and other django boilerplate files.

## Project setup

This project uses poetry[^1]. Make sure poetry is installed on your system then install dependencies via:
```shell script
$ poetry install
```

## Run project in development

Source the project's environment
```shell script
$ poetry shell
```
(or `poetry run`)

Start the development server
```shell script
$ python manage.py runserver
```

### tmuxp

If you like tmux you can use tmuxp to conveniently launch both development commands in one session using the [tmuxp.yml](tmuxp.yml).
Just install tmuxp[^5] and type `tmuxp load tmuxp.yml` in this directory.

## Tests

For the backend tests to run everywhere, we mock up Elastic responses via
following command (you need to have a connection to the elastic host for that):
```
$ poetry run python manage.py create_mocks
```

Run the tests:
```
poetry run coverage run --source 'tazboard' manage.py test
```

## Run app in production

Assuming you have a wheel distribution of this application (built with `poetry run full-build`) the deployment process
looks like this.

```
$ pip install tazboard-x.x.x-py3-none-any.whl 
$ export DJANGO_SECRET_KEY=thisismysupersecretsecret
$ gunicorn tazboard.core.wsgi:application --bind 0.0.0.0:8000
```

Using gunicorn is optional and can be replaced with any wsgi compatible system.

### Using your own settings.py

It is possible to use your own django settings module if you need more control over the application behavior.
Just set the DJANGO_SETTINGS_MODULE variable to a settings module in you PYTHONPATH:

```
$ pip install tazboard-x.x.x-py3-none-any.whl
$ cd /etc/tazboard 
$ export DJANGO_SETTINGS_MODULE=config
$ gunicorn tazboard.core.wsgi:application --bind 0.0.0.0:8000
```

In this example it's required to have a file named `config.py` in /etc/tazboard. You can of course reference any python module
in your PYTHONPATH. In this file you can inherit from the base config and override variables:

```
from tazboard.core.settings.base import *
SECRET_KEY='mysecretkey'
```

## Frontend

The frontend is developed in a seperate toolchain in [frontend/static_src/](frontend/static_src) using `vue CLI`. For development instructions 
follow the [README.md  there](frontend/static_src/README.md).


## Building project to wheel and sdist

`pyproject.toml` contains all infos for distributing. Generally the command for building a python distribution in poetry is `poetry build`.
In our case we want to build the frontend assets first to bundle in the python package. As poetry doesn't support build hooks or similar
functioniality yet[^2][^3][^4] we introduced a wrapper command executing [build.py](build.py), which executes the frontend build before building
the python package.

[^1]: https://python-poetry.org/
[^2]: https://github.com/python-poetry/poetry/issues/1856
[^3]: https://github.com/python-poetry/poetry/issues/537
[^4]: https://github.com/python-poetry/poetry/issues/1992
[^5]: https://github.com/tmux-python/tmuxp
