# Copyright (C) 2022, Pyronear.

# This program is licensed under the Apache License version 2.
# See LICENSE or go to <https://www.apache.org/licenses/LICENSE-2.0.txt> for full license details.

import time
from datetime import date

import streamlit as st


def main():

    # Wide mode
    st.set_page_config(
        page_title="Pyronear - Wildfire image crowdsourcing",
        page_icon="https://raw.githubusercontent.com/pyronear/pyronear.github.io/master/img/favicon.ico",
        layout="wide",
    )

    # Designing the interface
    st.title("Wildfire image crowdsourcing")
    st.write("The image you upload here will be used to create a public image dataset for wildfire detection.")
    # Set the columns
    cols = st.columns((2, 1))
    cols[0].subheader("Input image")
    cols[1].subheader("Image tags")

    # Sidebar
    # File selection
    st.sidebar.title("Image selection")
    # Disabling warning
    st.set_option('deprecation.showfileUploaderEncoding', False)
    # Choose your own image
    uploaded_file = st.sidebar.file_uploader("Upload files", type=['png', 'jpeg', 'jpg'])
    submitted = False
    if uploaded_file is not None:
        st.warning(
            "By clicking the 'Submit' button, you hereby declare that you are authorized to share this picture "
            "and forsake all the rights of exclusive exploitation of this content."
        )
        img = uploaded_file.read()
        cols[0].image(img)
        form = cols[1].form("Image information")
        form.date_input("Date of the picture", max_value=date.today())
        form.time_input("Approx time of the picture")
        form.text_input("Where was this taken?")
        form.multiselect("Event tags", ["smoke", "flames"])
        submitted = form.form_submit_button("Submit")

    # For newline
    st.sidebar.write('\n')

    if submitted:

        if uploaded_file is None:
            st.sidebar.write("Please upload an image")

        else:

            with st.spinner('Uploading...'):

                # Call API to send image + labels
                time.sleep(.5)
            st.success('Thanks for your upload!')
            st.balloons()


if __name__ == '__main__':
    main()
