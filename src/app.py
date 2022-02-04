# Copyright (C) 2022, Pyronear.

# This program is licensed under the Apache License version 2.
# See LICENSE or go to <https://www.apache.org/licenses/LICENSE-2.0.txt> for full license details.

import time
from datetime import date
from pathlib import Path

import streamlit as st


def main():

    # Wide mode
    st.set_page_config(
        page_title="Pyronear - Wildfire image crowdsourcing",
        page_icon="https://raw.githubusercontent.com/pyronear/pyronear.github.io/master/img/favicon.ico",
        layout="wide",
    )

    # Designing the interface
    st.title("Collecte de photos de feux de forêt")
    st.write("La photo que vous partagez ici sera utilisée pour créer un jeu de données public "
             "pour la detection de feux de forêts")

    # Set the columns
    cols = st.columns((2, 1))
    cols[0].subheader("Selection de la photo")
    cols[1].subheader("Informations de la photo")

    # Sidebar
    st.sidebar.image("src/static/logo_letters.png")

    # new line
    st.sidebar.write('\n')

    st.sidebar.markdown("""**A propos de Pyronear** - Pyronear est une association loi 1901, uniquement constituée \
    de bénévoles, qui a pour objet la préservation des espaces naturels contre les risques d’incendies, \
    et autres aléas naturels. \n \n Pour cela, nous nous efforçons de trouver des solutions technologiques \
    performantes, accessibles, open-source et abordables pour la protection contre les risques naturels. """)

    st.sidebar.write('\n')
    st.sidebar.markdown("""[Site Web](https://pyronear.org/) | [contact](mailto:contact@pyronear.org)""")

    # Disabling warning
    st.set_option('deprecation.showfileUploaderEncoding', False)

    # Choose your own image
    uploaded_file = cols[0].file_uploader("Upload files", type=['png', 'jpeg', 'jpg'])
    submitted = False
    if uploaded_file is not None:
        st.warning(
            """En partageant cette photo, vous adhérez à la démarche Pyronear """
            """de construction d'un jeu de données collaboratif."""
        )
        img = uploaded_file.read()
        cols[0].image(img)
        form = cols[1].form("Information de la photo")
        form.date_input("Date de la photo", max_value=date.today())
        form.time_input("Heure approximative")
        form.text_input("Où a-t-elle été prise ?")
        form.multiselect("Étiquettes", ["fumée", "flammes"])
        submitted = form.form_submit_button("Envoyer")

    # Find out more section
    with st.expander("En savoir plus sur notre démarche de construction d'un dataset collaboratif"):
        st.markdown(Path("/src/static/find_out_more.md").read_text())


    if submitted:

        if uploaded_file is None:
            cols[0].write("Veuillez charger une photo")

        else:

            with st.spinner('Envoi en cours ...'):

                # Call API to send image + labels
                time.sleep(.5)
            st.success("Merci pour l'envoi !")
            st.balloons()


if __name__ == '__main__':
    main()
