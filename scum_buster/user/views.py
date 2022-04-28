from django.http import HttpResponse
from django.shortcuts import render

from user.models import TrustFactor

def player(request):
    return HttpResponse("Hey Scumbag")
