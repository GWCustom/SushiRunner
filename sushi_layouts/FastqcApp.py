from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from generic.callbacks import app

component_styles = {"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'}

title = 'FastqcApp'

sidebar = [
    html.P("paired", style={"margin-bottom": "0px", "font-weight": "bold"}),
    dbc.Checkbox(id='FastqcApp_paired', style=component_styles),
    
    html.P("showNativeReports", style={"margin-bottom": "0px", "font-weight": "bold"}),
    dbc.Checkbox(id='FastqcApp_showNativeReports', style=component_styles),
    
    html.P("cores", style={"margin-bottom": "0px", "font-weight": "bold"}),
    dbc.Select(id='FastqcApp_cores', options=[
        {'label': str(i), 'value': i} for i in [8, 1, 2, 4, 8]
    ], style=component_styles),
    
    html.P("ram", style={"margin-bottom": "0px", "font-weight": "bold"}),
    dbc.Select(id='FastqcApp_ram', options=[
        {'label': str(i), 'value': i} for i in [15, 30, 62]
    ], style=component_styles),
    
    html.P("scratch", style={"margin-bottom": "0px", "font-weight": "bold"}),
    dbc.Select(id='FastqcApp_scratch', options=[
        {'label': str(i), 'value': i} for i in [100, 10, 50, 100]
    ], style=component_styles),
    
    html.P("specialOptions", style={"margin-bottom": "0px", "font-weight": "bold"}),
    dbc.Input(id='FastqcApp_specialOptions', style=component_styles),
    
    html.P("cmdOptions", style={"margin-bottom": "0px", "font-weight": "bold"}),
    dbc.Input(id='FastqcApp_cmdOptions', style=component_styles),
    
    html.P("mail", style={"margin-bottom": "0px", "font-weight": "bold"}),
    dbc.Input(id='FastqcApp_mail', type='email', style=component_styles),
    
    dbc.Button('Submit', id='FastqcApp_submit', n_clicks=0, style=component_styles)
]


layout = html.Div([
    dbc.Alert("This App has not yet been tested! Do not use in production! Only for testing purposes!", 
                  color="danger", 
                  style={"color": "white", "backgroundColor": "red"}),
    html.Div([
        html.P('A quality control tool for NGS reads'),
        html.A('Web-site with docs and a tutorial video', href='http://www.bioinformatics.babraham.ac.uk/projects/fastqc'),
    ]),

])

@app.callback(
    Output('FastqcApp_paired', 'value'),
    [
        Input('FastqcApp_submit', 'n_clicks')
    ],
    [
        State('FastqcApp_paired', 'value'),
        State('FastqcApp_showNativeReports', 'value'),
        State('FastqcApp_cores', 'value'),
        State('FastqcApp_ram', 'value'),
        State('FastqcApp_scratch', 'value'),
        State('FastqcApp_specialOptions', 'value'),
        State('FastqcApp_cmdOptions', 'value'),
        State('FastqcApp_mail', 'value')
    ]
)
def callback(submit_n_clicks, paired, showNativeReports, cores, ram, scratch, specialOptions, cmdOptions, mail):
    pass