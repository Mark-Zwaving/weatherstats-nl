# -*- coding: utf-8 -*-
'''Redirect to functins to select days from data'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__version__    =  '0.0.8'
__license__    =  'GNU General Public License version 2 - GPLv2'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import numpy as np
import sources.model.dayvalues.chk_period as chk 
import sources.model.dayvalues.select as select 
import sources.view.console as cnsl

def process(
        np_lst_days, 
        period
    ):
    '''Function returns a np array with data based on a period.
       Function can be used to do date check_only too.'''
    ok = True
    np_res = np.array([[]])
    
    # OPTION: from date/day to date/day 
    # YYYYMMDD-YYYYMMDD 
    if chk.yyyymmdd_yyyymmdd(period):
        print('YYYYMMDD-YYYYMMDD')
        np_res = select.yyyymmdd_yyyymmdd(np_lst_days, period)

    # OPTION: from a given full start year untill maximum date
    # * or x are variable and can be omitted
    # YYYY****-********  
    # YYYY****-******    
    # YYYY****-****    
    # YYYY****-***  
    # YYYY****-**    
    # YYYY****-*
    # YYYY****- 
    # YYYY***- 
    # YYYY**- 
    # YYYY*- 
    # YYYY- 
    elif chk.yyyy_(period):
        print('YYYY****-********')
        np_res = select.yyyy_(np_lst_days,period)

    # OPTION: from a full year to a full year
    # Wildcards x and * are variable and can be omitted
    # YYYY****-YYYY****
    # YYYY-YYYY
    elif chk.yyyy_yyyy(period):
        print('YYYY****-YYYY****')
        np_res = select.yyyy_yyyy(np_lst_days,period)

    # TODO
    # OPTION: from a full year to a full year plus month
    # Wildcards x and * are variable and can be omitted
    # YYYY****-YYYYMM**
    # YYYY****-YYYYMM
    # YYYY-YYYYMM
    elif chk.yyyy_yyyymm(period):
        print('YYYY****-YYYYMM**')
        np_res = select.yyyy_yyyymm(np_lst_days,period)

    # TODO
    # OPTION: from a full year to a full year plus month and day
    # Wildcards x and * are variable and can be omitted
    # YYYY****-YYYYMMDD
    # YYYY-YYYYMMDD
    elif chk.yyyy_yyyymmdd(period):
        print('YYYY****-YYYYMMDD')
        np_res = select.yyyy_yyyymmdd(np_lst_days,period)

    # OPTION: from a full start date to an end month
    # Wildcards x and * are variable and can be omitted
    # YYYYMMDD-YYYYMM**
    # YYYYMMDD-YYYYMM
    elif chk.yyyymmdd_yyyymm(period):
        print('YYYYMMDD-YYYYMM**')
        np_res = select.yyyymmdd_yyyymm(np_lst_days,period)

    # OPTION: select a period of months and days, underscore must be used
    # _MMDD-_MMDD 
    # ****_MMDD-****_MMDD 
    # YYYY_MMDD-YYYY_MMDD
    # Examples: 
    # winter: _1201-_0228
    # summer: _0622-_0921
    elif chk.yyyy_mmdd_yyyy_mmdd(period):
        print('****_MMDD-****_MMDD')
        np_res = select.yyyy_mmdd_yyyy_mmdd(np_lst_days,period)

    # OPTION: get a day in a year
    # yyyymmdd
    elif chk.yyyymmdd(period):
        print('yyyymmdd')
        np_res = select.yyyymmdd(np_lst_days,period)

    # OPTION: All the data, one wildcard
    # OPTION * 
    elif chk.x(period):
        np_res = np_lst_days # All days

    # OPTION: The current whole year
    # ****
    elif chk.xxxx(period):
        print('xxxx')
        np_res = select.xxxx(np_lst_days,period)

    # The current month
    # **
    elif chk.xx(period):
        print('xxx')
        np_res = select.xx(np_lst_days,period)

    # OPTION: The current day/date in month
    # ***
    elif chk.xxx(period):
        print('xxx')
        np_res = select.xxx(np_lst_days,period)

    # OPTION: The whole year
    # YYYY****
    # YYYY
    elif chk.yyyyxxxx(period):
        print('yyyyxxxx')
        np_res = select.yyyyxxxx(np_lst_days,period)

    # OPTION: get the day for every available year
    # ****MMDD 
    elif chk.xxxxmmdd(period):
        print('xxxxmmdd')
        np_res = select.xxxxmmdd(np_lst_days,period)

    # OPTION: The whole month in a year
    # YYYYMM**
    # YYYYMM 
    # * or x can be omitted!
    elif chk.yyyymmxx(period):
        print('YYYYMM**')
        np_res = select.yyyymmxx(np_lst_days,period)

    # OPTION: get selected month for every years
    # ****MM**
    # ****MM
    elif chk.xxxxmmxx(period):
        print('****MM**, MM')
        np_res = select.xxxxmmxx(np_lst_days,period)

    # OPTION NOT FOUND ERROR
    else:
        ok = False
        cnsl.log(f"Period {period} option not available!", cfg.error)

    return ok, np_res



# OPTIONS: ********-********

# OPTION: YYYY****-YYYY**** | YYYY**-YYYY** | YYYY-YYYY
# From full year to year

# OPTION: YYYYMMDD-YYYYMM** | YYYYMMDD-YYYYMM**
# A start day untill possible month end end

# OPTION YYYY*MMDD*-YYYY*MMDD*
# A certain period in a year. From startyear to endyear

# ADVANCED OPTIONS for more different periods in a given period
# OPTION YYYY-YYYYMMDD* | YYYY****-YYYYMMDD*
# A certain day in a year. From startyear to endyear.

# OPTION YYYY****-YYYYMM** | YYYY-YYYYMM** | YYYY-YYYYMM
# A full 1 month in an year. From startyear to endyear

# OPTION ******** or *
# All the data # All time

# OPTION YYYYMMDD
# Get only one day in a year

# OPTION ****
# The current whole year

# OPTION **
# The current month

# OPTION YYYY**** | YYYY
# The whole year

# OPTION YYYYMM** | YYYYMM
# The whole month in a year

# ADVANCED OPTIONS for more different periods in a given period
# OPTION ****MM** | ****MM
# Get selected month in all the years

# OPTION ****MMDD
# Get the day for every available year
