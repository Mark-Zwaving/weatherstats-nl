# -*- coding: utf-8 -*-
'''
Library contains function for the calculation of the hellmann index
Formula: Σabs(TG < 0)  
'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.0.3'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import numpy as np
import sources.model.dayvalues.data as data
import sources.model.statistic.conditional as conditional

def calculate( 
        np_lst_days # Numpy list of days to calculate hellmann 
    ):
    # Init variables hellmann an tg column num
    hellmann = 0.0

    # Get lst with all the hellman days -> tg < 0 
    ok, np_lst_hellmann, _ = conditional.calculate(np_lst_days, 'tg', '<', 0.0)

    # If hellmann days found
    if ok: # Sum all abs(tg) to calculate the hellmann index
        hellmann = abs(np.sum(np_lst_hellmann[:, data.column('tg')]))

    # Return hman value plus np lst
    return hellmann, np_lst_hellmann
