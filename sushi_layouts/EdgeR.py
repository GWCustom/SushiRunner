from dash import html, dcc, ctx
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from generic.callbacks import app
import dash_daq as daq
from bfabric_web_apps.utils.components import charge_switch
import pandas as pd 
from dash.dash_table import DataTable
from bfabric_web_apps import (
    SCRATCH_PATH
)
from sushi_utils.dataset_utils import dataset_to_dictionary as dtd

from sushi_utils.component_utils import submitbutton_id
import os

######################################################################################################
####################### STEP 1: Get Data From the User! ##############################################
######################################################################################################
### We will define the following items in this section:   ############################################
###     A. Sidebar content                                ############################################
###     B. Application layout                             ############################################
###     C. Application callbacks (to handle user input)   ############################################
###     D. Populate some UI components with default vals  ############################################
######################################################################################################

####################################################################################
##### A. First we define the sidebar content (Step 1: Get data from the user) ######
####################################################################################
component_styles = {"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'}

title = 'FastqScreen'

label_style = {
    "font-size": "0.85rem",   # Smaller text
    "margin-left": "6px",     # Indent the label a bit
    "margin-bottom": "4px"
}

def id(name):
    return f"{title}_{name}"


from dash import html, dcc
import dash_bootstrap_components as dbc
from bfabric_web_apps.utils.components import charge_switch
from sushi_utils.component_utils import submitbutton_id

# Component styles
component_styles = {"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'}

# Sidebar layout for EdgeR
sidebar = dbc.Container(children=charge_switch + [
    html.P("EdgeR App Parameters:", style={"font-weight": "bold", "font-size": "1rem", "margin-bottom": "10px"}),

    html.Div([
        dbc.Label("Name", style={"font-size": "0.85rem"}),
        dbc.Input(id='EdgeR_name', value='0007072_EdgeR', type='text', style=component_styles)
    ]),

    html.Div([
        dbc.Label("Comment", style={"font-size": "0.85rem"}),
        dbc.Input(id='EdgeR_comment', value='', type='text', style=component_styles)
    ]),

    html.Div([
        dbc.Label("Cores", style={"font-size": "0.85rem"}),
        dbc.Input(id='EdgeR_cores', type='number', min=1, max=64, step=1, value=4, style=component_styles)
    ]),

    html.Div([
        dbc.Label("Param", style={"font-size": "0.85rem"}),
        dbc.Input(id='EdgeR_param', value='employee', type='text', style=component_styles)
    ]),

    html.Div([
        dbc.Label("Process Mode", style={"font-size": "0.85rem"}),
        dbc.Input(id='EdgeR_processMode', value='', type='text', style=component_styles)
    ]),

    html.Div([
        dbc.Label("Samples", style={"font-size": "0.85rem"}),
        dbc.Input(id='EdgeR_samples', value='', type='text', style=component_styles)
    ]),

    html.Div([
        dbc.Label("Reduce", style={"font-size": "0.85rem"}),
        dbc.Input(id='EdgeR_reduce', value='', type='text', style=component_styles)
    ]),

    html.Div([
        dbc.Label("Feature Level", style={"font-size": "0.85rem"}),
        dbc.Select(id='EdgeR_featureLevel', options=[{"label": opt, "value": opt} for opt in ["Gene", "Isoform"]], value="Gene", style=component_styles)
    ]),

    html.Div([
        dbc.Label("Test Method", style={"font-size": "0.85rem"}),
        dbc.Select(id='EdgeR_testMethod', options=[{"label": opt, "value": opt} for opt in ["glm", "exactTest"]], value="glm", style=component_styles)
    ]),

    html.Div([
        dbc.Label("Run GO Analysis", style={"font-size": "0.85rem"}),
        dbc.Select(id='EdgeR_runGo', options=[{"label": str(opt), "value": opt} for opt in [True, False]], value=True, style=component_styles)
    ]),

    html.Div([
        dbc.Label("Grouping", style={"font-size": "0.85rem"}),
        dbc.Select(id='EdgeR_grouping', options=[{"label": opt, "value": opt} for opt in ["condition"]], value="condition", style=component_styles)
    ]),

    html.Div([
        dbc.Label("Sample Group", style={"font-size": "0.85rem"}),
        dbc.Select(id='EdgeR_sampleGroup', options=[{"label": opt, "value": opt} for opt in ["Controls", "Hetero", "Homo"]], value="Controls", style=component_styles)
    ]),

    html.Div([
        dbc.Label("Sample Group Baseline", style={"font-size": "0.85rem"}),
        dbc.Select(id='EdgeR_sampleGroupBaseline', options=[{"label": opt, "value": opt} for opt in ["Controls", "Hetero", "Homo"]], value="Controls", style=component_styles)
    ]),

    html.Div([
        dbc.Label("Reference Group", style={"font-size": "0.85rem"}),
        dbc.Select(id='EdgeR_refGroup', options=[{"label": opt, "value": opt} for opt in ["Controls", "Hetero", "Homo"]], value="Controls", style=component_styles)
    ]),

    html.Div([
        dbc.Label("Reference Group Baseline", style={"font-size": "0.85rem"}),
        dbc.Select(id='EdgeR_refGroupBaseline', options=[{"label": opt, "value": opt} for opt in ["Controls", "Hetero", "Homo"]], value="Controls", style=component_styles)
    ]),

    html.Div([
        dbc.Label("Only Comparison Groups in Heatmap", style={"font-size": "0.85rem"}),
        dbc.Select(id='EdgeR_onlyCompGroupsHeatmap', options=[{"label": str(opt), "value": opt} for opt in [True, False]], value=True, style=component_styles)
    ]),

    html.Div([
        dbc.Label("Normalization Method", style={"font-size": "0.85rem"}),
        dbc.Select(id='EdgeR_normMethod', options=[{"label": opt, "value": opt} for opt in ["TMM", "RLE", "upperQuartile", "None"]], value="TMM", style=component_styles)
    ]),

    html.Div([
        dbc.Label("p-value High Threshold", style={"font-size": "0.85rem"}),
        dbc.Input(id='EdgeR_pValueHighThreshold', value=0.05, type='number', style=component_styles)
    ]),

    html.Div([
        dbc.Label("p-value Cut-off", style={"font-size": "0.85rem"}),
        dbc.Input(id='EdgeR_pvalCut', value=0.05, type='number', style=component_styles)
    ]),

    html.Div([
        dbc.Label("Log2 Fold-Change Threshold", style={"font-size": "0.85rem"}),
        dbc.Input(id='EdgeR_log2FoldChangeThreshold', value=1.0, type='number', style=component_styles)
    ]),

    html.Div([
        dbc.Label("Top N Tags", style={"font-size": "0.85rem"}),
        dbc.Input(id='EdgeR_topNtag', value=20, type='number', style=component_styles)
    ]),

    html.Div([
        dbc.Label("FDR Threshold for NSEA", style={"font-size": "0.85rem"}),
        dbc.Input(id='EdgeR_fdrThresholdForNSEA', value=0.05, type='number', style=component_styles)
    ]),

    html.Div([
        dbc.Label("Sparse Log Normalization", style={"font-size": "0.85rem"}),
        dbc.Input(id='EdgeR_sparselogNorm', value='', type='text', style=component_styles)
    ]),

    html.Div([
        dbc.Label("R Version", style={"font-size": "0.85rem"}),
        dbc.Select(id='EdgeR_Rversion', options=[{"label": "Dev/R/4.4.2", "value": "Dev/R/4.4.2"}], value="Dev/R/4.4.2", style=component_styles)
    ]),

    dbc.Button("Submit", id=submitbutton_id('EdgeR_submit1'), n_clicks=0, style={"margin-top": "18px"})
], style={"max-height": "62vh", "overflow-y": "auto", "overflow-x": "hidden"})



####################################################################################
##### B. Now we define the application layout (Step 1: Get data from the user) #####
####################################################################################

layout = dbc.Container(
    children = [
        html.Div(id=id("Layout"), style={"max-height":"62vh", "overflow-y":"auto", "overflow-x":"hidden"}),
        dcc.Store(id=id("dataset"), data={})
    ]
)

alerts = html.Div(
    [
        dbc.Alert("Success: Job Submitted!", color="success", id=id("alert-fade-success"), dismissable=True, is_open=False),
        dbc.Alert("Error: Job Submission Failed!", color="danger", id=id("alert-fade-fail"), dismissable=True, is_open=False),
    ],
    style={"margin": "20px"}
)
####################################################################################
### C. Now we define the application callbacks (Step 1: Get data from the user) ####
####################################################################################

@app.callback(
    Output(id("Layout"), "children"),
    [
        Input(id("dataset"), "data"),
        Input("sidebar", "children"),
    ]
)
def callback(data, sidebar):
    """
    Update the dataset in the layout.
    """

    df = pd.DataFrame(data) 

    if df.empty:
        return html.Div("No dataset loaded")

    else:

        table = DataTable(
            id='datatable',
            data=df.to_dict('records'),        
            columns=[{"name": i, "id": i} for i in df.columns], 
            selected_rows=[i for i in range(len(df))],
            row_selectable='multi',
            page_action="native",
            page_current=0,
            page_size=15,
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto'
            },
            style_table={
                'overflowX': 'auto', 
                'maxWidth': '90%'
            },
            style_cell={
                'textAlign': 'left',
                'padding': '5px',
                'whiteSpace': 'normal',
                'height': 'auto',
                'fontSize': '0.85rem',
                'font-family': 'Arial',
                'border': '1px solid lightgrey'
            },
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            }
        )

        container = html.Div([
            html.H4("Dataset"),
            table
        ])

        return container


