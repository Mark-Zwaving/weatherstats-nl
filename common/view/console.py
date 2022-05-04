# -*- coding: utf-8 -*-
'''Library contains a log function'''

__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU Lesser General Public License (LGPL)'
__version__    =  '0.0.7'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import os, threading
import common.cmn_cfg as cfg 
import common.control.fio as fio
import common.model.ymd as ymd

################################################################################
# Functions handling outputs to screen or log
def log(
        s, # String to print on the screen
        verbose=cfg.verbose,  # If set to True it always prints on a screen
        log=cfg.log,          # Overwrite default log
        debug=cfg.debug       # Overwrite default debug
    ):
    '''Function shows output string (s) on screen based on variable verbose and debug.
       Output always to screen, set variable always to True.
       If debug set to True it wait for keypress to move on.'''
    s = str(s)

    if debug: 
        input(s)
    elif verbose: 
        print(s)
   
    if log: # Write log if selected
        write_log(s)

def log_r(
        s, # String to print on the screen
        verbose=cfg.verbose,  # If set to True it always prints on a screen
        log=cfg.log,          # Overwrite default log
        debug=cfg.debug       # Overwrite default debug
    ):
    '''Function shows output string (s) --- on the same line --- based on the
       variable verbose. Output always to screen, set variable always to True.'''
    s = f'\r{s}'

    if debug: 
        input(s)
    elif verbose: 
        print(s, end='')
   
    if log: # Write log if selected
        write_log(s)

def write_log(s, verbose=False):
    '''Function writes a log from console output'''
    ok = False
    with threading.Lock():
        log_name = cfg.log_name if cfg.log_name else f'log_common_{ymd.yyyymmdd_now()}.log'
        path = os.path.join(cfg.dir_log, log_name)
        ok = fio.write(path, f'{s}\n', 'a', verbose=verbose)

    return ok

# Sometimes off or on TODO
def errors_on(): cfg.error = True 
def errors_off(): cfg.error = False 
def log_on(): cfg.log = True 
def log_off(): cfg.log = False 
def verbose_on(): cfg.verbose = True 
def verbose_off(): cfg.verbose = False 
