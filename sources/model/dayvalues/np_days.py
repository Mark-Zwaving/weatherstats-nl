# -*- coding: utf-8 -*-
'''Functions for updating, creating np days arrays'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.0.4'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg, stations
import numpy as np
import sources.model.dayvalues.data as data

def new():
    '''Create a new numpy dayvalues list '''
    shape = ( 1, len(data.knmi_entities) ) 
    return np.empty( shape, dtype=np.float32 )

def rm_row(np_lst, row=0):
    '''Remove row from np dayvalues list'''
    return np.delete(np_lst, (row), axis=0)

def get_station(np_days):
    # Get wmo number
    wmo = str(int(np_days[0, data.STN]))

    for station in stations.lst:
        if str(station.wmo) == wmo:
            return station
    
    return False

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

def update_low_values__1(np_lst_days):
    '''Function updates the -1 raw value in the data. 
       Note: -1 raw value in lst is 0.1 for real
       The -1 raw value is used for small values between 0.1 and 0.0 
       The weatherdata is given in integers. 
       That way it is not possible to have floating point values
    ''' 
    find_low_val = -1.0  # Lower dan 1 value, -1 raw is -> -0.1
    replace_val  = cfg.knmi_dayvalues_low_measure_val # Sustitute value

    # Columns to replace -1.0 for
    col_rh, col_rhx, col_sq = data.column('RH'), data.column('RHX'), data.column('SQ')

    # Loop days and update if -1 value for the spicific data is found 
    for ndx, value in np.ndenumerate(np_lst_days):
        row, col = ndx # Get current indices

        # Check rh
        if col == col_rh: # If col is rh col, Check if rh value is -1
            if value == find_low_val: # If rh == -1
                np_lst_days[row,col] = replace_val # Update rh value to replace value

        # Check rhx
        elif col == col_rhx: # If col is rhx col, Check if rhx value is -1
            if value == find_low_val: # If rhx == -1
                np_lst_days[row,col] = replace_val # Update rhx value to replace value

        # Check sq
        elif col == col_sq: # If col is sq col, Check if sq value is -1
            if value == find_low_val: # If sq == -1
                np_lst_days[row,col] = replace_val   # Update ss value to replace value

    return np_lst_days