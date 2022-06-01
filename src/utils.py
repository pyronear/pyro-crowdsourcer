from dash import dcc, html


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
