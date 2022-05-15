from django.urls import path

from . import views

urlpatterns = [
    path('scum', views.home, name='scum'),
    path('scum_search', views.scum_search, name='scum_search'),
    path('scum_profile/<str:steamId>', views.scum_profile, name='scum_profile')
]