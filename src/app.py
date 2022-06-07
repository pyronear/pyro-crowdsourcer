import base64
import csv
import os
from datetime import date, datetime

import dash
import dash_bootstrap_components as dbc
import dash_daq as daq
import requests
# Various modules provided by Dash and Dash Leaflet to build the page layout
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from user_agents import parse

########################################################################################################################
# Utils ----------------------------------------------------------------------------------------------------------------

# Fetching French departements
CSV_URL = 'https://static.data.gouv.fr/resources/departements-de-france/20200425-135513/departements-france.csv'

with requests.Session() as s:
    download = s.get(CSV_URL)

    decoded_content = download.content.decode('utf-8')

    cr = csv.reader(decoded_content.splitlines(), delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    department_options = [{"label": f"{code} - {name}", "value": name} for code, name, _, _ in cr][1:]

# Setting the options for the type of wildfire
etiquette_options = [
    {'label': 'Feu de forêt', 'value': 'wildfire'},
    {'label': 'Feu industriel', 'value': 'industrial_fire'}
]


def is_int(element):
    try:
        int(element)
        return True

    except ValueError:
        return False


def build_image_upload():

    upload = dcc.Upload(
        id='image-upload',
        children=html.Div(
            [

                html.Div(
                    'Placeholder',
                    style={
                        'font-size': '12px',
                        'font-weight': 'bold',
                        'color': '#DCE6EA',
                    }
                ),

                html.Div(
                    [
                        html.A(
                            'Glisser / déposer une photo ici ',
                            style={
                                'color': '#283B3D',
                                'font-size': '14px',
                            }
                        ),
                        html.A(
                            'ou parcourir',
                            style={
                                'font-weight': 'bold',
                                "text-decoration": "underline",
                                'color': '#283B3D',
                                'font-size': '14px',
                            }
                        )
                    ]
                ),

                html.Div(
                    'Maximum 200Mb - Formats acceptés : PNG, JPEG',
                    style={
                        'margin-top': '1%',
                        'color': '#737373',
                        'font-size': '10px',
                        'font-weight': 'bold',
                    }
                ),

                html.Div(
                    'Placeholder',
                    style={
                        'font-size': '14px',
                        'font-weight': 'bold',
                        'color': '#DCE6EA',
                    }
                ),
            ]
        ),
        style={
            'width': '100%',
            'borderRadius': '10px',
            'textAlign': 'left',
            'text-indent': '5%',
            'background-color': '#DCE6EA',
            'margin-top': '2%'
        },
        # Allow multiple files to be uploaded
        multiple=False
    )

    return upload


########################################################################################################################
# Main app -------------------------------------------------------------------------------------------------------------

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.UNITED]
)
server = app.server

# We define a few attributes of the app object
app.title = 'Pyronear - Crowdsourcing platform'
app.config.suppress_callback_exceptions = True

# Navbar Title
user_item = html.Div(
    "Surveillez les départs de feux",
    id="user-div",
    className="mx-auto order-0",
    style={'color': 'white', 'align': 'center', 'justify': 'center'}
)

# Alert monitoring screen, to be displayed in CODIS
link_to_website_button = dbc.NavLink(
    children=[
        html.Div(
            children=[
                html.I(
                    className="mx-auto order-0",
                ),
                html.Span("à propos de Pyronear"),
            ]
        )
    ],
    href="https://pyronear.org",
    style={
        "font-size": "17px",
        "font-weight": "bold",
        "color": "#054546",
        "text-decoration": "underline"
    }
)

left_column_width = '45%'
form_inputs_width = '80%'

