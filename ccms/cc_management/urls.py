from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='cc-management-home'),
    path('test/', views.test, name='cc-management-test'),
]

# Add the club CRUD and foreign relationship URLs
urlpatterns += [
    path('clubs/', views.club_list, name='club_list'),
    path('clubs/create', views.club_create, name='club_create'),
    path('clubs/<int:pk>', views.club_view, name='club_view'),
    path('clubs/<int:pk>/edit', views.club_edit, name='club_edit'),
    path('clubs/<int:pk>/delete', views.club_delete, name='club_delete'),
    path('clubs/<int:pk>/players', views.club_players, name='club_players'),
]