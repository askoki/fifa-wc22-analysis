import pandas as pd
from copy import deepcopy
from typing import Tuple, List
from scipy.stats import percentileofscore

from pages.helpers.typing_definitions import FBREF_PLOT_ITEM


def calculate_absolute_and_percentile(stat_df: pd.DataFrame, position: str, player: str, metric: str,
                                      should_normalize=False) -> Tuple[float, float, float, pd.DataFrame]:
    position_stats_df = stat_df.query(f'position == "{position}"')
    player_df = stat_df.query(f'player == "{player}"')
    pool_df = position_stats_df.copy()
    if player not in pool_df.player.unique():
        pool_df = pd.concat([pool_df, player_df])

    pool_df.loc[:, f'{metric}_per90'] = pool_df[metric] / pool_df.minutes_90s
    val = player_df.squeeze()[metric]
    non_norm = deepcopy(val)

    if should_normalize:
        val = pool_df.query(f'player == "{player}"').squeeze()[f'{metric}_per90']
        pool_df.loc[:, 'percentile_rank'] = pool_df[f'{metric}_per90'].rank(method='max', pct=True)
        pool_df.loc[:, 'POF'] = pool_df[f'{metric}_per90'].apply(
            lambda x: percentileofscore(pool_df[f'{metric}_per90'], x, kind='weak')
        )
    else:
        pool_df.loc[:, 'percentile_rank'] = pool_df[metric].rank(method='max', pct=True)
        pool_df.loc[:, 'POF'] = pool_df[metric].apply(
            lambda x: percentileofscore(pool_df[metric], x, kind='weak')
        )

    percentile = pool_df.query(f'player == "{player}"').squeeze()['POF']
    return percentile, non_norm, round(val, 2), pool_df


def extract_player_data(df: pd.DataFrame, position: str, player_name: str, stats_list: List[FBREF_PLOT_ITEM]):
    stats_df = pd.DataFrame()
    for param_name, param_label, should_normalize in stats_list:
        player_perc, player_raw, player_per90, position_stats_df = calculate_absolute_and_percentile(
            stat_df=df, position=position, player=player_name, metric=param_name, should_normalize=should_normalize
        )

        bound_key = f'{param_name}_per90' if should_normalize else param_name
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


def prepare_fbref_df_for_plotting(df: pd.DataFrame, player1_name: str, player2_name: str, position: str,
                                  stats_list: List[FBREF_PLOT_ITEM]):
    p1_df = extract_player_data(df, position=position, player_name=player1_name, stats_list=stats_list)
    p2_df = extract_player_data(df, position=position, player_name=player2_name, stats_list=stats_list)

    values1 = p1_df.per90.tolist()
    values2 = p2_df.per90.tolist()

    bound_low = p1_df.lb.tolist()
    bound_high = p1_df.ub.tolist()
    round_int = [False for _ in range(len(bound_low))]
    labels = p1_df.label.tolist()
    return values1, values2, round_int, labels, bound_low, bound_high, pd.concat([p1_df, p2_df])
