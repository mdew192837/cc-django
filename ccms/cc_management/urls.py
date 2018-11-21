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

# Add the classifications CRUD and foreign relationship URLs
urlpatterns += [
    path('classifications/', views.classification_list, name='classification_list'),
    path('classifications/create', views.classification_create, name='classification_create'),
    path('classifications/<int:pk>', views.classification_view, name='classification_view'),
    path('classifications/<int:pk>/edit', views.classification_edit, name='classification_edit'),
    path('classifications/<int:pk>/delete', views.classification_delete, name='classification_delete'),
]