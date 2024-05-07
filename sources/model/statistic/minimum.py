# -*- coding: utf-8 -*-
'''
Library contains function for the calculation of the minimum value for a given entity
'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.0.2'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import numpy as np
import sources.model.dayvalues.data as data
import sources.model.dayvalues.np_days as np_days

def calculate(np_lst_days, entity):
    '''Calculates the maximum value for a given entity'''
    col = data.column(entity) # Get column key

    # Get only valid values, remove NAN values from np lst
    ok, np_lst_valid = np_days.rm_nan(np_lst_days, entity)

    # Get minimum value
    minn = np.min(np_lst_days[:,col]) 

    # Get the min day
    np_day_min = np_lst_valid[np.where(np_lst_valid[:,col] == minn)] 

    return minn, np_day_min, np_lst_valid
