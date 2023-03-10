# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html

import dash_bootstrap_components as dbc
import dash

external_stylesheets = [
    "https://fonts.googleapis.com/css?family=Open+Sans",
    {
        'href': "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
        'rel': 'stylesheet',
        'integrity': 'sha384-wvfXpqpZZVQGK6TAh5PVlGOfQNHSoD2xbE+QkPxCAFlNEevoEH3Sl0sibVcOQVnN',
        'crossorigin': "anonymous"
    }
]

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Liked Songs", href='#',id='LikedSongs')),
        dbc.NavItem(dbc.NavLink("Recents", href="#",id="Recents")),
        dbc.NavItem(dbc.NavLink("Analytics", href="#",id="Analytics")),
        dbc.NavItem(dbc.NavLink("Back", href="#",id="Back"))
    ],
    brand="Spotify Analyzer",
    brand_href="#",
    color="primary",
    dark=True,
    style={'margin-bottom': '50px','background-image':'linear-gradient(135deg, #FAB2FF 10%, #1904E5 100%)'},
    id='NaviBar'
)

app = Dash(__name__, external_stylesheets=[
           dbc.themes.BOOTSTRAP], use_pages=True)

app.layout = html.Div([dash.page_container])


if __name__ == '__main__':
    app.run_server(debug=True)
