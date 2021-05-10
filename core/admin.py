from django.contrib import admin
from .models import topShot, Set, Challenge

# Register your models here.
class topShotAdmin(admin.ModelAdmin):
    list_display = [
        'player_name',
        'set_name',
        'rarity',
        'curr_price',
        'last_update'
    ]

class setAdmin(admin.ModelAdmin):
    list_display = [
        'set_name'
    ]

admin.site.register(topShot, topShotAdmin)
admin.site.register(Set, setAdmin)
admin.site.register(Challenge)


