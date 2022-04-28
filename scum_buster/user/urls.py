from django.urls import path

from . import views

urlpatterns = [
    path('', views.player, name='index'),
    path('<str:user_id>', views.player, name='user_id')
]