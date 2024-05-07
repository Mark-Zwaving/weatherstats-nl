# -*- coding: utf-8 -*-
'''
Library contains function for the calculation of the climate condtional counters 
'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.0.3'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import sources.model.dayvalues.data as data
import sources.model.dayvalues.select as select
import sources.model.statistic.conditional as conditonal

def calculate(
        np_lst_days_period, # All the days in the given period
        entity,             # E.g: tx, rh
        operator,           # E.g: >, <=
        value               # Input value of user
    ):
    '''Calculates the mean value for a given entity'''
    # Init vars
    total = cfg.no_val
    
    # Get all the clima days
    np_clima_days = select.clima_days(np_lst_days_period)

    # Get the list with the conditional days
    ok, np_lst_condit, np_lst_valid = conditonal.calculate(np_clima_days, entity, operator, value)

    if ok:
        # Count all the days 
        total = len(np_lst_condit)

        # Calculate total per year
        # Format yyyymmdd / 10000 => yyyy.mmdd => int(yyyy.mmdd) => yyyyy
        # Diff years = end year - start year + end year 
        col_ymd = data.column('yyyymmdd') # Column for the dates
        isy = int( np_lst_valid[ 0, col_ymd] / 10000 ) # Start year
        iey = int( np_lst_valid[-1, col_ymd] / 10000 ) # End years
        total /= ( iey - isy + 1.0 ) # Count for each year

    return total