app.layout = html.Div(
    [
        dcc.Store(id='store-user-agent-string'),

        # Navbar
        dbc.Navbar(
            [
                dbc.Collapse([user_item], id="navbar-collapse", navbar=True),
                html.Div(link_to_website_button)
            ],
            id="main_navbar",
            color='white',
        ),

        html.Div(
            'Placeholder',
            style={
                'font-size': '8px',
                'width': '100%',
                'background-color': '#DCE6EA',
                'color': '#DCE6EA'
            }
        ),

        html.Div(
            id='left-column-upper-div',
            children=[
                html.Div(
                    'Participez à la protection des forêts',
                    style={
                        'font-size': '3em',
                        'font-weight': 'bold',
                        'color': '#054546',
                        'margin-top': '5%',
                    }
                ),

                html.Div(
                    '🤝 Comment aider ?',
                    style={
                        'font-size': '2em',
                        'font-weight': 'bold',
                        'color': '#5BBD8C',
                        'margin-top': '2%',
                    }
                ),

                html.Div(
                    (
                        "En partageant une photo ou une vidéo, vous participez à la création d'un jeu de données public"
                        + " qui permet d'aider à la détection de feux de forêts."
                    ),
                    style={
                        'font-size': '1.3em',
                        'color': '#283B3D',
                        'margin-top': '2%',
                        'width': '90%'
                    }
                ),

                html.Button(
                    "En savoir plus sur notre système de détection",
                    id='know_more_on_detection_button',
                    style={
                        'font-size': '1em',
                        "text-decoration": "underline",
                        'color': '#F6B52A',
                        'margin-top': '1%',
                        'margin-right': '1%',
                        'width': '90%',
                        'text-align': 'right',
                        'border': 'none',
                        'background-color': 'white'
                    }
                ),

                dbc.Modal(
                    [
                        dbc.ModalHeader(
                            html.Div(
                                "Notre système de détection",
                                style={
                                    'font-size': '20px',
                                    'font-weight': 'bold',
                                    'color': '#054546',
                                    'margin-top': '5%',
                                    'width': '100%'
                                }
                            )
                        ),
                        dbc.ModalBody("TO BE COMPLETED."),
                        dbc.ModalFooter(
                            dbc.Button(
                                "Fermer",
                                id="know_more_on_detection_modal_close",
                                className="ms-auto",
                                n_clicks=0
                            )
                        ),
                    ],
                    id='know_more_on_detection_modal',
                    is_open=False,
                )
            ],
            style={
                'width': left_column_width,
                'background-color': 'white',
                'margin-left': '5%'
            }
        ),

        html.Div(
            [
                html.Div(
                    'Placeholder',
                    style={
                        'font-size': '20px',
                        'font-weight': 'bold',
                        'color': '#054546',
                        'margin-top': '5%',
                        'margin-left': '5%'
                    }
                ),

                html.Div(
                    '📷 Envoyer ma photo',
                    style={
                        'font-size': '2em',
                        'font-weight': 'bold',
                        'color': 'white',
                        'margin-top': '5%',
                        'margin-left': '5%'
                    }
                ),

                html.Div(
                    id='left-column-main-div',
                    children=[
                        html.Div(
                            'Télécharger une ou plusieurs photo(s)',
                            style={
                                'font-size': '1em',
                                'font-weight': 'bold',
                                'color': 'white'
                            }
                        ),

                        html.Div(
                            id='image-upload-div',
                            children=build_image_upload()
                        ),

                        html.Div(
                            id='image-upload-info',
                            children='',
                            style={
                                'display': 'none'
                            }
                        ),

                        html.Div(
                            id='image-container',
                            children=[
                                html.Div(
                                    'Placeholder',
                                    style={
                                        'font-size': '12px',
                                        'font-weight': 'bold',
                                        'color': '#DCE6EA',
                                    }
                                ),
                                html.Img(
                                    id='displayed-image',
                                    src=os.path.join(os.getcwd(), 'temp.jpg'),
                                    width='90%',
                                    style={'margin-left': '5%'}
                                ),
                                html.Div(
                                    'Placeholder',
                                    style={
                                        'font-size': '12px',
                                        'font-weight': 'bold',
                                        'color': '#DCE6EA',
                                    }
                                ),
                            ],
                            style={
                                'display': 'none',
                            }
                        ),

                        html.Div(
                            [
                                html.Div(
                                    'Placeholder',
                                    style={
                                        'font-size': '12px',
                                        'font-weight': 'bold',
                                        'color': '#DCE6EA',
                                    }
                                ),

                                dbc.Form(
                                    [
                                        html.Div(
                                            [
                                                dbc.Label(
                                                    'Date',
                                                    style={
                                                        'font-size': '1.2em',
                                                        'font-weight': 'bold',
                                                        'color': '#283B3D',
                                                        'margin-left': '5%'
                                                    }
                                                ),
                                                html.Div(
                                                    [
                                                        dcc.DatePickerSingle(
                                                            id='date-input',
                                                            min_date_allowed=date(2000, 1, 1),
                                                            max_date_allowed=datetime.today(),
                                                            initial_visible_month=date(2022, 5, 7),
                                                            display_format='DD/MM/YYYY',
                                                            placeholder='DD/MM/YYYY',
                                                            style={
                                                                'font-color': '#737373',
                                                                'font-size': '12px',
                                                                'borderRadius': '0px',
                                                                'border': 'none',
                                                                'border-bottom': '1px solid black'
                                                            }
                                                        ),
                                                        html.Div(
                                                            "Oops, il semblerait qu'il y ait une erreur",
                                                            id='feedback-date-input',
                                                            style={
                                                                'display': 'none'
                                                            }
                                                        )
                                                    ],
                                                    style={
                                                        'font-size': '1.2em',
                                                        'width': '100%',
                                                        'margin-left': '5%'
                                                    }
                                                )
                                            ]
                                        ),

                                        html.Div(
                                            [
                                                dbc.Label(
                                                    'Heure approximative',
                                                    style={
                                                        'font-size': '1.2em',
                                                        'font-weight': 'bold',
                                                        'color': '#283B3D',
                                                        'margin-left': '5%',
                                                        'margin-top': '3%'
                                                    }
                                                ),
                                                dbc.Input(
                                                    id='hour-input',
                                                    placeholder='HH:MM',
                                                    style={
                                                        'width': form_inputs_width,
                                                        'margin-left': '5%',
                                                        'font-color': '#737373',
                                                        'borderRadius': '0px',
                                                        'border': 'none',
                                                        'border-bottom': '1px solid black'
                                                    }
                                                ),
                                                dbc.FormFeedback(
                                                    "Oops, il semblerait qu'il y ait une erreur",
                                                    type='invalid',
                                                    style={'margin-left': '5%'}
                                                )
                                            ]
                                        ),

                                        html.Div(
                                            [
                                                dbc.Label(
                                                    'Département',
                                                    style={
                                                        'font-size': '1.2em',
                                                        'font-weight': 'bold',
                                                        'color': '#283B3D',
                                                        'margin-top': '3%'
                                                    }
                                                ),
                                                dbc.Select(
                                                    id='departement-input',
                                                    placeholder='SÉLECTIONNEZ',
                                                    options=department_options,
                                                    style={
                                                        'color': '#737373',
                                                        'borderRadius': '0px',
                                                        'border': 'none',
                                                        'border-bottom': '1px solid black'
                                                    }
                                                ),
                                                dbc.FormFeedback(
                                                    "Oops, il semblerait qu'il y ait une erreur",
                                                    type='invalid',
                                                )
                                            ],
                                            style={
                                                'width': form_inputs_width,
                                                'margin-left': '5%'
                                            }
                                        ),
                                        html.Div(
                                            [
                                                dbc.Label(
                                                    'Étiquette',
                                                    style={
                                                        'font-size': '1.2em',
                                                        'font-weight': 'bold',
                                                        'color': '#283B3D',
                                                        'margin-top': '3%'
                                                    }
                                                ),
                                                dbc.Select(
                                                    id='etiquette-input',
                                                    placeholder='SÉLECTIONNEZ',
                                                    options=etiquette_options,
                                                    style={
                                                        'color': '#737373',
                                                        'borderRadius': '0px',
                                                        'border': 'none',
                                                        'border-bottom': '1px solid black'
                                                    }
                                                ),
                                                dbc.FormFeedback(
                                                    "Oops, il semblerait qu'il y ait une erreur",
                                                    type='invalid',
                                                )
                                            ],
                                            style={
                                                'width': form_inputs_width,
                                                'margin-left': '5%'
                                            }
                                        )
                                    ]
                                ),
                                html.Div(
                                    'Placeholder',
                                    style={
                                        'margin-top': '2%',
                                        'font-size': '14px',
                                        'font-weight': 'bold',
                                        'color': '#DCE6EA',
                                    }
                                )
                            ],
                            style={
                                'width': '100%',
                                'borderRadius': '10px',
                                'background-color': '#DCE6EA',
                                'margin-top': '3%',
                            }
                        ),

                        html.Div(
                            [
                                html.Div(
                                    "En partageant cette photo, j'accepte..."
                                ),
                                daq.BooleanSwitch(
                                    id='acceptance-switch',
                                    on=False,
                                    style={'margin-top': '3%'}
                                    # label="En partageant cette photo, j'accepte..."
                                ),
                            ],
                            style={
                                'margin-top': '5%',
                                'margin-left': '5%',
                                'color': 'white',
                                'font-weight': 'bold',
                                'font-size': '1.2em',
                                'text-align': 'center'
                            }
                        ),

                        html.Div(
                            '',
                            id='temp-output',
                            style={
                                'color': 'white',
                                'font-weight': 'bold',
                                'font-size': '1.2em',
                                'text-align': 'center',
                                'margin-left': '5%',
                                'margin-top': '5%',
                            }
                        ),

                        html.Div(
                            dbc.Button(
                                'ENVOYER',
                                id='send-form-button',
                                size='lg',
                                style={
                                    'display': 'block',
                                    'margin-left': 'auto',
                                    'margin-right': '0px',
                                    'background-color': '#5BBD8C',
                                    'font-weight': 'bold',
                                    'font-size': '1.3em',
                                    'borderRadius': '0px',
                                    'border': 'none',
                                    'width': '30%',
                                }
                            ),
                            style={
                                'margin-top': '5%',
                                'margin-left': '5%',
                                'font-color': 'white',
                            }
                        ),
                    ],
                    style={
                        'width': left_column_width,
                        'margin-top': '3%',
                        'margin-left': '5%'
                    }
                ),

                html.Div(
                    'à propos de Pyronear - Site web - mentions légales',
                    style={
                        'font-size': '14px',
                        'align-text': 'center',
                        'font-weight': 'bold',
                        'color': 'white',
                        'margin-top': '40%',
                        'margin-left': '36%',
                    }
                ),

                html.Div(
                    'Placeholder',
                    style={
                        'font-size': '20px',
                        'font-weight': 'bold',
                        'color': '#054546',
                        'margin-top': '5%',
                        'margin-left': '5%'
                    }
                ),
            ],
            style={
                'width': '100%',
                'height': '100%',
                'background-color': '#054546',
                'margin-top': '5%'
            }
        ),
    ]
)


