from dash import Dash
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc

data = pd.read_csv("air4thai_08t_2024-02-27_2024-02-27.csv")
data.sort_values("DATETIMEDATA",inplace=True)
data[['Date', 'Time']] = data['DATETIMEDATA'].str.split(expand=True)


app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY,'/assets/styles.css'],
                suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                            )
#----------------------------------------navbar-----------------------------------------------
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="home")),
        dbc.NavItem(dbc.NavLink("New Page", href="/new-page")),  # Link to the new page
        dbc.NavItem(dbc.NavLink("Contact", href="#")),
    ],
    brand=dbc.NavbarBrand(
        children=[
            html.Img(src='/assets/logo.png', height='60px'),
            html.Span("PM.2.5", className="m1-2")
        ],
        href='#',
    ),
    brand_href="#",
    color="light",
    dark=False,
    style={'height': '100px','border-top': '5px solid #17B897'},
    className='navbar-shadow'
)
#-----------------------------------------home-------------------------------------------------
home_layout = html.Div(
    children=[
        navbar,
        html.Div(
            children=[
                html.Div(
                    children=[
                            html.Div(children="Select Station", className="menu-title"),
                        dcc.Dropdown(
                            id="station-filter",
                            options=[
                                {"label": station, "value": station}
                                for station in np.sort(data.stationID.unique())
                            ],
                            value="02t",
                            clearable=False,
                            className="dropdown",
                            style={'text-align': 'center','backgroundColor':'#B1FEEE'}
                        )
                    ],
                    className="select_station",
                    style={'display': 'inline-block'}
                    
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Date",
                            className="menu-title",
                            style={'text-align': 'center'}
                            ),
                        dcc.Dropdown(
                            id="date-filter",
                            options=[
                                {"label":date , 'value':date }
                                for date in np.sort(data.Date.unique())
                            ],
                            value="2024-02-27",
                            clearable=False,
                            className="dropdown",
                            style={'text-align': 'center','backgroundColor':'#B1FEEE'}
                        )
                    ],
                    className="date",
                    style={'display': 'inline-block',}
                ),
#-----------------------------------graph 1----------------------------------------------------------
                html.Div(
                    html.Div(
                        children=dcc.Graph(
                            id="pm25-chart1", config={"displayModeBar": True},
                            style={'border': '5px solid #17B89','height' :'400px','width' : '800px','margin': 'auto'}, 
                        ),
                        className="card",
                    ),style={'height' :'450px','width' : '1000px','margin': 'auto','backgroundColor' :'#F4F4F4'}
    )
    ],
    className="menu",
    style={'text-align': 'right','color':'#17B897','backgroundColor':'#F4F4F4','height':'550px'}
    
    ),
    html.Footer([
        html.Br(),
        html.P("PM2.5",style='font-size : 8px'),
    ],style={'height': '200px'}
    )

],style={'backgroundColor':'#F4F4F4'},)
#---------------------------------func chart 1---------------------------
@app.callback(
        Output('pm25-chart1','figure'),
        [Input('station-filter','value'),
        Input('date-filter','value')]
)
def update_chart(stationID,Date):
    mask = (
        (data.stationID == stationID)&
        (data.Date == Date)
    )
    filtered_data = data.loc[mask, :]
    pm25_figure = {
        "data": [
                {
                "x": filtered_data["DATETIMEDATA"],
                "y": filtered_data["PM25"],
                "type": "lines",
                "hovertemplate": "%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": f'Graph of Station: {stationID}',
                "x": 0.5,
                "xanchor": "center",
                "font": {"family": "Truculenta", "size": 24, "color": "#333"},
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#17B897"],
            
        },
    }
    return pm25_figure
# @app.callback(
        
# )
# def update_chart2():
#     pass

#-----------------------------------------------new page---------------------------------------------
new_page_layout = html.Div(
    children=[
        navbar,
        html.H1("This is the New Page!"),
        ]
)
#-----------------------------------------------new page2---------------------------------------------
new_page_layout2 = html.Div(
    children=[
        navbar,
        html.H1("This is the New Page!2"),
        ]
)
#----------------------------------------------app----------------------------------------------------
icon_path = 'logo.png'
app.title = "PM.2.5:Analytics !"   

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),[Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/new-page':
        return new_page_layout
    elif pathname =='home':
        return home_layout
    else:
        return home_layout

if __name__ == "__main__":
    app.run_server(debug=True)

