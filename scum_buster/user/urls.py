from django.urls import path

from . import views

urlpatterns = [
    path('', views.userSearch, name='index'),
    path('userSearch/<str:steamId>', views.userSearch, name='steamId-search')
]