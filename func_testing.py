from urllib.request import urlopen
from django.http import HttpResponse
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import scum_buster.keys_and_config.config as config
from urllib.request import Request, urlopen
#Helper Functions 

#Web Scrape Steam Search Functionality - since we cannot query API via displayName
def getScumbagProfileViaWeb(searchInput):
    URL = "https://steamcommunity.com/search/users/#text=" + str(searchInput)
    #Testing Purposes Only: Looks like we'll need to install a webdriver on hostmachine if this goes live 
    #Please download appropirate version for your local machine: https://chromedriver.chromium.org/downloads
    driver = webdriver.Chrome(config.webdriver_path)
    driver.get(URL)
    #TODO: Add pagination 
    #Allow page to fully render
    sleep(5)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    searchRow = soup.find_all("div", class_="search_row")
    result = []
    for info in searchRow:
        data = info.find("div", class_="searchPersonaInfo").find("a", class_="searchPersonaName")
        profileLink = data.get("href")
        displayName = data.text
        #URL Looks different depending on whether they have custom steamId or default steamId
        if 'profiles' in profileLink:
            steamId =  str(profileLink).removeprefix('https://steamcommunity.com/profiles/')
        else: 
            steamId = str(profileLink).removeprefix('https://steamcommunity.com/id/')
        finalInfo = {"displayName":displayName, "profileLink":profileLink, "steamId":steamId}
        result.append(finalInfo)
    return result

def getScumBagProfileViaWebOptimized(search, page_number):
    cookies = get_cookies()
    URL = "https://steamcommunity.com/search/SearchCommunityAjax?text=hasm&filter=users&"+ "sessionid=" + cookies['sessionid'] + "&steamid_user=false" + "&page=" + str(page_number)
    r = requests.get(URL, cookies=cookies)
    soup = BeautifulSoup(r.json()['html'], "html.parser")
    search_row = soup.find_all("div", class_="search_row")
    result = []
    for info in search_row:
        data = info.find("div", class_="searchPersonaInfo").find("a", class_="searchPersonaName")
        profileLink = data.get("href")
        displayName = data.text
        #URL Looks different depending on whether they have custom steamId or default steamId
        if 'profiles' in profileLink:
            steamId =  str(profileLink).removeprefix('https://steamcommunity.com/profiles/')
        else: 
            steamId = str(profileLink).removeprefix('https://steamcommunity.com/id/')
        finalInfo = {"displayName":displayName, "profileLink":profileLink, "steamId":steamId}
        result.append(finalInfo)
    return result

def get_cookies():
    URL = 'https://steamcommunity.com/search/users/'
    r = requests.get(URL)
    #print(r.cookies)
    return r.cookies
#Query API via steamid 
def getScumbagProfileViaAPI(searchInput):
    #API Docs: https://developer.valvesoftware.com/wiki/Steam_Web_API#GetPlayerSummaries_.28v0001.29
    steamId = str(searchInput)
    #if steam id is normal (i.e. 64bit number) --> use GetPlayerSummaries ap
    if steamId.isdigit() == True and int(steamId).bit_length() <= 63 and len(steamId) == 17:
        API_QUERY = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + config.api_key + "&steamids=" + steamId
        r = requests.get(API_QUERY)
        result = r.json()['response']['players'][0]
    #otherwise, its a custom id i.e. not a 64 bit number, 17 digits long --> use ResolveVanityURL
    else:
        #need to use the /id/customsteamid thing here.. passing in display name does NOT work here
        API_QUERY = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=" + config.api_key + "&vanityurl=" + steamId
        r = requests.get(API_QUERY)
        temp = r.json()['response']
        print(temp)
        #pass result['steamid'] --> other api 
        r = requests.get("https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + config.api_key + "&steamids=" + temp['steamid'])
        result = r.json()['response']['players'][0]
    return result

if __name__ == "__main__":
   #print(getScumbagProfileViaWeb("hasm"))
    #print(getScumbagProfileViaAPI("hasm"))
    print(getScumBagProfileViaWebOptimized('hasm', 1))
    #get_cookies()
