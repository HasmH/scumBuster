from django.http import HttpResponse
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from user.models import TrustFactor
import secrets.config as config

def player(request, user_id):
    
    #User makes request that looks like www.scumbuster.com/searchuser?user=<whatever_the_cunts_name_is>
    #get user var
    #query steam api with user vi
    #clean out useless info we dont want with steam api json
    #return our version of it 
    return HttpResponse(user_id)


#Helper Functions 

#Web Scrape Steam Search Functionality - since we cannot query API via displayName
def getScumbagProfileViaWeb(searchInput):
    URL = "https://steamcommunity.com/search/users/#text=" + str(searchInput)
    #Testing Purposes Only: Looks like we'll need to install a webdriver on hostmachine if this goes live 
    #Please download appropirate version for your local machine: https://chromedriver.chromium.org/downloads
    driver = webdriver.Chrome(config.webdriver_path)
    driver.get(URL)
    page = requests.get(url=URL)

    #Allow page to fully render
    sleep(5)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    searchRow = soup.find_all("div", class_="search_row")
    result = []
    for info in searchRow:
        data = info.find("div", class_="searchPersonaInfo").find("a", class_="searchPersonaName")
        profileLink = data.get("href")
        displayName = data.text
        finalInfo = {"displayName":displayName, "profileLink":profileLink}
        result.append(finalInfo)
    #print(result)
    return result

#Query API via steamid 
def getScumbagProfileViaAPI(searchInput):
    #API Docs: https://developer.valvesoftware.com/wiki/Steam_Web_API#GetPlayerSummaries_.28v0001.29
    profileLink = getScumbagProfileViaWeb(searchInput)[0]["profileLink"]
    steamId = str(profileLink)[30:]
    
    #if custom steam id (i.e. not a 64bit number) --> use ResolveVanityURL
    if steamId.isdigit() == False:
        API_QUERY = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=" + config.api_key + "&vanityurl=" + steamId
    #if steam id is normal (i.e. 64bit number) --> use GetPlayerSummaries api
    if steamId.isdigit() == True and int(steamId).bit_length() <= 63:
        API_QUERY = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + config.api_key + "&steamids=" + steamId
    r = requests.get(API_QUERY)
    #print(r.json())
    return r.json()
    
