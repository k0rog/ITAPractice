#!/bin/bash

python manage.py makemigrations users --no-input
python manage.py makemigrations gamehub --no-input
python manage.py makemigrations --no-input

python manage.py migrate --no-input

python manage.py runserver 0.0.0.0:8000

exec gunicorn config.wsgi:application -b 0.0.0.0:8000 --reload
