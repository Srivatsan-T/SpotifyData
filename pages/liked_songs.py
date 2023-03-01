from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output,State
from dash import html
from dotenv import load_dotenv
import dash
import pandas as pd
from spotify import spotify_init,get_liked_songs
from datetime import datetime


import postgres

load_dotenv()
dash.register_page(__name__,path_template='/liked/<username>')

def check_date(timestamp):
    return datetime.fromisoformat(timestamp[:-1])

def layout(username = None):

    token = spotify_init(username)
    songs = get_liked_songs(token)
    df = pd.DataFrame.from_dict(songs)
    df_display = df.copy()
    postgres.create_liked_songs_table()
    #Check if the table already contains data

    res,flag = postgres.check_liked_songs()
    if flag:
        df['added_at'] = df['added_at'].apply(check_date)
        print(df['added_at'],res)
        df = df[ df['added_at'] > res]    

    songs = list(df.T.to_dict().values())
    postgres.add_liked_songs_dict(songs)

    return html.Div([html.Div([dbc.Button("Back",href='/',className='me-2')]) ,dbc.Table.from_dataframe(df_display,dark = True,striped=True, bordered=True, hover=True, index=True)]) 