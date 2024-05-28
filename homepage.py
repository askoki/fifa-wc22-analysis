import os

import streamlit as st
from pages.helpers.utils import add_page_logo, add_sidebar_logo

add_page_logo()
add_sidebar_logo()

st.title('Analysis of World Cup 2022 in Qatar')

st.text('Available pages')

st.page_link(os.path.join('pages', '1_fifa_page.py'), label='FIFA (game) rating', icon="🎮️")
st.page_link(os.path.join('pages', '2_fbref_page.py'), label='FBRef player stats', icon="⚽")
st.page_link(os.path.join('pages', '3_running_page.py'), label='Running (physical) player stats', icon="👟")
