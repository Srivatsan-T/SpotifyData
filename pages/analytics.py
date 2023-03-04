from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output,State
from dash import html
import dash
import pandas as pd

dash.register_page(__name__,path_template='/analytics/<username>')

def layout(username = None):

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
            dbc.Button("Back", href=f'/tools/{username}', className='me-2',style={'margin-top': '25px'},color='info')
        ], style={'padding-top': '25px', "padding-left": "25px"}),
        html.Div([])
    ],style={'display': 'flex', 'flex-direction': 'row'})
