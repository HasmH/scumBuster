from django.urls import path

from . import views

urlpatterns = [
    path('scum', views.home, name='scum'),
    path('search_scum', views.scum_search, name='scum_search')
]