# -*- coding: utf-8 -*-
'''
Library contains function for the calculation of the frostsum
NL:
    Get all the days with a TX < 0 and TN < 0
    Calculate the sum of all these days and make it absolute (=positive)
    Sum the result of tn and tx together 
'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.0.3'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import numpy as np
import sources.model.statistic.conditional as conditional
import sources.model.dayvalues.data as data

def calculate_nl(np_lst_days):
    '''Function calculates frost sum''' 
    # Init variables
    frostsum, tx_sum, tn_sum = 0.0, 0.0, 0.0

    # Get days tx < 0
    ok_tx, np_days_tx_0, _ = conditional.calculate(np_lst_days, 'tx', '<', 0.0)
    if ok_tx: 
        # Sum tx < 0
        tx_sum = abs(np.sum(np_days_tx_0[:, data.column('tx')]))

    # Get days tn < 0 
    ok_tn, np_days_tn_0, _ = conditional.calculate(np_lst_days, 'tn', '<', 0.0) 
    if ok_tn: 
        # Sum tn < 0
        tn_sum = abs(np.sum(np_days_tn_0[:, data.column('tn')]))

    # Make total days with frostsum days
    np_lst_frostsum = np.concatenate( [np_days_tx_0, np_days_tn_0], axis=0 )

    # Frostsum
    frostsum = tx_sum + tn_sum

    return frostsum, np_lst_frostsum, np_days_tn_0, np_days_tx_0, tn_sum, tx_sum
