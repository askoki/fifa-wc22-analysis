import json
import os

import pandas as pd
import streamlit as st

from pages.helpers.plotting import plot_mpl_comparison_radar, FBREF_COLOR_DICT
from pages.helpers.processing_fbref import prepare_fbref_df_for_plotting
from pages.helpers.utils import add_page_logo, add_sidebar_logo, add_expander_toggle, add_pages_to_sidebar
from settings import DATA_DIR, FBREF_ATT_STATS, FBREF_TEC_PHY_STATS

add_page_logo()
add_sidebar_logo()
add_pages_to_sidebar()

st.title('FBRef performance')

df = pd.read_csv(os.path.join(DATA_DIR, 'fbref_dataset_cleaned.csv'))

countries = df.team.unique().tolist()
default_country = countries.index('Croatia')
player1_country = st.selectbox('Select player 1 country', countries, index=default_country)
country1_players = df[df.team == player1_country].player.unique().tolist()
default_player1 = country1_players.index('Bruno Petković')
player1 = st.selectbox('Select player 1', country1_players, index=default_player1)

player2_country = st.selectbox('Select player 2 country', countries, index=default_country)
country2_players = df[df.team == player2_country].player.unique().tolist()
default_player2 = country1_players.index('Marko Livaja')
player2 = st.selectbox('Select player 2', country2_players, index=default_player2)

playing_positions = df.position.unique().tolist()
player1_position = df[df.player == player1].iloc[0].squeeze().position
default_position = playing_positions.index(player1_position)
playing_position = st.selectbox(
    'Select playing position for comparison', playing_positions, index=default_position
)

st.header('Attacking stats')
values1, values2, round_int, labels, bl, bh, att_comp_df = prepare_fbref_df_for_plotting(
    df, player1_name=player1, player2_name=player2, position=playing_position, stats_list=FBREF_ATT_STATS
)
fig, ax = plot_mpl_comparison_radar(
    values1, values2, labels,
    bound_low=bl, bound_high=bh,
    colors=FBREF_COLOR_DICT, label1=player1, label2=player2, round_int=[round_int],
    num_rings=6
)
st.pyplot(fig)
add_expander_toggle(button_text='Click for viewing table data', df=att_comp_df)

st.divider()

st.header('Tactical, passing and physical stats')
tac_values1, tac_values2, tac_round_int, tac_labels, tac_bl, tac_bh, tac_comp_df = prepare_fbref_df_for_plotting(
    df, player1_name=player1, player2_name=player2, position=playing_position, stats_list=FBREF_TEC_PHY_STATS
)
fig2, ax2 = plot_mpl_comparison_radar(
    tac_values1, tac_values2, tac_labels,
    bound_low=tac_bl, bound_high=tac_bh,
    colors=FBREF_COLOR_DICT, label1=player1, label2=player2, round_int=[tac_round_int],
    num_rings=6
)
st.pyplot(fig2)
add_expander_toggle(button_text='Click for viewing table data', df=tac_comp_df)

st.subheader('Metrics explanation')

with open(os.path.join(DATA_DIR, 'fbref_data_description.json'), 'r') as j:
    description_json = json.loads(j.read())
st.json(description_json)
