import streamlit as st
import os
import pandas as pd
from matplotlib import pyplot as plt

from pages.helpers.utils import add_page_logo, add_sidebar_logo
from settings import DATA_DIR

add_page_logo()
add_sidebar_logo()

st.title('Reference matches 2022/2023 season')

df = pd.read_csv(os.path.join(DATA_DIR, 'fifa_players_22.csv'))
st.dataframe(df)
# default_metric = ref_s.index[0]
# selected_metric = st.selectbox('Select GPS parameter to watch', ref_s.index, index=0)
