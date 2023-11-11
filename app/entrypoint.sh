#!/bin/sh

#poetry run python manage.py makemigrations --noinput
poetry run python manage.py migrate --noinput
#poetry run python manage.py collectstatic --noinput
#poetry run gunicorn backpack_store.wsgi:application --bind 0.0.0.0:8000
poetry run python manage.py runserver 0.0.0.0:8000
