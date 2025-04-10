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

title = 'DESeq2'

label_style = {
    "font-size": "0.85rem",   # Smaller text
    "margin-left": "6px",     # Indent the label a bit
    "margin-bottom": "4px"
}

def id(name):
    return f"{title}_{name}"

# Component styles
component_styles = {"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'}


# DESeq2 Sidebar layout with tooltips
sidebar = dbc.Container(
    children=charge_switch + [
        html.P(
            "DESeq2 App Generic Parameters:",
            style={"font-weight": "bold", "font-size": "1rem", "margin-bottom": "10px"}
        ),

        html.Div([
            dbc.Label("Name", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_name', value='', type='text', style=component_styles)
        ]),

        html.Div([
            dbc.Label("Comment", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_comment', value='', type='text', style=component_styles)
        ]),

        html.P(
            "DESeq2 App Specific Parameters:",
            style={"font-weight": "bold", "font-size": "1rem", "margin-bottom": "10px"}
        ),

        html.Div([
            dbc.Label("Cores", style=label_style),
            dbc.Select(
                id=f'{title}_cores',
                options=[{'label': str(x), 'value': x} for x in [1, 2, 4, 8]],
                value=4,
                style=component_styles
            )
        ]),

        html.Div([
            dbc.Label("RAM", style=label_style),
            dbc.Select(
                id=f'{title}_ram',
                options=[{'label': str(x), 'value': x} for x in [12, 24, 48]],
                value=12,
                style=component_styles
            )
        ]),

        html.Div([
            dbc.Label("Scratch", style=label_style),
            dbc.Select(
                id=f'{title}_scratch',
                options=[{'label': str(x), 'value': x} for x in [10, 50, 100]],
                value=10,
                style=component_styles
            )
        ]),

        html.Div([
            dbc.Label("Partition", style=label_style),
            dbc.Select(
                id=f'{title}_partition',
                options=[{'label': x, 'value': x} for x in ['employee', 'manyjobs', 'user']],
                value='employee',
                style=component_styles
            )
        ]),

        html.Div([
            dbc.Label("Process Mode", style=label_style),
            dbc.Select(
                id=f'{title}_process_mode',
                options=[{'label': 'DATASET', 'value': 'DATASET'}],
                value='DATASET',
                style=component_styles
            )
        ]),

        html.Div([
            dbc.Label("Samples", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_samples', value='', type='text', style=component_styles)
        ]),

        html.Div([
            dbc.Label("refBuild", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_refBuild', value='Homo_sapiens/GENCODE/GRC', type='text', style=component_styles)
        ]),

        html.Div([
            dbc.Label("refFeatureFile", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_refFeatureFile', value='genes.gtf', type='text', style=component_styles)
        ]),

        html.Div([
            dbc.Label("Feature Level", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_featureLevel',
                options=[{'label': 'gene', 'value': 'gene'}],
                value='gene',
                style=component_styles
            )
        ]),

        html.Div([
            dbc.Label("Grouping", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_grouping',
                options=[{'label': 'condition', 'value': 'condition'}],
                value='condition',
                style=component_styles
            ),
            dbc.Tooltip("required", target=f'{title}_grouping', placement="right")
        ]),

        html.Div([
            dbc.Label("Sample Group", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_sampleGroup',
                options=[
                    {"label": "Controls", "value": "Controls"},
                    {"label": "Hetero", "value": "Hetero"},
                    {"label": "Homo", "value": "Homo"}
                ],
                value='Hetero',
                style=component_styles
            ),
            dbc.Tooltip("required. sampleGroup should be different from refGroup", target=f'{title}_sampleGroup', placement="right")
        ]),

        html.Div([
            dbc.Label("Reference Group", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_refGroup',
                options=[
                    {"label": "Controls", "value": "Controls"},
                    {"label": "Hetero", "value": "Hetero"},
                    {"label": "Homo", "value": "Homo"}
                ],
                value='Controls',
                style=component_styles
            ),
            dbc.Tooltip("required. refGroup should be different from sampleGroup", target=f'{title}_refGroup', placement="right")
        ]),

        html.Div([
            dbc.Label("Only Comparison Groups in Heatmap", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_onlyCompGroupsHeatmap',
                options=[{"label": "True", "value": True}, {"label": "False", "value": False}],
                value=True,
                style=component_styles
            ),
            dbc.Tooltip("Only show the samples from comparison groups in heatmap", target=f'{title}_onlyCompGroupsHeatmap', placement="right")
        ]),

        html.Div([
            dbc.Label("grouping2", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_grouping2', value='', type='text', style=component_styles),
            dbc.Tooltip(
                "specify the column name of your secondary co-variate (factor or numeric, assuming there is one). Ensure the column name is in the format 'NAME [Factor]' or 'NAME [Numeric]'",
                target=f'{title}_grouping2',
                placement="right"
            )
        ]),

        html.Div([
            dbc.Label("backgroundExpression", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_backgroundExpression', value=10, type='number', style=component_styles),
            dbc.Tooltip("additive offset used in heatmaps", target=f'{title}_backgroundExpression', placement="right")
        ]),

        html.Div([
            dbc.Label("transcriptTypes", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_transcriptTypes',
                options=[
                    {"label": "protein_coding", "value": "protein_coding"},
                    {"label": "long_noncoding", "value": "long_noncoding"}
                ],
                value="protein_coding",
                style=component_styles
            )
        ]),

        html.Div([
            dbc.Label("runGO", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_runGO',
                options=[{"label": "True", "value": True}, {"label": "False", "value": False}],
                value=True,
                style=component_styles
            ),
            dbc.Tooltip("perform ORA and GSEA with Gene Ontology annotations", target=f'{title}_runGO', placement="right")
        ]),

        html.Div([
            dbc.Label("pValThreshGO", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_pValThreshGO', value=0.01, type='number', style=component_styles),
            dbc.Tooltip("pValue cut-off for ORA candidate gene selection", target=f'{title}_pValThreshGO', placement="right")
        ]),

        html.Div([
            dbc.Label("log2RatioThreshGO", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_log2RatioThreshGO', value=0, type='number', style=component_styles),
            dbc.Tooltip("log2 FoldChange cut-off for ORA candidate gene selection", target=f'{title}_log2RatioThreshGO', placement="right")
        ]),

        html.Div([
            dbc.Label("fdrThreshORA", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_fdrThreshORA', value=0.05, type='number', style=component_styles),
            dbc.Tooltip("adjusted pValue cut-off for GO terms in ORA", target=f'{title}_fdrThreshORA', placement="right")
        ]),

        html.Div([
            dbc.Label("fdrThreshGSEA", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_fdrThreshGSEA', value=0.05, type='number', style=component_styles),
            dbc.Tooltip("adjusted pValue cut-off for GO terms in GSEA", target=f'{title}_fdrThreshGSEA', placement="right")
        ]),

        html.Div([
            dbc.Label("specialOptions", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_specialOptions', value='', type='text', style=component_styles)
        ]),

        html.Div([
            dbc.Label("expressionName", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_expressionName', value='', type='text', style=component_styles)
        ]),

        html.Div([
            dbc.Label("Mail", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_mail', value='', type='email', style=component_styles)
        ]),

        html.Div([
            dbc.Label("Rversion", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_Rversion',
                options=[{"label": "Dev/R/4.4.2", "value": "Dev/R/4.4.2"}],
                value="Dev/R/4.4.2",
                style=component_styles
            )
        ]),

        dbc.Button("Submit", id=submitbutton_id(f'{title}_submit1'), n_clicks=0, style={"margin-top": "18px", 'borderBottom': '1px solid lightgrey'})
    ],
    style={"max-height": "62vh", "overflow-y": "auto", "overflow-x": "hidden"}
)




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
        dbc.Alert("", color="warning", id=id("alert-warning"), dismissable=True, is_open=False)
    ],
    style={"margin": "20px"}
)


####################################################################################
### C. Now we define the application callbacks (Step 1: Get data from the user) ####
####################################################################################

import re
from dash import html
from dash.dependencies import Input, Output

@app.callback(
    Output(id("alert-warning"), "children"),
    Output(id("alert-warning"), "is_open"),
    [
        Input(f"{title}_sampleGroup", "value"),
        Input(f"{title}_refGroup", "value"),
        Input(f"{title}_grouping2", "value"),
        Input(f"{title}_backgroundExpression", "value"),
        Input(f"{title}_pValThreshGO", "value"),
        Input(f"{title}_log2RatioThreshGO", "value"),
        Input(f"{title}_fdrThreshORA", "value"),
        Input(f"{title}_fdrThreshGSEA", "value"),
    ]
)
def check_image_based_warnings(sampleGroup, refGroup, grouping2,
                               backgroundExpression, pValThreshGO, log2RatioThreshGO,
                               fdrThreshORA, fdrThreshGSEA):
    warnings = []

    # 1. sampleGroup and refGroup must be different
    if sampleGroup and refGroup and sampleGroup == refGroup:
        warnings.append("Warning: sampleGroup should be different from refGroup.")

    # 2. grouping2 format: must match "NAME [Factor]" or "NAME [Numeric]"
    if grouping2:
        pattern = r".+\s*\[(Factor|Numeric)\]$"
        if not re.match(pattern, grouping2):
            warnings.append("Warning: grouping2 must be in the format 'NAME [Factor]' or 'NAME [Numeric]'.")

    # 3. backgroundExpression must be >= 0
    if backgroundExpression is not None and backgroundExpression < 0:
        warnings.append("Warning: backgroundExpression must be ≥ 0.")

    # 4. pValThreshGO, fdrThreshORA, fdrThreshGSEA must be > 0 and ≤ 1
    for val, name in [
        (pValThreshGO, "pValThreshGO"),
        (fdrThreshORA, "fdrThreshORA"),
        (fdrThreshGSEA, "fdrThreshGSEA"),
    ]:
        if val is None or not (0 < val <= 1):
            warnings.append(f"Warning: {name} must be > 0 and ≤ 1.")

    # 5. log2RatioThreshGO must be >= 0
    if log2RatioThreshGO is not None and log2RatioThreshGO < 0:
        warnings.append("Warning: log2RatioThreshGO must be ≥ 0.")

    # Output all warnings
    if warnings:
        return [html.Div(w) for w in warnings], True
    return "", False





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

@app.callback(
    [
        Output(id('name'), 'value'),
        Output(id('cores'), 'value'),
        Output(id('ram'), 'value'),
        Output(id('scratch'), 'value'),
        Output(id('onlyCompGroupsHeatmap'), 'value'),
        Output(id('transcriptTypes'), 'value'),
        Output(id('runGO'), 'value'),
        Output(id('pValThreshGO'), 'value'),
        Output(id('log2RatioThreshGO'), 'value'),
        Output(id('fdrThreshORA'), 'value'),
        Output(id('fdrThreshGSEA'), 'value'),
        Output(id('Rversion'), 'value'),
    ],
    [Input('entity', 'data')],
    [State('app_data', 'data')]
)
def populate_default_values(entity_data, app_data):
    name = entity_data.get("name", "Unknown") + "_DESeq2"
    return (
        name,
        4,
        12,
        10,
        True,
        "protein_coding",
        True,
        0.01,
        0,
        0.05,
        0.05,
        "Dev/R/4.4.2"
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
@app.callback(
    [
        Output(id("alert-fade-success"), "is_open"),
        Output(id("alert-fade-fail"), "is_open"),
    ],
    [
        Input(f'{title}_submit1', "n_clicks"),
    ],
    [
        State(id('name'), 'value'),
        State(id('comment'), 'value'),
        State(id('cores'), 'value'),
        State(id('ram'), 'value'),
        State(id('scratch'), 'value'),
        State(id('partition'), 'value'),
        State(id('process_mode'), 'value'),
        State(id('samples'), 'value'),
        State(id('refBuild'), 'value'),
        State(id('refFeatureFile'), 'value'),
        State(id('featureLevel'), 'value'),
        State(id('grouping'), 'value'),
        State(id('sampleGroup'), 'value'),
        State(id('refGroup'), 'value'),
        State(id('onlyCompGroupsHeatmap'), 'value'),
        State(id('grouping2'), 'value'),
        State(id('backgroundExpression'), 'value'),
        State(id('transcriptTypes'), 'value'),
        State(id('runGO'), 'value'),
        State(id('pValThreshGO'), 'value'),
        State(id('log2RatioThreshGO'), 'value'),
        State(id('fdrThreshORA'), 'value'),
        State(id('fdrThreshGSEA'), 'value'),
        State(id('specialOptions'), 'value'),
        State(id('expressionName'), 'value'),
        State(id('mail'), 'value'),
        State(id('Rversion'), 'value'),
        State("dataset", "data"),
        State('datatable', 'selected_rows'),
        State('token_data', 'data'),
        State('entity', 'data'),
        State('app_data', 'data'),
    ],
    prevent_initial_call=True
)
def submit_deseq_job(
    n_clicks, name, comment, cores, ram, scratch, partition, process_mode, samples,
    refBuild, refFeatureFile, featureLevel, grouping, sampleGroup, refGroup,
    onlyCompGroupsHeatmap, grouping2, backgroundExpression, transcriptTypes,
    runGO, pValThreshGO, log2RatioThreshGO, fdrThreshORA, fdrThreshGSEA,
    specialOptions, expressionName, mail, Rversion,
    dataset, selected_rows, token_data, entity_data, app_data
):
    try:
        dataset_df = pd.DataFrame(dtd(entity_data.get("full_api_response", {})))
        dataset_path = f"{SCRATCH_PATH}/{name}/dataset.tsv"
        os.makedirs(os.path.dirname(dataset_path), exist_ok=True)
        dataset_df.to_csv(dataset_path, sep="\t", index=False)

        param_dict = {
            'cores': cores,
            'ram': ram,
            'scratch': scratch,
            'partition': partition,
            'processMode': process_mode,
            'samples': samples,
            'refBuild': refBuild,
            'refFeatureFile': refFeatureFile,
            'featureLevel': featureLevel,
            'grouping': grouping,
            'sampleGroup': sampleGroup,
            'refGroup': refGroup,
            'onlyCompGroupsHeatmap': onlyCompGroupsHeatmap,
            'grouping2': grouping2,
            'backgroundExpression': backgroundExpression,
            'transcriptTypes': transcriptTypes,
            'runGO': runGO,
            'pValThreshGO': pValThreshGO,
            'log2RatioThreshGO': log2RatioThreshGO,
            'fdrThreshORA': fdrThreshORA,
            'fdrThreshGSEA': fdrThreshGSEA,
            'specialOptions': specialOptions,
            'expressionName': expressionName,
            'mail': mail,
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
            bundle exec sushi_fabric --class DESeq2 --dataset {dataset_path} --parameterset {param_path} --run \\
            --input_dataset_application {app_id} --project {project_id} --dataset_name {dataset_name} \\
            --mango_run_name {mango_run_name} --next_dataset_name {name}
        """
        print("[SUSHI BASH COMMAND]:", bash_command)
        return True, False

    except Exception as e:
        print("[SUSHI ERROR]:", str(e))
        return False, True
