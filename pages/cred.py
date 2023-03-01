from dash import dcc,callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output,State
from dash import html
import dash

dash.register_page(__name__,path='/')

def layout():
    return html.Div([
        dcc.Location(id='url', refresh=True),
        html.Div(id = 'main_content',children=[
            html.Label('Spotify UserName'),
            dbc.Input(type = "text",id = 'username_input'),
            html.Br(),
            dbc.Button("Submit",id = 'username_submit_button',color = 'primary',className='me-2'),
            html.Br(),
            html.Label("Initial Text",id = 'target_label')
        ])
    ])

@callback(
    Output('target_label','children'),
    Output('url','pathname'),
    [Input('username_submit_button','n_clicks')],
    [State('username_input','value')]
)
def button_on_clicked(n_clicks,value):
    if value == None:
        return '','/'
    else:
        return "Loading...",'/liked/{}'.format(value)