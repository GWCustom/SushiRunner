from dash import html, dcc, ctx
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from generic.callbacks import app
import dash_daq as daq
from bfabric_web_apps.utils.components import charge_switch
import pandas as pd 
from dash.dash_table import DataTable
import bfabric_web_apps
from bfabric_web_apps import (
    SCRATCH_PATH,
    run_main_job
)
from sushi_utils.dataset_utils import dataset_to_dictionary as dtd

from sushi_utils.component_utils import submitbutton_id
import os
import re  # for grouping2 format check

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

title = 'EdgeR'

label_style = {
    "font-size": "0.85rem",   # Smaller text
    "margin-left": "6px",     # Indent the label a bit
    "margin-bottom": "4px"
}

def id(name):
    return f"{title}_{name}"

# Component styles
component_styles = {"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'}
# Sidebar layout for EdgeR with tooltips

# Sidebar layout for EdgeR with tooltips (using existing IDs)
sidebar = dbc.Container(
    children=charge_switch + [
        html.P(
            "EdgeR App Generic Parameters:",
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
            "EdgeR App Specific Parameters:",
            style={"font-weight": "bold", "font-size": "1rem", "margin-bottom": "10px"}
        ),

        # Cores (no tooltip)
        html.Div([
            dbc.Label("Cores", style=label_style),
            dbc.Select(
                id=f'{title}_cores',
                options=[{'label': str(x), 'value': x} for x in [1, 2, 4, 8]],
                style={"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'}
            )
        ]),

        # RAM (no tooltip)
        html.Div([
            dbc.Label("RAM", style=label_style),
            dbc.Select(
                id=f'{title}_ram',
                options=[{'label': str(x), 'value': x} for x in [16, 32, 64]],
                style={"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'}
            )
        ]),

        # Scratch (no tooltip)
        html.Div([
            dbc.Label("Scratch", style=label_style),
            dbc.Select(
                id=f'{title}_scratch',
                options=[{'label': str(x), 'value': x} for x in [10, 50, 100]],
                style={"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'}
            )
        ]),

        # Partition (no tooltip)
        html.Div([
            dbc.Label("Partition", style=label_style),
            dbc.Select(
                id=f'{title}_partition',
                options=[{'label': x, 'value': x} for x in ['employee', 'manyjobs', 'user']],
                style={"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'}
            )
        ]),

        # Process Mode (no tooltip)
        html.Div([
            dbc.Label("Process Mode", style=label_style),
            dbc.Select(
                id=f'{title}_process_mode',
                options=[{'label': x, 'value': x} for x in ['DATASET']],
                style={"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'}
            )
        ]),


        # refBuild (no tooltip)
        html.Div([
            dbc.Label("refBuild", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_refBuild', value='', type='text', style=component_styles)
        ]),

        # refFeatureFile (no tooltip)
        html.Div([
            dbc.Label("refFeatureFile", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_refFeatureFile', value='', type='text', style=component_styles)
        ]),

        # Feature Level (no tooltip)
        html.Div([
            dbc.Label("Feature Level", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_featureLevel',
                options=[{"label": "Gene", "value": "Gene"}, {"label": "Isoform", "value": "Isoform"}],
                value="Gene",
                style=component_styles
            )
        ]),

        # Test Method (no tooltip)
        html.Div([
            dbc.Label("Test Method", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_testMethod',
                options=[{"label": "glm", "value": "glm"}, {"label": "exactTest", "value": "exactTest"}],
                value="glm",
                style=component_styles
            )
        ]),

        # deTest with tooltip (target is the same as the select component's id)
        html.Div([
            dbc.Label("deTest", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_deTest',
                options=[{"label": "QL", "value": "QL"},
                         {"label": "LR", "value": "LR"}],
                value="QL",
                style=component_styles
            ),
            dbc.Tooltip(
                "This option only works for glm method. Quasi-likelihood (QL) F-test or likelihood ratio (LR) test. LR is preferred for single-cell data.",
                target=f'{title}_deTest',
                placement="right"
            )
        ]),

        # Grouping with tooltip
        html.Div([
            dbc.Label("Grouping", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_grouping',
                options=[{"label": "condition", "value": "condition"}],
                value="condition",
                style=component_styles
            ),
            dbc.Tooltip(
                "required",
                target=f'{title}_grouping',
                placement="right"
            )
        ]),

        # Sample Group with tooltip
        html.Div([
            dbc.Label("Sample Group", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_sampleGroup',
                options=[
                    {"label": "please select", "value": "please_select"},
                    {"label": "Controls", "value": "Controls"},
                    {"label": "Hetero", "value": "Hetero"},
                    {"label": "Homo", "value": "Homo"}
                ],
                value="please_select",
                style=component_styles
            ),
            dbc.Tooltip(
                "required. sampleGroup should be different from refGroup",
                target=f'{title}_sampleGroup',
                placement="right"
            )
        ]),

        # Sample Group Baseline with tooltip
        html.Div([
            dbc.Label("Sample Group Baseline", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_sampleGroupBaseline',
                options=[
                    {"label": "please select", "value": "please_select"},
                    {"label": "Controls", "value": "Controls"},
                    {"label": "Hetero", "value": "Hetero"},
                    {"label": "Homo", "value": "Homo"}
                ],
                value="please_select",
                style=component_styles
            ),
            dbc.Tooltip(
                "select the baseline for sampleGroup if you have",
                target=f'{title}_sampleGroupBaseline',
                placement="right"
            )
        ]),

        # Reference Group with tooltip
        html.Div([
            dbc.Label("Reference Group", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_refGroup',
                options=[
                    {"label": "please select", "value": "please_select"},
                    {"label": "Controls", "value": "Controls"},
                    {"label": "Hetero", "value": "Hetero"},
                    {"label": "Homo", "value": "Homo"}
                ],
                value="please_select",
                style=component_styles
            ),
            dbc.Tooltip(
                "required. refGroup should be different from sampleGroup",
                target=f'{title}_refGroup',
                placement="right"
            )
        ]),

        # Reference Group Baseline with tooltip
        html.Div([
            dbc.Label("Reference Group Baseline", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_refGroupBaseline',
                options=[
                    {"label": "please select", "value": "please_select"},
                    {"label": "Controls", "value": "Controls"},
                    {"label": "Hetero", "value": "Hetero"},
                    {"label": "Homo", "value": "Homo"}
                ],
                value="please_select",
                style=component_styles
            ),
            dbc.Tooltip(
                "select the baseline for refGroup if you have",
                target=f'{title}_refGroupBaseline',
                placement="right"
            )
        ]),

        # Only Comparison Groups in Heatmap with tooltip
        html.Div([
            dbc.Label("Only Comparison Groups in Heatmap", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_onlyCompGroupsHeatmap',
                options=[
                    {"label": "True", "value": True},
                    {"label": "False", "value": False}
                ],
                value=True,
                style=component_styles
            ),
            dbc.Tooltip(
                "only show the samples from comparison groups in heatmap",
                target=f'{title}_onlyCompGroupsHeatmap',
                placement="right"
            )
        ]),

        # Normalization Method with tooltip
        html.Div([
            dbc.Label("Normalization Method", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_normMethod',
                options=[
                    {"label": "TTM", "value": "TTM"},
                    {"label": "RLE", "value": "RLE"},
                    {"label": "upperQuartile", "value": "upperQuartile"},
                    {"label": "None", "value": "None"}
                ],
                value="TTM",
                style=component_styles
            ),
            dbc.Tooltip(
                "see http://bioconductor.org/packages/edgeR/",
                target=f'{title}_normMethod',
                placement="right"
            )
        ]),

        # grouping2 with tooltip
        html.Div([
            dbc.Label("grouping2", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_grouping2', value='', type='text', style=component_styles),
            dbc.Tooltip(
                "specify the column name of your secondary co-variate (factor or numeric, assuming there is one). Ensure the column name is in the format 'NAME [Factor]' or 'NAME [Numeric]'",
                target=f'{title}_grouping2',
                placement="right"
            )
        ]),

        # backgroundExpression with tooltip
        html.Div([
            dbc.Label("backgroundExpression", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_backgroundExpression', value='', type='text', style=component_styles),
            dbc.Tooltip(
                "counts to be added to shrink estimated log2 ratios",
                target=f'{title}_backgroundExpression',
                placement="right"
            )
        ]),

        # transcriptTypes (no tooltip)
        html.Div([
            dbc.Label("transcriptTypes", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_transcriptTypes',
                options=[
                    {"label": "Controls", "value": "Controls"},
                    {"label": "Hetero", "value": "Hetero"},
                    {"label": "Homo", "value": "Homo"}
                ],
                value="Controls",
                style=component_styles
            )
        ]),

        # pValuesHighlightThresh with tooltip
        html.Div([
            dbc.Label("pValuesHighlightThresh", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_pValuesHighlightThresh', value=0.01, type='number', style=component_styles),
            dbc.Tooltip(
                "pValue cut-off for highlighting candidate features in plots",
                target=f'{title}_pValuesHighlightThresh',
                placement="right"
            )
        ]),

        # log2RatioHighlightThresh (pvalCut) with tooltip
        html.Div([
            dbc.Label("log2RatioHighlightThresh", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_pvalCut', value=0.05, type='number', style=component_styles),
            dbc.Tooltip(
                "log2 FoldChange cut-off for highlighting candidate features in plots",
                target=f'{title}_pvalCut',
                placement="right"
            )
        ]),

        # runGO with tooltip
        html.Div([
            dbc.Label("runGO", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_runGO',
                options=[{"label": "True", "value": True}, {"label": "False", "value": False}],
                value=True,
                style=component_styles
            ),
            dbc.Tooltip(
                "perform ORA and GSEA test with Gene Ontology annotations",
                target=f'{title}_runGO',
                placement="right"
            )
        ]),

        # pValTreshGo with tooltip
        html.Div([
            dbc.Label("pValTreshGo", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_pValTreshGo', value=0.01, type='number', style=component_styles),
            dbc.Tooltip(
                "pValue cut-off for ORA candidate gene selection",
                target=f'{title}_pValTreshGo',
                placement="right"
            )
        ]),

        # log2RatioTreshGo with tooltip
        html.Div([
            dbc.Label("log2RatioTreshGo", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_log2RatioTreshGo', value=0, type='number', style=component_styles),
            dbc.Tooltip(
                "log2 FoldChange cut-off for ORA candidate gene selection",
                target=f'{title}_log2RatioTreshGo',
                placement="right"
            )
        ]),

        # FDR Threshold for ORA with tooltip
        html.Div([
            dbc.Label("FDR Threshold for ORA", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_fdrThresholdForORA', value=0.05, type='number', style=component_styles),
            dbc.Tooltip(
                "adjusted pValue cut-off for GO terms in ORA",
                target=f'{title}_fdrThresholdForORA',
                placement="right"
            )
        ]),

        # FDR Threshold for GSEA with tooltip
        html.Div([
            dbc.Label("FDR Threshold for GSEA", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_fdrThresholdForGSEA', value=0.05, type='number', style=component_styles),
            dbc.Tooltip(
                "adjusted pValue cut-off for GO terms in GSEA",
                target=f'{title}_fdrThresholdForGSEA',
                placement="right"
            )
        ]),

        # specialOptions (no tooltip)
        html.Div([
            dbc.Label("specialOptions", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_specialOptions', value='', type='text', style=component_styles)
        ]),

        # expressionName (no tooltip)
        html.Div([
            dbc.Label("expressionName", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_expressionName', value='', type='text', style=component_styles)
        ]),

        # Mail (no tooltip)
        html.Div([
            dbc.Label("Mail", style=label_style),
            dbc.Input(
                id=f'{title}_mail',
                value='',
                type='email',
                style={"margin-bottom": "18px", "borderBottom": "1px solid lightgrey"}
            )
        ]),

        # R Version (no tooltip)
        html.Div([
            dbc.Label("R Version", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_Rversion',
                options=[{"label": "Dev/R/4.4.2", "value": "Dev/R/4.4.2"}],
                value="Dev/R/4.4.2",
                style=component_styles
            )
        ]),

    dbc.Button("Submit", id=submitbutton_id(f'{title}_submit1'), n_clicks=0, style={"margin-top": "18px", 'borderBottom': '1px solid lightgrey'})
], style={"max-height":"62vh", "overflow-y":"auto", "overflow-x":"hidden"})




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
        dbc.Alert("", color="danger", id=id("alert-warning"), dismissable=True, is_open=False)
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
        Output(id('normMethod'), 'value'),
        Output(id('transcriptTypes'), 'value'),
        Output(id('pValuesHighlightThresh'), 'value'),
        Output(id('pvalCut'), 'value'),
        Output(id('runGO'), 'value'),
        Output(id('pValTreshGo'), 'value'),
        Output(id('log2RatioTreshGo'), 'value'),
        Output(id('fdrThresholdForORA'), 'value'),
        Output(id('fdrThresholdForGSEA'), 'value'),
        Output(id('Rversion'), 'value')
    ],
    [Input("entity", "data")],
    [State("app_data", "data")]
)
def populate_default_values(entity_data, app_data):
    name = entity_data.get("name", "Unknown") + "_EdgeR"
    return (
        name,                      # EdgeR_name
        4,                         # EdgeR_cores
        15,                        # EdgeR_ram (default: first option from [15,32,64])
        10,                        # EdgeR_scratch (default: first option from [10,50,100])
        True,                      # EdgeR_onlyCompGroupsHeatmap
        "TTM",                     # EdgeR_normMethod (note: changed from TMM to TTM)
        "Controls",                # EdgeR_transcriptTypes
        0.01,                      # EdgeR_pValuesHighlightThresh
        0.05,                      # EdgeR_pvalCut (this corresponds to the log2 ratio highlight threshold)
        True,                      # EdgeR_runGO
        0.01,                      # EdgeR_pValTreshGo
        0,                         # EdgeR_log2RatioTreshGo
        0.05,                      # EdgeR_fdrThresholdForORA
        0.05,                      # EdgeR_fdrThresholdForGSEA
        "Dev/R/4.4.2"              # EdgeR_Rversion
    )


##############################################################################################
##### C. Check user inputs for invalid values (Step 1: Retrieve data from the user)      #####
##############################################################################################



@app.callback(
    Output(id("alert-warning"), "children"),
    Output(id("alert-warning"), "is_open"),
    [
        Input(f"{title}_sampleGroup", "value"),
        Input(f"{title}_sampleGroupBaseline", "value"),
        Input(f"{title}_refGroup", "value"),
        Input(f"{title}_refGroupBaseline", "value"),
        Input(f"{title}_grouping2", "value")
    ]
)
def check_warnings(sampleGroup, sampleGroupBaseline, refGroup, refGroupBaseline, grouping2):
    """
    Check user inputs for potential configuration issues and display warning messages in the UI.

    This Dash callback is triggered whenever the user modifies the sample groups or the grouping format 
    in the sidebar. It validates that the selected sample and reference groups are not identical, checks 
    for missing baseline selections, and ensures the grouping2 value follows the expected format.

    Args:
        sampleGroup (str): Name of the selected sample group.
        sampleGroupBaseline (str): Optional baseline for the sample group.
        refGroup (str): Name of the selected reference group.
        refGroupBaseline (str): Optional baseline for the reference group.
        grouping2 (str): Additional grouping variable, expected in the format 'NAME [Factor]' or 'NAME [Numeric]'.

    Returns:
        tuple:
            - list[html.Div] or str: List of warning messages as Dash `html.Div` components, or an empty string if no warnings.
            - bool: True if any warnings are present (to open the alert), False otherwise.
    """

    warnings = []
    # Check sampleGroup and refGroup; they should be different.
    if sampleGroup == refGroup and sampleGroup != "please_select":
        warnings.append("Warning: sampleGroup should be different from refGroup.")
    # Warning if baseline fields are empty (optional, per your spec).
    if not sampleGroupBaseline:
        warnings.append("Warning: Please select a baseline for sampleGroup if you have one.")
    if not refGroupBaseline:
        warnings.append("Warning: Please select a baseline for refGroup if you have one.")
    # Check grouping2 format (only if grouping2 is provided)
    if grouping2:
        # This regex requires at least one character, then a space (optional) and then "[Factor]" or "[Numeric]"
        # Define a regex pattern that matches strings like: "Something [Factor]" or "AnotherName [Numeric]"
        # Explanation of the pattern:
        # .+         → Matches one or more of any character except newline (ensures there is some name before the bracket)
        # \s*        → Matches zero or more whitespace characters (allows space or no space between name and bracket)
        # \[         → Matches the literal '[' character (escaped because '[' is special in regex)
        # (Factor|Numeric) → Matches either the word 'Factor' or 'Numeric'
        # \]$        → Matches the literal ']' at the end of the string (also escaped) and asserts that it's at the end of the line
        pattern = r".+\s*\[(Factor|Numeric)\]$"

        # re.match tries to match the pattern at the **beginning** of the string.
        # If the pattern matches, it returns a match object; otherwise, it returns None.
        if not re.match(pattern, grouping2):
            warnings.append("Warning: grouping2 must be in the format 'NAME [Factor]' or 'NAME [Numeric]'.")
    
    if warnings:
        # Return the warning messages as a list of <div> components, and set is_open to True.
        return [html.Div(w) for w in warnings], True
    else:
        return "", False


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
        Input("Submit", "n_clicks"),
    ],

    [
        State(id('name'), 'value'),
        State(id('comment'), 'value'),
        State(id('cores'), 'value'),
        State(id('ram'), 'value'),
        State(id('scratch'), 'value'),
        State(id('partition'), 'value'),
        State(id('process_mode'), 'value'),
        State(id('refBuild'), 'value'),
        State(id('refFeatureFile'), 'value'),
        State(id('featureLevel'), 'value'),
        State(id('testMethod'), 'value'),
        State(id('deTest'), 'value'),
        State(id('grouping'), 'value'),
        State(id('sampleGroup'), 'value'),
        State(id('sampleGroupBaseline'), 'value'),
        State(id('refGroup'), 'value'),
        State(id('refGroupBaseline'), 'value'),
        State(id('onlyCompGroupsHeatmap'), 'value'),
        State(id('normMethod'), 'value'),
        State(id('grouping2'), 'value'),
        State(id('backgroundExpression'), 'value'),
        State(id('transcriptTypes'), 'value'),
        State(id('pValuesHighlightThresh'), 'value'),
        State(id('pvalCut'), 'value'),
        State(id('runGO'), 'value'),
        State(id('pValTreshGo'), 'value'),
        State(id('log2RatioTreshGo'), 'value'),
        State(id('fdrThresholdForORA'), 'value'),
        State(id('fdrThresholdForGSEA'), 'value'),
        State(id('specialOptions'), 'value'),
        State(id('expressionName'), 'value'),
        State(id('mail'), 'value'),
        State(id('Rversion'), 'value'),
        State(id("dataset"), "data"),
        State('datatable', 'selected_rows'),
        State('token_data', 'data'),
        State('entity', 'data'),
        State('app_data', 'data'),
        State('url', 'search'),
        State("charge_run", "on"),
    ],
    prevent_initial_call=True
)
def submit_edger_job(
    n_clicks, name, comment, cores, ram, scratch, partition, process_mode,
    refBuild, refFeatureFile, featureLevel, testMethod, deTest, grouping, sampleGroup,
    sampleGroupBaseline, refGroup, refGroupBaseline, onlyCompGroupsHeatmap, normMethod,
    grouping2, backgroundExpression, transcriptTypes, pValuesHighlightThresh, pvalCut,
    runGO, pValTreshGo, log2RatioTreshGo, fdrThresholdForORA, fdrThresholdForGSEA,
    specialOptions, expressionName, mail, Rversion,
    dataset, selected_rows, token_data, entity_data, app_data, url, charge_run
):
    """
    Submit an EdgeR job by building dataset and parameter files, then invoking the Sushi backend.

    This Dash callback is triggered by the "Submit" button. It compiles job configuration settings 
    and selected dataset information into structured files, constructs a bash command to submit the job 
    via the Sushi framework, and returns alerts to indicate whether the submission was successful.

    Args:
        n_clicks (int): Number of times the "Submit" button has been clicked.
        name (str): Name of the EdgeR job.
        comment (str): Optional user comment or description.
        cores (int): Number of CPU cores requested.
        ram (int): Amount of RAM requested (in GB).
        scratch (int): Scratch disk space requested (in GB).
        partition (str): HPC partition/queue to submit the job to.
        process_mode (str): Mode in which the process should be executed.
        refBuild (str): Reference genome build.
        refFeatureFile (str): Feature annotation file.
        featureLevel (str): Level of genomic features to analyze (e.g., gene, transcript).
        testMethod (str): Statistical method used for differential expression testing.
        deTest (str): DE test configuration or mode.
        grouping (str): Primary grouping variable for DE analysis.
        sampleGroup (str): Group of samples being compared.
        sampleGroupBaseline (str): Baseline group for the sample group.
        refGroup (str): Reference group for comparison.
        refGroupBaseline (str): Baseline group for the reference group.
        onlyCompGroupsHeatmap (str): Whether to include only comparison groups in heatmap.
        normMethod (str): Normalization method used.
        grouping2 (str): Secondary grouping variable, must be in format 'NAME [Factor]' or 'NAME [Numeric]'.
        backgroundExpression (str): Expression background level setting.
        transcriptTypes (str): Types of transcripts to include.
        pValuesHighlightThresh (float): Threshold to highlight p-values in results.
        pvalCut (float): p-value cutoff for significance.
        runGO (str): Whether to run GO enrichment analysis.
        pValTreshGo (float): p-value threshold for GO analysis.
        log2RatioTreshGo (float): Log2 ratio threshold for GO analysis.
        fdrThresholdForORA (float): FDR threshold for ORA analysis.
        fdrThresholdForGSEA (float): FDR threshold for GSEA.
        specialOptions (str): Additional command-line options or flags.
        expressionName (str): Identifier for the expression matrix or experiment.
        mail (str): Email address for job status notifications.
        Rversion (str): Version of R to use for analysis.
        dataset (list): Dataset information from the frontend.
        selected_rows (list): Indices of selected rows in the dataset table.
        token_data (dict): Authentication token data.
        entity_data (dict): Metadata associated with the user or organization.
        app_data (dict): Metadata or configuration related to the EdgeR app.

    Returns:
        tuple:
            - bool: True if job submission succeeded (to open success alert).
            - bool: True if job submission failed (to open failure alert).
    """

    print(12)
    try:
        # Create the dataset file from the full API response
        dataset_df = pd.DataFrame(dtd(entity_data.get("full_api_response", {})))
        dataset_path = f"{SCRATCH_PATH}/{name}/dataset.tsv"
        os.makedirs(os.path.dirname(dataset_path), exist_ok=True)
        dataset_df.to_csv(dataset_path, sep="\t", index=False)

        # Build the parameter dictionary from the sidebar values
        param_dict = {
            'cores': cores,
            'ram': ram,
            'scratch': scratch,
            'partition': partition,
            'processMode': process_mode,
            'refBuild': refBuild,
            'refFeatureFile': refFeatureFile,
            'featureLevel': featureLevel,
            'testMethod': testMethod,
            'deTest': deTest,
            'grouping': grouping,
            'sampleGroup': sampleGroup,
            'sampleGroupBaseline': sampleGroupBaseline,
            'refGroup': refGroup,
            'refGroupBaseline': refGroupBaseline,
            'onlyCompGroupsHeatmap': onlyCompGroupsHeatmap,
            'normMethod': normMethod,
            'grouping2': grouping2,
            'backgroundExpression': backgroundExpression,
            'transcriptTypes': transcriptTypes,
            'pValuesHighlightThresh': pValuesHighlightThresh,
            'pvalCut': pvalCut,
            'runGO': runGO,
            'pValTreshGo': pValTreshGo,
            'log2RatioTreshGo': log2RatioTreshGo,
            'fdrThresholdForORA': fdrThresholdForORA,
            'fdrThresholdForGSEA': fdrThresholdForGSEA,
            'specialOptions': specialOptions,
            'expressionName': expressionName,
            'mail': mail,
            'Rversion': Rversion,
            'name': name,
            'comment': comment
        }

        # Write parameters to a TSV file
        param_df = pd.DataFrame({"col1": list(param_dict.keys()), "col2": list(param_dict.values())})
        param_path = f"{SCRATCH_PATH}/{name}/parameters.tsv"
        os.makedirs(os.path.dirname(param_path), exist_ok=True)
        param_df.to_csv(param_path, sep="\t", index=False, header=False)

        # Build the bash command for job submission
        app_id = app_data.get("id", "")
        project_id = "2220"

        # Update charge_run based on its value
        if charge_run and project_id:
            charge_run = [project_id]

        dataset_name = entity_data.get("name", "")
        mango_run_name = "None"
        bash_command = f"""
            bundle exec sushi_fabric --class EdgeR --dataset {dataset_path} --parameterset {param_path} --run \\
            --input_dataset_application {app_id} --project {project_id} --dataset_name {dataset_name} \\
            --mango_run_name {mango_run_name} --next_dataset_name {name}
        """
        print("[SUSHI BASH COMMAND]:", bash_command)

        run_main_job(
            files_as_byte_strings={},
            bash_commands=[bash_command],
            resource_paths={},
            attachment_paths={},
            token=url,
            service_id=bfabric_web_apps.SERVICE_ID,
            charge=charge_run
        )

        return True, False

    except Exception as e:
        print("[SUSHI ERROR]:", str(e))
        return False, True