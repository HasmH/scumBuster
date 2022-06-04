from django.http import HttpResponse
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from user.models import scumBag
import keys_and_config.config as config
from . import api

#Root Page for Scum Search Functionality 
#It's only responsiblity is to view a search bar to the end user
def home(request):
    return render(request, 'user.html')

#Search Results Page for Scum Search Functionality 
#Takes in Display Name
#TODO: Implement taking in steam Id
def search(request):
    if request.method == 'GET':
        search_value = str(request.GET.get('q'))
        result = getScumbagProfileViaWeb(search_value) 
        return render(request, 'result.html', {'result':result})

#Confirms End Users search result, and redirects to a profile page where they can downvote to impact trustworthy factor 
def profile(request, steamId):
    if request.method == 'GET':
        scum = getScumbagProfileViaAPI(steamId)
        #Here we decide - what information we want from API: 
        result = {
            'steamid': scum['steamid'],
            'personaname': scum['personaname'],
            'profileurl': scum['profileurl'],
            'avatar': scum['avatar']
        }
        return render(request, 'profile.html', {'scum': result })

#Downvotes a user and saves their information in a database
def downvote(request, steamId):
    print(steamId)
    if request.method == 'POST':
        new_scum = scumBag.objects.create(steam_id=steamId, number_of_reports=1)
        return render(request, 'test.html', {'scum':new_scum })
    else: 
        return render(request, 'test.html')    

# -- HELPER FUNCTIONS --# 
# -- (refer to api.py)--# 
def getScumbagProfileViaWeb(searchInput):
    return api.getScumbagProfileViaWeb(searchInput)

#Query API via steamid 
def getScumbagProfileViaAPI(searchInput):
    return api.getScumbagProfileViaAPI(searchInput)


#Current Thoughts:
    #Should I check that the logged in user, has the game that they are reporting for? 
        #Doesnt make sense, that if User A, is reporting User B for CS GO, but User A doesnt even fukn own CS GO????
        #So in saying that, should I implement that control measure, for a more integral report system - i.e. your reports MEAN something 
            #they arent just some invisible number that Steam stores, and acts upon bloody 3 years later
    #Control Measure: I dont think User A should be able to report User B for TWO or MORE games in rapid succession (i.e. should be some sort of cooldown timer of reporting! - on a particular player that is, User A can go on to report another guy)
    #Control Measure: One report for a particular game, and particular reporter, per reportee. 
        
