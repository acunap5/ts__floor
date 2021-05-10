from celery import shared_task, task
from .scrapers import scrape
import datetime

@task 
def scrape_team_data():
    day = str(datetime.datetime.now().date())
    for i in range(37, 67):
        URL = 'https://www.nbatopshot.com/search?byTeams=16106127'
        end = '&orderBy=GAME_DATE_ASC'
        scrape(URL + str(i) + end, day)
    return