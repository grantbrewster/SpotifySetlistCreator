import requests
from bs4 import BeautifulSoup
import urllib.parse
import datetime
import spotipy
import spotipy.util as util
import setListScraper as scraper


scope = "playlist-modify-private"

# ids

# redirect_uri = "your-redirectURI"
# clientId = "your-clientid"
# clientSecret = "your-clientSecret"

# spotifyUserId = "your-spotifyUserId"

redirect_uri = "your-redirectURI"
clientId = "your-clientid"
clientSecret = "your-clientSecret"

spotifyUserId = "your-spotifyUserId"

spotifyToken = ""

    
# ====================== METHOD DEFINITIONS ========================


def authHeader():
    return {'Authorization': 'Bearer {}'.format(spotifyToken)}

# obtain new Spotify access token using refresh_token
def getNewAccessToken():
    token = util.prompt_for_user_token(spotifyUserId,scope,client_id=clientId,client_secret=clientSecret,redirect_uri=redirect_uri)
    if token:
        return token
    else:
        raise Exception("Can't get token")
    

# return track id from Spotify search endpoint given song title and artists
def findSong(name, artist):
    songId = ''

    queryParams = '?q={}&type=track&limit=5'.format(name)

    r = requests.get('https://api.spotify.com/v1/search' + queryParams, headers=authHeader())
    res = r.json()
    # iterate through results
    for result in res['tracks']['items']:
        trackArtist = result['artists']
        for i in trackArtist:
            if i["name"].lower() == artist:
                songId = result['id']
                return songId
                
    return songId

# returns today's date as simple string (i.e. 10/08, 4/22)
def getTodaysDate():
    todaysDate = datetime.datetime.today().strftime('%m/%d')
    if todaysDate[0] == '0':
        todaysDate = todaysDate[1:]
    return todaysDate


# builds a new playlist on my Spotify account w/ tracks corresponding to provided song ids
def createPlaylist(songIds):
    # initialize playlist

    playlistName = 'SetList for {} Concert'.format(artist)

    reqHeader = {'Authorization': 'Bearer {}'.format(spotifyToken), 'Content-Type': 'application/json'}

    reqBody = {'name': playlistName, 'description': 'new playslit', 'public': False}

    r = requests.post('https://api.spotify.com/v1/users/{}/playlists'.format(spotifyUserId), headers=reqHeader, json=reqBody)
    
    if r.status_code in [200, 201]:
        newPlaylistId = r.json()['id']
    
    # add tracks to playlist
    addTracksToPlaylist(newPlaylistId, playlistName, songIds)

# place tracks with given ids into Spotify playlist with given id and name
def addTracksToPlaylist(playlistId, playlistName, songIds):
    # get user id (used in request)

    userId = spotifyUserId

    # send request to add tracks to Spotify playlist
    reqHeader = {'Authorization': 'Bearer {}'.format(spotifyToken), 'Content-Type': 'application/json'}
    reqBody = {'uris': list(map((lambda songId: 'spotify:track:' + songId), songIds))}

    r = requests.post('https://api.spotify.com/v1/users/{}/playlists/{}/tracks'.format(userId, playlistId), 
            headers=reqHeader, json=reqBody)


# ====================== BEGIN SCRIPT ========================


# first, test current access token
# testRequest = requests.get('https://api.spotify.com/v1/me', headers=authHeader())
# # if unauthorized, need to refresh access token
# if testRequest.status_code in [401, 403]:
#     spotifyToken = getNewAccessToken()

print ("what is your spotify userId? It is the numbers following when you share your account page. For example : https://open.spotify.com/user/1222222222?xxxxx. Then 1222222222 is your id")
spotifyUserId = input()

spotifyToken = getNewAccessToken()

# song candidates are songs to be added to playlist if
# 1) they are on Spotify and
# 2) they haven't already been added to current/prev playlist
songCandidates = scraper.getSongNames()

artist = scraper.artist.lower()

# define song ids to add list
songIdsToAdd = []

for candidate in songCandidates:
    # make sure song hasn't already been added to previous playlist
    # find song id on Spotify via search endpoint
    songId = findSong(candidate, artist)
    if songId:
        songIdsToAdd.append(songId)


dayOfWeek = int(datetime.datetime.today().strftime('%u'))


createPlaylist(list(set(songIdsToAdd)))
