from dash import dcc,callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output
from dash import html
import dash
import pandas as pd
import postgres

dash.register_page(__name__,path_template='/analytics/<username>')

def layout(username = None):

    years  = list(postgres.get_years())

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
        html.Div([dcc.Dropdown([year[0] for year in years],placeholder='Select year',id='year_drop')],style={'margin':'0 500px',"padding-top":'20px'}),
        html.Div(children = [],id='target_div',style={'margin':'30px 200px'}) 
    ])

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

        df = pd.DataFrame(albums,columns=['ALBUM','SONGS COUNT'])

        result = [html.H2("Your top 3 albums from that year are",style = {'color':'white','border-style':'solid','text-align':'center'}),
             dbc.Table.from_dataframe(df, striped=True, bordered=True,hover=True, 
                                      index=False,style = {'padding-top':'45px','text-align':'center'}),
             most_popular,
             least_popular
            ]
        
        return result
    else:
        return [html.H1("Choose a year from the dropdown to see results",style = {'border-style':'solid','font-size':'7vmax','color':'white','text-align':'center'})]