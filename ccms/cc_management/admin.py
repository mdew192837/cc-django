from django.contrib import admin

# Import the models
from .models import *

# Register your models here.
class ClubAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
admin.site.register(Club, ClubAdmin)
admin.site.register(Club_Classifications)

# Display all fields for player
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'classification', 'club_id', 'grade', 'rating', 'uscf_id', 'uscf_rating', 'games_played', 'is_active', 'created_at', 'updated_at')
    list_filter = ('club_id', 'classification', 'is_active', 'grade')
    # TODO - Figure out what else we want to search for
    search_fields = ['first_name', 'last_name', 'id']
admin.site.register(Player, PlayerAdmin)

# Display all fields for the game
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'club', 'white_player', 'black_player', 'result', 'processed', 'batch_id')
    list_filter = ('club_id', 'batch_id')
    search_fields = ['white_player', 'black_player', 'id']
admin.site.register(Game, GameAdmin)