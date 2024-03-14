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
from dash_table import DataTable


# print(prediction)
df = pd.read_csv('predict_regession_2024-02-01_To_2024-02-29.csv')
df['DATETIMEDATA'] = pd.to_datetime(df['DATETIMEDATA'])
df.rename(columns={'prediction_label': 'PM25'}, inplace=True)
df.sort_values("DATETIMEDATA",inplace=True)

df2 = pd.read_csv('air4thai_44t_2024-02-01_2024-02-29.csv')
del df2['Unnamed: 0']
df2[['Date', 'Time']] = df2['DATETIMEDATA'].str.split(' ', expand=True)
df2.sort_values("DATETIMEDATA", inplace=True)


app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY,'/assets/styles.css'],
                suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                            )

#-----------------------------------------------tabs----------------------------------------------                            
tabs_content = {
    'PM25': 'PM25',
    'O3': 'O3',
    'WS': 'WS',
    'TEMP': 'TEMP',
    'RH': 'RH',
    'WD': 'WD',
}
tabs = dcc.Tabs(
    id='tabs',
    value='PM25',
    children=[
        dcc.Tab(label=tab, value=value) for value, tab in tabs_content.items()
    ],style={'margin':'auto','width':'1000px'}
)
#----------------------------------------navbar-----------------------------------------------
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("ย้อนหลัง", href="home")),
        dbc.NavItem(dbc.NavLink("พยากรณ์", href="/new-page")),  # Link to the new page
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
#------------------------------------------table---------------------------------------------
data_table = DataTable(
    id='parameter-table',
    columns=[
        {'name': 'Date', 'id': 'Date'},
        {'name': 'PM25', 'id': 'PM25', 'type': 'numeric', 'format': {'specifier': '.2f'}},
        {'name': 'O3', 'id': 'O3', 'type': 'numeric', 'format': {'specifier': '.2f'}},
        {'name': 'WS', 'id': 'WS', 'type': 'numeric', 'format': {'specifier': '.2f'}},
        {'name': 'TEMP', 'id': 'TEMP', 'type': 'numeric', 'format': {'specifier': '.2f'}},
        {'name': 'RH', 'id': 'RH', 'type': 'numeric', 'format': {'specifier': '.2f'}},
        {'name': 'WD', 'id': 'WD', 'type': 'numeric', 'format': {'specifier': '.2f'}},
    ],
    style_table={'width':'1000px','height': '200px', 'overflowY': 'auto','margin':'auto'}, 
    fixed_rows={'headers': True},
)
#------------------------------------------footer--------------------------------------------
footer = html.Footer(
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
#-----------------------------------------home-------------------------------------------------
home_layout = html.Div(
    children=[
        navbar,
        html.Div([
            html.H1("Welcome‼ : Pls try \"พยากรณ์\" tab ",style={'margin-top': '120px','font-weight':'bold','color':'#17B897'}),
            ],className='topic_name',style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'height': '100vh'}),
            
            html.Div([
            html.Label("Select Parameter:"),
            dcc.Dropdown(
                id='parameter-dropdown',
                options=[
                    {'label': 'PM25', 'value': 'PM25'},
                    {'label': 'O3', 'value': 'O3'},
                    {'label': 'WS', 'value': 'WS'},
                    {'label': 'TEMP', 'value': 'TEMP'},
                    {'label': 'RH', 'value': 'RH'},
                    {'label': 'WD', 'value': 'WD'},
                ],
                value='PM25',  # Default selected value
                style={'width': '50%', 'margin': 'auto'}
            ),
            
            html.Div([
            dcc.Graph(
                id="chart2",
                config={"displayModeBar": True},
                style={'border': '5px solid #17B89', 'height': '400px', 'width': '800px', 'margin': 'auto'},
            ),
        ], className="card", style={'height': '400px', 'width': '1000px', 'margin': 'auto', 'margin-bottom': '20px'}),
            
        ], style={'margin-top': '20px', 'text-align': 'center'}),

        # Graph for selected parameter
        footer
    ],
)
#----------------------------------------chart2------------------------------------------------------
@app.callback(
    Output('chart2', 'figure'),
    [Input('parameter-dropdown', 'value')]  # Removed 'day-dropdown' input
)
def update_chart2_home(selected_parameter):
    mask = (df2['Date'] == df2['Date'].iloc[0])  # Assuming the first date in the dataset is the default
    filtered_data = df2.loc[mask, :]

    figure_data = [
        {
            "x": filtered_data["DATETIMEDATA"],
            "y": filtered_data[selected_parameter],
            "mode": "lines+markers",
            "hovertemplate": f"%{{y:.2f}}<extra></extra>",
            "name": selected_parameter,
        },
    ]

    figure_layout = {
        "title": {
            "text": f'Graph of {selected_parameter} prediction',
            "x": 0.5,
            "xanchor": "center",
            "font": {"family": "Truculenta", "size": 24, "color": "#333"},
        },
        "xaxis": {"title": "Date", "fixedrange": True},
        "yaxis": {"title": selected_parameter, "fixedrange": True},
        "colorway": ["#17B897"],
    }

    pm25_figure = {"data": figure_data, "layout": figure_layout}

    return pm25_figure
