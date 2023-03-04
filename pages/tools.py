import dash
from dash import html,dcc
import dash_bootstrap_components as dbc
import spotify
import pandas as pd
import postgres
from datetime import datetime

dash.register_page(__name__,path_template='/tools/<username>')

def check_date(timestamp):
    return datetime.fromisoformat(timestamp[:-1])

def layout(username = None):

    token = spotify.spotify_init(username)
    
    #Liked songs processed
    songs = spotify.get_liked_songs(token)
    songs_dict = spotify.process_liked_songs(songs)
    df = pd.DataFrame.from_dict(songs_dict)
    df_display = df.copy()
    postgres.create_liked_songs_table()

    res, flag = postgres.check_liked_songs()
    if flag:
        df['added_at'] = df['added_at'].apply(check_date)
        df = df[df['added_at'] > res]

    songs_dict= list(df.T.to_dict().values())
    postgres.add_liked_songs_dict(songs_dict)

    #Artists processed
    artist_ids_spotify = []

    for i in songs_dict:
        artist_ids_spotify.append(i['artists'])
    artist_ids_spotify = list(set(artist_ids_spotify))
    artists = spotify.get_artists(token,artist_ids_spotify)

    postgres.create_artist_table()
    artist_ids_tuple = postgres.select_unique_artists()
    artist_ids = []
    for i in artist_ids_tuple:
        artist_ids.append(i[0])
    
    new_artists = []
    for artist in artists:
        if artist['id'] not in artist_ids:
            new_artists.append(artist)

    artists = new_artists.copy()
    artists = spotify.process_artists(artists)
    postgres.add_artists_dict(artists) 
    
    #Albums processed
    album_ids_spotify = []

    for i in songs_dict:
        album_ids_spotify.append(i['album'])
    album_ids_spotify = list(set(album_ids_spotify))
    albums = spotify.get_albums(token,album_ids_spotify)
    #print(albums[0:2])
    postgres.create_album_table()
    album_ids_tuple = postgres.select_unique_albums()
    album_ids = []
    for i in album_ids_tuple:
        album_ids.append(i[0])
    
    new_albums = []
    for album in albums:
        if album['id'] not in album_ids:
            new_albums.append(album)

    albums = new_albums.copy()
    albums = spotify.process_albums(albums)
    #print(albums[0:2])
    postgres.add_albums_dict(albums)

    return html.Div([
        html.Div(id = 'left_tab',children=[
            dbc.Button("Liked Songs",className='me-2',color='primary',href = f'/liked/{username}'),
            html.Br(),
            dbc.Button("Recently Played Songs",className='me-2',color='success',href = f'/recents/{username}',style={'margin-top' : '25px'}),
            html.Br(),
            dbc.Button("Analytics",color = 'danger',className='me-2',href = f'/analytics/{username}',style={'margin-top' : '25px'}),
            html.Br()
        ],style={'padding-top':'25px',"padding-left":"25px"}),
        html.Div([html.Label("Select the feature to use")],style={"padding-left":"25px","padding-top":'90px'})
    ],style={'display': 'flex', 'flex-direction': 'row'})    