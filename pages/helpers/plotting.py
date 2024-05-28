from typing import List

from matplotlib import font_manager
from mplsoccer import Radar, grid
from pages.helpers.typing_definitions import MplComparisonRadarPlotColors, MatplotlibSubplots, RadarColors
from settings import SB_GRAY, SB_RED, SB_LIGHT_BLUE, DARK_RED, DARK_BLUE, PINK, TEAL, ROBOTO_THIN, ROBOTO_BOLD


def create_mpl_radar_color(facecolor: str, edgecolor: str, hatch=None) -> RadarColors:
    return {
        'facecolor': facecolor,
        'edgecolor': edgecolor,
        'hatch': hatch
    }


FIFA_COLOR_DICT = {
    'rings_inner': create_mpl_radar_color(facecolor=SB_GRAY, edgecolor='lightgray'),
    'radar1': create_mpl_radar_color(facecolor=SB_RED, edgecolor=SB_RED),
    'radar2': create_mpl_radar_color(facecolor=SB_LIGHT_BLUE, edgecolor=SB_LIGHT_BLUE),
}

FBREF_COLOR_DICT = {
    'rings_inner': create_mpl_radar_color(facecolor=SB_GRAY, edgecolor='darkgray', hatch='.'),
    'radar1': create_mpl_radar_color(facecolor=DARK_RED, edgecolor=DARK_RED),
    'radar2': create_mpl_radar_color(facecolor=DARK_BLUE, edgecolor=DARK_BLUE),
}

RUNNING_COLOR_DICT = {
    'rings_inner': create_mpl_radar_color(facecolor=SB_GRAY, edgecolor='gray', hatch='O'),
    'radar1': create_mpl_radar_color(facecolor=PINK, edgecolor=DARK_RED),
    'radar2': create_mpl_radar_color(facecolor=TEAL, edgecolor=DARK_BLUE),
}

robotto_thin = font_manager.FontProperties(fname=ROBOTO_THIN)
robotto_bold = font_manager.FontProperties(fname=ROBOTO_BOLD)


def plot_mpl_comparison_radar(
        values1: List[float], values2: List[float], parameter_labels: List[str], bound_low: List[float],
        bound_high: List[float], colors: MplComparisonRadarPlotColors, label1: str, label2: str,
        round_int=list or bool, num_rings=10) -> MatplotlibSubplots or None:
    round_int = round_int if type(round_int) == list else [True] * len(parameter_labels)
    radar = Radar(
        parameter_labels,
        bound_low,
        bound_high,
        round_int=round_int,
        num_rings=num_rings,
        ring_width=1,
        center_circle_radius=1
    )
    fig, axs = grid(
        figheight=6,
        grid_height=0.8,
        title_height=0.06,
        endnote_height=0.025,
        title_space=0,
        endnote_space=0,
        grid_key='radar',
        axis=False
    )
    radar.setup_axis(ax=axs['radar'])
    rings_inner = radar.draw_circles(
        ax=axs['radar'], facecolor=colors['rings_inner']['facecolor'],
        edgecolor=colors['rings_inner']['edgecolor'],
        hatch=colors['rings_inner']['hatch']
    )

    radar1, vertices1 = radar.draw_radar_solid(
        values1, ax=axs['radar'],
        kwargs={
            'facecolor': colors['radar1']['facecolor'],
            'alpha': 0.6,
            'edgecolor': colors['radar1']['edgecolor'],
            'lw': 3
        }
    )
    axs['radar'].scatter(
        vertices1[:, 0], vertices1[:, 1],
        label=label1,
        c=colors['radar1']['facecolor'], edgecolors=colors['radar1']['edgecolor'], marker='o', s=50, zorder=2
    )
    radar2, vertices2 = radar.draw_radar_solid(
        values2, ax=axs['radar'],
        kwargs={
            'facecolor': colors['radar2']['facecolor'],
            'alpha': 0.6,
            'edgecolor': colors['radar2']['edgecolor'],
            'lw': 3
        }
    )
    axs['radar'].scatter(
        vertices2[:, 0], vertices2[:, 1],
        label=label2,
        c=colors['radar2']['facecolor'], edgecolors=colors['radar2']['edgecolor'], marker='o', s=50, zorder=2
    )
    range_labels = radar.draw_range_labels(ax=axs['radar'], fontsize=6)
    param_labels = radar.draw_param_labels(ax=axs['radar'], fontsize=8)
    lines = radar.spoke(ax=axs['radar'], color='#a6a4a1', linestyle='--', zorder=2)
    # legend
    legend_left = axs['title'].text(
        0.01, 0.28, label1, fontsize=16,
        fontproperties=robotto_bold,
        ha='left', va='center', color=colors['radar1']['facecolor']
    )
    legend_right = axs['title'].text(
        0.6, 0.28, label2, fontsize=16,
        fontproperties=robotto_bold,
        ha='left', va='center', color=colors['radar2']['facecolor']
    )
    return fig, axs['radar']
