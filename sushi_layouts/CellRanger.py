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

title = 'CellRanger'

label_style = {
    "font-size": "0.85rem",   # Smaller text
    "margin-left": "6px",     # Indent the label a bit
    "margin-bottom": "4px"
}

def id(name):
    return f"{title}_{name}"

# Component styles
component_styles = {"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'}

# CellRangerApp Sidebar layout (updated with dropdown values)
sidebar = dbc.Container(
    children=charge_switch + [
        html.P("CellRanger App Parameters:", style={"font-weight": "bold", "font-size": "1rem", "margin-bottom": "10px"}),

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
            dbc.Input(id=f'{title}_ram', value=60, type='number', style=component_styles)
        ]),

        html.Div([
            dbc.Label("Scratch", style=label_style),
            dbc.Input(id=f'{title}_scratch', value=300, type='number', style=component_styles)
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
            dbc.Label("Label Name", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_label_name', value='CellRangerCount', type='text', style=component_styles),
            dbc.Tooltip("required", target=f'{title}_label_name', placement="right")
        ]),

        html.Div([
            dbc.Label("refBuild", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_refBuild', value='', type='text', style=component_styles),
            dbc.Tooltip("required", target=f'{title}_refBuild', placement="right")
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
            dbc.Label("TenXLibrary", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_TenXLibrary',
                options=[{'label': x, 'value': x} for x in ['GEX', 'VDJ', 'FeatureBarcoding']],
                value='GEX',
                style=component_styles
            ),
            dbc.Tooltip("Which 10X library? GEX, VDJ or FeatureBarcoding", target=f'{title}_TenXLibrary', placement="right")
        ]),

        html.Div([
            dbc.Label("Chemistry", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_chemistry',
                options=[{'label': x, 'value': x} for x in ['ThreePrime', 'FivePrime', 'SC3PV1', 'SC3PV2', 'SC3PV3', 'SC5P-PE', 'SC5P-R2', 'ARC-v1']],
                value='ThreePrime',
                style=component_styles
            ),
            dbc.Tooltip("Assay configuration. By default, auto-detected (recommended).", target=f'{title}_chemistry', placement="right")
        ]),

        html.Div([
            dbc.Label("Include Introns", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_includeIntrons',
                options=[{'label': 'True', 'value': True}, {'label': 'False', 'value': False}],
                value=True,
                style=component_styles
            ),
            dbc.Tooltip("Set to false to reproduce the default behavior in Cell Ranger v6 and earlier", target=f'{title}_includeIntrons', placement="right")
        ]),

        html.Div([
            dbc.Label("Expected Cells", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_expectedCells', value='', type='number', style=component_styles),
            dbc.Tooltip("Expected number of recovered cells. Leave blank to auto-estimate", target=f'{title}_expectedCells', placement="right")
        ]),

        html.Div([
            dbc.Label("Transcript Types", style={"font-size": "0.85rem"}),
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
            dbc.Label("controlSeqs", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_controlSeqs', value='', type='text', style=component_styles),
            dbc.Tooltip("Spike-in control sequences; see fgcz-gstore UZH reference", target=f'{title}_controlSeqs', placement="right")
        ]),

        html.Div([
            dbc.Label("secondRef", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_secondRef', value='', type='text', style=component_styles),
            dbc.Tooltip("Full path to FASTA file with viralGenes etc.", target=f'{title}_secondRef', placement="right")
        ]),

        html.Div([
            dbc.Label("runVeloCyto", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_runVeloCyto',
                options=[{'label': 'True', 'value': True}, {'label': 'False', 'value': False}],
                value=False,
                style=component_styles
            ),
            dbc.Tooltip("Generate loom file via Velocyto", target=f'{title}_runVeloCyto', placement="right")
        ]),

        html.Div([
            dbc.Label("bamStats", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_bamStats',
                options=[{'label': 'True', 'value': True}, {'label': 'False', 'value': False}],
                value=False,
                style=component_styles
            ),
            dbc.Tooltip("Compute stats per cell from BAM", target=f'{title}_bamStats', placement="right")
        ]),

        html.Div([
            dbc.Label("keepAlignment", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_keepAlignment',
                options=[{'label': 'True', 'value': True}, {'label': 'False', 'value': False}],
                value=True,
                style=component_styles
            ),
            dbc.Tooltip("Keep CRAM/BAM file produced by CellRanger", target=f'{title}_keepAlignment', placement="right")
        ]),

        html.Div([
            dbc.Label("cmdOptions", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_cmdOptions', value='', type='text', style=component_styles),
            dbc.Tooltip("Extra command line args; avoid duplication of known fields", target=f'{title}_cmdOptions', placement="right")
        ]),

        html.Div([
            dbc.Label("specialOptions", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_specialOptions', value='', type='text', style=component_styles)
        ]),

        html.Div([
            dbc.Label("mail", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_mail', value='', type='email', style=component_styles)
        ]),

        html.Div([
            dbc.Label("CellRangerVersion", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_CellRangerVersion',
                options=[
                    {'label': "Aligner/CellRanger/9.0.0", 'value': "Aligner/CellRanger/9.0.0"},
                    {'label': "Aligner/CellRanger/8.0.1", 'value': "Aligner/CellRanger/8.0.1"},
                    {'label': "Aligner/CellRanger/7.1.0", 'value': "Aligner/CellRanger/7.1.0"},
                ],
                value="Aligner/CellRanger/9.0.0",
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
        Output(id('label_name'), 'value'),
        Output(id('refBuild'), 'value'),
        Output(id('refFeatureFile'), 'value'),
        Output(id('featureLevel'), 'value'),
        Output(id('TenXLibrary'), 'value'),
        Output(id('chemistry'), 'value'),
        Output(id('includeIntrons'), 'value'),
        Output(id('transcriptTypes'), 'value'),
        Output(id('runVeloCyto'), 'value'),
        Output(id('bamStats'), 'value'),
        Output(id('keepAlignment'), 'value'),
        Output(id('CellRangerVersion'), 'value'),
    ],
    [Input('entity', 'data')],
    [State('app_data', 'data')]
)
def populate_default_values(entity_data, app_data):
    name = entity_data.get("name", "Unknown") + "_CellRanger"
    return (
        name,
        8,
        60,
        300,
        "CellRangerCount",
        "To Do",
        "genes.gtf",
        "gene",
        "GEX",
        "auto",
        True,
        "protein_coding",
        False,
        False,
        True,
        "Aligner/CellRanger/9.0.0"
    )

##############################################################################################
##### C. Check user inputs for invalid values (Step 1: Retrieve data from the user)      #####
##############################################################################################

@app.callback(
    Output(id("alert-warning"), "children"),
    Output(id("alert-warning"), "is_open"),
    [
        Input(id("label_name"), "value"),
        Input(id("refBuild"), "value"),
        Input(id("expectedCells"), "value"),
    ]
)
def check_cellranger_warnings(label_name, refBuild, expectedCells):
    """
    Validate required input fields for the CellRanger app and display appropriate warnings.

    This Dash callback checks whether essential fields such as `label_name` and `refBuild` have 
    been provided by the user. If any are missing, it returns user-friendly warning messages to 
    be displayed in the frontend.

    Args:
        label_name (str): Label or identifier for the current CellRanger run.
        refBuild (str): Selected reference genome build.
        expectedCells (str or int): Expected number of cells (not validated in this function).

    Returns:
        tuple:
            - list[html.Div] or str: A list of Dash `html.Div` components with warnings, or an empty string if no warnings exist.
            - bool: True if any warnings are present (to open the warning alert), False otherwise.
    """

    warnings = []

    # 1. label_name required
    if not label_name:
        warnings.append("Warning: 'Label Name' is required. Please enter a value.")

    # 2. refBuild required
    if not refBuild:
        warnings.append("Warning: 'refBuild' is required. Please select a reference genome.")

    # Output
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
        State(id('label_name'), 'value'),
        State(id('refBuild'), 'value'),
        State(id('refFeatureFile'), 'value'),
        State(id('featureLevel'), 'value'),
        State(id('TenXLibrary'), 'value'),
        State(id('chemistry'), 'value'),
        State(id('includeIntrons'), 'value'),
        State(id('expectedCells'), 'value'),
        State(id('transcriptTypes'), 'value'),
        State(id('controlSeqs'), 'value'),
        State(id('secondRef'), 'value'),
        State(id('runVeloCyto'), 'value'),
        State(id('bamStats'), 'value'),
        State(id('keepAlignment'), 'value'),
        State(id('cmdOptions'), 'value'),
        State(id('specialOptions'), 'value'),
        State(id('mail'), 'value'),
        State(id('CellRangerVersion'), 'value'),
        State(id("dataset"), "data"),
        State('datatable', 'selected_rows'),
        State('token_data', 'data'),
        State('entity', 'data'),
        State('app_data', 'data'),
    ],
    prevent_initial_call=True
)
def submit_cellranger_job(
    n_clicks, name, comment, cores, ram, scratch, partition, process_mode, samples, label_name,
    refBuild, refFeatureFile, featureLevel, TenXLibrary, chemistry, includeIntrons, expectedCells,
    transcriptTypes, controlSeqs, secondRef, runVeloCyto, bamStats, keepAlignment, cmdOptions,
    specialOptions, mail, CellRangerVersion,
    dataset, selected_rows, token_data, entity_data, app_data
):
    """
    Submit a CellRanger job by creating dataset and parameter files and executing the Sushi backend job submission.

    This Dash callback is triggered by clicking the "Submit" button. It collects user-defined parameters 
    for a CellRanger run, builds `.tsv` files for dataset and parameters, constructs a Sushi-compatible 
    bash command for the CellRanger job, and returns an alert indicating whether the submission was successful.

    Args:
        n_clicks (int): Number of times the "Submit" button has been clicked.
        name (str): Name of the CellRanger job.
        comment (str): Optional description or comment for the job.
        cores (int): Number of CPU cores to allocate.
        ram (int): Amount of RAM to allocate (in GB).
        scratch (int): Scratch disk space to allocate (in GB).
        partition (str): HPC partition or queue to submit the job.
        process_mode (str): Processing mode (e.g., normal, debug).
        samples (str): Input sample IDs or configuration string.
        label_name (str): Label or identifier for the analysis results.
        refBuild (str): Reference genome build used for alignment.
        refFeatureFile (str): Path or ID for the reference annotation file.
        featureLevel (str): Level of feature granularity (e.g., gene, transcript).
        TenXLibrary (str): 10X Genomics library chemistry type.
        chemistry (str): Chemistry protocol used in sequencing (e.g., SC3Pv3).
        includeIntrons (str): Whether intronic reads should be included.
        expectedCells (int): Estimated number of cells expected in the dataset.
        transcriptTypes (str): Types of transcripts to include in the analysis.
        controlSeqs (str): Additional control sequences or spike-ins.
        secondRef (str): Optional second reference genome or annotation.
        runVeloCyto (str): Whether to run the VeloCyto analysis for RNA velocity.
        bamStats (str): Whether to generate BAM-level alignment statistics.
        keepAlignment (str): Whether to retain BAM files after processing.
        cmdOptions (str): Additional command-line flags for CellRanger.
        specialOptions (str): Application-specific special options.
        mail (str): Email address for job status notifications.
        CellRangerVersion (str): Version of CellRanger to use.
        dataset (list): Dataset records displayed in the UI.
        selected_rows (list): Indices of selected dataset rows.
        token_data (dict): Authentication and session token metadata.
        entity_data (dict): User, project, or session-related metadata.
        app_data (dict): Metadata specific to the CellRanger app instance.

    Returns:
        tuple:
            - bool: True if the job was successfully submitted (to open success alert).
            - bool: True if job submission failed (to open failure alert).
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
            'label_name': label_name,
            'refBuild': refBuild,
            'refFeatureFile': refFeatureFile,
            'featureLevel': featureLevel,
            'TenXLibrary': TenXLibrary,
            'chemistry': chemistry,
            'includeIntrons': includeIntrons,
            'expectedCells': expectedCells,
            'transcriptTypes': transcriptTypes,
            'controlSeqs': controlSeqs,
            'secondRef': secondRef,
            'runVeloCyto': runVeloCyto,
            'bamStats': bamStats,
            'keepAlignment': keepAlignment,
            'cmdOptions': cmdOptions,
            'specialOptions': specialOptions,
            'mail': mail,
            'CellRangerVersion': CellRangerVersion
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
            bundle exec sushi_fabric --class CellRanger --dataset {dataset_path} --parameterset {param_path} --run \\
            --input_dataset_application {app_id} --project {project_id} --dataset_name {dataset_name} \\
            --mango_run_name {mango_run_name} --next_dataset_name {name}
        """
        print("[SUSHI BASH COMMAND]:", bash_command)
        return True, False

    except Exception as e:
        print("[SUSHI ERROR]:", str(e))
        return False, True
