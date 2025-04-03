# Ensure version compatibility between bfabric_web_apps and bfabric_web_app_template.
# Both must be the same version to avoid compatibility issues.
# Example: If bfabric_web_apps is version 0.1.3, bfabric_web_app_template must also be 0.1.3.
# Verify and update versions accordingly before running the application.

from dash import Input, Output, State, html, dcc
import dash_bootstrap_components as dbc
import bfabric_web_apps
from generic.callbacks import app
from generic.components import no_auth
from bfabric_web_apps import get_logger
from directory import DIRECTORY

######################################################################################################
####################### STEP 1: Get Data From the User! ##############################################
######################################################################################################

# Here we define the sidebar content, which includes a slider, a dropdown, an input field, and a button.
sidebar = []

# here we define the modal that will pop up when the user clicks the submit button.
modal = html.Div([
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Ready to Prepare Create Workunits?")),
        dbc.ModalBody("Are you sure you're ready to create workunits?"),
        dbc.ModalFooter(dbc.Button("Yes!", id="Submit", className="ms-auto", n_clicks=0)),],
    id="modal-confirmation",
    is_open=False,),
])

# Here are the alerts which will pop up when the user creates workunits 
alerts = html.Div(
    [
        dbc.Alert("Success: Report created!", color="success", id="alert-fade-success", dismissable=True, is_open=False),
        dbc.Alert("Error: Report creation failed!", color="danger", id="alert-fade-fail", dismissable=True, is_open=False),
    ], style={"margin": "20px"}
)

# Here we define a Dash layout, which includes the sidebar, and the main content of the app. 
app_specific_layout = dbc.Row(
    id="page-content-main",
    children=[
        dcc.Loading(alerts), 
        modal,  # Modal defined earlier.
        dbc.Col(
            html.Div(
                id="sidebar",
                children=sidebar,  # Sidebar content defined earlier.
                style={
                    "border-right": "2px solid #d4d7d9",
                    "height": "100%",
                    "padding": "20px",
                    "font-size": "20px"
                }
            ),
            width=3,  # Width of the sidebar column.
        ),
        dbc.Col(
            html.Div(
                id="page-content",
                children=[
                    html.Div(id="auth-div")  # Placeholder for `auth-div` to be updated dynamically.
                ],
                style={
                    "margin-top": "20vh",
                    "margin-left": "2vw",
                    "font-size": "20px"
                }
            ),
            width=9,  # Width of the main content column.
        ),
    ],
    style={"margin-top": "0px", "min-height": "40vh"}  # Overall styling for the row layout.
)

# Here we define the documentation content for the app.
documentation_content = []

app_title = "Sushi Runner"

# here we use the get_static_layout function from bfabric_web_apps to set up the app layout.
app.layout = bfabric_web_apps.get_static_layout(         # The function from bfabric_web_apps that sets up the app layout.
    base_title=app_title,                          # The app title we defined previously
    main_content=app_specific_layout,     # The main content for the app defined in components.py
    documentation_content=documentation_content,    # Documentation content for the app defined in components.py
    layout_config={"workunits": True, "queue": False, "bug": True}  # Configuration for the layout
)

# This callback is necessary for the modal to pop up when the user clicks the submit button.
@app.callback(
    Output("modal-confirmation", "is_open"),
    [Input("example-button", "n_clicks"), Input("Submit", "n_clicks")],
    [State("modal-confirmation", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    [
        Output('auth-div', 'children'),
        Output('sidebar', 'children')
    ],
    [Input('token_data', 'data'),
    Input('entity', 'data')]
)
def update_user_display(token_data, entity_data):

    print("Token Data:", token_data)
    print("Entity Data:", entity_data)

    if token_data and entity_data:
        user_name = token_data.get("user_data", "Unknown User")  
        
        L = get_logger(token_data)
        L.log_operation("User Login", f"User {user_name} logged in successfully.")
        
        environment = token_data.get("environment", "").lower()
        app_id = str(token_data.get("application_data", None))

        print("APP ID:", app_id)
        print("ENVIRONMENT:", environment)
        print("USER NAME:", user_name)
        print("TOKEN DATA:", token_data)
        print("ENTITY DATA:", entity_data)

        if environment and app_id:

            layout_data = DIRECTORY.get(environment, {}).get(app_id, None)

        return layout_data.get('layout', ""), layout_data.get('sidebar', None)
    else:
        return "Please log in."


# Here we run the app on the specified host and port.
if __name__ == "__main__":
    app.run(debug=bfabric_web_apps.DEBUG, port=bfabric_web_apps.PORT, host=bfabric_web_apps.HOST)

