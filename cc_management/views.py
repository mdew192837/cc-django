from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.forms import ModelForm, forms
from django.contrib import messages
from django.urls import reverse
from django_tables2 import RequestConfig
from .tables import *
from .models import *
from elo import rate_1vs1
import json

# Create your views here.
@login_required
def old_home(request):
    clubs = Club.objects.all()
    return render(request, 'cc_management/home.html', context={"clubs": clubs})

@login_required
def home(request):
    return redirect('/clubs')

@login_required
def test(request):
    club_classifications = Club_Classifications.objects.all()
    return render(request, 'cc_management/test.html', context={"classifications": club_classifications})

@login_required
@staff_member_required
def reset(request):
    TEST_RATINGS = {
        8: 500,
        9: 600,
        10: 700
    }

    GAMES = [7, 8, 9]

    # Set Processed to False
    for game_id in GAMES:
        game = Game.objects.get(pk=game_id)
        game.processed = False
        game.save()

    # Set those player ratings
    for player_id, rating in TEST_RATINGS.items():
        player = Player.objects.get(pk=player_id)
        player.rating = rating
        player.save()

    return redirect('/clubs')

# CRUD for Club
class ClubForm(ModelForm):
    class Meta:
        model = Club
        fields = ['name']

@login_required
def club_list(request, template_name="cc_management/clubs/club_list.html"):
    clubs = Club.objects.order_by('id')
    return render(request, template_name, {"clubs": clubs})

@login_required
def club_view(request, pk, template_name="cc_management/clubs/club_detail.html"):
    club = get_object_or_404(Club, pk=pk)
    return render(request, template_name, {"club": club})

@login_required
@staff_member_required
def club_create(request, template_name="cc_management/clubs/club_create.html"):
    form = ClubForm(request.POST or None)
    if form.is_valid():
        club_name = form.cleaned_data.get("name")
        form.save()
        messages.success(request, f'Club {club_name} created!')
        return redirect("club_list")
    return render(request, template_name, {"form": form})

@login_required
@staff_member_required
def club_edit(request, pk, template_name="cc_management/clubs/club_edit.html"):
    club = get_object_or_404(Club, pk=pk)
    form = ClubForm(request.POST or None, instance=club)
    if form.is_valid():
        new_name = form.cleaned_data.get("name")
        form.save()
        messages.success(request, f'Club name changed to {new_name}!')
        return redirect("club_list")
    return render(request, template_name, {"form": form, "club": club})

@login_required
@staff_member_required
def club_delete(request, pk, template_name="cc_management/clubs/club_confirm_delete.html"):
    club = get_object_or_404(Club, pk=pk)
    if request.method == "POST":
        club_name = club.name
        club.delete()
        messages.warning(request, f"Club {club_name} deleted.")
        return redirect("club_list")
    return render(request, template_name, {"club": club})

"""
Old - Before we swapped to the new url routes /club/<int:pk_club>/players
def club_players(request, pk, template_name="cc_management/clubs/club_players.html"):
    club = get_object_or_404(Club, pk=pk)
    players = club.player_set.all().order_by('id')
    return render(request, template_name, {"club_id": pk, "players": players})
"""

# CRUD for Classifications
class ClassificationForm(ModelForm):
    class Meta:
        model = Club_Classifications
        fields = ['name']

@login_required
def classification_list(request, template_name="cc_management/classifications/classification_list.html"):
    classifications_list = Club_Classifications.objects.order_by('id')
    return render(request, template_name, {"classifications": classifications_list})

@login_required
def classification_view(request, pk, template_name="cc_management/classifications/classification_view.html"):
    classification = get_object_or_404(Club_Classifications, pk=pk)
    return render(request, template_name, {"classification": classification})

@login_required
@staff_member_required
def classification_create(request, template_name="cc_management/classifications/classification_create.html"):
    form = ClassificationForm(request.POST or None)
    if form.is_valid():
        classification_name = form.cleaned_data.get("name")
        form.save()
        messages.success(request, f'Classification {classification_name} created!')
        return redirect("classification_list")
    return render(request, template_name, {"form": form})

@login_required
@staff_member_required
def classification_edit(request, pk, template_name="cc_management/classifications/classification_edit.html"):
    classification = get_object_or_404(Club_Classifications, pk=pk)
    form = ClassificationForm(request.POST or None, instance=classification)
    if form.is_valid():
        new_name = form.cleaned_data.get("name")
        form.save()
        messages.success(request, f'Classification name changed to {new_name}!')
        return redirect("classification_list")
    return render(request, template_name, {"form": form, "classification": classification})

@login_required
@staff_member_required
def classification_delete(request, pk, template_name="cc_management/classifications/classification_confirm_delete.html"):
    classification = get_object_or_404(Club_Classifications, pk=pk)
    if request.method == "POST":
        classification_name = classification.name
        classification.delete()
        messages.warning(request, f"Classification {classification_name} deleted.")
        return redirect("classification_list")
    return render(request, template_name, {"classification": classification})

