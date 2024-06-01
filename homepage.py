import os

import streamlit as st
from pages.helpers.utils import add_page_logo, add_sidebar_logo, add_pages_to_sidebar

add_page_logo()
add_sidebar_logo()
add_pages_to_sidebar()

st.title('Analysis of World Cup 2022 in Qatar')

st.header('Available pages', divider='gray')

st.subheader('FIFA (game) rating')
st.page_link(os.path.join('pages', '1_fifa_ratings.py'), label='Visit page', icon='🎮️')
st.page_link('https://www.kaggle.com/datasets/stefanoleone992/fifa-22-complete-player-dataset', label='Data source', icon='💾')
st.divider()

st.subheader('FBRef player stats')
st.page_link(os.path.join('pages', '2_fbref_stats.py'), label='Visit site', icon='⚽')
st.page_link('https://www.kaggle.com/datasets/swaptr/fifa-world-cup-2022-player-data', label='Data source', icon='💾')
st.divider()

st.subheader('Running (physical) player stats')
st.page_link(os.path.join('pages', '3_running_performance.py'), label='Visit site', icon='👟')
st.page_link('https://www.fifatrainingcentre.com/en/fwc2022/post-match-summaries/post-match-summary-reports.php', label='Data source', icon='💾')
