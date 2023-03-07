from dash import dcc,callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output,State
from dash import html
import dash
import spotify,postgres,pandas as pd
from datetime import datetime

dash.register_page(__name__,path='/')

def layout():
    return html.Div([
        dcc.Location(id='url', refresh=True),
        html.Div(id = 'main_content',children=[
            html.Label('Spotify UserName'),
            html.Br(),
            dbc.Input(type = "text",id = 'username_input',style={'margin-top':'15px'}),
            html.Br(),
            dbc.Button("Submit",id = 'username_submit_button',color = 'primary',className='me-2'),
            html.Br(),
            html.Label("Initial Text",id = 'target_label',style={'margin-top':"15px"})
        ],style={'padding-top':'25px',"padding-left":"25px"})
    ])


def check_date(timestamp):
    return datetime.fromisoformat(timestamp[:-1])

def fetch_data(username):

    token = spotify.spotify_init(username)
    
    #Liked songs processed
    songs = spotify.get_liked_songs(token)
    songs_dict = spotify.process_liked_songs(songs)
    df = pd.DataFrame.from_dict(songs_dict)
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


@callback(
    Output('target_label','children'),
    Output('url','pathname'),
    [Input('username_submit_button','n_clicks')],
    [State('username_input','value')]
)
def button_on_clicked(n_clicks,value):

    if value == None:
        return '','/'
    else:
        fetch_data(value)
        return "Loading...",'/tools/{}'.format(value)