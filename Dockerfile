FROM python:3.9.0-alpine
ENV PYTHONUNBUFFERED 1

WORKDIR /tmp
COPY dist/*.whl /tmp/
RUN apk add --no-cache \
        libressl-dev \
        postgresql-dev \
        gcc \
	libpq \
        python3-dev \
        musl-dev \
        libffi-dev && \
    pip install --no-cache-dir gunicorn *.whl  && \
    apk del \
        libressl-dev \
        musl-dev \
        libffi-dev \
        postgresql-dev \
        gcc

CMD gunicorn tazboard.core.wsgi:application --bind 0.0.0.0:8000
