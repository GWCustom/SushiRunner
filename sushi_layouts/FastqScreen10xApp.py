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

title = 'FastqScreen10xApp'

label_style = {
    "font-size": "0.85rem",   # Smaller text
    "margin-left": "6px",     # Indent the label a bit
    "margin-bottom": "4px"
}

def id(name):
    return f"{title}_{name}"

# Component styles
component_styles = {"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'}

# FastqS10x Sidebar layout with tooltips
sidebar = dbc.Container(
    children=charge_switch + [
        html.P("FastqScreen10x App Parameters:", style={"font-weight": "bold", "font-size": "1rem", "margin-bottom": "10px"}),

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
            dbc.Input(id=f'{title}_ram', value=30, type='number', style=component_styles)
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
                options=[{'label': 'DATASET', 'value': 'DATASET'}],
                value='DATASET',
                style=component_styles
            )
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
            dbc.Label("Label Name", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_label_name', value='FastQC_Result', type='text', style=component_styles),
            dbc.Tooltip("required", target=f'{title}_label_name', placement="right")
        ]),

        html.Div([
            dbc.Label("cmdOptions", style={"font-size": "0.85rem"}),
            dbc.Input(id=f'{title}_cmdOptions', value='', type='text', style=component_styles)
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
        Output(id('paired'), 'value'),
        Output(id('label_name'), 'value'),
    ],
    [Input('entity', 'data')],
    [State('app_data', 'data')]
)
def populate_default_values(entity_data, app_data):
    name = entity_data.get("name", "Unknown") + "_FastqScreen10x"
    return (
        name,
        8,
        30,
        300,
        True,
        "FastQC_Result"
    )


##############################################################################################
##### C. Check user inputs for invalid values (Step 1: Retrieve data from the user)      #####
##############################################################################################


@app.callback(
    Output(id("alert-warning"), "children"),
    Output(id("alert-warning"), "is_open"),
    [
        Input(id("paired"), "value"),
        Input(id("label_name"), "value"),
    ]
)
def check_FastqScreen10x_warnings(paired, label_name):
    """
    Validate input fields required for the FastqScreen10x app and return relevant user warnings.

    This Dash callback is triggered when the user modifies the `paired` or `label_name` fields. 
    It ensures both fields are set and returns appropriate warning messages if they are missing.

    Args:
        paired (str or bool): Indicates whether the reads are paired-end; must be selected.
        label_name (str): Label or identifier for the FastqScreen10x analysis run.

    Returns:
        tuple:
            - list[html.Div] or str: A list of Dash `html.Div` components with warning messages, or an empty string if no warnings exist.
            - bool: True if any warnings are present (to open the warning alert), False otherwise.
    """

    warnings = []

    # 1. paired is required
    if paired is None:
        warnings.append("Warning: 'paired' is required. Please select true or false.")

    # 2. label_name is required
    if not label_name:
        warnings.append("Warning: 'Label Name' is required. Please enter a value.")

    # Output formatted warnings
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
        State(id('paired'), 'value'),
        State(id('label_name'), 'value'),
        State(id('cmdOptions'), 'value'),
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
def submit_FastqScreen10x_job(
    n_clicks, name, comment, cores, ram, scratch, partition, process_mode,
    paired, label_name, cmdOptions, mail,
    dataset, selected_rows, token_data, entity_data, app_data, url, charge_run
):
    """
    Submit a FastqScreen10x job by generating dataset and parameter files and invoking the Sushi backend.

    This Dash callback is triggered when the "Submit" button is clicked. It gathers user input parameters 
    for a FastqScreen10x analysis run, writes the dataset and parameter files in TSV format, constructs the 
    appropriate bash command, and submits the job via the Sushi framework. It returns alerts to indicate 
    success or failure of the submission.

    Args:
        n_clicks (int): Number of times the "Submit" button was clicked.
        name (str): Name of the FastqScreen10x job.
        comment (str): Optional comment or job description.
        cores (int): Number of CPU cores to request.
        ram (int): RAM requested in GB.
        scratch (int): Scratch disk space requested in GB.
        partition (str): HPC partition or queue for job execution.
        process_mode (str): Execution mode (e.g., normal, test).
        paired (str or bool): Whether the input reads are paired-end.
        label_name (str): Label or identifier for the FastqScreen10x run.
        cmdOptions (str): Additional command-line flags for FastqScreen10x.
        mail (str): Email address for job status notifications.
        dataset (list): Dataset data shown in the frontend.
        selected_rows (list): Selected row indices in the dataset table.
        token_data (dict): Authentication token data for secure API access.
        entity_data (dict): Metadata related to the user or associated project.
        app_data (dict): Configuration and metadata specific to the FastqScreen10x app.

    Returns:
        tuple:
            - bool: True if job submission succeeded (triggers success alert).
            - bool: True if job submission failed (triggers failure alert).
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
            'paired': paired,
            'label_name': label_name,
            'cmdOptions': cmdOptions,
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
            bundle exec sushi_fabric --class FastqScreen10xApp --dataset {dataset_path} --parameterset {param_path} --run \\
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