# CRUD for Players
class PlayerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PlayerForm, self).__init__(*args, **kwargs)
        self.fields['club_id'].disabled = True

    class Meta:
        model = Player
        fields = ['first_name', 'middle_name', 'last_name', 'club_id', 'classification', 'grade', 'uscf_id', 'uscf_rating', 'rating', 'games_played', 'is_active']

@login_required
def player_list(request, template_name="cc_management/players/player_list.html"):
    players = Player.objects.order_by('last_name')
    return render(request, template_name, {"players": players})

@login_required
def player_view(request, pk_club, pk, template_name="cc_management/players/player_view.html"):
    player = get_object_or_404(Player, pk=pk)
    return render(request, template_name, {"player": player, "club_id": pk_club})

@login_required
@staff_member_required
def player_create(request, pk_club, template_name="cc_management/players/player_create.html"):
    classifications = len(Club_Classifications.objects.all())
    club = get_object_or_404(Club, pk=pk_club)
    form = PlayerForm(request.POST or None, initial={'club_id': pk_club})
    if form.is_valid():
        player_name = form.cleaned_data.get("first_name") + " " + form.cleaned_data.get("last_name")
        form.save()
        messages.success(request, f'Player {player_name} created!')
        return HttpResponseRedirect(reverse("club_players", args=(pk_club,)))
    return render(request, template_name, {"form": form, "club_id": pk_club, "classifications": classifications})

@login_required
@staff_member_required
def player_edit(request, pk_club, pk, template_name="cc_management/players/player_edit.html"):
    player = get_object_or_404(Player, pk=pk)
    form = PlayerForm(request.POST or None, instance=player)
    if form.is_valid():
        name = form.cleaned_data.get("first_name") + " " + form.cleaned_data.get("last_name")
        form.save()
        messages.success(request, f'Profile Updated for {name}!')
        return HttpResponseRedirect(reverse("club_players", args=(pk_club,)))
    return render(request, template_name, {"form": form, "player": player, "club_id": pk_club})

@login_required
@staff_member_required
def player_delete(request, pk_club, pk, template_name="cc_management/players/player_confirm_delete.html"):
    player = get_object_or_404(Player, pk=pk)
    if request.method == "POST":
        player_name = player.first_name + ' ' + player.last_name
        player.delete()
        messages.warning(request, f"Player {player_name} deleted.")
        return HttpResponseRedirect(reverse("club_players", args=(pk_club,)))
    return render(request, template_name, {"player": player, "club_id": pk_club})

@login_required
def club_players(request, pk_club, template_name="cc_management/players/club_players.html"):
    club = get_object_or_404(Club, pk=pk_club)
    queryset = Player.objects.filter(club_id=pk_club).order_by('last_name')
    filter = PlayerFilter(request.GET, queryset=queryset)
    table = PlayerTable(filter.qs)
    RequestConfig(request).configure(table)
    # Could just do 'club_id': pk_club but that's meta yo
    return render(request, template_name, {'table': table, 'filter': filter, 'club': club, 'players': queryset})

# CRUD for Games
@login_required
def club_games(request, pk_club, template_name="cc_management/games/club_games.html"):
    club = get_object_or_404(Club, pk=pk_club)
    queryset = Game.objects.filter(club_id=pk_club).order_by('id')
    # Determine if we have any games to process
    needs_processing = True if len(Game.objects.filter(club_id=pk_club, processed=False)) > 0 else False
    filter = GameFilter(request.GET, pk_club, queryset=queryset)
    table = GameTable(filter.qs)
    RequestConfig(request).configure(table)
    return render(request, 'cc_management/games/club_games.html', {'table': table, 'filter': filter, 'club': club, 'games': queryset, 'needs_processing': needs_processing})

@login_required
def game_list(request, template_name="cc_management/games/game_list.html"):
    games = Game.objects.order_by('club').order_by('id')
    return render(request, template_name, {"games": games})

class GameForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(GameForm, self).__init__(*args, **kwargs)
        self.fields['club'].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        black_player = cleaned_data.get("black_player")
        white_player = cleaned_data.get("white_player")
        if black_player.id == white_player.id:
            raise forms.ValidationError(
                "The black and white players must be different!"
            )

    class Meta:
        model = Game
        fields = ['club', 'black_player', 'white_player', 'result']

@login_required
@staff_member_required
def game_create(request, pk_club, template_name="cc_management/games/game_create.html"):
    club = get_object_or_404(Club, pk=pk_club)
    players = Player.objects.filter(club_id=pk_club)
    form = GameForm(request.POST or None, initial={'club': pk_club})
    form.fields['black_player'].queryset = players
    form.fields['white_player'].queryset = players
    if form.is_valid():
        black_player = get_object_or_404(Player, pk=form.cleaned_data.get("black_player").id)
        white_player = get_object_or_404(Player, pk=form.cleaned_data.get("white_player").id)
        # Update the game counts for both
        black_player.games_played = black_player.games_played + 1
        black_player.save()
        white_player.games_played = white_player.games_played + 1
        white_player.save()
        form.save()
        messages.success(request, f'Game added!')
        return HttpResponseRedirect(reverse("club_games", args=(pk_club,)))
    return render(request, template_name, {"form": form, "club_id": pk_club, "players": len(players)})

