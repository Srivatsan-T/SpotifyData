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
        for i in liked_songs['items']:
            songs.append(i)
        off = off + lim
        next = liked_songs['next']
    return songs

def process_liked_songs(liked_songs):
    number_of_songs = len(liked_songs)
    songs_dict = []
    for i in range(number_of_songs):
        temp_dict = {}
        temp_dict['song_id'] = liked_songs[i]['track']['id']
        temp_dict['song_name'] = liked_songs[i]['track']['name']
        temp_dict['added_at'] = liked_songs[i]['added_at']
        temp_dict['album'] = liked_songs[i]['track']['album']['id']
        temp_dict['popularity'] = liked_songs[i]['track']['popularity']
        temp_dict['preview_url'] = liked_songs[i]['track']['preview_url']
        temp_dict['duration_ms'] = liked_songs[i]['track']['duration_ms']

        for artist in liked_songs[i]['track']['artists']:
            temp_dict['artists'] = artist['id']
            songs_dict.append(temp_dict.copy())

    return songs_dict

def process_albums(liked_songs):
    number_of_songs = len(liked_songs)
    album_dict = []
    for i in range(number_of_songs):
        temp_dict = {}
        temp_dict['album_id'] = liked_songs[i]['album']['id']
        temp_dict['album_name'] = liked_songs[i]['album']['name']
        temp_dict['popularity'] = liked_songs[i]['album']['popularity']
        temp_dict['followers'] = liked_songs[i]['artists']['followers']['total']

        for genre in liked_songs[i]['album']['genres']:
            temp_dict['genres'] = genre
            album_dict.append(temp_dict.copy())
        for artist in liked_songs[i]['album']['artists']:
            temp_dict['artists'] = artist
            album_dict.append(temp_dict.copy())

    return album_dict