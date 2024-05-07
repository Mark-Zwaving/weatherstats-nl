# -*- coding: utf-8 -*-
'''
Library contains a function to select days based on a certain condition
E.g days: TX > 25
'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.0.5'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import numpy as np
import sources.view.console as cnsl
import sources.view.text as text
import sources.model.dayvalues.data as data
import sources.model.dayvalues.np_days as np_days

def calculate(
        np_lst_days,   # numpy days 2d
        entity,        # TX, TG
        operator,      # >, >=, lt, < et cetera
        value          # float
    ):
    '''Function an np array based on conditional values like TX > 30 for example
       Input valua is not a raw value!!!'''
    # Are there valid days for a given entity
    ok, np_lst_valid = np_days.rm_nan(np_lst_days, entity) 

    if ok: 
        # Make operator lowercase 
        op = operator.lower() 

        # Check if operator is allowed 
        if op in text.lst_op: 

            # Get correct user to raw value
            raw_val = data.user_to_raw(value, entity) 

            # Get column key for entity
            col = data.column(entity) 

            # Check condition
            if op in text.lst_gt: 
                np_lst_condit_keys = np.where( np_lst_valid[:,col]  > raw_val )

            elif op in text.lst_ge: 
                np_lst_condit_keys = np.where( np_lst_valid[:,col] >= raw_val )

            elif op in text.lst_eq: 
                np_lst_condit_keys = np.where( np_lst_valid[:,col] == raw_val )

            elif op in text.lst_lt: 
                np_lst_condit_keys = np.where( np_lst_valid[:,col]  < raw_val )

            elif op in text.lst_le: 
                np_lst_condit_keys = np.where( np_lst_valid[:,col] <= raw_val )

            elif op in text.lst_ne: 
                np_lst_condit_keys = np.where( np_lst_valid[:,col] != raw_val )

        else: 
            ok = False
            cnsl.log(f'Error in operator {operator} not found', True )

    # input(np_lst_condit_keys)

    if ok:
        np_lst_res = np_lst_valid[np_lst_condit_keys]
    else:
        np_lst_res = np.zeros(shape=(1, 41)) # Wrong

    # Return valid lst and conditional lst
    return ok, np_lst_res, np_lst_valid
