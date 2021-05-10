#!/bin/sh

celery -A topShotScrapper worker --beat --scheduler django_celery_beat.schedulers.DatabaseScheduler -l info