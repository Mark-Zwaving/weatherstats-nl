'''Library contains functions for validation'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 3 - GPLv3'
__version__    =  '0.0.9'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import datetime, os, math, numpy as np
import config as cfg
import sources.model.ymd as ymd
import sources.view.console as cnsl
from PIL import Image

def is_int(s, verbose=False):
    try: i = int(s)
    except ValueError:
        cnsl.log(f'Var {s} cannot be an integer', verbose)
        return False  
    return True

def is_float(s, verbose=False):
    try: f = float(s)
    except ValueError:
        cnsl.log(f'Var {s} cannot be a float', verbose)
        return False
    return True

def is_lst(lst):
    if isinstance(lst, list):
        return True 
    return False

def is_dict(dct):
    if isinstance(dct, dict):
        return True 
    return False

def is_date( dt ):
    try: datetime.datetime.strptime(dt, '%Y%m%d')
    except ValueError:
        return False
    return True

def is_leap(yyyy):
    y = int(yyyy)
    if y % 4 == 0:
        if y % 100 == 0:
            if y % 400 == 0:
                return True
        else:
            return True
    
    return False

def is_nan( val ):
    if val == np.isnan: 
        return True
    elif np.isnan(val): 
        return True
    elif math.isnan(val): 
        return True
    
    return False

def image(path, verbose=cfg.verbose):
    '''Function validates an image'''
    ok = False
    cnsl.log(f'[{ymd.now()}] validate image', verbose)
    cnsl.log(f'Image {path}', verbose)
    try:
        if os.path.exists(path):
            if os.path.isfile(path):
                if image_corrupt(path):
                    raise Exception(f'Image is corrupt')
            else:
                raise Exception(f'Image is not a file')
        else:
            raise Exception(f'Image does not exist')
    except Exception as e:
        cnsl.log(f'Validation error: {e}', verbose)
    else:
        cnsl.log('Image seems to be ok', verbose)
        ok = True
    cnsl.log(f'End validate image', verbose)
    return ok

def image_corrupt(path, verbose=cfg.verbose):
    '''Function checks is a file is corrupt returns True if it is else False'''
    corrupt = False
    try: Image.open(path).verify() # Open and verify
    except Exception as e:
        cnsl.log(f'Error file {path} is corrupt', verbose)
        corrupt = True
    return corrupt

# Function checks extensions
def extension(
        ext  # Extension of image to validate
    ):
    '''Function checks extensions for validity and adds a dot if needed'''
    if ext:
        if ext[0] != '.':
            ext = f'.{ext}'
    return ext

def yyyymmdd(
        yyyymmdd, # Date
        verbose = cfg.verbose
    ):
    '''Function validates a date with format yyyymmdd for existence'''
    ok, symd = False, str(yyyymmdd)
    cnsl.log(f'[{ymd.now()}] validate date', verbose)
    cnsl.log(f'Date - {symd} - format <yyyymmdd>', verbose)
    if len(symd) != 8:
        cnsl.log('Date has wrong length. Correct length must be 8', verbose)
    elif not symd.isdigit():
        cnsl.log('Date must only contain digits', verbose)
    elif int(symd) > int(ymd.yyyymmdd_now()):
        cnsl.log('Date is in the future. Try again later... ;-)', verbose)
    else:
        try:
            y, m, d = ymd.split_yyyymmdd(symd)
            d = datetime.datetime( int(y), int(m), int(d) )
        except Exception as e:
            cnsl.log(f'Error in date\n{e}', verbose)
        else:
            cnsl.log('Validate date success', verbose)
            ok = True
    cnsl.log('End validate date', verbose)
    return ok

# Function validates time and fills in missing values with 00
def hhmmss(
        hh_mm_ss  # String format is <hh:mm:ss> or <hhmmss>. Allowed too is <hh>, <hh:mm>
    ):
    '''Function validates time format and return the time in the format hh:mm:ss'''
    # Init default time values
    hhmmss = str(hh_mm_ss)
    h, m, s = hhmmss, '00', '00'
    h_max, m_max, s_max, t_min = '23', '59', '59', '00'

    if ':' in hhmmss:
        lst = hhmmss.split(':')
        size = len(lst)
        # Fill in the parts which are there
        if size >= 1: h = lst[0]
        if size >= 2: m = lst[1]
        if size >= 3: s = lst[2]
    elif '-' in hhmmss:
        lst = hhmmss.split('-')
        size = len(lst)
        # Fill in the parts which are there
        if size >= 1: h = lst[0]
        if size >= 2: m = lst[1]
        if size >= 3: s = lst[2]
    else:
        # Fill in the parts which are there
        size = len(hhmmss)
        if size >= 2: h = hhmmss[0:2]
        if size >= 4: m = hhmmss[2:4]
        if size >= 6: s = hhmmss[4:6]

    # Check false times
    if int(h) < int(t_min): h = t_min
    if int(m) < int(t_min): m = t_min
    if int(s) < int(t_min): s = t_min
    if int(h) > int(h_max): h = h_max
    if int(m) > int(m_max): m = m_max
    if int(s) > int(s_max): s = s_max
 
    # Make new time string with (possible) missing values
    return True, f'{h}{m}{s}'

def yyyymmdd_1(
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
        cnsl.log(f'Error in date {yymmdd}\n{e}', verbose)
    else:
        cnsl.log(f'Validate date {yymmdd} success', verbose)
        ok = True

    return ok, yymmdd  # Make new possible updated date