app.clientside_callback(
    # """
    # function(trigger) {
    #     //  can use any prop to trigger this callback - we just want to store the info on startup
    #     // USE THIS TO GET screen dimensions
    #     // const screenInfo = {height :screen.height, width: screen.width};
    #     // USE THIS TO GET useragent string
    #     screenInfo = navigator.userAgent;
    #     return screenInfo
    # }
    # """,
    """
    function(trigger) {
        // USE THIS TO GET useragent string
        screenInfo = navigator.userAgent;
        return screenInfo
    }
    """,
    Output('store-user-agent-string', 'data'),
    Input('main_navbar', 'children'),
)


@app.callback(
    [
        Output('left-column-main-div', 'style'),
        Output('left-column-upper-div', 'style')
    ],
    Input('store-user-agent-string', 'data'),
    [
        State('left-column-main-div', 'style'),
        State('left-column-upper-div', 'style')
    ]
)
def adapt_layout(JSoutput, current_style_main_div, current_style_upper_div):
    print('THIS IS USER AGENT STRING:', JSoutput)
    user_agent = parse(JSoutput)

    new_style_main_div = current_style_main_div.copy()
    new_style_upper_div = current_style_upper_div.copy()

    if user_agent.is_mobile or user_agent.is_tablet:
        new_style_main_div['width'] = '85%'
        new_style_upper_div['width'] = '85%'

    else:
        new_style_main_div['width'] = '45%'
        new_style_upper_div['width'] = '45%'

    return new_style_main_div.copy(), new_style_upper_div.copy()


