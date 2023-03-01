from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output,State
from dash import html
from dotenv import load_dotenv
import dash
import pandas as pd
from spotify import recent_songs,spotify_init,get_liked_songs


load_dotenv()
dash.register_page(__name__,path_template='/liked/<username>')

def layout(username = None):

    token = spotify_init(username)
    songs = get_liked_songs(token)
    df = pd.DataFrame.from_dict(songs)

    return dbc.Table.from_dataframe(df,dark = True,striped=True, bordered=True, hover=True, index=True)