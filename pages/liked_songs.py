from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import html
from dotenv import load_dotenv
import dash
import pandas as pd
import spotify
from datetime import datetime


load_dotenv()
dash.register_page(__name__, path_template='/liked/<username>')


def layout(username=None):



    return html.Div([])

    return html.Div([
            html.Div(id='left_tab', children=[
            dbc.Button("Liked Songs", className='me-2',
                       color='primary', href=f'/liked/{username}'),
            html.Br(),
            dbc.Button("Recently Played Songs", className='me-2', color='success',
                       href=f'/recents/{username}', style={'margin-top': '25px'}),
            html.Br(),
            dbc.Button("Analytics", color='danger', className='me-2',
                       href=f'/analytics/{username}', style={'margin-top': '25px'}),
            html.Br(),
            dbc.Button("Back", href=f'/tools/{username}', className='me-2',style={'margin-top': '25px'},color = 'info')
        ], style={'padding-top': '25px', "padding-left": "25px"}),

        html.Div([dbc.Table.from_dataframe(df_display, dark=True, striped=True, bordered=True,
                 hover=True, index=True)]) 
    ],style={'display': 'flex', 'flex-direction': 'row'})
