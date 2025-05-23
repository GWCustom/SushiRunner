from dash import html, dcc, ctx
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from generic.callbacks import app
import dash_daq as daq
import bfabric_web_apps
from bfabric_web_apps.utils.components import charge_switch
import pandas as pd 
from dash.dash_table import DataTable
from bfabric_web_apps import (
    SCRATCH_PATH,
    run_main_job,
    get_power_user_wrapper
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

title = 'FastqcApp'

label_style = {
    "font-size": "0.85rem",   # Smaller text
    "margin-left": "6px",     # Indent the label a bit
    "margin-bottom": "4px"
}

def id(name):
    return f"{title}_{name}"

def get_project_id_for_order(order_id, environment):
    """
    Get the project ID for a given order ID.

    Args:
        container_id (str): The order ID.

    Returns:
        str: The project ID.
    """

    B = get_power_user_wrapper({"environment": environment})
    order = B.read("container", {"id": order_id})[0]

    project_id = order.get("project", {}).get("id", None)
    return project_id
    

sidebar = dbc.Container(children=charge_switch + [ 
    html.P(f"{title} Generic Parameters: ", style={"margin-bottom": "0px", "font-weight": "bold"}),

    html.Div([
        dbc.Label("Name", style=label_style),
        dbc.Input(id=f'{title}_name', value='', type='text', style={"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'})
    ]),
    html.Div([
        dbc.Label("Comment", style=label_style),
        dbc.Input(id=f'{title}_comment', value='', type='text', style={"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'})
    ]),
    html.Div([
        dbc.Label("RAM", style=label_style),
        dbc.Select(id=f'{title}_ram', options=[{'label': str(x), 'value': x} for x in [15, 32, 64]], style={"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'})
    ]),
    html.Div([
        dbc.Label("Cores", style=label_style),
        dbc.Select(id=f'{title}_cores', options=[{'label': str(x), 'value': x} for x in [1, 2, 4, 8]], style={"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'})
    ]),
    html.Div([
        dbc.Label("Scratch", style=label_style),
        dbc.Select(id=f'{title}_scratch', options=[{'label': str(x), 'value': x} for x in [10, 50, 100]], style={"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'})
    ]),
    html.Div([
        dbc.Label("Partition", style=label_style),
        dbc.Select(id=f'{title}_partition', options=[{'label': x, 'value': x} for x in ['employee', 'manyjobs', 'user']], style={"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'})
    ]),
    html.Div([
        dbc.Label("Process Mode", style=label_style),
        dbc.Select(id=f'{title}_process_mode', options=[{'label': x, 'value': x} for x in ['DATASET']], style={"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'})
    ]),
    html.Div([
        dbc.Label("Mail", style=label_style),
        dbc.Input(id=f'{title}_mail', value='', type='email', style={"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'})
    ]),

    html.P(f"{title} App Specific Parameters: ", style={"margin-bottom": "0px", "font-weight": "bold"}),

    daq.BooleanSwitch(
        id=f'{title}_paired',
        on=False,
        label="Paired",
        labelPosition="top",
        style={"margin-bottom": "18px"}
    ),
    daq.BooleanSwitch(
        id=f'{title}_showNativeReports',
        on=False,
        label="Show Native Reports",
        labelPosition="top",
        style={"margin-bottom": "18px"}
    ),
    html.Div([
        dbc.Label("Special Options", style=label_style),
        dbc.Input(id=f'{title}_specialOptions', value='', type='text', style={"margin-bottom": "18px"})
    ]),
    html.Div([
        dbc.Label("Command Options", style=label_style),
        dbc.Input(id=f'{title}_cmdOptions', value='', type='text', style={"margin-bottom": "18px"})
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
        Output(id("name"), "value"),
        Output(id("comment"), "value"),
        Output(id("ram"), "value"),
        Output(id("cores"), "value"),
        Output(id("scratch"), "value"),
        Output(id("partition"), "value"),
        Output(id("process_mode"), "value")
    ],
    [
        Input("entity", "data"),
    ],
    [
        State("app_data", "data")
    ]
)
def populate_default_values(entity_data, app_data):
    """
    Populate the default values for the input fields.

    This callback is triggered once on page load using the 'entity' data input.
    It sets default values for the job submission form fields such as name, comment,
    resource allocations, and job configuration, based on the user's entity data.

    Args:
        entity_data (dict): Dictionary containing metadata or configuration settings 
                            associated with the current user or organization. This 
                            may include default values for RAM, cores, partition, 
                            and other submission-related fields.

    Returns:
        tuple:
            - name (str): Default job name.
            - comment (str): Default comment or description.
            - ram (str): Default RAM allocation.
            - cores (str): Default number of CPU cores.
            - scratch (str): Default scratch disk allocation.
            - partition (str): Default SLURM partition.
            - process_mode (str): Default processing mode.
    """

    name = entity_data.get("name", "Unknown") + "_FastQC"

    return name, "", 32, 4, 50, 'employee', 'DATASET'


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
        State(id("name"), "value"),
        State(id("comment"), "value"),
        State(id("ram"), "value"),
        State(id("cores"), "value"),
        State(id("scratch"), "value"),
        State(id("partition"), "value"),
        State(id("process_mode"), "value"),
        State(id("mail"), "value"),
        State(id("paired"), "on"),
        State(id("showNativeReports"), "value"),
        State(id("specialOptions"), "value"),
        State(id("cmdOptions"), "value"),
        State(id("dataset"), "data"),
        State("charge_run", "on"),
        State("datatable", "selected_rows"),
        State("token_data", "data"),
        State("entity", "data"),
        State("app_data", "data"),
        State('url', 'search')
    ],
    prevent_initial_call=True
)
def submit_suhshi_job(submission, name, comment, ram, cores, scratch, partition, process_mode, mail, paired, showNativeReports, specialOptions, cmdOptions, dataset, charge_run, selected_rows, token_data, entity_data, app_data, url):
    """
    Construct the bash command which calls the sushi app from the backend.

    This Dash callback is triggered by a click on the "Submit" button. It collects user-specified
    input parameters, constructs a bash command to submit a job to the backend, and 
    returns alerts indicating success or failure of the job submission.

    Args:
        submission (int): Number of times the "Submit" button has been clicked.
        name (str): Name of the job.
        comment (str): User-provided comment or description for the job.
        ram (str): Amount of RAM requested.
        cores (str): Number of CPU cores requested.
        scratch (str): Amount of scratch disk space requested.
        partition (str): Target partition (queue) to submit the job to.
        process_mode (str): Mode in which the job should be processed.
        mail (str): Email address for job notifications.
        paired (bool): Whether the input data is paired-end (True) or single-end (False).
        showNativeReports (bool): Whether to include native reports in output.
        specialOptions (str): Any special options to be passed to the FastQC app.
        cmdOptions (str): Additional command-line options for the FastQC app.
        dataset (list): List of dataset records displayed in the frontend.
        selected_rows (list): Indices of selected rows from the dataset table.
        token_data (dict): Authentication token data for secure backend communication.
        entity_data (dict): Metadata related to the user or organization entity.
        app_data (dict): Metadata or configuration specific to the app being submitted.

    Returns:
        tuple:
            - is_open_success (bool): True if job submission succeeded, to show the success alert.
            - is_open_fail (bool): True if job submission failed, to show the failure alert.
    """

    ### A. Construct the dataset.tsv file to send to the backend
    dataset = pd.DataFrame(dtd(entity_data.get("full_api_response", {})))
    dataset_path = f"{SCRATCH_PATH}/{name}/dataset.tsv"
    param_path = f"{SCRATCH_PATH}/{name}/parameters.tsv"

    for filepath in [dataset_path, param_path]:
        if not os.path.exists(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))
    
    ### B. Construct parameters.tsv to send to the backend and assign necessary variables for bash command
    parameters = pd.DataFrame({
        "col1": ['cores', 'ram', 'scratch', 'node', 'process_mode', 'partition', 'paired', 'perLibrary', 'name', 'cmdOptions', 'mail'], 
        "col2": [cores, ram, scratch, '', process_mode, partition, str(paired).lower(), 'true', name, cmdOptions, mail]
    })
    
    parameters.to_csv(param_path, sep="\t", index=False, header=False)
    dataset.to_csv(dataset_path, sep="\t", index=False)

    ### Complete the remaining variables
    container_id, app_id = entity_data.get("full_api_response", {}).get("container",{}).get("id", None), app_data.get("id", "")

    if not container_id:
        project_id = "2220"
    elif entity_data.get("full_api_response", {}).get("container",{}).get("classname", None) != "project":
        project_id = get_project_id_for_order(container_id, token_data.get("environment", "TEST").upper())
    else: 
        project_id = container_id

    dataset_name, mango_run_name = entity_data.get("name", ""), "None"
    
    # Update charge_run based on its value
    projects_to_charge = [project_id] if charge_run and project_id else []

    ### C. Construct the bash command to send to the backend (invoke sushi_fabric)
    bash_command = f"""
        cd /srv/sushi/production/master && \
        bundle exec sushi_fabric --class FastqcApp --dataset \
        {dataset_path} --parameterset {param_path} --run  \
        --input_dataset_application {app_id} --project {project_id} \
        --dataset_name {dataset_name} --mango_run_name {mango_run_name} \
        --next_dataset_name {name}
    """
    try:
        run_main_job(
            files_as_byte_strings={},
            bash_commands=[bash_command],
            resource_paths={},
            attachment_paths={},
            token=url,
            service_id=bfabric_web_apps.SERVICE_ID,
            charge=projects_to_charge
        )
        return True, False
    
    except Exception as e:
        print(f"Job submission failed: {e}")
        return False, True
