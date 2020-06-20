FROM python:3
ENV PYTHONUNBUFFERED 1

WORKDIR /app
RUN pip install poetry gunicorn
COPY pyproject.toml /app/
COPY poetry.lock /app/
RUN poetry export -f requirements.txt -o requirements.txt
RUN pip install -r requirements.txt
COPY tazboard/ /app/

ENV DJANGO_SETTINGS_MODULE core.settings.docker

RUN python manage.py collectstatic --noinput
CMD gunicorn core.wsgi:application --bind 0.0.0.0:8000
