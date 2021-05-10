from django.shortcuts import render
from django.views import generic
from .models import topShot, Set, Challenge
import datetime, time
import functools

#Table of TS
class topShotListView(generic.ListView):
    model = topShot 
    template_name = 'top_shot_list.html'
    paginate_by = 20

    def get_queryset(self):
        qs = topShot.objects.all()
        name = self.request.GET.get('player_name', None)
        if name:
            qs = qs.filter(player_name__icontains=name)
        return qs.order_by('-date_game')

#List of Sets
class setView(generic.ListView):
    model = Set
    template_name = 'sets.html'

#List of Challenges
class challengeView(generic.ListView):
    model = Challenge
    template_name = 'challenges.html'

def topShot_detail(request, id):
    ts = topShot.objects.get(id=id)

    #ALL ARRAYS NEEDED FOR CANDLESTICK DATA

    ##making open price string into an integer array
    open_price = ts.open_price
    open_price = open_price.split(',')
    open_price = list(map(float, open_price)) 

    ##making close price string into an integer array
    close_price = ts.close_price
    close_price = close_price.split(',')
    close_price = list(map(float, close_price)) 

    ##making high price string into an integer array
    high_price = ts.high_price
    high_price = high_price.split(',')
    high_price = list(map(float, high_price)) 

    ##making low price string into an integer array
    low_price = ts.low_price
    low_price = low_price.split(',')
    low_price = list(map(float, low_price)) 

    #making time string into a date array 
    dates = ts.scrape_date
    dates = dates.split(',')
    print(dates)

    context = {
        'ts' : ts,
        'open_price' : open_price,
        'close_price' : close_price,
        'high_price' : high_price,
        'low_price' : low_price,
        'dates' : dates,
        
    }
    return render(request, 'top_shot_detail.html', context)


def set_detail(request, id):
    ts_set = Set.objects.get(id=id)
    moments = list(ts_set.moments.all())
    market_cap = 0
    tot_price = 0
    for moment in moments:
        tot_price += moment.curr_price
        market_cap += ( moment.curr_price * moment.out_of )
        moment.curr_price = "{:,}".format(moment.curr_price)
    tot_price = "{:,}".format(tot_price)
    market_cap = "{:,}".format(market_cap)
    context = {
        'set' : ts_set,
        'moments' : moments,
        'market_cap' : market_cap,
        'tot' : tot_price
    }
    return render(request, 'indiv_set.html', context)
