import io

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image
from random import choice
from string import ascii_letters, digits, punctuation
from matplotlib.backends.backend_pdf import PdfPages


def add_download_image_button(fig: plt.Figure, button_text: str, filename: str, bbox_inches=None):
    img = io.BytesIO()
    fig.savefig(img, format='png', facecolor=fig.get_facecolor(), bbox_inches=bbox_inches)

    btn = st.download_button(
        label=button_text,
        data=img,
        file_name=filename,
        mime="image/png"
    )


def add_page_logo():
    img = Image.open('2022_FIFA_World_Cup_logo.png')
    st.set_page_config(
        page_title="FIFA World Cuo 2022",
        page_icon=img
    )


def add_sidebar_logo():
    img = Image.open('2022_FIFA_World_Cup_logo.png')
    st.markdown(
        """
        <style>
            [data-testid=stSidebar] [data-testid=stImage]{
                text-align: center;
                display: block;
                margin-left: auto;
                margin-right: auto;
                width: 100%;
            }
        </style>
        """, unsafe_allow_html=True
    )
    st.sidebar.image(image=img)
    st.sidebar.title('WC 2022 Analytics')


def add_download_pdf_from_plots_button(button_text: str, filename: str):
    pdf_name = 'pdf_output.pdf'
    pdf = PdfPages(pdf_name)

    for fig in range(1, plt.gcf().number + 1):
        pdf.savefig(fig)
        plt.close()
    pdf.close()
    plt.close()

    with open(pdf_name, "rb") as pdf_file:
        pdf_byte = pdf_file.read()

    st.download_button(
        label=button_text,
        data=pdf_byte,
        file_name=filename,
        mime='application/octet-stream'
    )


def add_expander_toggle(button_text: str, df: pd.DataFrame):
    with st.expander(button_text):
        st.dataframe(df)


def generate_random_string(length=8):
    characters = ascii_letters + digits + punctuation
    random_string = ''.join(choice(characters) for _ in range(length))
    return random_string
