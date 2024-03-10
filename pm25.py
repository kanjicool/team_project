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


app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                            )

icon_path = 'logo.png'
app.title = "PM.2.5:Analytics !"   

app.layout = html.Div(
    children=[
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("หน้าแรก", href="#")),
            dbc.NavItem(dbc.NavLink("พยากรณ์", href="#")),
            dbc.NavItem(dbc.NavLink("Contact", href="#")),
        ],
        brand=dbc.NavbarBrand(
            children=[
                html.Img(src='/assets/logo.png',height='60px'),
                html.Span("PM.2.5",className="m1-2")
            ],
            href='#',
        ),
        
        #brand_style={'color':'black'},
        brand_href="#",
        color="light",
        dark=False,
        style={'height':'100px'},
        className='navbar-shadow'
    ),
    html.Div(
            children =[
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
                            style={'text-align': 'center'}
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
                            style={'text-align': 'center'}
                        )
                    ],
                    className="date",
                    style={'display': 'inline-block'}
                )
    ],
    className="menu",
    style={'text-align': 'right'}
    
    ),
    html.Div(
                html.Div(
                    children=dcc.Graph(
                        id="pm25-chart", config={"displayModeBar": True},
                    ),
                    className="card",
                )
    )

])
@app.callback(
        Output('pm25-chart','figure'),
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
                "text": f'Graph of<br>Station: {stationID}',
                "x": 0.5,
                "xanchor": "center",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#17B897"],
            
        },
    }
    return pm25_figure

if __name__ == "__main__":
    app.run_server(debug=True)

