# tazboard

This is a real time analytics tool for managing the taz website.
It is meant for internal usage by the taz website editorial team.


## Project setup

This project uses poetry[^1]. Make sure poetry is installed on your system then install dependencies via:
```shell script
$ poetry install
```

## Run project in development

Start the development server with

```shell script
$ python manage.py runserver
```

⚠ Note that this command need to be executed in the virtualenv poetry created, start it either with `poetry shell` or prepend
`poetry run` to your command.

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