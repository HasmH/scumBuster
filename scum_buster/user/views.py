from django.http import HttpResponse
from django.shortcuts import render

from user.models import TrustFactor

def player(request, player_id):
    player = TrustFactor.objects.get(player_id=player_id)
    return HttpResponse("Player: %s." % player.player_id)

def reports(request, player_id):
    player = TrustFactor.objects.get(player_id=player_id)
    reports = "Reported this many times: %s."
    return HttpResponse(reports % player.number_of_reports)

def trust(request, player_id):
    player = TrustFactor.objects.get(player_id=player_id)
    return HttpResponse("Are they trustworthy? %s." % player.trust_factor)
