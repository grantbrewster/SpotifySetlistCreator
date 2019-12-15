# python web scraper
# https://github.com/mileshenrichs/spotify-playlist-generator

import urllib.request
from bs4 import BeautifulSoup

artist = ""

def getSongNames(): 
# specify the url
    names = []

    print("what is the page of setlist you want into a playlist? Must be from setlist.fm")

    url = input()

    page = urllib.request.urlopen(url)

    soup = BeautifulSoup(page, "html.parser")

    song_containers = soup.find_all('li', class_ = 'setlistParts song')

    for container in song_containers:
        if container.find('div', class_ = 'songPart') is not None:
            name = container.a.text
            names.append(name)
    global artist
    artist = getArtist(soup)
    return names

def getArtist(soup): 
# specify the url
    artist = ""
    artistContainers = soup.find_all('div', class_ = 'setlistHeadline')
    artist = artistContainers[0].h1.strong.span.a.text
    if (artist == "") :
        artist = artist = artistContainers[0].h1.strong.span.a.span
    
    return artist

