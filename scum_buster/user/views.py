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
def scum_search(request):
    if request.method == 'GET':
        search_value = str(request.GET.get('search_value'))
        result = getScumbagProfileViaWeb(search_value) 
        return render(request, 'result.html', {'result':result})

#Confirms End Users search result, and redirects to a profile page where they can downvote to impact trustworthy factor 
def scum_profile(request, steamId):
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
def scum_downvote(request, steamId):
    print(steamId)
    if request.method == 'POST':
        new_scum = scumBag.objects.create(steam_id=steamId, number_of_reports=1)
        return render(request, 'profile.html', {'scum':new_scum })
    else: 
        return render(request, 'profile.html')
    #First need to check: does the user already exist in the database? --> If so, display current information 
        #Display Downvote Button
        #Display Trust Factor/Number of Reports 

    #else If user does not exist in database.. --> Once player clicks on downvote, save their information (model) to db     



#Helper Functions in api.py
#Web Scrape Steam Search Functionality - since we cannot query API via displayName
def getScumbagProfileViaWeb(searchInput):
    return api.getScumbagProfileViaWeb(searchInput)

#Query API via steamid 
def getScumbagProfileViaAPI(searchInput):
    return api.getScumbagProfileViaAPI(searchInput)
        
