from django.shortcuts import render
from .models import *
# from django.http import HttpResponse

# Create your views here.
def home(request):
    clubs = Club.objects.all()
    return render(request, 'cc_management/home.html', context={"clubs": clubs})

def test(request):
    club_classifications = Club_Classifications.objects.all()
    return render(request, 'cc_management/test.html', context={"classifications": club_classifications})