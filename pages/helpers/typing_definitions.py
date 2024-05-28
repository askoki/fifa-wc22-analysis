from typing import Tuple, TypedDict

from matplotlib import pyplot as plt

RadarColors = TypedDict(
    'RadarColors', {
        'facecolor': str,
        'edgecolor': str,
        'hatch': str or None,
    }
)

MplRadarPlotColors = TypedDict(
    'MplRadarPlotColors', {
        'rings_inner': RadarColors,
        'radar': RadarColors,
    }
)

MplComparisonRadarPlotColors = TypedDict(
    'MplComparisonRadarPlotColors', {
        'rings_inner': RadarColors,
        'radar1': RadarColors,
        'radar2': RadarColors,
    }
)

MatplotlibSubplots = Tuple[plt.Figure, plt.Axes]