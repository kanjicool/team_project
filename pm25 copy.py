from dash import Dash
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
from pycaret.classification import *
import requests
import jinja2
from pycaret.regression import *

loaded_model = load_model('model_air4_thai_demo')
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
        dbc.NavItem(dbc.NavLink("ย้อนหลัง", href="home")),
        dbc.NavItem(dbc.NavLink("พยากรณ์", href="/new-page")),  # Link to the new page
        dbc.NavItem(dbc.NavLink("Contact", href="#")),
    ],
    brand=dbc.NavbarBrand(
        children=[
            html.Img(src='/assets/logo.png', height='60px'),
            html.Span("PM2.5", className="m1-2")
        ],
        href='#',
    ),
    brand_href="#",
    color="light",
    dark=False,
    style={'height': '100px','border-top': '5px solid #17B897'},
    className='navbar'
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
                            style={'text-align': 'center','backgroundColor':'#A0C5FF'}
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
                            style={'text-align': 'center','backgroundColor':'#A0C5FF'}
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
                    ),style={'height' :'450px','width' : '1000px','margin': 'auto',}
                ),
                html.Div(
                    html.Div(
                        children=dcc.Graph(
                            id="parameter-chart1", config={"displayModeBar": True},
                            style={'border': '5px solid #17B89','height' :'400px','width' : '800px','margin': 'auto'}, 
                        ),
                        className="card",
                    ),style={'height' :'450px','width' : '1000px','margin': 'auto',}
                )
            ],
        className="content",
        style={'text-align': 'center','color':'#17B897','margin-top': '80px'}    
    ),
    html.Footer(
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    html.Div([
                        html.Br(),
                        html.H1("PM2.5", className='hightlight-text',style = {'color': 'white'}),
                        html.P('เว็บไซต์สำหรับการพยากรณ์ PM2.5 ', style={'margin-left': '10%', 'color': 'white'}),
                    ]),
                    style={'margin-left': '10%', 'color': 'white'},
                    width=4  # Adjust the width as needed
                ),
                dbc.Col(
                    html.Div([
                        html.Br(),
                        html.P("Contact", style={'color': 'white','font-weight': 'bold'}),
                        html.Small('Phone : 000-181-1111        ', style={'color': 'white'}),
                        html.Br(),
                        html.Small('email : pm25air4me@gmail.com', style={'color': 'white'}),
                    ]),
                    width=3  # Adjust the width as needed
                ),
                dbc.Col(
                    html.Div([
                        html.Br(),
                        html.P("Social", style={'color': 'white','font-weight': 'bold'}),
                        html.Img(src='/assets/line.png', alt='Social Image', style={'width': '30px', 'height': '30px','margin-right':'3px'}),
                        html.Img(src='/assets/ig.png', alt='Social Image2', style={'width': '30px', 'height': '30px','margin-right':'3px'}),
                        html.Img(src='/assets/line.png', alt='Social Image3', style={'width': '30px', 'height': '30px'}),
                        html.Br(),
                        html.Small('ติดต่อสอบถามได้ 00.00 - 00.01 น', style={'color': 'white'}),
                        html.Br(),
                    ]),
                    width=3  # Adjust the width as needed
                ),
            ],
            style={'border-bottom':'1px solid white'}
        ),
        html.P('© Copyright 2024 PM25Air4me. All rights reserved.', style={'color': 'white', 'text-align': 'center'}),
    ],
    style={'height': '150px', 'backgroundColor': '#17B897'},
    )

],style={'backgroundColor':'#33'},)
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
@app.callback(
        Output('parameter-chart1','figure'),
        [Input('station-filter','value'),
        Input('date-filter','value')]   
)
def update_chart2(stationID,Date):
    mask = (
        (data.stationID == stationID)&
        (data.Date == Date)
    )
    filtered_data = data.loc[mask, :]
    prameter_figure = {
        "data": [
                {"x": filtered_data["DATETIMEDATA"],"y": filtered_data["PM25"],"type": "bar",'name': 'PM25',},
                {"x": filtered_data["DATETIMEDATA"],"y": filtered_data["WS"],"type": "bar",'name': 'WS',},
                {"x": filtered_data["DATETIMEDATA"],"y": filtered_data["TEMP"],"type": "bar",'name': 'TEMP',},
                {"x": filtered_data["DATETIMEDATA"],"y": filtered_data["RH"],"type": "bar",'name': 'RH',},
                {"x": filtered_data["DATETIMEDATA"],"y": filtered_data["WD"],"type": "bar",'name': 'WD',},

        ],
        "layout": {
            "title": {
                "text": f'Graph of Station: {stationID}',
                
            },
            
        },
    }
    return prameter_figure


#-----------------------------------------------new page---------------------------------------------
new_page_layout = html.Div(
    children=[
        navbar,
        html.H1("This is the New Page!!!"),
        ],className='content'
)
#-----------------------------------------------new page2---------------------------------------------
new_page_layout2 = html.Div(
    children=[
        navbar,
        html.H1("This is the New Page!2"),
        ],className='content'
)
#----------------------------------------------app----------------------------------------------------
icon_path = 'logo.png'
app.title = "PM.2.5:Analytics !"   

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    html.Link(rel='stylesheet', href='/assets/styles.css')
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