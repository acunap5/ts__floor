#!/bin/sh

python manage.py migrate
python manage.py makesuper
python manage.py collectstatic
gunicorn topShotScrapper.wsgi --bind=0.0.0.0:80