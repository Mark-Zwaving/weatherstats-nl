# -*- coding: utf-8 -*-
'''Library contains default cells for statistics'''
__author__     = 'Mark Zwaving'
__email__      = 'markzwaving@gmail.com'
__copyright__  = 'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    = '0.0.6' 
__maintainer__ = 'Mark Zwaving'
__status__     = 'Development'

################################################################################
# EXAMPLES
# INFO                                                            TABLE COLUMN
################################################################################
# Info place name                                              => inf_place 
# Info province name                                           => inf_province 
# Info period 1                                                => inf_period-1 
# Mean temperature                                             => ave_tg
# Climate mean temperature                                     => clima_ave_tg
# Maximum temperature                                          => max_tx
# Minimum maximum temperatuur                                  => min_tx 
# Minimum mean temperatuur                                     => min_tg 
# Minimum temperature                                          => min_tn
# Minimum temperature 10cm                                     => min_t10n 
# Hellmann index/number                                        => ndx_hellmann
# Frostsum index/number (NL)                                   => ndx_frostsum
# Sum hours sunshine                                           => sum_sq
# Climate sum sunshine hours                                   => clima_sum_sq 
# Sum rain millimeter                                          => sum_rh 
# Climate sum rain millimeter                                  => clima_sum_rh 
# Count days _ sunshine _ greater equal _ 10hours              => cnt_sq_ge_10 
# Count days _ rain _ greater equal _ 10mm                     => cnt_rh_ge_10 
# Count days _ maximum temperature  _ greater than 25C         => cnt_tx_>_25
# Count days _ mean temperature _ lower than _  0C             => cnt_tg_<_0
# Count days _ mininimum temperature  _ lower than _ 10C       => cnt_tn_<_-10
################################################################################

################################################################################
# Default statistics cells for seasons (winter, summer and winter-summer), 
# extremes, counters and default lists
################################################################################ 

# Favorite default 1 
lst_favorite_1 = [ 
    'inf_place', 'inf_province', 'inf_period-1', 
    'ave_tg', 'clima_ave_tg', 'max_tx', 'min_tn', 
    'cnt_tx_>=_25', 'clima_cnt_tx_>=_25', 
    'cnt_tn_<_0', 'clima_cnt_tn_<_0', 
    'sum_sq', 'clima_sum_sq', 'cnt_sq_>=_10',
    'sum_rh', 'clima_sum_rh', 'cnt_rh_>=_10',
    'ndx_heat-ndx', 'clima_ndx_heat-ndx',
    'ndx_hellmann', 'clima_ndx_hellmann'
]

# Add your own favorite option to the menu
# See - lst_menu - 
lst_favorite_2 = [ 
    # Here your statistics cells
]


# Default cell options for a table of extremes
lst_extremes = [
    'inf_place', 'inf_period-1', 
    'max_tx', 'max_tg', 'max_tn', 'max_t10n', 
    'min_tx', 'min_tg', 'min_tn', 'min_t10n',
    'max_sq', 'max_rh', 'max_rhx', 'max_fg', 'max_fhx', 'max_px', 'max_pg', 
    'min_pg', 'min_pn',  'min_ux', 'min_ug', 'min_un', 
    'max_ev24', 'max_q'
]

# Default cells to count conditional days
lst_counters = [
    'inf_place', 'inf_period-1', 
    'cnt_tx_>=_20', 'cnt_tx_>=_25', 'cnt_tx_>=_30', 'cnt_tx_>=_35', 
    'cnt_tx_ge_40', 'cnt_tg_>=_18', 'cnt_tn_>=_20', 
    'cnt_tx_<_0', 'cnt_tg_<_0', 'cnt_tn_<_0', 'cnt_tn_<_-5', 
    'cnt_tn_<_-10', 'cnt_tn_<_-15', 'cnt_tn_<_-20'
]

# Default cells winter
lst_winter = [
    'inf_place', 'inf_province', 'inf_period-1', 
    'ave_tg', 'clima_ave_tg', 
    'min_tx', 'min_tg', 'min_tn', 'min_t10n', 
    'ndx_hellmann', 'ndx_frost-sum', # 'ndx_ijnsen', 
    'sum_sq', 'clima_sum_sq', 
    'sum_rh', 'clima_sum_rh', 'cnt_rh_>=_10', 
    'cnt_tx_<_0', 'cnt_tg_<_0', 
    'cnt_tn_<_0', 'cnt_tn_<_-5', 
    'cnt_tn_<_-10', 'cnt_tn_<_-15', 'cnt_tn_<_-20', 
]

