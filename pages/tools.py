import dash
from dash import html,dcc
import dash_bootstrap_components as dbc




dash.register_page(__name__,path_template='/tools/<username>')

def layout(username = None):

    return html.Div([
        html.Div(id = 'left_tab',children=[
            dbc.Button("Liked Songs",className='me-2',color='primary',href = f'/liked/{username}'),
            html.Br(),
            dbc.Button("Recently Played Songs",className='me-2',color='success',href = f'/recents/{username}',style={'margin-top' : '25px'}),
            html.Br(),
            dbc.Button("Analytics",color = 'danger',className='me-2',href = f'/analytics/{username}',style={'margin-top' : '25px'}),
            html.Br(),
            dbc.Button("Back", href='/', className='me-2',style={'margin-top': '25px'},color = 'info')
        ],style={'padding-top':'25px',"padding-left":"25px"}),
        html.Div([html.Label("Select the feature to use")],style={"padding-left":"25px","padding-top":'90px'})
    ],style={'display': 'flex', 'flex-direction': 'row'})    