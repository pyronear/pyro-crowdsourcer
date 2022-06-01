import pandas as pd
from datetime import datetime, date

import dash

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

# Various modules provided by Dash and Dash Leaflet to build the page layout
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash_daq as daq

from user_agents import parse


# Fetching French departements
departments = pd.read_csv(
    'https://static.data.gouv.fr/resources/departements-de-france/20200425-135513/departements-france.csv'
)

department_options = []
departments['to_be_displayed'] = departments['code_departement'] + ' - ' + departments['nom_departement']
for _, row in departments.iterrows():
    department_options.append(
        {
            'label': row['to_be_displayed'],
            'value': row['code_departement']
        }
    )

etiquette_options = [
    {'label': 'Feu de forêt', 'value': 'wildfire'},
    {'label': 'Feu industriel', 'value': 'industrial_fire'}
]


app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.UNITED]
)

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
                # html.A(
                #     dbc.Row(
                #         [
                #             dbc.Col(html.Div('Hello')),
                #         ],
                #         align="center",
                #         no_gutters=True,
                #     ),
                #     href="#",
                # ),
                dbc.NavbarToggler(id="navbar-toggler"),
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
            [
                html.Div(
                    'Participez à la protection des forêts',
                    style={
                        'font-size': '25px',
                        'font-weight': 'bold',
                        'color': '#054546',
                        'margin-top': '5%',
                        'margin-left': '5%'
                    }
                ),

                html.Div(
                    '🤝 Comment aider ?',
                    style={
                        'font-size': '20px',
                        'font-weight': 'bold',
                        'color': '#5BBD8C',
                        'margin-top': '2%',
                        'margin-left': '5%'
                    }
                ),

                html.Div(
                    (
                        "En partageant une photo ou une vidéo, vous participez à la création d'un jeu de données public"
                        + " qui permet d'aider à la détection de feux de forêts."
                    ),
                    style={
                        'font-size': '16px',
                        'color': '#283B3D',
                        'margin-top': '2%',
                        'margin-left': '5%',
                        'width': '38%'
                    }
                ),

                html.Button(
                    "En savoir plus sur notre système de détection",
                    id='know_more_on_detection_button',
                    style={
                        'font-size': '12px',
                        "text-decoration": "underline",
                        'color': '#F6B52A',
                        'margin-top': '1%',
                        'margin-left': '5%',
                        'margin-right': '1%',
                        'width': '38%',
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
                                    'margin-left': '5%',
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
                'width': '100%',
                'background-color': 'white'
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
                        'font-size': '20px',
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
                                'font-size': '12px',
                                'font-weight': 'bold',
                                'color': 'white'
                            }
                        ),

                        dcc.Upload(
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
                                    src='',
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
                                                        'font-size': '14px',
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
                                                        'font-size': '14px',
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
                                                        'font-size': '14px',
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
                                                        'font-size': '14px',
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
                                                        'font-size': '14px',
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
                        )
                    ],
                    style={
                        'width': left_column_width,
                        'margin-top': '3%',
                        'margin-left': '5%'
                    }
                ),

                html.Div(
                    [
                        daq.BooleanSwitch(
                            id='acceptance-switch',
                            on=False,
                            label="En partageant cette photo, j'accepte..."
                        ),
                    ],
                    style={
                        'width': left_column_width,
                        'margin-top': '1%',
                        'margin-left': '5%',
                        'color': 'white',
                        'font-weight': 'bold',
                        'font-size': '14px'
                    }
                ),

                html.Div(
                    '',
                    id='temp-output',
                    style={
                        'color': 'white',
                        'font-weight': 'bold',
                        'font-size': '14px',
                        'text-align': 'center',
                        'margin-left': '5%',
                        'margin-top': '3%',
                        'width': left_column_width
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
                            'font-size': '13px',
                            'borderRadius': '0px',
                            'border': 'none',
                            'width': '30%',
                        }
                    ),
                    style={
                        'width': left_column_width,
                        'margin-top': '3%',
                        'margin-left': '5%',
                        'font-color': 'white',
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
    Output('left-column-main-div', 'style'),
    Input('store-user-agent-string', 'data')
)
def adapt_layout(JSoutput):
    print('THIS IS USER AGENT STRING:', JSoutput)
    user_agent = parse(JSoutput)

    if user_agent.is_mobile or user_agent.is_tablet:
        left_column_width = '45%'

    else:
        left_column_width = '45%'

    return {
        'width': left_column_width,
        'margin-top': '3%',
        'margin-left': '5%'
    }


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
        Output('etiquette-input', 'invalid')
    ],
    [
        Input('image-upload', 'contents'),
        Input('send-form-button', 'n_clicks')
    ],
    [
        State('image-upload', 'contents'),
        State('date-input', 'date'),
        State('hour-input', 'value'),
        State('departement-input', 'value'),
        State('etiquette-input', 'value'),
        State('acceptance-switch', 'on'),
        State('temp-output', 'children')
    ]
)
def send_form(
    image_upload_contents_input,
    n_clicks,
    image_upload_contents,
    date_input,
    hour_input,
    departement_input,
    etiquette_input,
    acceptance_switch,
    temp_output
):
    ctx = dash.callback_context
    triggerer_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if triggerer_id == 'image-upload':

        if image_upload_contents_input is None:
            raise PreventUpdate

        else:
            style = {
                'borderRadius': '10px',
                'textAlign': 'left',
                'text-indent': '5%',
                'background-color': '#DCE6EA',
                'margin-top': '3%'
            }

            return [
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
                image_upload_contents_input,
                style,
                dash.no_update,
                False,
                False,
                False
            ]

    elif triggerer_id == 'send-form-button':

        if n_clicks is None or n_clicks == 0:
            raise PreventUpdate

        else:
            if image_upload_contents is None:
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
                    False
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
                    ] + form_feedbacks

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
                    ]

                else:
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
                        False
                    ]

    else:
        raise PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=True, port=8050)  # , host='0.0.0.0'
