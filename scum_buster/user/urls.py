from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='scum'),
    path('search', views.search, name='search'),
    path('profile/<str:steamId>', views.profile, name='profile'),
    path('downvote/<str:steamId>', views.downvote, name='downvote')
]