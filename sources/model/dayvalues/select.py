# -*- coding: utf-8 -*-
'''Select days from data'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__version__    =  '0.0.9'
__license__    =  'GNU General Public License version 2 - GPLv2'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import calendar, numpy as np
import sources.model.ymd as ymd 
import sources.model.utils as utils 
import sources.model.dayvalues.data as data 
import sources.model.dayvalues.chk_period as chk
import sources.model.dayvalues.np_days as np_days
import sources.model.stations as stations
import sources.control.dayvalues.read as dayval_read

# OPTION: from date/day to date/day 
# YYYYMMDD-YYYYMMDD
def yyyymmdd_yyyymmdd(
        np_lst_days,  # Numpy list with days
        period,  # Period startdate untill enddate 
    ):
    '''Functions gets all days in period start yyyymmdd to end yyyymmdd''' 
    col = data.column('yyyymmdd')   # Get data column
    symd, eymd = period.split('-')  # Get start and end date
    np_lst_ymd = np_lst_days[:,col] # List with all the dates

    # Select correct keys for dates
    np_lst_sel_keys = np.where( (np_lst_ymd >= float(symd)) & (np_lst_ymd <= float(eymd)) )

    # Update array with selected keys
    np_lst_days = np_lst_days[np_lst_sel_keys]

    return np_lst_days

# OPTION: get a day in a year
# yyyymmdd
def yyyymmdd( np_lst, period ):
    '''Selct one day from a lst'''
    symd, eymd = period, period # Get start and end date (are the same)
    period = f'{symd}-{eymd}'   # Make period
    np_lst = yyyymmdd_yyyymmdd(np_lst, period) # Select only one day

    return np_lst

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
def yyyy_( 
        np_lst,
        period 
    ):
    '''
    OPTION: YYYY****-********
    * or x can be omitted
    Functions gets all days in period start yyyymmdd to end yyyymmdd
    ''' 
    symd = f'{period[:4]}0101' # Get start date
    eymd = ymd.yyyymmdd_now()  # Get possible end date
    period = f'{symd}-{eymd}'  # Make period
    np_lst = yyyymmdd_yyyymmdd(np_lst, period) # Select days from np_lst

    return np_lst

# OPTION: from a full year to a full year
# Wildcards x and * are variable and can be omitted
# YYYY****-YYYY****
# YYYY-YYYY
def yyyy_yyyy( 
        np_lst,
        period 
    ):
    '''
    OPTION: YYYY****-yyyy****
    * or x are variable and can be omitted
    '''
    sy, ey = period.split('-')  # Get dates from period 
    symd = f'{sy[:4]}0101'      # Make start date  
    eymd = f'{ey[:4]}1231'      # Make possible end date 
    period = f'{symd}-{eymd}'    # Make period
    np_lst = yyyymmdd_yyyymmdd(np_lst, period) # Select days from np_lst 

    return np_lst

# OPTION: from a full year to a full year plus month
# Wildcards x and * are variable and can be omitted
# YYYY****-YYYYMM**
# YYYY****-YYYYMM
# YYYY-YYYYMM
def yyyy_yyyymm( np_lst, period ):
    '''
    '''
    sy, eym = period.split('-') # Get dates from period 
    dd      = ymd.days_in_month(eym[4:6]) # Get end day num for month
    symd    = f'{sy[:4]}0101'   # Make start date
    eymd    = f'{eym[:6]}{dd}'  # Make end date 
    period  = f'{symd}-{eymd}'   # Make period
    np_lst  = yyyymmdd_yyyymmdd(np_lst, period) # Select days from np_lst 

    return np_lst   

# OPTION: from a full year to a full year plus month and day
# Wildcards x and * are variable and can be omitted
# YYYY-YYYYMMDD
def yyyy_yyyymmdd( np_lst, period ):
    sy, eymd = period.split('-') # Get dates from period 
    symd    = f'{sy[:4]}0101'   # Make start date
    period  = f'{symd}-{eymd}'   # Make period
    np_lst  = yyyymmdd_yyyymmdd(np_lst, period) # Select days from np_lst 

    return np_lst   

# OPTION: from a full start date to an end month
# Wildcards x and * are variable and can be omitted
# YYYYMMDD-YYYYMM**
# YYYYMMDD-YYYYMM
def yyyymmdd_yyyymm( 
        np_lst,
        period 
    ):
    '''OPTION: YYYYMMDD-YYYYMM**, YYYYMMDD-YYYYMM
       * or x can be omitted
    '''
    symd, eymx = period.split('-')    # Get dates from period
    dd = ymd.days_in_month(eymx[4:6]) # Make possible end date day
    eymd = f'{eymx[:6]}{dd}'          # Make End date
    period = f'{symd}-{eymd}'         # Make period
    np_lst = yyyymmdd_yyyymmdd(np_lst, period) # Select days from np_lst 

    return np_lst

# OPTION: select a period of days in month, underscore must be used
# ****_MMDD-****_MMDD 
# 1991_MMDD-2000_MMDD 
def yyyy_mmdd_yyyy_mmdd( np_lst, period ):
    '''
    OPTION: select a period of days, underscore must be used
    ****_MMDD-****_MMDD 
    YYYY_MMDD-YYYY_MMDD
    Examples: 
    1st decade july for all the years:  ****_0701-****_0710 
    2nd decade july for all the years:  ****_0711-****_0720 
    3trd decade july for all the years: ****_0721-****_0731 
    1st decade january from 1991-01 to 2001-01: 1991_0101-2001_0110 
    All winters all the years: ****_1201-****_0229
    All summers all the years: ****_0622-****_0921
    All winters from 1991 tot 2001: 1991_1201-2001_0229
    All summers from 2011 tot 2020: 2011_0622-2020_0922
    underscore _ must be used
    * or x can not be omitted (if used)
    '''
    np_res = np_days.new() # Make start np lst result
    col = data.column('yyyymmdd') # Get col num of date in data
    symd, eymd = period.split('-') # Get start and end period
    sy, smmdd = symd.split('_') # Split start date
    ey, emmdd = eymd.split('_') # Split end date 
    smm, emm =  smmdd[0:2], emmdd[0:2] # Get start / end month
    ism = int(smm[1:] if smm[0] == '0' else smm) # Start month (int) 
    iem = int(emm[1:] if emm[0] == '0' else emm) # End month (int)

    # Get first year (int)
    isy = int( str(int(np_lst[0:[col]]))[:4] 
               if chk.only_wildcards(sy) 
               else sy )
    
    # Get last year (int)
    iey = int( str(int(np_lst[-1:[col]]))[:4] 
               if chk.only_wildcards(ey) 
               else ey )
    
    # Check if dates cross over year -> end year plus 1
    ey_plus = True if ism > iem else False 

    while isy <= iey: # Select days from month in year
        iey     = iey + 1 if ey_plus else iey # End year plus 1 or not
        symd    = f'{isy}{smmdd}' # Get start date in year
        eymd    = f'{iey}{emmdd}' # Get end date in year
        period  = f'{symd}{eymd}' # Date
        np_yyyy = yyyymmxx( np_lst, period ) # Get days in current year
        np_res  = np.concatenate( (np_res, np_yyyy), axis=0) # Mergedays in np res
        isy    += 1  # Next year

    np_res = np_days.rm_row(np_res, 0) # Remove 1st row

# OPTION: All the data, one wildcard
# OPTION *
def x( np_lst ):
    '''All the data
       Option: * 
       * or x can not be omitted!
    ''' 
    return np_lst # Just return all the data

# OPTION: The current whole year
# ****
def xxxx( np_lst ):
    '''The current whole year
       ****
       * or x can not be omitted!
       '''
    syyyy  = ymd.yyyy() # Get the current year
    period = f'{syyyy}0101-{syyyy}1231' # Make period
    np_lst = yyyymmdd_yyyymmdd(np_lst, period) # Get data from current year

    return np_lst

# The current month
# ** 
def xx( np_lst, period ):
    '''The current whole current month
       **
       * or x can not be omitted!
       '''
    syyyy = ymd.yyyy() # Get the current year
    smm = ymd.mm() # Get the current month
    period = f'{syyyy}{smm}**' # Make period
    np_lst = yyyymmxx( np_lst, period ) # Get days from current month

    return np_lst 

# OPTION: The current day/date
# ***
def xxx( np_lst, period ):
    '''The current day/date
       **
       * or x can not be omitted!
       '''
    np_res = np_days.new() # Make start np lst result
    col = data.column('yyyymmdd') # Get col num of date in data
    isy = int(str(int(np_lst[ 0:[col]]))[:4]) # Get first year (int)
    iey = int(str(int(np_lst[-1:[col]]))[:4]) # Get last year (int)
    smmdd = f'{ymd.mm()}{ymd.dd()}' # Get current month / day 

    while isy <= iey: # Select days month and day in year
        period = f'{isy}{smmdd}' # Date
        np_ymd = yyyymmdd( np_lst, period ) # Get days in current year
        np_res = np.concatenate( (np_res, np_ymd), axis=0) # Merge days in np res
        isy   += 1  # Next year

    np_res = np_days.rm_row(np_res, 0) # Remove 1st row

    return np_res

# OPTION: The whole year
# YYYY****
# YYYY
def yyyyxxxx( np_lst, period ):
    '''OPTION: The whole year
       YYYY****
       YYYY
       * or x can be omitted!
    '''
    syyyy  = period[:4] # Get year
    period = f'{syyyy}0101-{syyyy}1231' # Make period
    np_lst = yyyymmdd_yyyymmdd(np_lst, period)

    return np_lst

# OPTION: get the day for every available year
# ****MMDD 
def xxxxmmdd( np_lst, period ): 
    '''OPTION: One day only 
       ****mmdd
       * or x can not be omitted!
    '''
    np_res = np_days.new() # Make start np lst result
    col = data.column('yyyymmdd') # Get col num of date in data
    isy = int(str(int(np_lst[ 0,col]))[:4]) # Get first year (int)
    iey = int(str(int(np_lst[-1,col]))[:4]) # Get last year (int)
    smm = period[4:6] # Get month string from period
    sdd = period[6:8] # Get day from period

    while isy <= iey: # Select days from month in year
        period  = f'{isy}{smm}{sdd}' # Date
        np_yyyy = yyyymmdd( np_lst, period ) # Get day in current year
        np_res  = np.concatenate( (np_res, np_yyyy), axis=0) # Mergedays in np res
        isy    += 1  # Next year

    np_res = np_days.rm_row(np_res, 0) # Remove 1st row

    return np_res

# OPTION: The whole month in a year
# YYYYMM**
# YYYYMM 
# * or x can be omitted!
def yyyymmxx( np_lst, period ):
    '''OPTION: the whole month in a year 
       yyyymm**
       yyyymm
       * or x can be omitted!
    ''' 
    syyyy, smm = period[:4], period[4:6] # Get year and month from period
    im = int(smm[1:] if smm[0] == '0' else smm)   # Get month in integer
    _, days = calendar.monthrange(int(syyyy), im) # Get days in month
    dd      = utils.add_l0(days)  # Add leading zero if needed
    symd    = f'{syyyy}{smm}01'   # Start date
    eymd    = f'{syyyy}{smm}{dd}' # End date
    period  = f'{symd}-{eymd}'     # Make period for current year
    np_lst  = yyyymmdd_yyyymmdd( np_lst, period ) # Get days in current year

    return np_lst

# OPTION: get selected month for every years
# ****MM**
# ****MM
# MM
def xxxxmmxx( np_lst, period ):
    '''OPTION: get selected month MM in all the available data
        ****MM**
        ****MM
        MM
    '''
    np_res = np_days.new() # Make start np lst result
    col = data.column('yyyymmdd') # Get col num of date in data
    isy = int(str(int(np_lst[ 0,col]))[:4]) # Get first year (int)
    iey = int(str(int(np_lst[-1,col]))[:4]) # Get last year (int)

    # Get month string from period
    smm = period[:2] if len(period) == 2 else period[4:6]

    while isy <= iey: # Select days from month in year
        period  = f'{isy}{smm}**' # Date
        np_yyyy = yyyymmxx( np_lst, period ) # Get the days in current year
        np_res  = np.concatenate( [np_res, np_yyyy], axis=0) # Merge days in np res
        isy    += 1  # Next year

    np_res = np_days.rm_row(np_res, 0) # Remove 1st row

    return np_res 

# Make a list with all the days for the calculation 
# of the specific climate value 
def clima_days(
        np_days_period, # Period to calculate climate values for
        clima_period='' # Climate period
    ):
    '''Function get climate days based on two periods
       1: Climate period
       2: Days for the calculation given by np_days_period
    '''
    # Climate period
    if clima_period == '': # If not given
        # Get climate years from config.py
        clima_period = f'{cfg.climate_start_year}0101-{cfg.climate_end_year}1231' 

    # Get station object
    station = np_days.get_station(np_days_period)

    # Read all data in the station
    ok, np_lst_days = dayval_read.weatherstation(station)

    # Get all the climate days
    np_clima_days = yyyymmdd_yyyymmdd(np_lst_days, clima_period)

    # Get clima and period days
    # Logical and: put the - mmdd - days from clima and period together
    # The result days, are the days for the calculation of the clima value 
    lst_np_clima_period = np_days.new()
    col_ymd = data.column('yyyymmdd') # Get column of date
    for np_clima_day in np_clima_days: 
        for np_period_day in np_days_period: 
            # Get the clima and period days
            clima_mmdd  = str(int(np_clima_day[col_ymd]))[4:] 
            period_mmdd = str(int(np_period_day[col_ymd]))[4:] 
            
            # Compare the mmdd of the dates clima and period 
            if clima_mmdd == period_mmdd: # If the same 
                np_lst_day = np.array([np_clima_day])
                # Add to np clima period
                lst_np_clima_period = np.vstack([lst_np_clima_period, np_lst_day])  

    # Remove 1st row
    np_res = np_days.rm_row(lst_np_clima_period, 0)       

    return np_res
