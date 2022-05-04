'''Library contains functions for validation'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'MIT License'
__version__    =  '0.0.8'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import datetime, os, math, numpy as np
import common.cmn_cfg as cfg
import common.model.ymd as ymd
import common.view.console as cnsl
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

