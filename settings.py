import os
from typing import List

from pages.helpers.typing_definitions import FBREF_PLOT_ITEM

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
FONTS_DIR = os.path.join(ROOT_DIR, 'pages', 'fonts')

SB_RED = '#dc2228'
SB_LIGHT_RED = '#b9888c'

DARK_BLUE = '#4a86e8'
DARK_RED = '#db070d'
SB_LIGHT_BLUE = '#7fc3dd'
SB_GRAY = '#dddddd'

PINK = '#ffabab'
TEAL = '#6ec4d6'

ROBOTO_THIN = os.path.join(FONTS_DIR, 'Roboto-Thin.ttf')
ROBOTO_BOLD = os.path.join(FONTS_DIR, 'RobotoSlab.ttf')

FBREF_ATT_STATS: List[FBREF_PLOT_ITEM] = [
    ('goals_pens', 'npG', True),
    ('npxg', 'npxG', True),
    ('shots_per90', '$Shots_{90}$', False),
    ('assists', '$Assists_{90}$', True),
    ('xg_assist', 'npxG+xAG', True),
    ('npxg_xg_assist', 'xAG', True),
    ('sca_per90', 'Shot-Creating Actions', False),
]

FBREF_TEC_PHY_STATS: List[FBREF_PLOT_ITEM] = [
    ('passes', 'Passes Attempted', True),
    ('passes_pct', 'Pass Completion (%)', False),
    ('progressive_passes', 'Progressive Passes', True),
    ('dribbles_completed', 'Successful Take-Ons', True),
    ('touches_att_pen_area', 'Touches in Att', True),
    ('progressive_passes_received', 'Progressive Passes Received', True),
    ('tackles', 'Tackles', True),
    ('interceptions', 'Interceptions', True),
    ('blocks', 'Blocks', True),
    ('clearances', 'Clearances', True),
    ('aerials_won', 'Aerials Won', True),
]