# Default cells summer
lst_summer = [ 
    'inf_place', 'inf_province', 'inf_period-1', 
    'ave_tg', 'clima_ave_tg', 
    'max_tx', 'max_tg', 'max_tn', 
    'ndx_heat-ndx', 
    'sum_sq', 'clima_sum_sq', 'cnt_sq_>=_10',
    'sum_rh', 'clima_sum_rh', 'cnt_rh_>=_10',
    'cnt_tx_>=_25', 'cnt_tx_>=_30', 'cnt_tx_>=_35', 
    'cnt_tn_>=_20'
]

# Example spring ?
lst_spring = [ 
    'inf_place', 'inf_period-1', 
    'ave_tg', 'clima_ave_tg',  
    'max_tx', 'min_tx', 'max_tn', 
    'min_tn', 'ndx_heat-ndx', 'ndx_frost-sum', 
    'sum_sq', 'sum_rh', 
    'cnt_tx_>_20', 'cnt_tn_<_0', 'cnt_tn_<_-5'
]

# Default cells winter and summer
lst_winter_summer = [
    'inf_place', 'inf_province', 'inf_period-1', 
    'ave_tg', 'clima_ave_tg',
    'ndx_heat-ndx', 'ndx_hellmann', 'ndx_frost-sum', # 'ndx_ijnsen', 
    'max_tx', 'max_tg', 'max_tn', 
    'min_tx', 'min_tg', 'min_tn', 'min_t10n', 
    'sum_sq', 'clima_sum_sq', 'cnt_sq_>=_10',
    'sum_rh', 'clima_sum_rh', 'cnt_rh_>=_10',
    'cnt_tx_>=_20', 'cnt_tx_>=_25', 'cnt_tx_>=_30', 'cnt_tx_>=_35', 'cnt_tg_>=_20', 
    'cnt_tx_<_0', 'cnt_tg_<_0', 'cnt_tn_<_0', 
    'cnt_tn_<_-5', 'cnt_tn_<_-10', 'cnt_tn_<_-15', 'cnt_tn_<_-20'
]


################################################################################
################################################################################
# Menu with the default statistics lists to show in the default statistics menu

# Main header title text
title_statistics = 'STATISTICS TABLES (see defaults.py)' 

# Add the menu titles with the statistics lists to the default tables menu
lst_menu = [
    ['OK Winter statistics',             lst_winter ],
    ['OK Summer statistics',             lst_summer ],
    ['OK Winter and summer statistics',  lst_winter_summer ],
    ['OK Extreme statistics',            lst_extremes ], 
    ['OK Counter statistics',            lst_counters ], 
    ['OK My favorite statistics 1',      lst_favorite_1],
    # ['OK My favorite statistics 2',      lst_favorite_2],
]
################################################################################
################################################################################

################################################################################
# Other options

# Default cells to show in search for days
lst_search4day = [
    'inf_num', 'inf_place', 'inf_province', 'inf_period-1', 'inf_day', 
    'day_tx', 'day_tg', 'day_tn', 'day_t10n', 'day_sq', 'day_sp', 'day_rh', 
    'day_rhx', 'day_dr', 'day_pg', 'day_px', 'day_pn', 'day_ug', 'day_ux', 
    'day_un', 'day_ng', 'day_ddvec', 'day_fhvec', 'day_fg', 'day_fhx', 
    'day_fhn', 'day_fxx', 'day_vvx', 'day_vvn', 'day_q', 'day_ev24'
]

# All the cells for making dayvalues
lst_dayvalues = [
    'tx', 'tg', 'tn', 't10n', 'ddvec', 'fhvec', 'fg', 'fhx', 'fhn', 'fxx', 
    'sq', 'sp', 'rh', 'rhx',  'dr', 'px', 'pg', 'pn', 'ux', 'ug', 'un', 
    'vvx', 'vvn', 'ng', 'q', 'ev24'
]
