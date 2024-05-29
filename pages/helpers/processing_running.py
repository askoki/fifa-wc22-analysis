from typing import Tuple, List

import numpy as np
import pandas as pd
from scipy.stats import percentileofscore

from pages.helpers.typing_definitions import RUNNING_PLOT_ITEM


def calculate_and_normalize_physical_stats(stat_df: pd.DataFrame, position: str, player: str, metric: str) -> Tuple[
    float, float]:
    position_stats_df = stat_df.query(f'position == "{position}"')
    player_df = stat_df.query(f'player == "{player}"')
    pool_df = position_stats_df.copy()
    if player not in pool_df.player.unique():
        pool_df = pd.concat([pool_df, player_df])

    pool_df.loc[:, f'{metric}_per90'] = pool_df[metric] / pool_df.total_playing_time * 90
    if metric == 'max_speed':
        pool_df.loc[:, f'{metric}_per90'] = pool_df[metric]
    val = pool_df.query(f'player == "{player}"').squeeze()[f'{metric}_per90']
    pool_df.loc[:, 'percentile_rank'] = pool_df[f'{metric}_per90'].rank(method='max', pct=True)
    pool_df.loc[:, 'POF'] = pool_df[f'{metric}_per90'].apply(
        lambda x: percentileofscore(pool_df[f'{metric}_per90'], x, kind='weak')
    )

    percentile = pool_df.query(f'player == "{player}"').squeeze()['POF']
    return percentile, round(val, 2)


def extract_player_running_data(df: pd.DataFrame, position: str, player_name: str,
                                running_params_list: List[RUNNING_PLOT_ITEM]):
    stats_df = pd.DataFrame()
    for param_name, param_label in running_params_list:
        position_stats_df = df.query(f'position == "{position}" & total_playing_time >  1')
        position_stats_df.loc[:, f'{param_name}_per90'] = position_stats_df[
                                                              param_name] / position_stats_df.total_playing_time * 90
        # do not normalize max speed by 90 min
        if param_name == 'max_speed':
            position_stats_df.loc[:, f'{param_name}_per90'] = position_stats_df[param_name]

        player_perc, player_per90 = calculate_and_normalize_physical_stats(
            stat_df=df, position=position, player=player_name, metric=param_name
        )

        bound_key = f'{param_name}_per90'
        lb = position_stats_df[bound_key].quantile(0.05)
        ub = position_stats_df[bound_key].quantile(0.95)

        p_df = pd.DataFrame({
            'player': player_name,
            'metric': param_name,
            'percentile': player_perc,
            'position': position,
            'per90': player_per90,
            'lb': lb,
            'ub': ub,
            'label': param_label
        }, index=[0])
        stats_df = pd.concat([stats_df, p_df])
    stats_df.reset_index(inplace=True, drop=True)
    return stats_df


def prepare_running_df_for_plotting(df: pd.DataFrame, player1_name: str, player2_name: str, position: str,
                                    param_list: List[RUNNING_PLOT_ITEM]):
    p1_df = extract_player_running_data(df, position=position, player_name=player1_name, running_params_list=param_list)
    p2_df = extract_player_running_data(df, position=position, player_name=player2_name, running_params_list=param_list)

    values1 = p1_df.per90.tolist()
    values2 = p2_df.per90.tolist()

    bound_low = p1_df.lb.tolist()
    bound_low = [1 for val1, val2 in zip(bound_low, p2_df.lb.tolist())]
    bound_high = p1_df.ub.tolist()
    bound_high = [np.max([val1, val2]) for val1, val2 in zip(bound_high, p2_df.ub.tolist())]

    round_int = [False for _ in range(len(bound_low))]
    labels = p1_df.label.tolist()
    return values1, values2, round_int, labels, bound_low, bound_high, pd.concat([p1_df, p2_df])
