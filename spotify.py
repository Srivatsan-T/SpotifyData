import spotipy
import pandas as pd
import os
from dotenv import load_dotenv


load_dotenv()

username = 	"Srivatsan Thiruvengadam"
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = 'http://localhost:7777/callback'
scope = 'user-read-recently-played user-library-read'


#Gets spotify data for recent songs and returns a dictionary
def spotify_init(spotify_username):
    #username = input("Enter your Spotify username ")
    token = spotipy.util.prompt_for_user_token(username=spotify_username, 
                                    scope=scope, 
                                    client_id=client_id,   
                                    client_secret=client_secret,     
                                    redirect_uri=redirect_uri)
    return token


def recent_songs(token):
    sp = spotipy.Spotify(token)
    user_recent = sp.current_user_recently_played(limit = 50)
    number_of_songs = len(user_recent['items'])
    songs = []
    for i in range(number_of_songs):
        temp_dict = {}
        temp_dict['song_id'] = user_recent['items'][i]['track']['id']
        temp_dict['song_name'] = user_recent['items'][i]['track']['name']
        temp_dict['played_at'] = user_recent['items'][i]['played_at']
        songs.append(temp_dict)
    return songs

def get_liked_songs(token):
    sp = spotipy.Spotify(token)
    lim = 50
    off =  0
    songs = []
    next = 'not none'
    while next is not None:
        liked_songs = sp.current_user_saved_tracks(offset=off,limit=lim)
        number_of_songs = len(liked_songs['items'])
        for i in range(number_of_songs):
            temp_dict = {}
            temp_dict['song_id'] = liked_songs['items'][i]['track']['id']
            temp_dict['song_name'] = liked_songs['items'][i]['track']['name']
            temp_dict['added_at'] = liked_songs['items'][i]['added_at']
            temp_dict['album'] = liked_songs['items'][i]['track']['album']['name']
            songs.append(temp_dict)
        off = off + lim
        next = liked_songs['next']
    return songs

'''
token = spotify_init("Srivatsan Thiruvengadam")
b = get_liked_songs(token)
print(len(b))
'''