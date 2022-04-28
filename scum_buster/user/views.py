from django.http import HttpResponse
from django.shortcuts import render

from user.models import TrustFactor

def player(request, user_id):
    
    #User makes request that looks like www.scumbuster.com/searchuser?user=<whatever_the_cunts_name_is>
    #get user var
    #query steam api with user vi
    #clean out useless info we dont want with steam api json
    #return our version of it 
    return HttpResponse("Hey Scumbag")
