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

title = 'FeatureCounts'

label_style = {
    "font-size": "0.85rem",   # Smaller text
    "margin-left": "6px",     # Indent the label a bit
    "margin-bottom": "4px"
}

def id(name):
    return f"{title}_{name}"

# Component styles
component_styles = {"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'}

# FeatureCounts Sidebar layout with tooltips
sidebar = dbc.Container(
    children=charge_switch + [
        html.P("FeatureCounts App Parameters:", style={"font-weight": "bold", "font-size": "1rem", "margin-bottom": "10px"}),

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
            dbc.Input(id=f'{title}_cores', value=8, type='number', style=component_styles)
        ]),

        html.Div([
            dbc.Label("RAM", style=label_style),
            dbc.Input(id=f'{title}_ram', value=20, type='number', style=component_styles)
        ]),

        html.Div([
            dbc.Label("Scratch", style=label_style),
            dbc.Input(id=f'{title}_scratch', value=10, type='number', style=component_styles)
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
            dbc.Input(id=f'{title}_refBuild', value='Homo_sapiens/GENCODE/GRC', type='text', style=component_styles),
            dbc.Tooltip("required", target=f'{title}_refBuild', placement="right")
        ]),

        html.Div([
            dbc.Label("Paired", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_paired',
                options=[{'label': 'True', 'value': True}, {'label': 'False', 'value': False}],
                value=True,
                style=component_styles
            ),
            dbc.Tooltip("required", target=f'{title}_paired', placement="right")
        ]),

        html.Div([
            dbc.Label("Strand Mode", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_strandMode',
                options=[{'label': x, 'value': x} for x in ['none', 'sense', 'antisense']],
                value='antisense',
                style=component_styles
            ),
            dbc.Tooltip("required", target=f'{title}_strandMode', placement="right")
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
            dbc.Label("gtfFeatureType", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_gtfFeatureType', value='exon', type='text', style=component_styles),
            dbc.Tooltip("which atomic features of the gtf should be used to define the meta-features; see featureLevel", target=f'{title}_gtfFeatureType', placement="right")
        ]),

        html.Div([
            dbc.Label("allowMultiOverlap", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_allowMultiOverlap',
                options=[{'label': 'True', 'value': True}, {'label': 'False', 'value': False}],
                value=True,
                style=component_styles
            ),
            dbc.Tooltip("count alignments that fall in a region where multiple features are annotated", target=f'{title}_allowMultiOverlap', placement="right")
        ]),

        html.Div([
            dbc.Label("countPrimaryAlignmentsOnly", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_countPrimaryAlignmentsOnly',
                options=[{'label': 'True', 'value': True}, {'label': 'False', 'value': False}],
                value=True,
                style=component_styles
            )
        ]),

        html.Div([
            dbc.Label("minFeatureOverlap", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_minFeatureOverlap', value=10, type='number', style=component_styles),
            dbc.Tooltip("minimum overlap of a read with a transcript feature", target=f'{title}_minFeatureOverlap', placement="right")
        ]),

        html.Div([
            dbc.Label("minMapQuality", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_minMapQuality', value=10, type='number', style=component_styles)
        ]),

        html.Div([
            dbc.Label("keepMultiHits", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_keepMultiHits',
                options=[{'label': 'True', 'value': True}, {'label': 'False', 'value': False}],
                value=True,
                style=component_styles
            )
        ]),

        html.Div([
            dbc.Label("ignoreDup", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_ignoreDup',
                options=[{'label': 'True', 'value': True}, {'label': 'False', 'value': False}],
                value=False,
                style=component_styles
            )
        ]),

        html.Div([
            dbc.Label("transcriptTypes", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_transcriptTypes',
                options=[
                    {"label": "protein_coding", "value": "protein_coding"},
                    {"label": "rRNA", "value": "rRNA"},
                    {"label": "tRNA", "value": "tRNA"},
                    {"label": "Mt_rRNA", "value": "Mt_rRNA"},
                    {"label": "Mt_tRNA", "value": "Mt_tRNA"},
                    {"label": "long_noncoding", "value": "long_noncoding"},
                    {"label": "short_noncoding", "value": "short_noncoding"},
                    {"label": "pseudogene", "value": "pseudogene"}
                ],
                value='protein_coding',
                style=component_styles
            )
        ]),

        html.Div([
            dbc.Label("secondRef", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_secondRef', value='', type='text', style=component_styles),
            dbc.Tooltip("extra DNA/RNA sequences to use for alignment; needs to point to a file on FGCZ servers; if the .fasta file has a corresponding .gtf file, this file needs to have the same base name, e.g. a file 'foo.fa' in folder /path/to/file/ requires a file 'foo.gtf' in the same folder in order for the gtf file to be used; ask for upload sushi@fgcz.ethz.ch.", target=f'{title}_secondRef', placement="right")
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
        Output(id('refBuild'), 'value'),
        Output(id('paired'), 'value'),
        Output(id('strandMode'), 'value'),
        Output(id('refFeatureFile'), 'value'),
        Output(id('featureLevel'), 'value'),
        Output(id('gtfFeatureType'), 'value'),
        Output(id('allowMultiOverlap'), 'value'),
        Output(id('countPrimaryAlignmentsOnly'), 'value'),
        Output(id('minFeatureOverlap'), 'value'),
        Output(id('minMapQuality'), 'value'),
        Output(id('keepMultiHits'), 'value'),
        Output(id('ignoreDup'), 'value'),
        Output(id('transcriptTypes'), 'value'),
    ],
    [Input('entity', 'data')],
    [State('app_data', 'data')]
)
def populate_default_values(entity_data, app_data):
    name = entity_data.get("name", "Unknown") + "_FeatureCounts"
    return (
        name,
        8,
        20,
        10,
        "Homo_sapiens/GENCODE/GRC",
        True,
        "antisense",
        "genes.gtf",
        "gene",
        "exon",
        True,
        True,
        10,
        10,
        True,
        False,
        "protein_coding"
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
        Input(id("minFeatureOverlap"), "value"),
        Input(id("minMapQuality"), "value"),
    ]
)
def check_featurecounts_warnings(refBuild, paired, strandMode, minFeatureOverlap, minMapQuality):
    """
    Validate required inputs and parameters for the FeatureCounts app and return relevant warnings.

    This Dash callback checks for missing or invalid input values related to the reference build, 
    read pairing, strand-specific mode, and numerical thresholds. It provides warnings to help 
    users ensure valid configuration before job submission.

    Args:
        refBuild (str): Selected reference genome build.
        paired (str or bool): Whether the reads are paired-end.
        strandMode (str): Strand-specific mode; should be 'sense' or 'antisense'.
        minFeatureOverlap (int): Minimum number of overlapping bases for a read to be assigned to a feature.
        minMapQuality (int): Minimum mapping quality threshold (not validated in this function).

    Returns:
        tuple:
            - list[html.Div] or str: List of warning messages wrapped in Dash `html.Div` components, or an empty string if no warnings.
            - bool: True if any warnings are present (to open the alert), False otherwise.
    """

    warnings = []

    # 1. refBuild required
    if not refBuild:
        warnings.append("Warning: refBuild is required. Please select a reference genome.")

    # 2. paired required
    if paired is None:
        warnings.append("Warning: paired is required. Please select true or false.")

    # 3. strandMode required
    if strandMode == "none":
        warnings.append("Warning: strandMode is required. Please select a mode (sense, antisense).")

    # 4. minFeatureOverlap must be ≥ 0
    if minFeatureOverlap is not None and minFeatureOverlap < 0:
        warnings.append("Warning: minFeatureOverlap must be ≥ 0.")

    # Output warnings
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
        State(id('strandMode'), 'value'),
        State(id('refFeatureFile'), 'value'),
        State(id('featureLevel'), 'value'),
        State(id('gtfFeatureType'), 'value'),
        State(id('allowMultiOverlap'), 'value'),
        State(id('countPrimaryAlignmentsOnly'), 'value'),
        State(id('minFeatureOverlap'), 'value'),
        State(id('minMapQuality'), 'value'),
        State(id('keepMultiHits'), 'value'),
        State(id('ignoreDup'), 'value'),
        State(id('transcriptTypes'), 'value'),
        State(id('secondRef'), 'value'),
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
def submit_featurecounts_job(
    n_clicks, name, comment, cores, ram, scratch, partition, process_mode, samples,
    refBuild, paired, strandMode, refFeatureFile, featureLevel, gtfFeatureType,
    allowMultiOverlap, countPrimaryAlignmentsOnly, minFeatureOverlap, minMapQuality,
    keepMultiHits, ignoreDup, transcriptTypes, secondRef, specialOptions, mail,
    dataset, selected_rows, token_data, entity_data, app_data
):
    """
    Submit a FeatureCounts job by generating dataset and parameter files and invoking the Sushi backend.

    This Dash callback is triggered by the "Submit" button. It collects all required job parameters from
    the sidebar inputs, creates `.tsv` files for the dataset and parameters, builds the corresponding 
    bash command to launch the FeatureCounts job via the Sushi system, and returns an alert indicating 
    whether the submission was successful.

    Args:
        n_clicks (int): Number of times the "Submit" button has been clicked.
        name (str): Name of the FeatureCounts job.
        comment (str): Optional description or annotation for the job.
        cores (int): Number of CPU cores to allocate.
        ram (int): Amount of RAM to allocate (in GB).
        scratch (int): Scratch disk space to allocate (in GB).
        partition (str): Name of the HPC partition (queue) for job submission.
        process_mode (str): Execution mode (e.g., standard, debug).
        samples (str): Sample IDs or configuration.
        refBuild (str): Reference genome build.
        paired (str or bool): Whether input reads are paired-end.
        strandMode (str): Strand-specific counting mode (e.g., sense, antisense).
        refFeatureFile (str): Path or identifier for the reference feature annotation file.
        featureLevel (str): Level of features to be counted (e.g., gene, transcript).
        gtfFeatureType (str): GTF feature type to use for read counting (e.g., exon).
        allowMultiOverlap (str): Whether to allow reads overlapping multiple features.
        countPrimaryAlignmentsOnly (str): Count only primary alignments if enabled.
        minFeatureOverlap (int): Minimum number of overlapping bases to count a read.
        minMapQuality (int): Minimum required mapping quality.
        keepMultiHits (str): Whether to include multi-mapped reads.
        ignoreDup (str): Whether to ignore duplicate reads.
        transcriptTypes (str): Types of transcripts to include in the analysis.
        secondRef (str): Optional secondary reference genome or annotation file.
        specialOptions (str): Any extra command-line options.
        mail (str): Email address for job status notifications.
        dataset (list): Dataset content from the UI.
        selected_rows (list): Selected dataset row indices.
        token_data (dict): Auth token and user session data.
        entity_data (dict): Metadata about the current user/project context.
        app_data (dict): Metadata related to the FeatureCounts application.

    Returns:
        tuple:
            - bool: True if the job was successfully submitted (shows success alert).
            - bool: True if the job submission failed (shows failure alert).
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
            'strandMode': strandMode,
            'refFeatureFile': refFeatureFile,
            'featureLevel': featureLevel,
            'gtfFeatureType': gtfFeatureType,
            'allowMultiOverlap': allowMultiOverlap,
            'countPrimaryAlignmentsOnly': countPrimaryAlignmentsOnly,
            'minFeatureOverlap': minFeatureOverlap,
            'minMapQuality': minMapQuality,
            'keepMultiHits': keepMultiHits,
            'ignoreDup': ignoreDup,
            'transcriptTypes': transcriptTypes,
            'secondRef': secondRef,
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
            bundle exec sushi_fabric --class FeatureCounts --dataset {dataset_path} --parameterset {param_path} --run \\
            --input_dataset_application {app_id} --project {project_id} --dataset_name {dataset_name} \\
            --mango_run_name {mango_run_name} --next_dataset_name {name}
        """
        print("[SUSHI BASH COMMAND]:", bash_command)
        return True, False

    except Exception as e:
        print("[SUSHI ERROR]:", str(e))
        return False, True
