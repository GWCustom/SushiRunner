
from generic.callbacks import app
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

component_styles = {"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'}



sidebar= dbc.Container(children=[ 
        html.P("Generic Parameters: ", style={"margin-bottom": "0px", "font-weight": "bold"}),
        dbc.Input(id='name', value='', type='text', placeholder='Name', style={"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'}),
        dbc.Input(id='comment', value='', type='text', placeholder='Comment', style={"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'}),
        dbc.Select(id='ram', options=[15, 32, 64], placeholder='RAM', style={"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'}),
        dbc.Select(id='cores', options=[1, 2, 4, 8], placeholder='Cores', style={"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'}),
        dbc.Select(id='scratch', options=[10, 50, 100], placeholder='Scratch', style={"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'}),
        dbc.Select(id='partition', options=['employee', 'manyjobs', 'user'], placeholder='Partition', style={"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'}),
        dbc.Select(id='process_mode', options=['DATASET'], placeholder='Process Mode', style={"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'}),
        dbc.Input(id='mail', value='', type='email', placeholder='Mail', style={"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'}),
        html.P("App Specific Parameters: ", style={"margin-bottom": "0px", "font-weight": "bold"}),
        dbc.Button("Submit", id='submit1', n_clicks=0, style={"margin-top": "18px", 'borderBottom': '1px solid lightgrey'})],
        style={"max-height":"62vh", "overflow-y":"auto", "overflow-x":"hidden"})


layout = dbc.Container(
    [
        dbc.Alert("This App has not yet been tested! Do not use in production! Only for testing purposes!", 
                  color="danger", 
                  style={"color": "white", "backgroundColor": "red"}),
    ]
)
@app.callback(
    Output('FastqScreen-submit', 'n_clicks'),
    [Input('FastqScreen-submit', 'n_clicks')],
    [State('FastqScreen-process_mode', 'value'),
     State('FastqScreen-name', 'value'),
     State('FastqScreen-paired', 'value'),
     State('FastqScreen-cores', 'value'),
     State('FastqScreen-ram', 'value'),
     State('FastqScreen-scratch', 'value'),
     State('FastqScreen-nReads', 'value'),
     State('FastqScreen-nTopSpecies', 'value'),
     State('FastqScreen-minAlignmentScore', 'value'),
     State('FastqScreen-cmdOptions', 'value'),
     State('FastqScreen-trim_front1', 'value'),
     State('FastqScreen-trim_tail1', 'value'),
     State('FastqScreen-cut_front', 'value'),
     State('FastqScreen-cut_front_window_size', 'value'),
     State('FastqScreen-cut_front_mean_quality', 'value'),
     State('FastqScreen-cut_tail', 'value'),
     State('FastqScreen-cut_tail_window_size', 'value'),
     State('FastqScreen-cut_tail_mean_quality', 'value'),
     State('FastqScreen-cut_right', 'value'),
     State('FastqScreen-cut_right_window_size', 'value'),
     State('FastqScreen-cut_right_mean_quality', 'value'),
     State('FastqScreen-average_qual', 'value'),
     State('FastqScreen-max_len1', 'value'),
     State('FastqScreen-max_len2', 'value'),
     State('FastqScreen-poly_x_min_len', 'value'),
     State('FastqScreen-length_required', 'value'),
     State('FastqScreen-cmdOptionsFastp', 'value'),
     State('FastqScreen-mail', 'value')]
)
def callback(n_clicks, *args):
    pass
