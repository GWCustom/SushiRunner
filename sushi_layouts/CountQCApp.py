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

title = 'CountQC'

label_style = {
    "font-size": "0.85rem",   # Smaller text
    "margin-left": "6px",     # Indent the label a bit
    "margin-bottom": "4px"
}

def id(name):
    return f"{title}_{name}"

# Component styles
component_styles = {"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'}

# CountQC Sidebar layout with tooltips
sidebar = dbc.Container(
    children=charge_switch + [
        html.P("CountQC App Parameters:", style={"font-weight": "bold", "font-size": "1rem", "margin-bottom": "10px"}),

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
                value=1,
                style=component_styles
            )
        ]),

        html.Div([
            dbc.Label("RAM", style=label_style),
            dbc.Input(id=f'{title}_ram', value=4, type='number', style=component_styles)
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
                options=[{'label': 'DATASET', 'value': 'DATASET'}],
                value='DATASET',
                style=component_styles
            )
        ]),

        html.Div([
            dbc.Label("Name (Label)", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_label_name', value='Count_QC', type='text', style=component_styles)
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
            dbc.Label("normMethod", style={"font-size": "0.85rem"}),
            dbc.Input(
                id=f'{title}_normMethod',
                value='logMean',
                type='text',
                style=component_styles
            )
        ]),

        html.Div([
            dbc.Label("runGO", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_runGO',
                options=[{'label': 'True', 'value': True}, {'label': 'False', 'value': False}],
                value=True,
                style=component_styles
            )
        ]),

        html.Div([
            dbc.Label("backgroundExpression", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_backgroundExpression', value=10, type='number', style=component_styles),
            dbc.Tooltip("counts to be added to shrink estimated log2 ratios", target=f'{title}_backgroundExpression', placement="right")
        ]),

        html.Div([
            dbc.Label("topGeneSize", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_topGeneSize', value=100, type='number', style=component_styles)
        ]),

        html.Div([
            dbc.Label("selectByFtest", style={"font-size": "0.85rem"}),
            dbc.Select(
                id=f'{title}_selectByFtest',
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
                    {"label": "long_noncoding", "value": "long_noncoding"}
                ],
                value='protein_coding',
                style=component_styles
            )
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
        Output(id('refFeatureFile'), 'value'),
        Output(id('featureLevel'), 'value'),
        Output(id('normMethod'), 'value'),
        Output(id('runGO'), 'value'),
        Output(id('backgroundExpression'), 'value'),
        Output(id('topGeneSize'), 'value'),
        Output(id('selectByFtest'), 'value'),
        Output(id('transcriptTypes'), 'value'),
    ],
    [Input('entity', 'data')],
    [State('app_data', 'data')]
)
def populate_default_values(entity_data, app_data):
    name = entity_data.get("name", "Unknown") + "_CountQC"
    return (
        name,
        1,
        4,
        10,
        "Homo_sapiens/GENCODE/GRC",
        "genes.gtf",
        "gene",
        "logMean",
        True,
        10,
        100,
        False,
        "protein_coding"
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
    [Input("Submit", "n_clicks")],
    [
        State(id('name'), 'value'),
        State(id('comment'), 'value'),
        State(id('cores'), 'value'),
        State(id('ram'), 'value'),
        State(id('scratch'), 'value'),
        State(id('partition'), 'value'),
        State(id('process_mode'), 'value'),
        State(id('label_name'), 'value'),
        State(id('refBuild'), 'value'),
        State(id('refFeatureFile'), 'value'),
        State(id('featureLevel'), 'value'),
        State(id('normMethod'), 'value'),
        State(id('runGO'), 'value'),
        State(id('backgroundExpression'), 'value'),
        State(id('topGeneSize'), 'value'),
        State(id('selectByFtest'), 'value'),
        State(id('transcriptTypes'), 'value'),
        State(id('specialOptions'), 'value'),
        State(id('expressionName'), 'value'),
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
def submit_countqc_job(
    n_clicks, name, comment, cores, ram, scratch, partition, process_mode, label_name,
    refBuild, refFeatureFile, featureLevel, normMethod, runGO, backgroundExpression, topGeneSize,
    selectByFtest, transcriptTypes, specialOptions, expressionName, mail,
    dataset, selected_rows, token_data, entity_data, app_data, url, charge_run
):
    """
    Submit a CountQC job by creating dataset and parameter files, then triggering the Sushi backend.

    This Dash callback is activated by clicking the "Submit" button. It collects user-defined parameters 
    for the CountQC analysis, writes them into structured `.tsv` files, constructs the appropriate bash 
    command to submit the job using Sushi, and returns an alert indicating the result of the submission.

    Args:
        n_clicks (int): Number of times the "Submit" button was clicked.
        name (str): Name of the CountQC job.
        comment (str): Optional job comment or description.
        cores (int): Number of CPU cores requested.
        ram (int): Amount of RAM requested (in GB).
        scratch (int): Scratch disk space requested (in GB).
        partition (str): HPC partition or queue to which the job will be submitted.
        process_mode (str): Processing mode to use for the job (e.g., normal or debug).
        label_name (str): Label name for the output.
        refBuild (str): Reference genome build.
        refFeatureFile (str): Annotation file with gene or feature information.
        featureLevel (str): Level of features to analyze (e.g., gene, transcript).
        normMethod (str): Normalization method used for counts.
        runGO (str): Whether to perform Gene Ontology enrichment analysis.
        backgroundExpression (str): Background expression filtering setting.
        topGeneSize (int): Number of top genes to retain for further analysis.
        selectByFtest (str): Whether to use F-test for feature selection.
        transcriptTypes (str): Types of transcripts to include.
        specialOptions (str): Additional command-line flags or custom settings.
        expressionName (str): Identifier for the expression matrix.
        mail (str): Email address to receive job status updates.
        dataset (list): Dataset as shown in the frontend table.
        selected_rows (list): Selected row indices from the dataset.
        token_data (dict): Authentication and session data.
        entity_data (dict): Metadata about the user or project entity.
        app_data (dict): Metadata or configuration specific to the CountQC app.

    Returns:
        tuple:
            - bool: True if the job was successfully submitted (triggers success alert).
            - bool: True if the job submission failed (triggers failure alert).
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
            'label_name': label_name,
            'refBuild': refBuild,
            'refFeatureFile': refFeatureFile,
            'featureLevel': featureLevel,
            'normMethod': normMethod,
            'runGO': runGO,
            'backgroundExpression': backgroundExpression,
            'topGeneSize': topGeneSize,
            'selectByFtest': selectByFtest,
            'transcriptTypes': transcriptTypes,
            'specialOptions': specialOptions,
            'expressionName': expressionName,
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

        # Update charge_run based on its value
        if charge_run and project_id:
            charge_run = [project_id]

        bash_command = f"""
            bundle exec sushi_fabric --class CountQC --dataset {dataset_path} --parameterset {param_path} --run \\
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
