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

title = 'STAR'

label_style = {
    "font-size": "0.85rem",   # Smaller text
    "margin-left": "6px",     # Indent the label a bit
    "margin-bottom": "4px"
}

def id(name):
    return f"{title}_{name}"

# Component styles
component_styles = {"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'}

# STAR Sidebar layout with tooltips
sidebar = dbc.Container(
    children=charge_switch + [

        html.Div([
            dbc.Label("Name", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_name', value='', type='text', style=component_styles)
        ]),

        html.Div([
            dbc.Label("Comment", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_comment', value='', type='text', style=component_styles)
        ]),

        html.P("STAR App Parameters:", style={"font-weight": "bold", "font-size": "1rem", "margin-bottom": "10px"}),

        html.Div([
            dbc.Label("Cores", style=label_style),
            dbc.Select(
                id=f'{title}_cores',
                options=[{'label': str(x), 'value': x} for x in [1, 2, 4, 8]],
                value=8,
                style=component_styles
            )
        ]),

        html.Div([
            dbc.Label("RAM", style=label_style),
            dbc.Input(id=f'{title}_ram', value=30, type='number', style=component_styles),
            dbc.Tooltip("30/40 GB is enough for human and mouse data, 60 GB for a hybrid genome. Only use the 200GB option for very large genomes (e.g. plants)", target=f'{title}_ram', placement="right")
        ]),

        html.Div([
            dbc.Label("Scratch", style=label_style),
            dbc.Input(id=f'{title}_scratch', value=100, type='number', style=component_styles)
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
                options=[{'label': 'SAMPLE', 'value': 'SAMPLE'}],
                value='SAMPLE',
                style=component_styles
            )
        ]),

        html.Div([
            dbc.Label("refBuild", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_refBuild', value='', type='text', style=component_styles),
            dbc.Tooltip("required! Select the reference genome you wish to map your reads to. Use the most recent version", target=f'{title}_refBuild', placement="right")
        ]),

        html.Div([
            dbc.Label("Paired", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_paired',
                options=[{"label": "True", "value": True}, {"label": "False", "value": False}],
                value=True,
                style=component_styles
            ),
            dbc.Tooltip("required! If this is not autopopulated, check which sequencing config was used to determine. If you only have R1, set to false. If you have R1 and R2, set to true.", target=f'{title}_paired', placement="right")
        ]),

        html.Div([
            dbc.Label("Strand Mode", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_strandMode',
                options=[{"label": x, "value": x} for x in ["none", "forward", "reverse", "both"]],
                value="both",
                style=component_styles
            ),
            dbc.Tooltip("required! If this is not autopopulated, check which library kit was used to determine. If you are unsure, ask your coach.", target=f'{title}_strandMode', placement="right")
        ]),

        html.Div([
            dbc.Label("refFeatureFile", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_refFeatureFile', value='genes.gtf', type='text', style=component_styles)
        ]),

        html.Div([
            dbc.Label("secondRef", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_secondRef', value='', type='text', style=component_styles),
            dbc.Tooltip("extra DNA/RNA sequences to use for alignment; needs to point to a file on FGCZ servers; ask for upload sushi@fgcz.ethz.ch", target=f'{title}_secondRef', placement="right")
        ]),

        html.Div([
            dbc.Label("cmdOptions", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_cmdOptions', value='--sjdbOverhang 150 --outFilterTy', type='text', style=component_styles)
        ]),

        html.Div([
            dbc.Label("getJunctions", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_getJunctions',
                options=[{"label": "True", "value": True}, {"label": "False", "value": False}],
                value=False,
                style=component_styles
            )
        ]),

        html.Div([
            dbc.Label("twopassMode", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_twopassMode',
                options=[{"label": "True", "value": True}, {"label": "False", "value": False}],
                value=False,
                style=component_styles
            ),
            dbc.Tooltip("Per-sample 2-pass mapping or 1-pass mapping in STAR. 2-pass mapping allows to detect more splice reads mapping to novel junctions.", target=f'{title}_twopassMode', placement="right")
        ]),

        html.P("fastp parameters:", style={"font-weight": "bold", "font-size": "1rem", "margin-top": "20px"}),

        html.Div([
            dbc.Label("trimAdapter", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_trimAdapter',
                options=[{"label": "True", "value": True}, {"label": "False", "value": False}],
                value=True,
                style=component_styles
            )
        ]),

        html.Div([
            dbc.Label("trim_front1", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_trim_front1', value=0, type='number', style=component_styles),
            dbc.Tooltip("Trimming how many bases in front for read1 (and read2), default is 0.", target=f'{title}_trim_front1', placement="right")
        ]),

        html.Div([
            dbc.Label("trim_tail1", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_trim_tail1', value=0, type='number', style=component_styles),
            dbc.Tooltip("Trimming how many bases in tail for read1 (and read2), default is 0.", target=f'{title}_trim_tail1', placement="right")
        ]),

        html.Div([
            dbc.Label("cut_front", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_cut_front',
                options=[{"label": "True", "value": True}, {"label": "False", "value": False}],
                value=False,
                style=component_styles
            ),
            dbc.Tooltip("Move a sliding window from front (5p) to tail, drop the bases in the window if its mean quality < threshold, stop otherwise.", target=f'{title}_cut_front', placement="right")
        ]),

        html.Div([
            dbc.Label("cut_front_window_size", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_cut_front_window_size', value=4, type='number', style=component_styles),
            dbc.Tooltip("Size of the window used by cut_front.", target=f'{title}_cut_front_window_size', placement="right")
        ]),

        html.Div([
            dbc.Label("cut_front_mean_quality", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_cut_front_mean_quality', value=20, type='number', style=component_styles),
            dbc.Tooltip("Quality threshold for bases to be dropped by cut_front.", target=f'{title}_cut_front_mean_quality', placement="right")
        ]),

        html.Div([
            dbc.Label("cut_tail", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_cut_tail',
                options=[{"label": "True", "value": True}, {"label": "False", "value": False}],
                value=False,
                style=component_styles
            ),
            dbc.Tooltip("Move a sliding window from tail (3p) to front, drop the bases in the window if mean quality < threshold, stop otherwise.", target=f'{title}_cut_tail', placement="right")
        ]),

        html.Div([
            dbc.Label("cut_tail_window_size", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_cut_tail_window_size', value=4, type='number', style=component_styles),
            dbc.Tooltip("Size of the window used by cut_tail.", target=f'{title}_cut_tail_window_size', placement="right")
        ]),

        html.Div([
            dbc.Label("cut_tail_mean_quality", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_cut_tail_mean_quality', value=20, type='number', style=component_styles),
            dbc.Tooltip("Quality threshold for bases to be dropped by cut_tail.", target=f'{title}_cut_tail_mean_quality', placement="right")
        ]),

        html.Div([
            dbc.Label("cut_right", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_cut_right',
                options=[{"label": "True", "value": True}, {"label": "False", "value": False}],
                value=False,
                style=component_styles
            ),
            dbc.Tooltip("Move one window from front to tail, if one window has mean quality < threshold, drop the bases in that window and everything to the right.", target=f'{title}_cut_right', placement="right")
        ]),

        html.Div([
            dbc.Label("cut_right_window_size", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_cut_right_window_size', value=4, type='number', style=component_styles),
            dbc.Tooltip("Size of the window used by cut_right.", target=f'{title}_cut_right_window_size', placement="right")
        ]),

        html.Div([
            dbc.Label("cut_right_mean_quality", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_cut_right_mean_quality', value=20, type='number', style=component_styles),
            dbc.Tooltip("Quality threshold for bases to be dropped by cut_right.", target=f'{title}_cut_right_mean_quality', placement="right")
        ]),

        html.Div([
            dbc.Label("average_qual", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_average_qual', value=0, type='number', style=component_styles),
            dbc.Tooltip("If one read average quality score < this, then this read/pair is discarded. Default 0 means no requirement.", target=f'{title}_average_qual', placement="right")
        ]),

        html.Div([
            dbc.Label("max_len1", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_max_len1', value=0, type='number', style=component_styles),
            dbc.Tooltip("If read1 is longer than max_len1, then trim read1 at its tail to make it as long as max_len1. Default 0 means no limitation.", target=f'{title}_max_len1', placement="right")
        ]),

        html.Div([
            dbc.Label("max_len2", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_max_len2', value=0, type='number', style=component_styles),
            dbc.Tooltip("If read2 is longer than max_len2, then trim read2 at its tail to make it as long as max_len2. Default 0 means no limitation. If two reads are present, the same will apply to read2.", target=f'{title}_max_len2', placement="right")
        ]),

        html.Div([
            dbc.Label("poly_x_min_len", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_poly_x_min_len', value=10, type='number', style=component_styles),
            dbc.Tooltip("The minimum length to detect polyX in the read tail. 10 by default.", target=f'{title}_poly_x_min_len', placement="right")
        ]),

        html.Div([
            dbc.Label("length_required", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_length_required', value=18, type='number', style=component_styles),
            dbc.Tooltip("Reads shorter than length_required will be discarded.", target=f'{title}_length_required', placement="right")
        ]),

        html.Div([
            dbc.Label("cmdOptionsFastp", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_cmdOptionsFastp', value='', type='text', style=component_styles)
        ]),


        html.P("UMI tools:", style={"font-weight": "bold", "font-size": "1rem", "margin-top": "20px"}),

        html.Div([
            dbc.Label("barcodePattern", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_barcodePattern', value='', type='text', style=component_styles),
            dbc.Tooltip("Optional for libraries which are including UMIs e.g. NNNNNNNN for TakRa SMARTer pico RNA kit v3", target=f'{title}_barcodePattern', placement="right")
        ]),

        html.P("Additional Parameters:", style={"font-weight": "bold", "font-size": "1rem", "margin-top": "20px"}),

        html.Div([
            dbc.Label("markDuplicates", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_markDuplicates',
                options=[{"label": "True", "value": True}, {"label": "False", "value": False}],
                value=False,
                style=component_styles
            ),
            dbc.Tooltip("Should duplicates be marked with picard. It is recommended for ChIP-seq and ATAC-seq data.", target=f'{title}_markDuplicates', placement="right")
        ]),

        html.Div([
            dbc.Label("specialOptions", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_specialOptions', value='', type='text', style=component_styles)
        ]),

        html.Div([
            dbc.Label("mail", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_mail', value='', type='email', style=component_styles)
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
        Output(id('paired'), 'value'),
        Output(id('strandMode'), 'value'),
        Output(id('refFeatureFile'), 'value'),
        Output(id('twopassMode'), 'value'),
        Output(id('trimAdapter'), 'value'),
        Output(id('cut_front'), 'value'),
        Output(id('cut_tail'), 'value'),
        Output(id('cut_right'), 'value'),
        Output(id('average_qual'), 'value'),
        Output(id('length_required'), 'value'),
        Output(id('refBuild'), 'value'),
    ],
    [Input('entity', 'data')],
    [State('app_data', 'data')]
)
def populate_default_values(entity_data, app_data):
    name = entity_data.get("name", "Unknown") + "_STAR"
    return (
        name,
        8,
        30,
        100,
        True,
        "both",
        "genes.gtf",
        False,
        True,
        False,
        False,
        False,
        0,
        18,
        "ToDo"
    )


##############################################################################################
##### C. Check user inputs for invalid values (Step 1: Retrieve data from the user)      #####
##############################################################################################


@app.callback(
    Output(id("alert-warning"), "children"),
    Output(id("alert-warning"), "is_open"),
    [
        Input(id("refBuild"), "value"),
        Input(id("paired"), "value"),
        Input(id("strandMode"), "value"),

        Input(id("trim_front1"), "value"),
        Input(id("trim_tail1"), "value"),
        Input(id("cut_front_window_size"), "value"),
        Input(id("cut_tail_window_size"), "value"),
        Input(id("cut_right_window_size"), "value"),

        Input(id("cut_front_mean_quality"), "value"),
        Input(id("cut_tail_mean_quality"), "value"),
        Input(id("cut_right_mean_quality"), "value"),

        Input(id("average_qual"), "value"),
        Input(id("length_required"), "value"),
        Input(id("max_len1"), "value"),
        Input(id("max_len2"), "value"),
        Input(id("poly_x_min_len"), "value"),
    ]
)
def check_warnings(refBuild, paired, strandMode,
                        trim_front1, trim_tail, cut_front_ws, cut_tail_ws, cut_right_ws,
                        cut_front_q, cut_tail_q, cut_right_q,
                        avg_qual, length_required, max_len1, max_len2, poly_x_min_len):
    """
    Validate input settings for read preprocessing and reference alignment and return relevant warnings.

    This Dash callback checks for common input issues related to reference genome selection, strand mode, 
    and various read trimming or filtering thresholds. It alerts the user if required fields are missing 
    or if values are out of acceptable ranges.

    Args:
        refBuild (str): Selected reference genome build.
        paired (str or bool): Whether the reads are paired-end (typically True/False or string equivalent).
        strandMode (str): Selected strand-specific alignment mode.
        trim_front1 (int): Number of bases to trim from the front of read 1.
        trim_tail (int): Number of bases to trim from the tail of read 1.
        cut_front_ws (int): Window size for quality trimming from the front.
        cut_tail_ws (int): Window size for quality trimming from the tail.
        cut_right_ws (int): Window size for quality trimming from the right.
        cut_front_q (int): Minimum average quality required in the front trimming window.
        cut_tail_q (int): Minimum average quality required in the tail trimming window.
        cut_right_q (int): Minimum average quality required in the right trimming window.
        avg_qual (int): Minimum average read quality required.
        length_required (int): Minimum read length to keep after trimming.
        max_len1 (int): Maximum allowed length for read 1.
        max_len2 (int): Maximum allowed length for read 2.
        poly_x_min_len (int): Minimum length of polyX stretch to trigger trimming.

    Returns:
        tuple:
            - list[html.Div] or str: List of warning messages wrapped in Dash `html.Div` components, or an empty string if no warnings.
            - bool: True if any warnings are detected (to open the alert), False otherwise.
    """
    warnings = []

    # 1. refBuild required
    if not refBuild:
        warnings.append("Warning: refBuild is required. Please select a reference genome.")

    # 2. strandMode required
    if not strandMode:
        warnings.append("Warning: strandMode is required when paired is set to true.")

    # 5. read quality/length values must be ≥ 0
    for val, name in [
        (avg_qual, "average_qual"),
        (length_required, "length_required"),
        (max_len1, "max_len1"),
        (max_len2, "max_len2"),
        (poly_x_min_len, "poly_x_min_len"),
    ]:
        if val is not None and val < 0:
            warnings.append(f"Warning: {name} must be ≥ 0.")

    if warnings:
        return [html.Div(w) for w in warnings], True
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
    [Input("Submit", "n_clicks")],
    [
        State(id('name'), 'value'),
        State(id('comment'), 'value'),
        State(id('cores'), 'value'),
        State(id('ram'), 'value'),
        State(id('scratch'), 'value'),
        State(id('partition'), 'value'),
        State(id('process_mode'), 'value'),
        State(id('refBuild'), 'value'),
        State(id('paired'), 'value'),
        State(id('strandMode'), 'value'),
        State(id('refFeatureFile'), 'value'),
        State(id('secondRef'), 'value'),
        State(id('cmdOptions'), 'value'),
        State(id('getJunctions'), 'value'),
        State(id('twopassMode'), 'value'),
        State(id('trimAdapter'), 'value'),
        State(id('trim_front1'), 'value'),
        State(id('trim_tail1'), 'value'),
        State(id('cut_front'), 'value'),
        State(id('cut_front_window_size'), 'value'),
        State(id('cut_front_mean_quality'), 'value'),
        State(id('cut_tail'), 'value'),
        State(id('cut_tail_window_size'), 'value'),
        State(id('cut_tail_mean_quality'), 'value'),
        State(id('cut_right'), 'value'),
        State(id('cut_right_window_size'), 'value'),
        State(id('cut_right_mean_quality'), 'value'),
        State(id('average_qual'), 'value'),
        State(id('max_len1'), 'value'),
        State(id('max_len2'), 'value'),
        State(id('poly_x_min_len'), 'value'),
        State(id('length_required'), 'value'),
        State(id('cmdOptionsFastp'), 'value'),
        State(id('barcodePattern'), 'value'),
        State(id('markDuplicates'), 'value'),
        State(id('specialOptions'), 'value'),
        State(id('mail'), 'value'),
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
def submit_star_job(
    n_clicks, name, comment, cores, ram, scratch, partition, process_mode,
    refBuild, paired, strandMode, refFeatureFile, secondRef, cmdOptions, getJunctions, twopassMode,
    trimAdapter, trim_front1, trim_tail1, cut_front, cut_front_window_size, cut_front_mean_quality,
    cut_tail, cut_tail_window_size, cut_tail_mean_quality,
    cut_right, cut_right_window_size, cut_right_mean_quality,
    average_qual, max_len1, max_len2, poly_x_min_len, length_required,
    cmdOptionsFastp, barcodePattern, markDuplicates, specialOptions, mail,
    dataset, selected_rows, token_data, entity_data, app_data, url, charge_run
):

    """
    Submit a STAR job by generating required dataset and parameter files and invoking the Sushi backend.

    This Dash callback runs when the "Submit" button is clicked. It collects user-defined settings 
    from the sidebar, builds the dataset and parameters `.tsv` files, constructs a bash command to 
    execute the STAR job via the Sushi framework, and returns success or failure alerts.

    Args:
        n_clicks (int): Number of times the "Submit" button has been clicked.
        name (str): Name of the STAR job.
        comment (str): Optional user comment or job description.
        cores (int): Number of CPU cores to request.
        ram (int): Requested RAM (in GB).
        scratch (int): Requested scratch disk space (in GB).
        partition (str): HPC partition or queue for job submission.
        process_mode (str): Execution mode (e.g., test or production).
        refBuild (str): Reference genome build.
        paired (str or bool): Whether sequencing data is paired-end.
        strandMode (str): Strand-specific mode for alignment.
        refFeatureFile (str): Path or ID of the reference feature file.
        secondRef (str): Optional secondary reference file.
        cmdOptions (str): Additional command-line options for STAR.
        getJunctions (str): Whether to extract splice junctions.
        twopassMode (str): Enable STAR two-pass mode.
        trimAdapter (str): Whether to trim adapter sequences.
        trim_front1 (int): Number of bases to trim from the start of read 1.
        trim_tail1 (int): Number of bases to trim from the end of read 1.
        cut_front (str): Enable quality trimming from the front.
        cut_front_window_size (int): Window size for trimming front bases.
        cut_front_mean_quality (int): Quality threshold for trimming front.
        cut_tail (str): Enable quality trimming from the tail.
        cut_tail_window_size (int): Window size for trimming tail bases.
        cut_tail_mean_quality (int): Quality threshold for trimming tail.
        cut_right (str): Enable quality trimming from the right.
        cut_right_window_size (int): Window size for trimming right-end bases.
        cut_right_mean_quality (int): Quality threshold for trimming right.
        average_qual (int): Minimum average read quality.
        max_len1 (int): Maximum length allowed for read 1.
        max_len2 (int): Maximum length allowed for read 2.
        poly_x_min_len (int): Minimum polyX length to trigger trimming.
        length_required (int): Minimum read length after trimming.
        cmdOptionsFastp (str): Additional options for Fastp preprocessing.
        barcodePattern (str): Optional barcode pattern for demultiplexing.
        markDuplicates (str): Whether to mark duplicate reads.
        specialOptions (str): Special execution flags or custom options.
        mail (str): Email address to send job notifications.
        dataset (list): Dataset loaded in the frontend table.
        selected_rows (list): Selected row indices from the dataset table.
        token_data (dict): Authentication token information.
        entity_data (dict): Metadata about the user or project.
        app_data (dict): Metadata specific to the STAR app instance.

    Returns:
        tuple:
            - bool: True if job submission succeeded (shows success alert).
            - bool: True if job submission failed (shows failure alert).
    """


    try:
        dataset_df = pd.DataFrame(dtd(entity_data.get("full_api_response", {})))
        dataset_path = f"{SCRATCH_PATH}/{name}/dataset.tsv"
        os.makedirs(os.path.dirname(dataset_path), exist_ok=True)
        dataset_df.to_csv(dataset_path, sep="\t", index=False)

        param_dict = {
            'name': name,
            'comment': comment,
            'cores': cores,
            'ram': ram,
            'scratch': scratch,
            'partition': partition,
            'processMode': process_mode,
            'refBuild': refBuild,
            'paired': paired,
            'strandMode': strandMode,
            'refFeatureFile': refFeatureFile,
            'secondRef': secondRef,
            'cmdOptions': cmdOptions,
            'getJunctions': getJunctions,
            'twopassMode': twopassMode,
            'trimAdapter': trimAdapter,
            'trim_front1': trim_front1,
            'trim_tail1': trim_tail1,
            'cut_front': cut_front,
            'cut_front_window_size': cut_front_window_size,
            'cut_front_mean_quality': cut_front_mean_quality,
            'cut_tail': cut_tail,
            'cut_tail_window_size': cut_tail_window_size,
            'cut_tail_mean_quality': cut_tail_mean_quality,
            'cut_right': cut_right,
            'cut_right_window_size': cut_right_window_size,
            'cut_right_mean_quality': cut_right_mean_quality,
            'average_qual': average_qual,
            'max_len1': max_len1,
            'max_len2': max_len2,
            'poly_x_min_len': poly_x_min_len,
            'length_required': length_required,
            'cmdOptionsFastp': cmdOptionsFastp,
            'barcodePattern': barcodePattern,
            'markDuplicates': markDuplicates,
            'specialOptions': specialOptions,
            'mail': mail
        }

        param_df = pd.DataFrame({"col1": list(param_dict.keys()), "col2": list(param_dict.values())})
        param_path = f"{SCRATCH_PATH}/{name}/parameters.tsv"
        os.makedirs(os.path.dirname(param_path), exist_ok=True)
        param_df.to_csv(param_path, sep="\t", index=False, header=False)

        app_id = app_data.get("id", "")
        project_id = "2220"

        # Update charge_run based on its value
        if charge_run and project_id:
            charge_run = [project_id]

        dataset_name = entity_data.get("name", "")
        mango_run_name = "None"
        bash_command = f"""
            bundle exec sushi_fabric --class STAR --dataset {dataset_path} --parameterset {param_path} --run \\
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
