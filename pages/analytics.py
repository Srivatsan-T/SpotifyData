from dash import dcc,callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output,State
from dash import html
import dash
import pandas as pd
import postgres

dash.register_page(__name__,path_template='/analytics/<username>')

def layout(username = None):

    #Get all years for the given liked songs
    #Add a drop-down with all such years
    #Once you click the year, give analytics for such year

    years  = list(postgres.get_years())

    return html.Div([ 
    html.Div([

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
        ], style={'padding-top': '25px', "padding-left": "25px",'outline-style':'solid','width':'300px'}),
        html.Div([dcc.Dropdown([year[0] for year in years],placeholder='Select year',id='year_drop')],style={'margin-left':'25px',"padding-top":'20px','width':'300px','outline-style':'solid'}),
    ],style={'display': 'flex', 'flex-direction': 'row'}),html.Div(children = [],id='target_div',style={'outline-style':'solid','margin-left':'25px','margin-top':'25px'}) ])

@callback(
    Output('target_div','children'),
    [Input('year_drop','value')]
)

def analytics_display(value):
    if value is not None:
        albums = postgres.get_albums_for_year(value)
        most_pop_list = []
        most_names_list = []
        most_populars = postgres.get_popular_for_year(value,'desc')
        for i in range(1,13):
            most_pop_list.append(0)
            most_names_list.append('NONE')
            for j in most_populars:
                if j[4] == i:
                    most_pop_list[i-1] = j[2]*10 + 100
                    most_names_list[i-1] = j[0]

        most_popular = dcc.Graph(
            figure= {'data': [ {'x': [i for i in range(1,13)],'type':'bar','y':most_pop_list,'text':most_names_list} ] ,'layout':{'title':'Most Popular Songs Graph'}}
        )

        least_pop_list = []
        least_names_list = []
        least_populars = postgres.get_popular_for_year(value,'asc')
        for i in range(1,13):
            least_pop_list.append(0)
            least_names_list.append('NONE')
            for j in least_populars:
                if j[4] == i:
                    least_pop_list[i-1] = j[2]*10 + 100
                    least_names_list[i-1] = j[0]
        
        least_popular = dcc.Graph(
            figure= {'data': [ {'x': [i for i in range(1,13)],'type':'bar','y':least_pop_list,'text':least_names_list} ] ,'layout':{'title':'Least Popular Songs Graph'}}
        )

        df = pd.DataFrame(albums,columns=['Album','Number of Songs'])
        a = [html.Label("Your top 3 albums from that year are",style = {'padding-top':'20px','margin-bottom':'20px','padding-left':'100px'}),dbc.Table.from_dataframe(df, dark=True, striped=True, bordered=True,
                    hover=True, index=False,style = {'padding-top':'45px'}),most_popular,least_popular]
        return a
    else:
        return [html.Label("Make a selection from dropdown",style = {'padding-top':'20px'})]