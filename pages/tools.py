import dash
from dash import html
import dash_bootstrap_components as dbc


dash.register_page(__name__,path_template='/tools/<username>')

def layout(username = None):

    navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Liked Songs", href=f'http://localhost:8050/liked/{username}',id='LikedSongs')),
        dbc.NavItem(dbc.NavLink("Recents", href=f'http://localhost:8050/recents/{username}',id="Recents",)),
        dbc.NavItem(dbc.NavLink("Analytics", href=f'http://localhost:8050/analytics/{username}',id="Analytics"))
    ],
    brand="Spotify Analyzer",
    brand_href="http://localhost:8050/",
    className='box-form left'
    )

    first_name = str(username).split('%20')[0]

    return html.Div([navbar,
        html.Div([html.H1("Hello",style={'font-size':'10vmax','color':'white'}), 
                  html.H1(first_name ,style={'font-size':'10vmax','color':'white'}),
                  html.H5("use the navigation links to access various features of the tool",style={'color':'white'})]
                  ,style={"padding-left":"25px","padding-top":'10px'})
    ],style={'width':'100vw'})    
