import dash
from dash import html,dcc
import dash_bootstrap_components as dbc
import spotify
import pandas as pd
import postgres
import datetime

dash.register_page(__name__,path_template='/tools/<username>')

def check_date(timestamp):
    return datetime.fromisoformat(timestamp[:-1])


def layout(username = None):

    token = spotify.spotify_init(username)
    songs = spotify.get_liked_songs(token)

    #Liked songs processed

    songs_dict = spotify.process_liked_songs(songs)
    df = pd.DataFrame.from_dict(songs_dict)
    df_display = df.copy()
    postgres.create_liked_songs_table()

    res, flag = postgres.check_liked_songs()
    if flag:
        df['added_at'] = df['added_at'].apply(check_date)
        df = df[df['added_at'] > res]

    songs = list(df.T.to_dict().values())
    postgres.add_liked_songs_dict(songs)

    #Artists processed
    
    
    #Albums processed

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