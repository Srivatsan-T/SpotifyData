from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output,State
from dash import html
from dotenv import load_dotenv
import dash
import pandas as pd
from spotify import spotify_init,get_liked_songs
from datetime import datetime
import re

import postgres

load_dotenv()
dash.register_page(__name__,path_template='/liked/<username>')

def check_date(timestamp):
    return datetime.strptime(timestamp,"%Y-%m-%dT%H:%M:%SZ")

def layout(username = None):

    token = spotify_init(username)
    songs = get_liked_songs(token)
    df = pd.DataFrame.from_dict(songs)
    postgres.create_liked_songs_table()
    #Check if the table already contains data

    res,flag = postgres.check_liked_songs()
    if flag:
        #df['added_at'].apply(check_date)
        #df = df[ df['added_at'] > res]    
        pass

    songs = list(df.T.to_dict().values())
    print(type(songs))
    postgres.add_liked_songs_dict(songs)

    return dbc.Table.from_dataframe(df,dark = True,striped=True, bordered=True, hover=True, index=True)