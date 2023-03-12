# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html
import dash_bootstrap_components as dbc
import dash

app = Dash(__name__, external_stylesheets=[
           dbc.themes.BOOTSTRAP], use_pages=True)

app.layout = html.Div([dash.page_container])

if __name__ == '__main__':
    app.run_server(debug=True)
