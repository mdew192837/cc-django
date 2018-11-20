from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='cc-management-home'),
    path('test', views.test, name='cc-management-test')
]