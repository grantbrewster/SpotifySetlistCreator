# python web scraper
# https://github.com/mileshenrichs/spotify-playlist-generator


import urllib.request
from bs4 import BeautifulSoup

# specify the url

print("what is the page of setlist you want into a playlist?")

url = input()

page = urllib.request.urlopen(url)

soup = BeautifulSoup(page, "html.parser")

print(soup.prettify())