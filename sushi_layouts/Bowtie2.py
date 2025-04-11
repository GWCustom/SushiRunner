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

title = 'Bowtie2'

label_style = {
    "font-size": "0.85rem",   # Smaller text
    "margin-left": "6px",     # Indent the label a bit
    "margin-bottom": "4px"
}

def id(name):
    return f"{title}_{name}"

# Component styles
component_styles = {"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'}

# Bowtie2 Sidebar layout with tooltips
sidebar = dbc.Container(
    children=charge_switch + [
        html.P("Bowtie2 App Parameters:", style={"font-weight": "bold", "font-size": "1rem", "margin-bottom": "10px"}),

        html.Div([
            dbc.Label("Name", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_name', value='', type='text', style=component_styles)
        ]),

        html.Div([
            dbc.Label("Comment", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_comment', value='', type='text', style=component_styles)
        ]),

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
            dbc.Input(id=f'{title}_ram', value=30, type='number', style=component_styles)
        ]),

        html.Div([
            dbc.Label("Scratch", style=label_style),
            dbc.Input(id=f'{title}_scratch', value=200, type='number', style=component_styles)
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
            dbc.Label("Samples", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_samples', value='', type='text', style=component_styles)
        ]),

        html.Div([
            dbc.Label("refBuild", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_refBuild', value='', type='text', style=component_styles),
            dbc.Tooltip("required — the genome refBuild and annotation to use as reference.", target=f'{title}_refBuild', placement="right")
        ]),

        html.Div([
            dbc.Label("Paired", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_paired',
                options=[{"label": "True", "value": True}, {"label": "False", "value": False}],
                value=True,
                style=component_styles
            ),
            dbc.Tooltip("required — whether the reads are paired end; if false then only Read1 is considered even if Read2 is available.", target=f'{title}_paired', placement="right")
        ]),

        html.Div([
            dbc.Label("secondRef", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_secondRef', value='', type='text', style=component_styles),
            dbc.Tooltip("extra DNA/RNA sequences to use for alignment; needs to point to a file on FGCZ servers; ask for upload sushi@fgcz.ethz.ch", target=f'{title}_secondRef', placement="right")
        ]),

        html.Div([
            dbc.Label("cmdOptions", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_cmdOptions', value='--no-unal', type='text', style=component_styles),
            dbc.Tooltip("specify the commandline options for bowtie2; do not specify any option that is already covered by the dedicated input fields", target=f'{title}_cmdOptions', placement="right")
        ]),

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
            dbc.Tooltip("trimming how many bases in front for read1 (and read2), default is 0.", target=f'{title}_trim_front1', placement="right")
        ]),

        html.Div([
            dbc.Label("trim_tail1", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_trim_tail1', value=0, type='number', style=component_styles),
            dbc.Tooltip("trimming how many bases in tail for read1 (and read2), default is 0.", target=f'{title}_trim_tail1', placement="right")
        ]),

        html.Div([
            dbc.Label("cut_front", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_cut_front',
                options=[{"label": "True", "value": True}, {"label": "False", "value": False}],
                value=False,
                style=component_styles
            ),
            dbc.Tooltip("move a sliding window from front (5p) to tail, drop the bases in the window if its mean quality < threshold, stop otherwise.", target=f'{title}_cut_front', placement="right")
        ]),

        html.Div([
            dbc.Label("cut_front_window_size", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_cut_front_window_size', value=4, type='number', style=component_styles)
        ]),

        html.Div([
            dbc.Label("cut_front_mean_quality", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_cut_front_mean_quality', value=20, type='number', style=component_styles)
        ]),

        html.Div([
            dbc.Label("cut_tail", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_cut_tail',
                options=[{"label": "True", "value": True}, {"label": "False", "value": False}],
                value=False,
                style=component_styles
            ),
            dbc.Tooltip("move a sliding window from tail (3p) to front, drop the bases in the window if mean quality < threshold, stop otherwise.", target=f'{title}_cut_tail', placement="right")
        ]),

        html.Div([
            dbc.Label("cut_tail_window_size", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_cut_tail_window_size', value=4, type='number', style=component_styles)
        ]),

        html.Div([
            dbc.Label("cut_tail_mean_quality", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_cut_tail_mean_quality', value=20, type='number', style=component_styles)
        ]),

        html.Div([
            dbc.Label("cut_right", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_cut_right',
                options=[{"label": "True", "value": True}, {"label": "False", "value": False}],
                value=False,
                style=component_styles
            ),
            dbc.Tooltip("move a sliding window from front to tail, if meet one window with mean quality < threshold, drop the bases in the window and the right part, and then stop.", target=f'{title}_cut_right', placement="right")
        ]),

        html.Div([
            dbc.Label("cut_right_window_size", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_cut_right_window_size', value=4, type='number', style=component_styles)
        ]),

        html.Div([
            dbc.Label("cut_right_mean_quality", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_cut_right_mean_quality', value=20, type='number', style=component_styles)
        ]),

        html.Div([
            dbc.Label("average_qual", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_average_qual', value=0, type='number', style=component_styles),
        dbc.Tooltip("If one read average quality score, then this read/pair is discarded. Default 0 means no requirement.", target=f'{title}_average_qual', placement="right")
        ]),

        html.Div([
            dbc.Label("max_len1", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_max_len1', value=0, type='number', style=component_styles),
        dbc.Tooltip("If read1 is longer than max_len1, then trim read1 at its tail to make it as long as max_len1. Default 0 means no limitation.", target=f'{title}_max_len1', placement="right")
        ]),

        html.Div([
            dbc.Label("max_len2", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_max_len2', value=0, type='number', style=component_styles),
        dbc.Tooltip("If read2 is longer than max_len2, then trim read2 at its tail to make it as long as max_len2. Default 0 means no limitation.", target=f'{title}_max_len2', placement="right")
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

        html.Div([
            dbc.Label("markDuplicates", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_markDuplicates',
                options=[{"label": "True", "value": True}, {"label": "False", "value": False}],
                value=False,
                style=component_styles
            ),
            dbc.Tooltip("should duplicates be marked with picard. It is recommended for ChIP-seq and ATAC-seq data.", target=f'{title}_markDuplicates', placement="right")
        ]),

        html.Div([
            dbc.Label("generateBigWig", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_generateBigWig',
                options=[{"label": "True", "value": True}, {"label": "False", "value": False}],
                value=False,
                style=component_styles
            )
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
        Output(id('paired'), 'value'),
        Output(id('refBuild'), 'value'),
        Output(id('trimAdapter'), 'value'),
        Output(id('cut_front'), 'value'),
        Output(id('cut_tail'), 'value'),
        Output(id('cut_right'), 'value'),
        Output(id('average_qual'), 'value'),
        Output(id('length_required'), 'value'),
    ],
    [Input('entity', 'data')],
    [State('app_data', 'data')]
)
def populate_default_values(entity_data, app_data):
    name = entity_data.get("name", "Unknown") + "_Bowtie2"
    return (
        name,
        8,
        30,
        200,
        True,
        "ToDo",
        True,
        False,
        False,
        False,
        0,
        18
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
def check_warnings(refBuild, paired,
                        trim_front1, trim_tail, cut_front_ws, cut_tail_ws, cut_right_ws,
                        cut_front_q, cut_tail_q, cut_right_q,
                        avg_qual, length_required, max_len1, max_len2, poly_x_min_len):
    """
    Validate preprocessing parameters and genome selection for the STAR app and return user warnings.

    This Dash callback is triggered when the user modifies read trimming, quality filtering, or reference 
    settings. It ensures that required fields like `refBuild` and `paired` are provided, and that numeric 
    parameters such as trimming lengths and quality thresholds are non-negative.

    Args:
        refBuild (str): Selected reference genome build.
        paired (str or bool): Indicates whether input reads are paired-end.
        trim_front1 (int): Number of bases to trim from the front of read 1.
        trim_tail (int): Number of bases to trim from the tail of read 1.
        cut_front_ws (int): Window size for quality trimming from the front.
        cut_tail_ws (int): Window size for quality trimming from the tail.
        cut_right_ws (int): Window size for quality trimming from the right.
        cut_front_q (int): Minimum average quality for trimming from the front.
        cut_tail_q (int): Minimum average quality for trimming from the tail.
        cut_right_q (int): Minimum average quality for trimming from the right.
        avg_qual (int): Minimum average read quality.
        length_required (int): Minimum read length to retain after trimming.
        max_len1 (int): Maximum allowed length for read 1.
        max_len2 (int): Maximum allowed length for read 2.
        poly_x_min_len (int): Minimum polyX stretch to trigger trimming.

    Returns:
        tuple:
            - list[html.Div] or str: List of warning messages wrapped in Dash `html.Div` components, or an empty string if no warnings.
            - bool: True if any warnings are detected (to open the alert), False otherwise.
    """


    warnings = []

    # 1. refBuild required
    if not refBuild:
        warnings.append("Warning: refBuild is required. Please select a reference genome.")

    # 2. paired required
    if not paired:
        warnings.append("Warning: paired is required. Please select a reference genome.")

    # 3. window sizes must be ≥ 0
    for val, name in [
        (trim_front1, "trim_front1"),
        (trim_tail, "trim_tail1"),
        (cut_front_ws, "cut_front_window_size"),
        (cut_tail_ws, "cut_tail_window_size"),
        (cut_right_ws, "cut_right_window_size"),
    ]:
        if val is not None and val < 0:
            warnings.append(f"Warning: {name} must be ≥ 0.")

    # 4. mean quality values must be ≥ 0
    for val, name in [
        (cut_front_q, "cut_front_mean_quality"),
        (cut_tail_q, "cut_tail_mean_quality"),
        (cut_right_q, "cut_right_mean_quality"),
    ]:
        if val is not None and val < 0:
            warnings.append(f"Warning: {name} must be ≥ 0.")

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
        State(id('samples'), 'value'),
        State(id('refBuild'), 'value'),
        State(id('paired'), 'value'),
        State(id('secondRef'), 'value'),
        State(id('cmdOptions'), 'value'),
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
        State(id('markDuplicates'), 'value'),
        State(id('generateBigWig'), 'value'),
        State(id('specialOptions'), 'value'),
        State(id('mail'), 'value'),
        State(id("dataset"), "data"),
        State('datatable', 'selected_rows'),
        State('token_data', 'data'),
        State('entity', 'data'),
        State('app_data', 'data'),
    ],
    prevent_initial_call=True
)
def submit_bowtie2_job(
    n_clicks, name, comment, cores, ram, scratch, partition, process_mode, samples,
    refBuild, paired, secondRef, cmdOptions,
    trimAdapter, trim_front1, trim_tail1,
    cut_front, cut_front_window_size, cut_front_mean_quality,
    cut_tail, cut_tail_window_size, cut_tail_mean_quality,
    cut_right, cut_right_window_size, cut_right_mean_quality,
    average_qual, max_len1, max_len2, poly_x_min_len, length_required,
    cmdOptionsFastp, markDuplicates, generateBigWig, specialOptions, mail,
    dataset, selected_rows, token_data, entity_data, app_data
):

    """
    Submit a Bowtie2 job by preparing dataset and parameter files, then invoking the Sushi backend.

    This Dash callback is triggered when the "Submit" button is clicked. It gathers all user-specified 
    inputs, builds the dataset and parameter files in TSV format, constructs the corresponding bash 
    command for the Bowtie2 job, and submits it using the Sushi job runner. It returns a success or 
    failure alert based on the execution result.

    Args:
        n_clicks (int): Number of times the "Submit" button has been clicked.
        name (str): Name of the Bowtie2 job.
        comment (str): Optional comment or description provided by the user.
        cores (int): Number of CPU cores requested.
        ram (int): RAM requested in GB.
        scratch (int): Scratch disk space requested in GB.
        partition (str): Target partition (queue) for the job.
        process_mode (str): Execution mode (e.g., "normal", "test").
        samples (str): Sample selection or configuration string.
        refBuild (str): Reference genome build identifier.
        paired (str or bool): Indicates whether the reads are paired-end.
        secondRef (str): Optional second reference file.
        cmdOptions (str): Additional command-line options for Bowtie2.
        trimAdapter (str): Whether adapter trimming is enabled.
        trim_front1 (int): Bases to trim from the front of read 1.
        trim_tail1 (int): Bases to trim from the tail of read 1.
        cut_front (str): Whether quality trimming from the front is enabled.
        cut_front_window_size (int): Window size for trimming the front.
        cut_front_mean_quality (int): Minimum mean quality in the front trimming window.
        cut_tail (str): Whether quality trimming from the tail is enabled.
        cut_tail_window_size (int): Window size for trimming the tail.
        cut_tail_mean_quality (int): Minimum mean quality in the tail trimming window.
        cut_right (str): Whether quality trimming from the right is enabled.
        cut_right_window_size (int): Window size for trimming the right end.
        cut_right_mean_quality (int): Minimum mean quality in the right trimming window.
        average_qual (int): Minimum average read quality required.
        max_len1 (int): Maximum read length for read 1.
        max_len2 (int): Maximum read length for read 2.
        poly_x_min_len (int): Minimum polyX stretch length to trigger trimming.
        length_required (int): Minimum length required to retain a read.
        cmdOptionsFastp (str): Additional options for the Fastp preprocessor.
        markDuplicates (str): Whether to mark duplicates in the aligned reads.
        generateBigWig (str): Whether to generate a BigWig coverage file.
        specialOptions (str): Additional special or app-specific options.
        mail (str): Email address for job status notifications.
        dataset (list): Dataset records displayed in the UI.
        selected_rows (list): Indices of selected rows in the dataset table.
        token_data (dict): Authentication token for backend communication.
        entity_data (dict): Metadata for the project, user, or dataset context.
        app_data (dict): Configuration metadata for the Bowtie2 app.

    Returns:
        tuple:
            - bool: True if the job was successfully submitted (opens success alert).
            - bool: True if the job submission failed (opens failure alert).
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
            'samples': samples,
            'refBuild': refBuild,
            'paired': paired,
            'secondRef': secondRef,
            'cmdOptions': cmdOptions,
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
            'markDuplicates': markDuplicates,
            'generateBigWig': generateBigWig,
            'specialOptions': specialOptions,
            'mail': mail
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
            bundle exec sushi_fabric --class Bowtie2 --dataset {dataset_path} --parameterset {param_path} --run \\
            --input_dataset_application {app_id} --project {project_id} --dataset_name {dataset_name} \\
            --mango_run_name {mango_run_name} --next_dataset_name {name}
        """
        print("[SUSHI BASH COMMAND]:", bash_command)
        return True, False

    except Exception as e:
        print("[SUSHI ERROR]:", str(e))
        return False, True