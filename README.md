# Top Shot Floor
A Django Website that Scrapes TS Floor Prices and stores historical data on each moment

## Installation
Make sure to install the following:
- [pip](https://pip.pypa.io/en/stable/) our python package manager 
- [redis](https://redis.io/download) for our celery broker
- [chromedriver](https://chromedriver.chromium.org/), the current chromedriver in the project is the one that works on my personal computer make sure to download correct verison given your chrome version



## Environment Set-Up
Set up is rather easy with the pipenv package simply run the following terminal commands in the project directory

```bash
pip install pipenv
pipenv shell
pipenv lock
pipenv install
```
Just like that all the dependecies for the project are installed in our virtual environment!  To run the server, execute the following in the pipenv shell

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Celery Broker and Scrapper
To start scrapping you will need to start up the redis server, open up a new terminal where you installed redis and run

```bash
redis-server
```
Now that thats running, open two new terminals in your pipenv environment and run each in a different shell

```bash
celery -A topShotScrapper worker -l info
celery -A topShotScrapper beat -l info
```
It is currently configured to run every hour as it takes ~20 minutes to scrape every moment. 
To edit how many teams you want to scrape go to core/tasks.py and lower the upperbound of the for loop.
To edit the scheduler go to topShotScrapper/settings.py and go to the CELERY_BEAT_SCHEDULE and change the schedule value (in seconds).

## Have fun!