#-----------------------------------------------new page---------------------------------------------
new_page_layout = html.Div(
    children=[
        navbar,
        html.Div(
            children=[
                html.Div([
                    html.H1('PM2.5 - Regression: forecast',className='topic_name',style={'margin-top':'25px','display': 'inline-block'})
                ]),
                html.Div(
                        children=[
                            html.Div(
                                children="Date Range",
                                className="menu-title",
                                style={'text-align': 'center'}
                            ),
                            dcc.DatePickerRange(
                                id="date-filter",
                                start_date="2024-03-01",
                                end_date="2024-03-07",
                                display_format="YYYY-MM-DD",
                                style={'text-align': 'center', 'backgroundColor': '#A0C5FF'}
                            )
                        ],
                        className="date",
                        style={'display': 'inline-block','width':'300px'},
                    ),
                tabs,
#-----------------------------------graph 1----------------------------------------------------------
                html.Div(
                    children=[
                        dcc.Graph(
                            id="pm25-chart1", config={"displayModeBar": True},
                            style={'border': '5px solid #17B89', 'height': '400px', 'width': '800px', 'margin': 'auto'},
                        ),
                    ],
                    className="card",
                    style={'height': '400px', 'width': '1000px', 'margin': 'auto','margin-bottom':'20px'},
                ),
                data_table,
            ],
            className="content",
            style={'text-align': 'center', 'color': '#17B897', 'margin-top': '80px','margin-bottom': '10px'}
        ),
    footer

],style={'backgroundColor':'#33'},
)

#----------------------------------------------function----------------------------------------------
#----------------------------------------chart1------------------------------------------------------
@app.callback(
    Output('pm25-chart1', 'figure'),
    [Input('date-filter', 'start_date'),
    Input('date-filter', 'end_date'),
    Input('tabs', 'value')]  # Add tabs value as an input
)
def update_chart(start_date, end_date, selected_tab):
    parameter = selected_tab  # Use the selected_tab value as the parameter

    mask = (
        (df['DATETIMEDATA'] >= start_date) &
        (df['DATETIMEDATA'] <= end_date)
    )
    filtered_data = df.loc[mask, :]

    figure_data = [
        {
            "x": filtered_data["DATETIMEDATA"],
            "y": filtered_data[parameter],
            "mode": "lines+markers",
            "hovertemplate": f"%{{y:.2f}}<extra></extra>",
            "name": parameter,
        },
    ]

    figure_layout = {
        "title": {
            "text": f'Graph of {parameter} prediction',
            "x": 0.5,
            "xanchor": "center",
            "font": {"family": "Truculenta", "size": 24, "color": "#333"},
        },
        "xaxis": {"title": "Date", "fixedrange": True},
        "yaxis": {"title": parameter, "fixedrange": True},
        "colorway": ["#17B897"],
    }

    pm25_figure = {"data": figure_data, "layout": figure_layout}

    return pm25_figure

# ----------------------------------DataTable-------------------------------
@app.callback(
    Output('parameter-table', 'data'),
    [Input('date-filter', 'start_date'),
    Input('date-filter', 'end_date')]
)
def update_table(start_date, end_date):
    mask = (
        (df['DATETIMEDATA'] >= start_date) &
        (df['DATETIMEDATA'] <= end_date)
    )
    filtered_data = df.loc[mask, :]
    filtered_data['Date'] = filtered_data['DATETIMEDATA'].dt.date
    

    # Group by date and calculate average for each parameter
    day_data = filtered_data.groupby(['Date'])
    avg_data = day_data.mean().reset_index()
    # Format the data for DataTable
    table_data = avg_data[['Date', 'PM25', 'O3', 'WS', 'TEMP', 'RH', 'WD']].to_dict('records')

    return table_data


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