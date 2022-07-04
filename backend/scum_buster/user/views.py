from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from user.models import scumBag
from user.models import report
import keys_and_config.config as config
from . import api
import datetime

#Root Page for Scum Search Functionality 
#It's only responsiblity is to view a search bar to the end user
def home(request):
    return render(request, 'user.html')

#Search Results Page for Scum Search Functionality 
#TODO: Implement taking in steam Id
def search(request):
    if request.method == 'GET':
        search_value = str(request.GET.get('q'))
        result = getScumbagProfileViaWeb(search_value) #deadly function - try to run as little as possible
        for player in result:
            extra_info = getScumbagProfileViaAPI(player['steamId']) 
            player['avatar'] = extra_info['avatar']
            player['number_of_reports'] = int(report.objects.filter(scum_bag=scumBag.objects.filter(steam_id=extra_info['steamid']).first()).count())
        return render(request, 'result.html', {'result':result })

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
        scum_bag = scumBag.objects.filter(steam_id=scum['steamid']).first()
        if scum_bag is None:
            return render(request, 'profile.html', {'scum': result})
        elif scum_bag is not None: 
            report_history = report.objects.filter(scum_bag=scum_bag)
            if report_history is None: 
                return render(request, 'profile.html', {'scum': result})
            else: 
                return render(request, 'profile.html', {'scum': result, 'reports': report_history})

#Downvotes a user and saves their information in a database
#Login Required here 
#Pseudo Code to clean up with javascript:
    #User Clicks on Search Result --> will append either vanityurl or steam id
    #Then user clicks on downvote --> will send either steam id OR the vanityurl's steam id --> leading to url looking botched??
    #So, to fix this... 
    #As Downvote is clicked, do not send either to append to url, url stays same, make ajax request and update the div with info 
    
def downvote(request, steamId):
    if request.method == 'POST':
        report_game = game_enum(str(request.POST.get('game')))
        report_type = report_enum(str(request.POST.get('report_type')))
        time_of_report = datetime.datetime.now()
        if scumBag.objects.filter(steam_id=steamId).first():
            scum_bag = scumBag.objects.filter(steam_id=steamId).first()
            report.objects.create(scum_bag=scum_bag, time_of_report=time_of_report, report_game=report_game, report_type_enum=report_type)
        else: 
            scum_bag = scumBag.objects.create(steam_id=steamId)
            report.objects.create(scum_bag=scum_bag, time_of_report=time_of_report, report_game=report_game,  report_type_enum=report_type)
        return redirect('profile', steamId=steamId)


# -- HELPER FUNCTIONS --# 
# -- (refer to api.py)--# 
def getScumbagProfileViaWeb(searchInput):
    return api.getScumbagProfileViaWeb(searchInput)

#Query API via steamid 
def getScumbagProfileViaAPI(searchInput):
    return api.getScumbagProfileViaAPI(searchInput)

#Grabs the enum value for the game scum is being reported on
def game_enum(value): 
    if value == 'CSGO':
        return report.game.CSGO
    if value == 'TF2':
        return report.game.TF2
    if value == 'CSS':
        return report.game.CSS
    if value == 'GMOD':
        return report.game.GMOD
    if value == 'CS16':
        return report.game.CS16

def report_enum(value): 
    if value == 'TOXIC':
        return report.report_type.TOXIC
    if value == 'CHEATER':
        return report.report_type.CHEATER
#Current Thoughts:
    #Should I check that the logged in user, has the game that they are reporting for? 
        #Doesnt make sense, that if User A, is reporting User B for CS GO, but User A doesnt even fukn own CS GO????
        #So in saying that, should I implement that control measure, for a more integral report system - i.e. your reports MEAN something 
            #they arent just some invisible number that Steam stores, and acts upon bloody 3 years later
    #Control Measure: I dont think User A should be able to report User B for TWO or MORE games in rapid succession (i.e. should be some sort of cooldown timer of reporting! - on a particular player that is, User A can go on to report another guy)
    #Control Measure: One report for a particular game, and particular reporter, per reportee. 
        
