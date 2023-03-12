from dash import dcc,callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output,State
from dash import html
import dash
import pandas as pd
import postgres
import math

dash.register_page(__name__,path_template='/recents/<username>')

def layout(username = None):

    recents = postgres.select_recent_songs(0)

    number_of_recent_songs = len(recents)
    page_size = 50
    number_of_pages = math.ceil(number_of_recent_songs/page_size)

    navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Liked Songs", href=f'http://localhost:8050/liked/{username}',id='LikedSongs')),
        dbc.NavItem(dbc.NavLink("Recents", href=f'http://localhost:8050/recents/{username}',id="Recents",)),
        dbc.NavItem(dbc.NavLink("Analytics", href=f'http://localhost:8050/analytics/{username}',id="Analytics")),
        dbc.NavItem(dbc.NavLink("Back", href=f'http://localhost:8050/tools/{username}',id="Back"))
    ],
    brand="Spotify Analyzer",
    brand_href="http://localhost:8050/",
    className='box-form left'
    )


    return html.Div([
        navbar,
        html.Div([dcc.Slider(id='Pagination',min=1,max=number_of_pages,step=1,value=1,marks={i : str(i) for i in range(1,number_of_pages+1)})],style={'margin':'0 40px'}),
        html.Div(children=[],id='recents_table',style={'margin':'0 40px'}) 
    ],style={})


@callback(
    Output('recents_table','children'),
    [Input('Pagination','value')],
    [State('Pagination','max')]
)
def pages(active_page,max):

    column_names = ['song_id','SONG','ALBUM','ARTISTS','POPULARITY','preview_url']
    
    if active_page == max:
        recent_songs = postgres.select_recent_songs(active_page*50-50)
    else:
        recent_songs = postgres.select_recent_songs(active_page*50-50,active_page*50)

    df = pd.DataFrame(recent_songs,columns=column_names)
    df = df.drop(['song_id','preview_url'],axis=1)
    return dbc.Table.from_dataframe(df, striped=True, bordered=True,hover=True)