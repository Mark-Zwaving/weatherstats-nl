'''Library has functions with checks is an object is true or false'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.0.4'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import sources.model.ymd as ymd
import sources.view.console as cnsl
import datetime, math, os, numpy as np
from PIL import Image

def is_nan( s ):
    ok = False
    try:
        if s != s:
            ok = True
        elif s == np.isnan:
            ok = True
        elif np.isnan(s):
            ok = True
        elif math.isnan(s):
            ok = True
    except Exception as e:
        cnsl.log(f'{s} not an NAN.\n{e}', cfg.error)

    return ok

def is_int(s, verbose=False):
    try: 
        i = int(s)
    except ValueError:
        cnsl.log(f'{s} not an integer.', cfg.error)
        return False  
    return True

def is_float(s):
    try: 
        fl = float(s)
    except ValueError:
        cnsl.log(f'{s} not an float.', cfg.error)
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

def is_date( yyyymmdd ):
    try: 
        d = datetime.datetime.strptime(yyyymmdd, '%Y%m%d')
    except Exception as e:
        cnsl.log(f'Date {yyyymmdd} incorrect\n{e}', cfg.error)
        return False
    return True

def is_image_corrupt(path, verbose=cfg.verbose):
    '''Function checks is a file is corrupt returns True if it is else False'''
    corrupt = False
    try: Image.open(path).verify() # Open and verify
    except Exception as e:
        cnsl.log(f'Error in validate image_corrupt(). Path {path}\{e}', cfg.error)
        corrupt = True
    return corrupt


def is_image(path, verbose=cfg.verbose):
    '''Function validates an image'''
    ok = False
    cnsl.log(f'[{ymd.now()}] validate image', verbose)
    cnsl.log(f'Image {path}', verbose)
    try:
        if os.path.exists(path):
            if os.path.isfile(path):
                if is_image_corrupt(path):
                    raise Exception(f'Image is corrupt')
            else:
                raise Exception(f'Image is not a file')
        else:
            raise Exception(f'Image does not exist')
    except Exception as e:
        cnsl.log(f'Error in validate image()\n{e}', verbose)
    else:
        cnsl.log('Image seems to be ok', verbose)
        ok = True
    cnsl.log(f'End validate image', verbose)
    return ok
