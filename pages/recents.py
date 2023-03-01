from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output,State
from dash import html
from dotenv import load_dotenv
import dash
import pandas as pd
from spotify import recent_songs,spotify_init,get_liked_songs


load_dotenv()
dash.register_page(__name__,path_template='/recents/<username>')

def layout(username = None):

    token = spotify_init(username)
    songs = recent_songs(token)
    df = pd.DataFrame.from_dict(songs)

    return dbc.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in df.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(df.iloc[i][col]) for col in df.columns
            ]) for i in range(len(df))
        ])
    ])

