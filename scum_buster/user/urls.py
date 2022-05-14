from django.urls import path

from . import views

urlpatterns = [
    path('scum', views.home, name='scum'),
    path('scum_search', views.scum_search, name='scum_search')
]