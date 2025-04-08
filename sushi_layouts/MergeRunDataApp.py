from dash import html, dcc, ctx
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
# from generic.callbacks import app
import dash_daq as daq
from bfabric_web_apps.utils.components import charge_switch
import pandas as pd 
from dash.dash_table import DataTable
from bfabric_web_apps import (
    SCRATCH_PATH
)
from sushi_utils.dataset_utils import dataset_to_dictionary as dtd
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

sidebar = dbc.Container(children=charge_switch + [ 
    html.P("Generic Parameters: ", style={"margin-bottom": "0px", "font-weight": "bold"}),

    html.Div([
        dbc.Label("Name", style=label_style),
        dbc.Input(id='name', value='', type='text', style={"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'})
    ]),
    html.Div([
        dbc.Label("Comment", style=label_style),
        dbc.Input(id='comment', value='', type='text', style={"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'})
    ]),
    html.Div([
        dbc.Label("RAM", style=label_style),
        dbc.Select(id='ram', options=[{'label': str(x), 'value': x} for x in [15, 32, 64]], style={"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'})
    ]),
    html.Div([
        dbc.Label("Cores", style=label_style),
        dbc.Select(id='cores', options=[{'label': str(x), 'value': x} for x in [1, 2, 4, 8]], style={"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'})
    ]),
    html.Div([
        dbc.Label("Scratch", style=label_style),
        dbc.Select(id='scratch', options=[{'label': str(x), 'value': x} for x in [10, 50, 100]], style={"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'})
    ]),
    html.Div([
        dbc.Label("Partition", style=label_style),
        dbc.Select(id='partition', options=[{'label': x, 'value': x} for x in ['employee', 'manyjobs', 'user']], style={"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'})
    ]),
    html.Div([
        dbc.Label("Process Mode", style=label_style),
        dbc.Select(id='process_mode', options=[{'label': x, 'value': x} for x in ['DATASET']], style={"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'})
    ]),
    html.Div([
        dbc.Label("Mail", style=label_style),
        dbc.Input(id='mail', value='', type='email', style={"margin-bottom": "18px", 'borderBottom': '1px solid lightgrey'})
    ]),

    html.P("App Specific Parameters: ", style={"margin-bottom": "0px", "font-weight": "bold"}),

    daq.BooleanSwitch(
        id='FastqcApp_paired',
        on=False,
        label="Paired",
        labelPosition="top",
        style={"margin-bottom": "18px"}
    ),
    daq.BooleanSwitch(
        id='FastqcApp_showNativeReports',
        on=False,
        label="Show Native Reports",
        labelPosition="top",
        style={"margin-bottom": "18px"}
    ),
    html.Div([
        dbc.Label("Special Options", style=label_style),
        dbc.Input(id='FastqcApp_specialOptions', value='', type='text', style={"margin-bottom": "18px"})
    ]),
    html.Div([
        dbc.Label("Command Options", style=label_style),
        dbc.Input(id='FastqcApp_cmdOptions', value='', type='text', style={"margin-bottom": "18px"})
    ]),
    dbc.Button("Submit", id='submit1', n_clicks=0, style={"margin-top": "18px", 'borderBottom': '1px solid lightgrey'})
], style={"max-height":"62vh", "overflow-y":"auto", "overflow-x":"hidden"})


####################################################################################
##### B. Now we define the application layout (Step 1: Get data from the user) #####
####################################################################################

layout = dbc.Container(
    children = [
        html.Div(id="FastqcApp_Layout", style={"max-height":"62vh", "overflow-y":"auto", "overflow-x":"hidden"}),
        dcc.Store(id="dataset", data={})
    ]
)


def callbacks(app):

    ####################################################################################
    ### C. Now we define the application callbacks (Step 1: Get data from the user) ####
    ####################################################################################

    @app.callback(
        Output('FastqcApp_Layout', 'children'),
        [
            Input('dataset', 'data')
        ], prevent_initial_call=True
    )
    def callback(data):
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
                    'height': 'auto'
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
            Output('name', 'value'),
            Output('comment', 'value'),
            Output('ram', 'value'),
            Output('cores', 'value'),
            Output('scratch', 'value'),
            Output('partition', 'value'),
            Output('process_mode', 'value')
        ],
        [
            Input('entity', 'data'), # Just triggers on page load one time.
        ],
        [
            State('app_data', 'data')
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
        Output("dataset", "data"),
        Input("entity", "data"),
        State("dataset", "data"),
    )
    def update_dataset(entity_data, dataset):
        
        df = dtd(entity_data.get("full_api_response", {}))
        return df



    ######################################################################################################
    ############################### STEP 3: Submit the Job! ##############################################
    ###################################################################################################### 

    @app.callback(
        [
            Output("alert-fade-success", "is_open"),
            Output("alert-fade-fail", "is_open"),
        ],
        [
            Input("Submit", "n_clicks"),
        ],
        [
            State('name', 'value'),
            State('comment', 'value'),
            State('ram', 'value'),
            State('cores', 'value'),
            State('scratch', 'value'),
            State('partition', 'value'),
            State('process_mode', 'value'),
            State('mail', 'value'),
            State('FastqcApp_paired', 'on'),
            State('FastqcApp_showNativeReports', 'value'),
            State('FastqcApp_specialOptions', 'value'),
            State('FastqcApp_cmdOptions', 'value'),
            State('dataset', 'data'),
            State('datatable', 'selected_rows'),
            State('token_data', 'data'),
            State('entity', 'data'),
            State('app_data', 'data')
        ],
        prevent_initial_call=True
    )
    def submit_suhshi_job(submission, name, comment, ram, cores, scratch, partition, process_mode, mail, paired, showNativeReports, specialOptions, cmdOptions, dataset, selected_rows, token_data, entity_data, app_data):
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

        ### Step I. Construct the dataset.tsv file to send to the backend
        dataset = pd.DataFrame(dtd(entity_data.get("full_api_response", {})))
        dataset_path = f"{SCRATCH_PATH}/{name}/dataset.tsv"
        if not os.path.exists(os.path.dirname(dataset_path)):
            os.makedirs(os.path.dirname(dataset_path))
        dataset.to_csv(dataset_path, sep="\t", index=False)

        ### Step II. Construct parameters.tsv to send to the backend 
        param_names = ['cores', 'ram', 'scratch', 'node', 'process_mode', 'partition', 'paired', 'perLibrary', 'name', 'cmdOptions', 'mail']
        param_values = [cores, ram, scratch, '', process_mode, partition, str(paired).lower(), 'true', name, cmdOptions, mail]
        parameters = pd.DataFrame({
            "col1": param_names, 
            "col2": param_values
        })
        param_path = f"{SCRATCH_PATH}/{name}/parameters.tsv"
        if not os.path.exists(os.path.dirname(param_path)):
            os.makedirs(os.path.dirname(param_path))
        parameters.to_csv(param_path, sep="\t", index=False, header=False)


        ### Complete the remaining variables
        app_id = app_data.get("id", "")
        # project_id = entity_data.get("full_api_response", {}).get("container", {}).get("id", "")
        project_id = "2220"
        dataset_name = entity_data.get("name", "")
        mango_run_name = "None"

        ### Step III. Construct the bash command to send to the backend (invoke sushi_fabric)
        bash_command = f"""
            bundle exec sushi_fabric --class FastqcApp --dataset \
            {dataset_path} --parameterset {param_path} --run  \
            --input_dataset_application {app_id} --project {project_id} \
            --dataset_name {dataset_name} --mango_run_name {mango_run_name} \
            --next_dataset_name {name}
        """

        print(bash_command)

        return True, False