# -*- coding: utf-8 -*-
'''Check periods for validity'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__version__    =  '0.0.9'
__license__    =  'GNU General Public License version 2 - GPLv2'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import sources.model.ymd as ymd 

# Possible minimum and maximum dates
i_min_ymd, i_max_ymd = 19010101, int(ymd.yyyymmdd_now()) 

def has_wildcards( period ):
    '''Check for the wildcard character in a period
       if a char is a wildcard it found one and will 
       return false'''
    for ch in period:
        if ch.lower() in ['x', '*']:
            return True

    return False

def rm_wildcards( period ):
    '''Remove wildcard type chars x and *
       and return whats left of it'''
    return period.replace('x', '').replace('*', '').strip()

def has_only_wildcards( period ):
    '''Check if a period has only wildcards'''
    return True if rm_wildcards(period) == '' else False

def has_underscore( period ):
    return '_' in period

def has_only_wildcards_or_is_empty( period ):
    ok = False
    if has_only_wildcards( period ) or period == '':
        ok = True

    return ok

# Not ok.
def possible(yyyymmdd):
    '''Check date on possibility within start and end date'''
    i_ymd = int(yyyymmdd)
    return False if i_ymd < i_min_ymd or i_ymd > i_max_ymd else True 

# OPTION: from date/day to date/day 
# YYYYMMDD-YYYYMMDD
def yyyymmdd_yyyymmdd(
        period
    ):
    '''Functions checks validity period yyyymmdd-yyyymmdd''' 
    ok = True
    if period.find('-') == -1: # No there must be a -
        ok = False
    elif has_only_wildcards(period): # No there must be digits
        ok = False
    else:
        # Split period
        s_symd, s_eymd = period.split('-')
        print(s_symd, s_eymd)

        # Check length of dates must be 8
        if len(s_symd) != 8 or len(s_eymd) != 8:
            print('length? ')
            ok = False 
        
        # Check if dates are digits
        elif not ( s_symd.isdigit() and s_eymd.isdigit() ):
            print('All Digits?')
            ok = False 
        
        # Check if dates ranges are valid 
        # elif not possible(s_symd) or not possible(s_eymd):
        #     ok = False 
        
        # Check dates for valid
        elif not ( ymd.valid_yyyymmdd(s_symd) and ymd.valid_yyyymmdd(s_eymd) ):
            print('Not valid??')
            ok = False

    return ok

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
def yyyy_( period ):
    '''
    OPTION: YYYY****-********
    * or x can be omitted
    '''
    ok = True
    if period.find('-') == -1:
        ok = False
    elif has_only_wildcards(period): # No there must be digits
        ok = False
    elif has_underscore(period): # No underscore allowed
        ok = False
    else:
        # Split period
        s_symd, s_eymd = period.split('-')
        s_symd, s_eymd = rm_wildcards(s_symd), rm_wildcards(s_eymd)

        # Check length (must be 4) of start year: yyyy
        if len(s_symd) != 4:
            ok = False
        
        # yyyy must be numbers
        elif not s_symd.isdigit():
            ok = False

        # yyyy must be numbers
        elif not s_symd.isdigit():
            ok = False

        # yyyy must be possible within range of available dates
        # elif not possible(s_symd):
        #     ok = False

        # Check end date: ********
        elif len(s_symd) > 0:
            ok = False 

    return ok

# OPTION: from a full year to a full year
# Wildcards x and * are variable and can be omitted
# YYYY****-YYYY****
# YYYY-YYYY
def yyyy_yyyy( period ):
    '''
    OPTION: YYYY****-yyyy****
    * or x are variable and can be omitted
    '''
    ok = True

    if period.find('-') == -1:
        ok = False
    elif has_only_wildcards(period): # No there must be digits
        ok = False
    elif has_underscore(period): # No underscore allowed
        ok = False
    else:
        # Split period
        s_symd, s_eymd = period.split('-')
        s_symd, s_eymd = rm_wildcards(s_symd), rm_wildcards(s_eymd)

        # Check length of start year and end year, must be 4
        if len(s_symd) != 4 or len(s_eymd) != 4:
            ok = False 

        # Years must be digits
        elif not s_symd.isdigit() or not s_eymd.isdigit():
            ok = False

         # Years must be possible (within range)
        # elif not possible(s_symd) or not possible(s_eymd):
        #     ok = False 
          
    return ok

# TODO
# OPTION: from a full year to a full year plus month
# Wildcards x and * are variable and can be omitted
# YYYY****-YYYYMM**
# YYYY****-YYYYMM
# YYYY-YYYYMM
def yyyy_yyyymm( period ):
    '''
    OPTION: YYYY-YYYYMM**
    * or x are variable and can be omitted
    '''
    ok = True
    if period.find('-') == -1:
        ok = False
    elif has_only_wildcards(period): # No there must be digits
        ok = False
    elif has_underscore(period): # No underscore allowed
        ok = False
    else:
        # Split period
        s_symd, s_eymd = period.split('-')
        s_symd, s_eymd = rm_wildcards(s_symd), rm_wildcards(s_eymd)

        # Check length of start year and end year, must be 4
        if len(s_symd) != 4 or len(s_eymd) != 4:
            ok = False 

        # Years must be digits
        elif not s_symd.isdigit() or not s_eymd.isdigit():
            ok = False

         # Years must be possible (within range)
        # elif not possible(s_symd) or not possible(s_eymd):
        #     ok = False 
          
    return ok

# TODO
# OPTION: from a full year to a full year plus month and day
# Wildcards x and * are variable and can be omitted
# YYYY****-YYYYMMDD
# YYYY-YYYYMMDD
def yyyy_yyyymmdd( period ):
    '''
    OPTION: YYYY****-yyyy****
    * or x are variable and can be omitted
    '''
    ok = True
    if period.find('-') == -1:
        ok = False
    elif has_only_wildcards(period): # No there must be digits
        ok = False
    elif has_underscore(period): # No underscore allowed
        ok = False
    else:
        # Split period
        s_symd, s_eymd = period.split('-')
        s_symd, s_eymd = rm_wildcards(s_symd), rm_wildcards(s_eymd)

        # Check length of start year and end year, must be 4
        if len(s_symd) != 4 or len(s_eymd) != 4:
            ok = False 

        # Years must be digits
        elif not s_symd.isdigit() or not s_eymd.isdigit():
            ok = False

        # Years must be possible (within range)
        # elif not possible(s_symd) or not possible(s_eymd):
        #     ok = False 
          
    return ok

# OPTION: from a full start date to an end month
# Wildcards x and * are variable and can be omitted
# YYYYMMDD-YYYYMM**
# YYYYMMDD-YYYYMM
def yyyymmdd_yyyymm( period ):
    '''OPTION: YYYYMMDD-YYYYMM**, YYYYMMDD-YYYYMM
       * or x can be omitted'''
    ok = True
    if period.find('-') == -1:
        ok = False
    elif has_only_wildcards(period): # No there must be digits
        ok = False
    elif has_underscore(period): # No underscore allowed
        ok = False
    else:
        # Split period
        s_symd, s_eymd = period.split('-')
        s_symd, s_eymd = rm_wildcards(s_symd), rm_wildcards(s_eymd)

        # Check length of start date and end date, must be 8 and 6
        if len(s_symd) != 8 or len(s_eymd) != 6:
            ok = False 

        # Dates must be all digits
        elif not s_symd.isdigit() or not s_eymd.isdigit():
            ok = False

        # Dates must be possible (within range)
        # elif not possible(s_symd) or not possible(s_eymd):
        #     ok = False 

    return ok

# OPTION: select a period of months and days, underscore must be used
# _MMDD-_MMDD 
# ****_MMDD-****_MMDD 
# YYYY_MMDD-YYYY_MMDD
# Examples: 
# winter: _1201-_0228
# summer: _0622-_0921
def yyyy_mmdd_yyyy_mmdd( period ):
    '''OPTION: select a period (mmdd to mmdd) from a start year to an end year
    YYYY_MMDD-YYYY_MMDD 
    ****_MMDD-****_MMDD 
    Examples:
    All winters: ****_1201-****_0229
    All summers: ****_0622-****_0921
    All winters from 1991 tot 2001: 1991_1201-2001_0229
    All summers from 2011 tot 2020: 2011_0622-2020_0922
    underscore _ must be used
    * or x can not be omitted!
    '''
    ok = True
    if period.find('-') == -1:
        ok = False
    elif has_only_wildcards(period): # No there must be digits
        ok = False
    else:
        s_symd, s_eymd = period.split('-') # Split period
        s_smmdd, s_emmdd = s_symd[5:], s_eymd[5:] # Month and day
        s_syyyy, s_eyyyy = s_symd[:4], s_eymd[:4] # Get years

        # Check for the obliged underscores _
        if not has_underscore(s_symd) or not has_underscore(s_eymd):
            ok = False

        # Check for the length, must be 9
        elif len(s_symd) != 9 or len(s_eymd) != 9:
            ok = False 

        # Underscore must be at pos index is 4
        elif s_symd[4] != '_' or s_eymd[4] != '_':
            ok = False

        # Check for digits only for the month and day
        elif not s_smmdd.isdigit() or not s_emmdd.isdigit():
            ok = False 
            
        # Check for valid mmdd: 0101 - 1231
        elif not ymd.valid_mmdd(s_smmdd) or not ymd.valid_mmdd(s_emmdd):
            ok = False

        # elif not possible(f'2020{s_smmdd}') or not possible(f'2020{s_emmdd}'):
        #     return False

        # Year can be 4 digits or 4 wildcard chars of: x, *
        # Must be all wildcards or if its not wildcards it must be all digits 
        if not has_only_wildcards(s_syyyy) and not s_syyyy.isdigit(): # Check s_syyyy
            return False
        elif not has_only_wildcards(s_eyyyy) and not s_eyyyy.isdigit(): # Check s_eyyyy
            return False                            

    return ok 

# OPTION: All the data, one wildcard
# OPTION *
def x( period ):
    '''All the data
       Option: * 
       * or x can not be omitted!
    '''
    ok = True
    if period.find('-') != -1: # No '-' in period
        ok = False
    elif len(period) != 1:
        ok = False
    elif not has_only_wildcards(period): # Must be wildcards
        ok = False
    elif has_underscore(period): # No underscore allowed
        ok = False

    return ok

# The current month
# **
def xx( period ):
    '''The current whole month
       **
       * or x can not be omitted!
       '''
    ok = True
    if period.find('-') != -1: # No '-' in period
        ok = False
    elif len(period) != 2: # Must be 2 wildcards
        ok = False
    elif not has_only_wildcards(period): # Must be wildcards only
        ok = False
    elif has_underscore(period): # No underscore allowed
        ok = False
    
    return ok

# OPTION: The current day/date in month
# ***
def xxx( period ):
    '''The current day/date in month
       ***
       * or x can not be omitted!
       '''
    ok = True
    if period.find('-') != -1: # No '-' in period
        ok = False
    elif len(period) != 3: # Must be 3 wildcards
        ok = False
    elif not has_only_wildcards(period): # Must be wildcards only
        ok = False
    elif has_underscore(period): # No underscore allowed
        ok = False
    
    return ok

# OPTION: The current whole year
# ****
def xxxx( period ):
    '''The current whole year
       ****
       * or x can not be omitted!
       '''
    ok = True
    if period.find('-') != -1: # No '-' in period
        ok = False
    elif len(period) != 4: # Must be 4 wildcards
        ok = False
    elif not has_only_wildcards(period): # Must be wildcards only
        ok = False
    elif has_underscore(period): # No underscore allowed
        ok = False
    
    return ok

# OPTION: The whole year
# YYYY****
# YYYY
def yyyyxxxx( period ):
    '''OPTION: The whole year
       YYYY****
       YYYY
       * or x can be omitted!
    '''
    ok = True
    if period.find('-') != -1: # No '-' in period
        ok = False
    elif has_only_wildcards(period): # No there must be digits
        ok = False
    elif len(period) == 4 and period.isdigit(): # four digits is always a year
        pass
    elif has_underscore(period): # No underscore allowed
        ok = False
    else:
        sy, smmdd = period[:4], period[4:]
        # sy must be a digit 
        if sy.isdigit(): 
            ok = False 
        # sx not only wildcards or not empthy
        elif not (has_only_wildcards(smmdd) or smmdd == ''):
            ok = False

    return ok

# OPTION: get the day for every available year
# ****MMDD 
def xxxxmmdd( period ): 
    '''OPTION: One day only 
       ****mmdd
       * or x can not be omitted!
    '''
    ok = True
    if period.find('-') != -1: # No '-' in period
        ok = False
    elif has_only_wildcards(period): # No there must be digits
        ok = False
    elif len(period) != 8: # Length must be 8
        ok = False 
    elif has_underscore(period): # No underscore allowed
        ok = False
    else: 
        s_yyyy, s_mmdd = period[:4], period[4:] 

        # Year and months can be 6 digits or 6 wildcard chars of: x, *
        # Must be all wildcards or if its not wildcards it must be all digits 
        if not has_only_wildcards(s_yyyy): # Check s_syyyy
            ok = False
        
        # Must month and day must be all digits
        elif not s_mmdd.isdigit(): 
            ok = False 

    return ok 

# OPTION: The whole month in a year
# YYYYMM**
# YYYYMM 
# * or x can be omitted!
def yyyymmxx( period ):
    '''OPTION: the whole month in a year 
       yyyymm**
       yyyymm
       * or x can be omitted!
    '''
    ok = True
    if period.find('-') != -1: # No '-' in period
        ok = False
    elif has_only_wildcards(period): # No there must be digits
        ok = False
    elif has_underscore(period): # No underscore allowed
        ok = False
    else:
        s_yyyymm, s_mm, s_dd = period[:6], period[4:6], period[6:8]
    
        if not s_yyyymm.isdigit(): # Check for digits
            ok = False 
        elif not ymd.valid_mm( s_mm ): # Correct month num
            ok = False
        
    return ok

# OPTION: get selected month for every years
# ****MM**
# ****MM
# MM
def xxxxmmxx( period ):
    '''OPTION: get selected month with a leading zero in all the years
        ****MM**
        ****MM
        MM
    '''
    ok = True
    if period.find('-') != -1: # No '-' in period
        ok = False 
    elif has_only_wildcards(period): # No there must be digits
        ok = False 
    elif has_underscore(period): # No underscore allowed
        ok = False 
    elif len(period) == 2 and period.isdigit(): # two digits is always a month
        pass 
    else:
        sy, smm, sdd = period[:4], period[4:6], period[6:8] 

        if not has_only_wildcards_or_is_empty(sy) or sy == '': 
            ok = False 

        elif not smm.isdigit(): 
            ok = False 

    return ok 

# OPTION: get a day in a year 
# yyyymmdd 
def yyyymmdd( period ):
    '''Select only one day'''
    ok = True
    if period.find('-') != -1: # No '-' in period
        ok = False
    elif has_wildcards(period): # No there must be only digits
        ok = False
    elif len(period) != 8: # Length must be 8
        ok = False
    elif has_underscore(period): # No underscore allowed
        ok = False
    elif not period.isdigit(): # Must be all digits
        ok = False
    elif not ymd.valid_yyyymmdd(period): # Must be a valid date
        ok = False 

    return ok

# Check all period options
def process ( period ):
    '''Checks all the periods for validity'''
    ok = False
    if   yyyymmdd(period): ok = True 
    elif yyyymmdd_yyyymmdd(period): ok = True 
    elif yyyy_(period): ok = True 
    elif yyyy_yyyy(period): ok = True 
    elif yyyy_yyyymm(period): ok = True 
    elif yyyy_yyyymmdd(period): ok = True 
    elif yyyymmdd_yyyymm(period): ok = True
    elif yyyy_mmdd_yyyy_mmdd(period): ok = True 
    elif x(period): ok = True 
    elif xx(period): ok = True 
    elif xxxx(period): ok = True 
    elif yyyyxxxx(period): ok = True 
    elif xxxxmmdd(period):ok = True 
    elif yyyymmxx(period): ok = True 
    elif xxxxmmxx(period): ok = True

    return ok
