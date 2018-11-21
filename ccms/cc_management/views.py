from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.contrib import messages
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
    players = club.player_set.all()
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