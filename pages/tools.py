import dash
from dash import html,callback,Output,Input
import dash_bootstrap_components as dbc




dash.register_page(__name__,path_template='/tools/<username>')

def layout(username = None):

    navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Liked Songs", href='#',id='LikedSongs')),
        dbc.NavItem(dbc.NavLink("Recents", href="#",id="Recents")),
        dbc.NavItem(dbc.NavLink("Analytics", href="#",id="Analytics")),
        dbc.NavItem(dbc.NavLink("Back", href="#",id="Back"))
    ],
    brand="Spotify Analyzer",
    brand_href="#",
    #style={'margin-bottom': '50px','background-image':'url("https://i.pinimg.com/736x/5d/73/ea/5d73eaabb25e3805de1f8cdea7df4a42--tumblr-backgrounds-iphone-phone-wallpapers-iphone-wallaper-tumblr.jpg")','background-color':'#3b5998'},
    id='NaviBar',
    className='box-form left'
    )

    first_name = str(username).split('%20')[0]

    return html.Div([navbar,
        html.Div([html.H1("Hello",style={'font-size':'10vmax','color':'white'}), 
                  html.H1(first_name ,style={'font-size':'10vmax','color':'white'}),
                  html.H5("use the navigation links to access various features of the tool",style={'color':'white'})]
                  ,style={"padding-left":"25px","padding-top":'10px'})
    ],style={'width':'100vw'})    
