# -*- coding: utf-8 -*-
'''Functions for updating, creating np days arrays'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.0.4'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import numpy as np
import sources.model.dayvalues.data as data

def new():
    '''Create a new numpy dayvalues list '''
    shape = ( 1, len(data.knmi_entities) ) 
    return np.empty( shape, dtype=np.float32 )

def rm_row(np_lst, row=0):
    '''Remove row from np dayvalues list'''
    return np.delete(np_lst, (row), axis=0)

def rm_nan(np_lst_days, entity):
    '''Removes nan values based on entity values from np days period 2d . 
        Returns a new 2D np days array'''
    # Get colum key entity
    col = data.column(entity) 

    # Get only valid values, remove NAN values from np lst
    np_lst_valid = np_lst_days[~np.isnan(np_lst_days[:,col])]

    # Are there valid values?
    ok = True if np_lst_valid.size > 0 else False

    return ok, np_lst_valid

def unique(np_lst_days, entity):
    '''Removes double values based on a entity column'''
    # Are there doubles found or not
    found = False 

    # Get colum key entity
    col = data.column(entity) 

    # Make a new result np ldays lst
    np_lst_result = new()

    # Walkthrough and check if on same day
    for day1 in np_lst_days:
        for day2 in np_lst_days:
            # Same value for entity found
            if day1[col] == day2[col]: 
                np_lst_result.append(day1) 
                found = True

    # Remove first dummy row
    rm_row(np_lst_result, 0)

    return found, np_lst_result
