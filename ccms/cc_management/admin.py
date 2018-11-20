from django.contrib import admin

# Import the models
from .models import *

# Register your models here.
admin.site.register(Club)
admin.site.register(Club_Classifications)