# -*- coding: utf-8 -*-
'''
Library contains function for the calculation of the ijnsen index
Calculation:
v = TN <  0
y = TX <  0
z = TN < -10 
ijnsen = (v * v / 363.0)  +  (2.0 * y / 3.0)  +  (10.0 * z / 9.0) 
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
import sources.model.dayvalues.select as select

def calculate( 
        np_lst_days # Numpy list of days to calculate ijnsen
    ):
    # Init variables
    ijnsen, V, Y, Z = 0.0, 0.0, 0.0, 0.0

    # List ijnsen (new)
    np_days_ijnsen = select.new_np_lst_days()

    # V: get days tn < 0
    ok, np_days_tn_0, _ = conditional.calculate(np_lst_days, 'tn', '<', 0.0)
    if ok:
        V = len(np_days_tn_0)
        # Add np_days_tn_0 to np_days_ijnsen
        np_days_ijnsen = np.concatenate( [np_days_ijnsen, np_days_tn_0], axis=0 )

    # Y: get days tx < 0 
    ok, np_days_tx_0, _ = conditional.calculate(np_lst_days, 'tx', '<', 0.0) 
    if ok:
        Y = len(np_days_tx_0)
        # Add np_days_tx_0 to np_days_ijnsen
        np_days_ijnsen = np.concatenate( [np_days_ijnsen, np_days_tx_0], axis=0 )

    # Z: get days tn < -10 
    ok, np_days_tn__10, _ = conditional.calculate(np_lst_days, 'tn', '<', -100.0) 
    if ok:
        Z = len(np_days_tn__10)
        # Add np_days_tx_0 to np_days_ijnsen
        np_days_ijnsen = np.concatenate( [np_days_ijnsen, np_days_tx_0], axis=0 )

    # Remove 1st row
    np_days_ijnsen = select.rm_row_lst_days(np_days_ijnsen, 0)

    # Remove duplicates based on the dates
    np_days_ijnsen = np.unique(np_days_ijnsen[:,data.column('yyyymmdd')], axis=0)

    # Calculate ijnsen
    ijnsen = (V * V / 363.0)  +  (2.0 * Y / 3.0)  +  (10.0 * Z / 9.0) 

    return ijnsen, np_days_ijnsen, np_days_tx_0, np_days_tn_0, np_days_tn__10
