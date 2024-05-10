'''Library contains functions for validation'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.1.2'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import datetime
import sources.model.ymd as ymd
import sources.view.console as cnsl

# Function checks extensions
def extension(
        ext  # Extension of image to validate
    ):
    '''Function checks extensions for validity and adds a dot if needed'''
    if ext:
        if ext[0] != '.':
            ext = f'.{ext}'
    return ext

# Function validates time and fills in missing values with 00
def hhmmss(
        hh_mm_ss  # String format is <hh:mm:ss> or <hhmmss>. Allowed too is <hh>, <hh:mm>
    ):
    '''Function validates a time. 
       Allowed dtime formats are
       1. HHMMSS   | HHMM  | HH
       2. HH:MM:SS | HH:MM
       2. HH-MM-SS | HH-MM
       3. HH MM SS | HH MM 
    '''
     # Make string, remove whitespeace before and after
    hms = str(hh_mm_ss).strip()
    h_max, ms_max, hms_min = 23, 59, 0

    # Fill in default parts
    HH, MM, SS = hms, hms_min, hms_min 

    # Make a lst with the parts 
    lst = [HH, MM, SS] 

    # format HH:MM:SS
    if ':' in hms: 
        lst = hms.split(':') 
    # format HH-MM-SS
    elif '-' in hms: 
        lst = hms.split('-') 
    # format HH MM SS
    elif ' ' in hms: 
        lst = hms.split(' ') 
     # format HHMMSS
    else:
        # Get HH, MM en SS hh_mm_ss
         # format H | HH
        if len(hms) in [1, 2]:  
            lst[0] = hms[:2].zfill(2)
        # format HHM | HHMM
        elif len(hms) in [3, 4]:
            lst[0] = hms[0:2].zfill(2)
            lst[1] = hms[2:4].zfill(2)
        # format HHMMS | HHMMSS
        elif len(hms) in [5, 6]:
            lst[0] = hms[0:2].zfill(2)
            lst[1] = hms[2:4].zfill(2)
            lst[2] = hms[4:6].zfill(2)

    # Get size of list
    size = len(lst)

    # Update the parts which are given
    if size == 1: 
        HH = lst[0].zfill(2)
    elif size == 2:
        HH = lst[0].zfill(2)
        MM = lst[1].zfill(2)
    elif size >= 3:
        HH = lst[0].zfill(2)
        MM = lst[1].zfill(2)
        SS = lst[2].zfill(2)

    # Check false times and get them within range
    # HH - hours
    H = int(lst[0])
    if H < hms_min: 
        HH = str(hms_min).zfill(2)
    elif H > h_max: 
        HH = str(h_max)
    # MM - minutes
    M = int(lst[0])
    if M < hms_min: 
        MM = str(hms_min).zfill(2)
    elif M > ms_max: 
        MM = str(ms_max)
    # SS - seconds
    S = int(lst[1])
    if S < hms_min: 
        SS = str(hms_min).zfill(2)
    elif S > ms_max:  
        SS = str(ms_max)

    # Return string with (possible) missing values
    return True, f'{HH}{MM}{SS}'

def yyyymmdd(
        yyyymmdd = cfg.e,  # String date format is <yyyymmdd>
        verbose = cfg.verbose
    ):
    '''Function validates a date stamp'''
    ok = False
    y, m, d = '9999', '12', '31'
    yymmdd = str(yyyymmdd)

    if '-' in yymmdd:
        lst = yymmdd.split('-')
        size = len(lst)
        # Fill in the parts which are there
        if size >= 1: y = lst[0]
        if size >= 2: m = lst[1]
        if size >= 3: d = lst[2]
    else:
        size = len(yymmdd)
        if size >= 4: y = yymmdd[0:4]
        if size >= 6: m = yymmdd[4:6]
        if size >= 8: d = yymmdd[6:8]

    yymmdd = f'{y}{m}{d}'

    try:
        y, m, d = ymd.split_yyyymmdd(yymmdd)
        d = datetime.datetime(int(y), int(m), int(d))
    except Exception as e:
        cnsl.log(f'Error validate yyyymmdd_1(). Date {yymmdd}\n{e}', cfg.error)
    else:
        # cnsl.log(f'Validate date {yymmdd} success', verbose)
        ok = True

    return ok, yymmdd  # Make new possible updated date