##############################################################################################
##### C. Now we populate components with default values (Step 1: Get data from the user) #####
##############################################################################################

# Adjusted populate_default_values callback
@app.callback(
    [
        Output('EdgeR_name', 'value'),
        Output('EdgeR_comment', 'value'),
        Output('EdgeR_cores', 'value'),
        Output('EdgeR_param', 'value'),
        Output('EdgeR_processMode', 'value'),
        Output('EdgeR_featureLevel', 'value'),
        Output('EdgeR_testMethod', 'value'),
        Output('EdgeR_runGo', 'value'),
        Output('EdgeR_grouping', 'value'),
        Output('EdgeR_sampleGroup', 'value'),
        Output('EdgeR_sampleGroupBaseline', 'value'),
        Output('EdgeR_refGroup', 'value'),
        Output('EdgeR_refGroupBaseline', 'value'),
        Output('EdgeR_onlyCompGroupsHeatmap', 'value'),
        Output('EdgeR_normMethod', 'value'),
        Output('EdgeR_pValueHighThreshold', 'value'),
        Output('EdgeR_pvalCut', 'value'),
        Output('EdgeR_log2FoldChangeThreshold', 'value'),
        Output('EdgeR_topNtag', 'value'),
        Output('EdgeR_fdrThresholdForNSEA', 'value'),
        Output('EdgeR_sparselogNorm', 'value'),
        Output('EdgeR_Rversion', 'value')
    ],
    [Input("entity", "data")],
    [State("app_data", "data")]
)
def populate_default_values(entity_data, app_data):
    name = entity_data.get("name", "Unknown") + "_EdgeR"
    return (
        name, "", 4, "employee", "", "Gene", "glm", True, "condition", 
        "Controls", "Controls", "Controls", "Controls", True, "TMM", 
        0.05, 0.05, 1.0, 20, 0.05, "", "Dev/R/4.4.2"
    )

