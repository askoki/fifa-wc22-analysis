import streamlit as st
import os
import pandas as pd
from pages.helpers.plotting import create_mpl_radar_color, plot_mpl_comparison_radar
from pages.helpers.utils import add_page_logo, add_sidebar_logo
from settings import DATA_DIR, SB_GRAY, SB_RED, SB_LIGHT_BLUE

add_page_logo()
add_sidebar_logo()

st.title('FIFA football game dataset for WC 2022')

df = pd.read_csv(os.path.join(DATA_DIR, 'fifa_players_22.csv'))

countries = df.nationality_name.unique().tolist()
default_country = countries.index('Croatia')
player1_county = st.selectbox('Select player 1 country', countries, index=default_country)
country1_players = df[df.nationality_name == player1_county].short_name.unique()
player1 = st.selectbox('Select player 1', country1_players, index=0)

player2_county = st.selectbox('Select player 2 country', countries, index=default_country)
country2_players = df[df.nationality_name == player2_county].short_name.unique()
player2 = st.selectbox('Select player 2', country2_players, index=1)

fifa_overall_values = ['overall', 'pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic']

values1 = df[df.short_name == player1][fifa_overall_values].values[0]
values2 = df[df.short_name == player2][fifa_overall_values].values[0]

bound_low = [1 for _ in range(len(values2))]
bound_high = [100 for _ in range(len(values2))]
round_int = [True for _ in range(len(values2))]
labels = [s.capitalize() for s in fifa_overall_values]

colors = {
    'rings_inner': create_mpl_radar_color(facecolor=SB_GRAY, edgecolor=SB_GRAY),
    'radar1': create_mpl_radar_color(facecolor=SB_RED, edgecolor=SB_RED),
    'radar2': create_mpl_radar_color(facecolor=SB_LIGHT_BLUE, edgecolor=SB_LIGHT_BLUE),
}

fig, ax = plot_mpl_comparison_radar(
    values1, values2, labels,
    bound_low=bound_low, bound_high=bound_high,
    colors=colors, label1=player1, label2=player2, round_int=[round_int]
)
ax.legend(ncols=2, fontsize=10, loc='best', bbox_to_anchor=(0, 0., 0.95, 1.1))
st.pyplot(fig)
