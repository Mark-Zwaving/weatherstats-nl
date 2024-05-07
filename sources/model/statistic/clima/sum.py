# -*- coding: utf-8 -*-
'''
Library contains a function for the calculation of the climate sum
'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.0.3'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import numpy as np
import sources.model.dayvalues.data as data
import sources.model.dayvalues.select as select
import sources.model.dayvalues.np_days as np_days

def calculate(
        np_lst_days, 
        entity 
    ):
    '''Calculates the mean value for a given entity'''
    sum = cfg.no_val

    # Get the clima days
    np_clima_days = select.clima_days(np_lst_days)

    # Get only valid values, remove NAN values from np lst
    ok, np_lst_valid = np_days.rm_nan(np_clima_days, entity)

    # Calculate climate sum
    if ok:
        col_ent = data.column(entity)
        col_ymd = data.column('yyyymmdd')
        sum = np.sum(np_lst_valid[:,col_ent]) # Calculate sum of all

        # Calculate sum per year
        # Format yyyymmdd / 10000 => yyyy.mmdd => int(yyyy.mmdd) => yyyyy
        # Diff years = end year - start year + end year 
        isy = int( np_lst_valid[ 0, col_ymd] / 10000 ) # Start year
        iey = int( np_lst_valid[-1, col_ymd] / 10000 ) # End yearss
        sum /= ( iey - isy + 1.0 ) # Sum for each year

    return sum