######################################################################################################
####################### STEP 2: Get data from B-Fabric! ##############################################
###################################################################################################### 
### This is a short section, because we've already generalized most      #############################
### of the data acquisition for Sushi apps which you get out of the box  #############################
######################################################################################################

@app.callback(
    Output(id("dataset"), "data"),
    Input("entity", "data"),
    State(id("dataset"), "data"),
)
def update_dataset(entity_data, dataset):
    
    df = dtd(entity_data.get("full_api_response", {}))
    return df



######################################################################################################
############################### STEP 3: Submit the Job! ##############################################
###################################################################################################### 
# Adjusted submit_edger_job callback
@app.callback(
    [Output('EdgeR_alert-fade-success', 'is_open'), Output('EdgeR_alert-fade-fail', 'is_open')],
    [Input(submitbutton_id('EdgeR_submit1'), 'n_clicks')],
    [
        State('EdgeR_name', 'value'),
        State('EdgeR_comment', 'value'),
        State('EdgeR_cores', 'value'),
        State('EdgeR_param', 'value'),
        State('EdgeR_processMode', 'value'),
        State('EdgeR_featureLevel', 'value'),
        State('EdgeR_testMethod', 'value'),
        State('EdgeR_runGo', 'value'),
        State('EdgeR_grouping', 'value'),
        State('EdgeR_sampleGroup', 'value'),
        State('EdgeR_sampleGroupBaseline', 'value'),
        State('EdgeR_refGroup', 'value'),
        State('EdgeR_refGroupBaseline', 'value'),
        State('EdgeR_onlyCompGroupsHeatmap', 'value'),
        State('EdgeR_normMethod', 'value'),
        State('EdgeR_pValueHighThreshold', 'value'),
        State('EdgeR_pvalCut', 'value'),
        State('EdgeR_log2FoldChangeThreshold', 'value'),
        State('EdgeR_topNtag', 'value'),
        State('EdgeR_fdrThresholdForNSEA', 'value'),
        State('EdgeR_sparselogNorm', 'value'),
        State('EdgeR_Rversion', 'value'),
        State('FastqScreen_dataset', 'data'),
        State('datatable', 'selected_rows'),
        State('token_data', 'data'),
        State('entity', 'data'),
        State('app_data', 'data')
    ],
    prevent_initial_call=True
)
def submit_edger_job(
    n_clicks, name, comment, cores, param, processMode, featureLevel, testMethod, runGo, grouping,
    sampleGroup, sampleGroupBaseline, refGroup, refGroupBaseline, onlyCompGroupsHeatmap, normMethod,
    pValueHighThreshold, pvalCut, log2FoldChangeThreshold, topNtag, fdrThresholdForNSEA,
    sparselogNorm, Rversion, dataset, selected_rows, token_data, entity_data, app_data
):
    try:
        dataset_df = pd.DataFrame(dtd(entity_data.get("full_api_response", {})))
        dataset_path = f"{SCRATCH_PATH}/{name}/dataset.tsv"
        os.makedirs(os.path.dirname(dataset_path), exist_ok=True)
        dataset_df.to_csv(dataset_path, sep="\t", index=False)

        param_dict = {
            'cores': cores,
            'param': param,
            'processMode': processMode,
            'featureLevel': featureLevel,
            'testMethod': testMethod,
            'runGo': runGo,
            'grouping': grouping,
            'sampleGroup': sampleGroup,
            'sampleGroupBaseline': sampleGroupBaseline,
            'refGroup': refGroup,
            'refGroupBaseline': refGroupBaseline,
            'onlyCompGroupsHeatmap': onlyCompGroupsHeatmap,
            'normMethod': normMethod,
            'pValueHighThreshold': pValueHighThreshold,
            'pvalCut': pvalCut,
            'log2FoldChangeThreshold': log2FoldChangeThreshold,
            'topNtag': topNtag,
            'fdrThresholdForNSEA': fdrThresholdForNSEA,
            'sparselogNorm': sparselogNorm,
            'Rversion': Rversion,
            'name': name,
            'comment': comment
        }

        param_df = pd.DataFrame({"col1": list(param_dict.keys()), "col2": list(param_dict.values())})
        param_path = f"{SCRATCH_PATH}/{name}/parameters.tsv"
        os.makedirs(os.path.dirname(param_path), exist_ok=True)
        param_df.to_csv(param_path, sep="\t", index=False, header=False)

        app_id = app_data.get("id", "")
        project_id = "2220"
        dataset_name = entity_data.get("name", "")
        mango_run_name = "None"

        bash_command = f"""
            bundle exec sushi_fabric --class EdgeR --dataset \
            {dataset_path} --parameterset {param_path} --run \
            --input_dataset_application {app_id} --project {project_id} \
            --dataset_name {dataset_name} --mango_run_name {mango_run_name} \
            --next_dataset_name {name}
        """
        print("[SUSHI BASH COMMAND]:", bash_command)
        return True, False

    except Exception as e:
        print("[SUSHI ERROR]:", str(e))
        return False, True