from django.db import models
from django.contrib.auth import get_user_model



# An individual topShot contains all relivant info for each TS
class topShot(models.Model):
    #constants
    player_name = models.CharField(max_length=60)
    team = models.CharField(max_length=100)
    play_type = models.CharField(max_length=15)
    set_name = models.CharField(max_length=50)
    rarity = models.CharField(max_length=50)
    date_game = models.DateField()
    pic = models.CharField(max_length=300)

    #Never changes if is LE, subject to change for CC moments
    out_of = models.IntegerField()
    edition = models.CharField(max_length=2)

    #last updated price with datetime
    curr_price = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)

    #historical data needed for candlestick charts
    open_price = models.TextField()
    close_price = models.TextField()
    high_price = models.TextField()
    low_price = models.TextField()
    scrape_date = models.TextField()

    def __str__(self):
        return self.player_name + " :" + self.set_name

#An object that holds all TS in a set for all sets
class Set(models.Model):
    set_name = models.CharField(max_length=50)
    moments = models.ManyToManyField(topShot)
    img_link = models.CharField(max_length=100)

#An object that holds all TS in a challenge for all active Challneges
class Challenge(models.Model):
    player_name = models.CharField(max_length=50)
    challenege_name = models.CharField(max_length=50)
    moments = models.ManyToManyField(topShot)

#An object that is user specific that holds all TS that a user wants to watch
class WatchList(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        primary_key=True,
        on_delete=models.CASCADE,
    )
    watch_list = models.ManyToManyField(topShot)
