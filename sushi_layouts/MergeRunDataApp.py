from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from generic.callbacks import app

component_styles = {"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'}

title = 'MergeRunData App'

sidebar = html.Div(
    [
        html.P("FirstDataSet", style={"margin-bottom": "0px", "font-weight": "bold"}),
        dbc.Input(id='mergerundata-firstdataset', value='', type='text', style=component_styles),
        
        html.P("SecondDataSet", style={"margin-bottom": "0px", "font-weight": "bold"}),
        dcc.Dropdown(
            id='mergerundata-seconddataset',
            style=component_styles
        ),
        
        html.P("matchingColumn", style={"margin-bottom": "0px", "font-weight": "bold"}),
        dcc.Dropdown(
            id='mergerundata-matchingcolumn',
            options=[{'label': col, 'value': col} for col in ['Name', 'Tube', 'Sample Id']],
            style=component_styles
        ),
        
        html.P("Name", style={"margin-bottom": "0px", "font-weight": "bold"}),
        dbc.Input(id='mergerundata-name', value='MergedRunData', type='text', style=component_styles),
        
        html.P("minReadCount", style={"margin-bottom": "0px", "font-weight": "bold"}),
        dbc.Input(id='mergerundata-minreadcount', value=10000, type='number', style=component_styles),

        html.P("cores", style={"margin-bottom": "0px", "font-weight": "bold"}),
        dbc.Input(id='mergerundata-cores', value=8, type='number', style=component_styles),

        html.P("ram", style={"margin-bottom": "0px", "font-weight": "bold"}),
        dbc.Input(id='mergerundata-ram', value=10, type='number', style=component_styles),

        html.P("scratch", style={"margin-bottom": "0px", "font-weight": "bold"}),
        dbc.Input(id='mergerundata-scratch', value=200, type='number', style=component_styles),

        html.P("paired", style={"margin-bottom": "0px", "font-weight": "bold"}),
        dbc.Checklist(
            options=[{"label": "", "value": True}],
            value=[],
            id='mergerundata-paired',
            style=component_styles
        ),

        html.P("mail", style={"margin-bottom": "0px", "font-weight": "bold"}),
        dbc.Input(id='mergerundata-mail', value='', type='email', style=component_styles),
        
        dbc.Button("Submit", id='mergerundata-submit-button', n_clicks=0, style=component_styles)
    ]
)

layout = dbc.Container(
    [
        dbc.Alert("This App has not yet been tested! Do not use in production! Only for testing purposes!", 
                  color="danger", 
                  style={"color": "white", "backgroundColor": "red"}),
    ]
)

@app.callback(
    Output('mergerundata-name', 'value'),
    Input('mergerundata-submit-button', 'n_clicks'),
    State('mergerundata-firstdataset', 'value'),
    State('mergerundata-seconddataset', 'value'),
    State('mergerundata-matchingcolumn', 'value'),
    State('mergerundata-name', 'value'),
    State('mergerundata-minreadcount', 'value'),
    State('mergerundata-cores', 'value'),
    State('mergerundata-ram', 'value'),
    State('mergerundata-scratch', 'value'),
    State('mergerundata-paired', 'value'),
    State('mergerundata-mail', 'value'),
)
def callback(n_clicks, firstdataset, seconddataset, matchingcolumn, name, minreadcount, cores, ram, scratch, paired, mail):
    pass