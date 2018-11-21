from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.forms import ModelForm
from django.contrib import messages
from django.urls import reverse
from django_tables2 import RequestConfig
from .tables import *
from .models import *
# from django.http import HttpResponse

# Create your views here.
def home(request):
    clubs = Club.objects.all()
    return render(request, 'cc_management/home.html', context={"clubs": clubs})

def test(request):
    club_classifications = Club_Classifications.objects.all()
    return render(request, 'cc_management/test.html', context={"classifications": club_classifications})

# CRUD for Club
class ClubForm(ModelForm):
    class Meta:
        model = Club
        fields = ['name']

def club_list(request, template_name="cc_management/clubs/club_list.html"):
    clubs = Club.objects.order_by('id')
    return render(request, template_name, {"clubs": clubs})

def club_view(request, pk, template_name="cc_management/clubs/club_detail.html"):
    club = get_object_or_404(Club, pk=pk)
    return render(request, template_name, {"club": club})

def club_create(request, template_name="cc_management/clubs/club_create.html"):
    form = ClubForm(request.POST or None)
    if form.is_valid():
        club_name = form.cleaned_data.get("name")
        form.save()
        messages.success(request, f'Club {club_name} created!')
        return redirect("club_list")
    return render(request, template_name, {"form": form})

def club_edit(request, pk, template_name="cc_management/clubs/club_edit.html"):
    club = get_object_or_404(Club, pk=pk)
    form = ClubForm(request.POST or None, instance=club)
    if form.is_valid():
        new_name = form.cleaned_data.get("name")
        form.save()
        messages.success(request, f'Club name changed to {new_name}!')
        return redirect("club_list")
    return render(request, template_name, {"form": form, "club": club})

def club_delete(request, pk, template_name="cc_management/clubs/club_confirm_delete.html"):
    club = get_object_or_404(Club, pk=pk)
    if request.method == "POST":
        club_name = club.name
        club.delete()
        messages.warning(request, f"Club {club_name} deleted.")
        return redirect("club_list")
    return render(request, template_name, {"club": club})

def club_players(request, pk, template_name="cc_management/clubs/club_players.html"):
    club = get_object_or_404(Club, pk=pk)
    players = club.player_set.all().order_by('id')
    return render(request, template_name, {"club": club, "players": players})

# CRUD for Classifications
class ClassificationForm(ModelForm):
    class Meta:
        model = Club_Classifications
        fields = ['name']

def classification_list(request, template_name="cc_management/classifications/classification_list.html"):
    classifications_list = Club_Classifications.objects.order_by('id')
    return render(request, template_name, {"classifications": classifications_list})

def classification_view(request, pk, template_name="cc_management/classifications/classification_view.html"):
    classification = get_object_or_404(Club_Classifications, pk=pk)
    return render(request, template_name, {"classification": classification})

def classification_create(request, template_name="cc_management/classifications/classification_create.html"):
    form = ClassificationForm(request.POST or None)
    if form.is_valid():
        classification_name = form.cleaned_data.get("name")
        form.save()
        messages.success(request, f'Classification {classification_name} created!')
        return redirect("classification_list")
    return render(request, template_name, {"form": form})

def classification_edit(request, pk, template_name="cc_management/classifications/classification_edit.html"):
    classification = get_object_or_404(Club_Classifications, pk=pk)
    form = ClassificationForm(request.POST or None, instance=classification)
    if form.is_valid():
        new_name = form.cleaned_data.get("name")
        form.save()
        messages.success(request, f'Classification name changed to {new_name}!')
        return redirect("classification_list")
    return render(request, template_name, {"form": form, "classification": classification})

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
    class Meta:
        model = Player
        fields = ['first_name', 'middle_name', 'last_name', 'club_id', 'classification', 'grade', 'uscf_id', 'uscf_rating', 'rating', 'games_played', 'is_active']

def player_list(request, template_name="cc_management/players/player_list.html"):
    players = Player.objects.order_by('last_name')
    return render(request, template_name, {"players": players})

def player_view(request, pk, template_name="cc_management/players/player_view.html"):
    player = get_object_or_404(Player, pk=pk)
    return render(request, template_name, {"player": player})

def player_create(request, template_name="cc_management/players/player_create.html"):
    form = PlayerForm(request.POST or None)
    if form.is_valid():
        player_name = form.cleaned_data.get("first_name") + " " + form.cleaned_data.get("last_name")
        club_id = form.cleaned_data.get("club_id").id
        form.save()
        messages.success(request, f'Player {player_name} created!')
        return HttpResponseRedirect(reverse("club_players", args=(club_id,)))
    return render(request, template_name, {"form": form})

def player_edit(request, pk, template_name="cc_management/players/player_edit.html"):
    player = get_object_or_404(Player, pk=pk)
    form = PlayerForm(request.POST or None, instance=player)
    if form.is_valid():
        name = form.cleaned_data.get("first_name") + " " + form.cleaned_data.get("last_name")
        form.save()
        messages.success(request, f'Profile Updated for {name}!')
        return HttpResponseRedirect(reverse("club_players", args=(player.club_id.id,)))
    return render(request, template_name, {"form": form, "player": player})

def player_delete(request, pk, template_name="cc_management/players/player_confirm_delete.html"):
    player = get_object_or_404(Player, pk=pk)
    if request.method == "POST":
        player_name = player.first_name + ' ' + player.last_name
        club_id = player.club_id.id
        player.delete()
        messages.warning(request, f"Player {player_name} deleted.")
        return HttpResponseRedirect(reverse("club_players", args=(club_id,)))
    return render(request, template_name, {"player": player})

def filter_players(request):
    queryset = Player.objects.order_by('last_name')
    filter = PlayerFilter(request.GET, queryset=queryset)
    table = PlayerTable(filter.qs)
    RequestConfig(request).configure(table)
    return render(request, 'cc_management/players/players.html', {'table': table, 'filter': filter})