@login_required
@staff_member_required
def game_edit(request, pk_club, pk, template_name="cc_management/games/game_edit.html"):
    game = get_object_or_404(Game, pk=pk)
    form = GameForm(request.POST or None, instance=game)
    form.fields['black_player'].disabled = True
    form.fields['white_player'].disabled = True
    if form.is_valid():
        form.save()
        messages.success(request, f'Game Result Updated!')
        return HttpResponseRedirect(reverse("club_games", args=(pk_club,)))
    return render(request, template_name, {"form": form, "club_id": pk_club})

def add_differential(differentials, white_player, white_differential, black_player, black_differential):
    if white_player.id in differentials["players"]:
        differentials["players"][white_player.id]["differential"] = differentials["players"][white_player.id]["differential"] + white_differential
    else:
        differentials["players"][white_player.id] = {}
        differentials["players"][white_player.id]["differential"] = white_differential

    if black_player.id in differentials["players"]:
        differentials["players"][black_player.id]["differential"] = differentials["players"][black_player.id]["differential"] + black_differential
    else:
        differentials["players"][black_player.id] = {}
        differentials["players"][black_player.id]["differential"] = black_differential

    return differentials

@login_required
@staff_member_required
def process_games(request, pk_club):
    club = get_object_or_404(Club, pk=pk_club)
    games = club.game_set.filter(processed=False).order_by('id')

    # Redirect if no games to process
    if not games:
        messages.warning(request, 'No games to process')
        return HttpResponseRedirect(reverse("club_games", args=(pk_club,)))

    # Results are hardcoded, as defined in the models
    RESULTS = {
        0: "BLACK",
        1: "DRAW",
        2: "WHITE"
    }

    differentials = {
        "players": {},
        "games": []
    }

    for game in games:
        # Add the game id
        # TODO - Go through the IDs and update their batch_id
        differentials["games"].append(game.id)

        black_player = get_object_or_404(Player, pk=game.black_player.id)
        white_player = get_object_or_404(Player, pk=game.white_player.id)

        differential = {
            "black": {
                "rating_before": black_player.rating,
                "id": black_player.id
            },
            "white": {
                "rating_before": white_player.rating,
                "id": white_player.id
            }
        }

        # Process the game
        if RESULTS[game.result] == "BLACK":
            results = rate_1vs1(black_player.rating, white_player.rating)
            differential["black"]["differential"] = round(results[0]) - black_player.rating
            differential["white"]["differential"] = round(results[1]) - white_player.rating
        elif RESULTS[game.result] == "WHITE":
            results = rate_1vs1(white_player.rating, black_player.rating)
            # Since black player is second now
            differential["black"]["differential"] = round(results[1]) - black_player.rating
            differential["white"]["differential"] = round(results[0]) - white_player.rating
        else:
            # Must be a draw
            results = rate_1vs1(white_player.rating, black_player.rating)
            differential["black"]["differential"] = round(results[1]) - black_player.rating
            differential["white"]["differential"] = round(results[0]) - white_player.rating

        # Add the differentials
        differentials = add_differential(differentials,
                                        white_player,
                                        differential["white"]["differential"],
                                        black_player,
                                        differential["black"]["differential"])

        # Save the differential in the JSON column
        game.json = differential
        # Mark the game as processed
        game.processed = True
        game.save()

    # Update the player ratings
    for player_id, properties in differentials["players"].items():
        player = get_object_or_404(Player, pk=player_id)
        # Store the previous rating
        differentials["players"][player_id]["rating_before"] = player.rating
        # Update the rating
        player.rating = player.rating + properties["differential"]
        player.save()
        # Store the new rating
        differentials["players"][player_id]["rating_after"] = player.rating

    # TODO - Save the differentials in a batch
    print(differentials)

    # Create the batch
    batch = Batch.objects.create(club=get_object_or_404(Club, pk=pk_club), json=differentials)
    batch_id = batch.id

    # Update the batch number
    for game_id in differentials["games"]:
        game = Game.objects.get(id=game_id)
        game.batch_id = batch_id
        game.save()

    # Redirect to the games page
    return HttpResponseRedirect(reverse("club_games", args=(pk_club,)))

@login_required
def club_batches(request, pk_club, template_name="cc_management/batches/club_batches.html"):
    club = get_object_or_404(Club, pk=pk_club)
    queryset = Batch.objects.filter(club=pk_club)
    table = BatchTable(queryset)
    RequestConfig(request).configure(table)
    return render(request, 'cc_management/batches/club_batches.html', {'table': table, 'club': club, 'batches': queryset})
