import os
import pandas as pd
import streamlit as st
from pages.helpers.plotting import plot_mpl_comparison_radar, RUNNING_COLOR_DICT
from pages.helpers.processing_running import prepare_running_df_for_plotting
from pages.helpers.utils import add_page_logo, add_sidebar_logo, add_expander_toggle
from settings import DATA_DIR, RUNNING_STATS

add_page_logo()
add_sidebar_logo()

st.title('Running performance')

df = pd.read_csv(os.path.join(DATA_DIR, 'running_aggregated_dataset.csv'))

countries = df.team.unique().tolist()
default_country = countries.index('Croatia')
player1_country = st.selectbox('Select player 1 country', countries, index=default_country)
country1_players = df[df.team == player1_country].player.unique().tolist()
default_player1 = country1_players.index('PETKOVIC BRUNO')
player1 = st.selectbox('Select player 1', country1_players, index=default_player1)

player2_country = st.selectbox('Select player 2 country', countries, index=default_country)
country2_players = df[df.team == player2_country].player.unique().tolist()
default_player2 = country1_players.index('LIVAJA MARKO')
player2 = st.selectbox('Select player 2', country2_players, index=default_player2)

playing_positions = df.position.unique().tolist()
player1_position = df[df.player == player1].iloc[0].squeeze().position
default_position = playing_positions.index(player1_position)
playing_position = st.selectbox(
    'Select playing position for comparison', playing_positions, index=default_position
)

values1, values2, round_int, labels, bl, bh, run_comp_df = prepare_running_df_for_plotting(
    df, player1_name=player1, player2_name=player2, position=playing_position, param_list=RUNNING_STATS
)
fig, ax = plot_mpl_comparison_radar(
    values1, values2, labels,
    bound_low=bl, bound_high=bh,
    colors=RUNNING_COLOR_DICT, label1=player1, label2=player2, round_int=[round_int],
    num_rings=6
)
st.pyplot(fig)
add_expander_toggle(button_text='Click for viewing table data', df=run_comp_df)
