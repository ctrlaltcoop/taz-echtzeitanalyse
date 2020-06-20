FROM python:3
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app
RUN pip install poetry gunicorn
COPY pyproject.toml /app/
COPY poetry.lock /app/
RUN poetry export -f requirements.txt -o requirements.txt
RUN pip install -r requirements.txt
COPY . /app/

ENV DJANGO_SETTINGS_MODULE tazboard.settings.docker

RUN python manage.py collectstatic --noinput
CMD gunicorn tazboard.wsgi:application --bind 0.0.0.0:8000
