# -*- coding: utf-8 -*-
'''
Library contains functions for the calculation of the heat ndx
'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.0.2'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import numpy as np
import sources.model.statistic.conditional as conditional
import sources.model.dayvalues.data as data

def calculate_nl(
    np_lst_days
):
    '''Function calculates heatndx NL version'''
    # Inits for heat and tg column
    heat = 0.0

    # Get lst with all the heat days
    # Value must not be raw!
    ok, np_lst_heat, _ = conditional.calculate(np_lst_days, 'tg', '>', 18.0)

    if ok: 
        # Column TG
        col_tg = data.column('tg')

        # Sum substract 18 degrees
        np_lst_heat_nl = np_lst_heat[:, col_tg] - 180.0 # Must be raw value

        # Sum the heat nl
        heat = np.sum(np_lst_heat_nl)  

    return heat, np_lst_heat
