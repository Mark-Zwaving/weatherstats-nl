# -*- coding: utf-8 -*-
'''
Library contains function to sort a lst with day values
'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.0.1'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import numpy as np
import sources.model.dayvalues.data as data
import sources.model.dayvalues.np_days as np_days

def calculate(
        np_lst_days, 
        entity,
        sort_type='H-L' # high-low or low-high or A-Z, Z-A
    ):
    '''Sorts the np days lst based on a entity e.g: tx, tg, tn)'''
    # Get only valid values, remove NAN values from np lst
    ok, np_lst_valid = np_days.rm_nan(np_lst_days, entity)

    if ok:
        col_ent = data.column(entity)
        # Default sort is ascending HIGH-LOW
        np_lst_sort = np_lst_valid[ np.argsort(np_lst_valid[:,col_ent], axis=0 ,kind='stable') ]

        if sort_type == 'H-L':
            np_lst_sort = np.flip(np_lst_sort, axis=0) # Sort rows

    return np_lst_sort