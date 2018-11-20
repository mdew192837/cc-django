from django.contrib import admin

# Import the models
from .models import *

# Register your models here.
admin.site.register(Club)
admin.site.register(Club_Classifications)

# Display all fields for player
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'classification', 'club_id', 'grade', 'rating', 'uscf_id', 'uscf_rating', 'is_active', 'created_at', 'updated_at')
    list_filter = ('club_id', 'classification', 'is_active', 'grade')
    # TODO - Figure out what else we want to search for
    search_fields = ['first_name', 'last_name']
admin.site.register(Player, PlayerAdmin)