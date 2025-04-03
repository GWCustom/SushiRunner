
from generic.callbacks import app
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

title = "FastqScreen App"

component_styles = {"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'}

sidebar = dbc.Col(
    [
        html.P("process_mode", style={"margin-bottom": "0px", "font-weight": "bold"}),
        dbc.Input(id='FastqScreen-process_mode', value='DATASET', style=component_styles),

        html.P("name", style={"margin-bottom": "0px", "font-weight": "bold"}),
        dbc.Input(id='FastqScreen-name', value='FastqScreen_Result', style=component_styles),

        html.P("paired", style={"margin-bottom": "0px", "font-weight": "bold"}),
        dbc.Checklist(
            options=[{"label": "Paired", "value": True}],
            value=False,
            id='FastqScreen-paired',
            inline=True,
            style=component_styles,
        ),

        html.P("cores", style={"margin-bottom": "0px", "font-weight": "bold"}),
        dbc.Input(id='FastqScreen-cores', value='8', style=component_styles),

        html.P("ram", style={"margin-bottom": "0px", "font-weight": "bold"}),
        dbc.Input(id='FastqScreen-ram', value='60', style=component_styles),

        html.P("scratch", style={"margin-bottom": "0px", "font-weight": "bold"}),
        dbc.Input(id='FastqScreen-scratch', value='100', style=component_styles),

        html.P("nReads", style={"margin-bottom": "0px", "font-weight": "bold"}),
        dbc.Input(id='FastqScreen-nReads', value='100000', style=component_styles),

        html.P("nTopSpecies", style={"margin-bottom": "0px", "font-weight": "bold"}),
        dbc.Input(id='FastqScreen-nTopSpecies', value='5', style=component_styles),

        html.P("minAlignmentScore", style={"margin-bottom": "0px", "font-weight": "bold"}),
        dbc.Input(id='FastqScreen-minAlignmentScore', value='-20', style=component_styles),

        html.P("cmdOptions", style={"margin-bottom": "0px", "font-weight": "bold"}),
        dbc.Input(id='FastqScreen-cmdOptions', value="-k 10 --trim5 4 --trim3 4 --very-sensitive", style=component_styles),

        html.P("trim_front1", style={"margin-bottom": "0px", "font-weight": "bold"}),
        dbc.Input(id='FastqScreen-trim_front1', value='0', style=component_styles),

        html.P("trim_tail1", style={"margin-bottom": "0px", "font-weight": "bold"}),
        dbc.Input(id='FastqScreen-trim_tail1', value='0', style=component_styles),

        html.P("cut_front", style={"margin-bottom": "0px", "font-weight": "bold"}),
        dbc.Checklist(
            options=[{"label": "Cut Front", "value": True}],
            value=False,
            id='FastqScreen-cut_front',
            inline=True,
            style=component_styles,
        ),

        html.P("cut_front_window_size", style={"margin-bottom": "0px", "font-weight": "bold"}),
        dbc.Input(id='FastqScreen-cut_front_window_size', value='4', style=component_styles),

        html.P("cut_front_mean_quality", style={"margin-bottom": "0px", "font-weight": "bold"}),
        dbc.Input(id='FastqScreen-cut_front_mean_quality', value='20', style=component_styles),

        html.P("cut_tail", style={"margin-bottom": "0px", "font-weight": "bold"}),
        dbc.Checklist(
            options=[{"label": "Cut Tail", "value": True}],
            value=False,
            id='FastqScreen-cut_tail',
            inline=True,
            style=component_styles,
        ),

        html.P("cut_tail_window_size", style={"margin-bottom": "0px", "font-weight": "bold"}),
        dbc.Input(id='FastqScreen-cut_tail_window_size', value='4', style=component_styles),

        html.P("cut_tail_mean_quality", style={"margin-bottom": "0px", "font-weight": "bold"}),
        dbc.Input(id='FastqScreen-cut_tail_mean_quality', value='20', style=component_styles),

        html.P("cut_right", style={"margin-bottom": "0px", "font-weight": "bold"}),
        dbc.Checklist(
            options=[{"label": "Cut Right", "value": True}],
            value=False,
            id='FastqScreen-cut_right',
            inline=True,
            style=component_styles,
        ),

        html.P("cut_right_window_size", style={"margin-bottom": "0px", "font-weight": "bold"}),
        dbc.Input(id='FastqScreen-cut_right_window_size', value='4', style=component_styles),

        html.P("cut_right_mean_quality", style={"margin-bottom": "0px", "font-weight": "bold"}),
        dbc.Input(id='FastqScreen-cut_right_mean_quality', value='20', style=component_styles),

        html.P("average_qual", style={"margin-bottom": "0px", "font-weight": "bold"}),
        dbc.Input(id='FastqScreen-average_qual', value='0', style=component_styles),

        html.P("max_len1", style={"margin-bottom": "0px", "font-weight": "bold"}),
        dbc.Input(id='FastqScreen-max_len1', value='0', style=component_styles),

        html.P("max_len2", style={"margin-bottom": "0px", "font-weight": "bold"}),
        dbc.Input(id='FastqScreen-max_len2', value='0', style=component_styles),

        html.P("poly_x_min_len", style={"margin-bottom": "0px", "font-weight": "bold"}),
        dbc.Input(id='FastqScreen-poly_x_min_len', value='10', style=component_styles),

        html.P("length_required", style={"margin-bottom": "0px", "font-weight": "bold"}),
        dbc.Input(id='FastqScreen-length_required', value='18', style=component_styles),

        html.P("cmdOptionsFastp", style={"margin-bottom": "0px", "font-weight": "bold"}),
        dbc.Input(id='FastqScreen-cmdOptionsFastp', value='', style=component_styles),

        html.P("mail", style={"margin-bottom": "0px", "font-weight": "bold"}),
        dbc.Input(id='FastqScreen-mail', value='', style=component_styles),

        dbc.Button("Submit", id='FastqScreen-submit', color="primary", style={"margin-top": "20px"})
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
