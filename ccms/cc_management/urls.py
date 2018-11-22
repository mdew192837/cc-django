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
    # path('clubs/<int:pk>/players', views.club_players, name='club_players'),
]

# Add the classifications CRUD and foreign relationship URLs
urlpatterns += [
    path('classifications/', views.classification_list, name='classification_list'),
    path('classifications/create', views.classification_create, name='classification_create'),
    path('classifications/<int:pk>', views.classification_view, name='classification_view'),
    path('classifications/<int:pk>/edit', views.classification_edit, name='classification_edit'),
    path('classifications/<int:pk>/delete', views.classification_delete, name='classification_delete'),
]

# Add the players CRUD and foreign relationship URLs
urlpatterns += [
    # Old - path('players/', views.player_list, name='player_list'),
    path('clubs/<int:pk_club>/players/<int:pk>', views.player_view, name='player_view'),
    path('clubs/<int:pk_club>/players/<int:pk>/edit', views.player_edit, name='player_edit'),
    path('clubs/<int:pk_club>/players/<int:pk>/delete', views.player_delete, name='player_delete'),
    path('clubs/<int:pk_club>/players/create', views.player_create, name='player_create'),
    path('clubs/<int:pk_club>/players', views.club_players, name='club_players'),
]

# Add the games CRUD
urlpatterns += [
    path('games/', views.game_list, name='game_list'),
    path('clubs/<int:pk_club>/games', views.club_games, name='club_games'),
    path('clubs/<int:pk_club>/games/create', views.game_create, name='game_create'),
    path('clubs/<int:pk_club>/games/<int:pk>/edit', views.game_edit, name='game_edit'),
]

# Begin Batches CRUD
urlpatterns += [
    path('clubs/<int:pk_club>/games/process', views.process_games, name='process_games')
]