@app.callback(
    Output('know_more_on_detection_modal', 'is_open'),
    [
        Input('know_more_on_detection_button', 'n_clicks'),
        Input('know_more_on_detection_modal_close', 'n_clicks'),
    ],
    State('know_more_on_detection_modal', 'is_open')
)
def open_close_detection_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open

    return is_open


@app.callback(
    Output('image-upload-info', 'children'),
    Input('image-upload', 'filename'),
    State('image-upload', 'contents'),
)
def upload_action(filename, contents):
    if filename is None:
        raise PreventUpdate

    # Save file to disk (on server)
    _, content_string = contents.split(',')

    path_to_image = os.path.dirname(os.path.abspath(__file__))
    path_to_image = os.path.join(path_to_image, 'temp.png')

    with open(path_to_image, 'wb') as f:
        f.write(base64.b64decode(content_string))

    return f'Latest upload was {filename}'


@app.callback(
    [
        Output('temp-output', 'children'),
        Output('date-input', 'date'),
        Output('hour-input', 'value'),
        Output('departement-input', 'value'),
        Output('etiquette-input', 'value'),
        Output('acceptance-switch', 'on'),
        Output('displayed-image', 'src'),
        Output('image-container', 'style'),
        Output('feedback-date-input', 'style'),
        Output('hour-input', 'invalid'),
        Output('departement-input', 'invalid'),
        Output('etiquette-input', 'invalid'),
        Output('image-upload-div', 'children')
    ],
    [
        Input('image-upload-info', 'children'),
        Input('send-form-button', 'n_clicks')
    ],
    [
        State('image-upload-info', 'children'),
        State('date-input', 'date'),
        State('hour-input', 'value'),
        State('departement-input', 'value'),
        State('etiquette-input', 'value'),
        State('acceptance-switch', 'on'),
        State('temp-output', 'children')
    ]
)
def send_form(
    info,
    n_clicks,
    info_state,
    date_input,
    hour_input,
    departement_input,
    etiquette_input,
    acceptance_switch,
    temp_output
):
    ctx = dash.callback_context
    triggerer_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if triggerer_id == 'image-upload-info':

        if not info.startswith('Latest'):
            raise PreventUpdate

        else:
            style = {
                'borderRadius': '10px',
                'textAlign': 'left',
                'text-indent': '5%',
                'background-color': '#DCE6EA',
                'margin-top': '3%'
            }

            path_to_image = os.path.dirname(os.path.abspath(__file__))
            path_to_image = os.path.join(path_to_image, 'temp.png')

            encoded_image = base64.b64encode(open(path_to_image, 'rb').read())
            src = 'data:image/png;base64,{}'.format(encoded_image.decode())

            return [
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
                src,
                style,
                dash.no_update,
                False,
                False,
                False,
                dash.no_update
            ]

    elif triggerer_id == 'send-form-button':

        if n_clicks is None or n_clicks == 0:
            raise PreventUpdate

        else:
            if not info_state.startswith('Latest'):
                return [
                    "Avez-vous bien ajouté une image ?",
                    dash.no_update,
                    dash.no_update,
                    dash.no_update,
                    dash.no_update,
                    dash.no_update,
                    dash.no_update,
                    dash.no_update,
                    {'display': 'none'},
                    False,
                    False,
                    False,
                    dash.no_update
                ]

            else:
                if (
                    date_input is None
                    or hour_input is None
                    or departement_input is None
                    or etiquette_input is None
                ):

                    if date_input is None:
                        form_feedbacks = [{'color': '#DF382F'}, False, False, False]

                    elif hour_input is None:
                        form_feedbacks = [{'display': 'none'}, True, False, False]

                    elif departement_input is None:
                        form_feedbacks = [{'display': 'none'}, False, True, False]

                    elif etiquette_input is None:
                        form_feedbacks = [{'display': 'none'}, False, False, True]

                    return [
                        "Le formulaire est incomplet.",
                        dash.no_update,
                        dash.no_update,
                        dash.no_update,
                        dash.no_update,
                        dash.no_update,
                        dash.no_update,
                        dash.no_update,
                    ] + form_feedbacks + [dash.no_update]

                elif (
                    ':' not in hour_input
                    or not is_int(hour_input.split(':')[0])
                    or not is_int(hour_input.split(':')[1])
                    or int(hour_input.split(':')[0]) > 24
                    or int(hour_input.split(':')[1]) > 60
                ):
                    form_feedbacks = [{'display': 'none'}, True, False, False]

                    return [
                        "Le formulaire est incomplet.",
                        dash.no_update,
                        dash.no_update,
                        dash.no_update,
                        dash.no_update,
                        dash.no_update,
                        dash.no_update,
                        dash.no_update,
                    ] + form_feedbacks + [dash.no_update]

                elif not acceptance_switch:
                    return [
                        "Pour valider l'envoi, veuillez accepter les conditions.",
                        dash.no_update,
                        dash.no_update,
                        dash.no_update,
                        dash.no_update,
                        dash.no_update,
                        dash.no_update,
                        dash.no_update,
                        {'display': 'none'},
                        False,
                        False,
                        False,
                        dash.no_update
                    ]

                else:
                    # INSERT BACK-END INSTRUCTIONS

                    path_to_image = os.path.dirname(os.path.abspath(__file__))
                    path_to_image = os.path.join(path_to_image, 'temp.png')

                    os.remove(path_to_image)

                    return [
                        "Merci pour votre contribution !",
                        None,
                        None,
                        None,
                        None,
                        False,
                        '',
                        {'display': 'none'},
                        {'display': 'none'},
                        False,
                        False,
                        False,
                        build_image_upload()
                    ]

    else:
        raise PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=True, port=8050)  # , host='0.0.0.0'
