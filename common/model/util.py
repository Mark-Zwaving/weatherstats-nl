# -*- coding: utf-8 -*-
'''Library for supportive divers functions'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'MIT License'
__version__    =  '0.1.0'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import common.cmn_cfg as cfg
import common.view.console as cnsl
import common.control.fio as fio
import common.model.ymd as ymd
import os, random, math, time, shutil
from urllib.parse import urlparse


l0          = lambda s, n=1: f'{s:0>{n}}' # Add leading zeros
add_l0      = lambda s, n=1: l0(s,n)
var_dump    = lambda v: print( f'Dump {id(v)} {type(v)} {v}' )
url_name    = lambda url: urlparse(url).netloc.split('.')[-2].lower()
name_ext    = lambda path: os.path.splitext(os.path.basename(path))
lst_unique  = lambda lst: list(set(lst))
lst_shuffle = lambda lst, lev=3: lst_fisher_yates_shuffle(lst, lev)
lst_to_s    = lambda lst, sep=', ': sep.join(lst)
rnd_digit   = lambda min, max: random.randint(min, max)


def rm_l0(s):
    while s[0] == '0': 
        s = s[1:]
    return s


def key_from_lst(lst, val):
    for i, el in enumerate(lst):
        if val == el:
            return i 
    return -1


def s_in_lst(lst, s, case_insensitive=True):
    if case_insensitive: 
        s = str(s).lower()
        lst = [ str(el).lower() for el in lst ]

    for el in lst:
        if el == s:
            return True
    return False


# Function pauses programm untill a certain date and time is reached (to move on)
def pause(
        hh_mm_ss,  # Time with format <HH:MM:SS> to pause untill to.
        yyyymmdd = '',  # <optional> Date to start. Format <yyyymmdd> If omitted current date will be used.
        output = 'programm will continue at',  # <optional> Output text second substring
        verbose = cfg.verbose  # <optional> Overwrite default value verbose -> see config.py
    ):
    '''Functions pauses execution of programm untill a certain date and time is
       reached and then continues the executing of the programm.'''
    cnsl.log(f'Start pause programm at {ymd.now()}', verbose)
    # Check if there is a time anyway
    if not hh_mm_ss: return # We dont need to wait
    if not yyyymmdd: yyyymmdd = ymd.yyyymmdd_now()

    # Helper fn for nice output
    timers = lambda t: f'Datetime is {ymd.now()}, {t}'

    # Get start date
    yyyymmdd = yyyymmdd if yyyymmdd else ymd.yyyymmdd_now() # Fill in the missing part with the current date

    # Make a nice output
    y, m, d, hh, mm, ss = ymd.split_yyyymmdd_hh_mm_ss(yyyymmdd, hh_mm_ss) # Date
    t = f'{output} {y}-{m}-{d} {hh}:{mm}:{ss}'
    if not cfg.timer: cnsl.log(timers(t), verbose)

    # Wait till correct date and time to start the download
    time_end = ymd.dt_to_epoch(yyyymmdd, hh_mm_ss) # Time end in epoch seconds
    time_act = ymd.epoch_act()
    time_mem = time_act
    while time_end > time_act:
        if cfg.timer:
            mem, cfg.log = cfg.log, False # Do not log
            cnsl.log_r( timers(t), True) # Write clock if True
            cfg.log = mem

        time.sleep(1)
        time_act = ymd.epoch_act() # New time act
        # Check time shift during pause/sleep not tested
        if ymd.is_time_shift(time_act, time_mem): # Check on minutes difference
            # Spring or Autumn
            cnsl.log('Time shift happened !', True)
            if time_act > time_mem: # Spring
                continue
            else: # Fall.
                # Wait for old time te keep up and go on. Skip diff time
                while ymd.epoch_act() < time_mem:
                    if cfg.timer:
                        mem, cfg.log = cfg.log, False # Do not log
                        cnsl.log_r( timers('pause untill time shift is overcome'), True)
                        cfg.log = mem
                    time.sleep(1)
            time_act = ymd.epoch_act() # New time act
        time_mem = time_act

    if cfg.timer: cnsl.log_r( timers(t) + '\n', verbose)
    cnsl.log('End pause programm\n')


def process_time(t='', delta_sec = 0):
    '''Function gives a time string from nano seconds till days '''
    # Calculate from seconds
    rest, total_sec = math.modf( delta_sec )
    rest, milli_sec = math.modf( rest * 1000 )
    rest, micro_sec = math.modf( rest * 1000 )
    rest, nano_sec  = math.modf( rest * 1000 )
    mill, micr, nano = int(milli_sec), int(micro_sec), int(nano_sec)
    # Calculate from seconds
    d = int(total_sec // cfg.sec_day) # Calculate days
    r = total_sec % cfg.sec_day       # Leftover seconds
    h = int(r // cfg.sec_hour)        # Calculate hours
    r = r % cfg.sec_hour              # Leftover seconds
    m = int(r // cfg.sec_minute)      # Calculate minutes
    r = r % cfg.sec_minute            # Leftover seconds
    s = int(r)                        # Calculate seconds
    # Make a nice output. Give emthpy string if 0
    # Only print to screen when counted amount > 0
    if d > 0: t += f"{d} {'days'    if d > 1 else 'day'} "
    if h > 0: t += f"{h} {'hours'   if h > 1 else 'hour'} "
    if m > 0: t += f"{m} {'minutes' if m > 1 else 'minute'} "
    t += f'{s}.{str(mill):0>3} seconds' # 3 dec with leading zeros
    return t


def time_passed(
        start_time,
        t = 'Time passed',
        verbose = cfg.verbose
    ):
    ts = process_time(delta_sec=time.time()-start_time)
    cnsl.log(f'{t} {ts}', verbose)


def app_time( verbose = cfg.verbose ):
    '''Function shows total time app is active from the start'''
    time_passed( cfg.app_start_time, 'Total time app active is', verbose )


def lst_rnd_el(lst, start=0, end=-1):
    '''Function returns a random element from a list. Using both
       normal and fisher-yates shuffle'''
    end = len(lst) if end == -1 else end # Check ranges
    lst = lst[start:end] # Get part of list
    lst = lst_shuffle(lst,3) # Shuffle list
    rnd = random.randrange(start, end) # Get random int (from part)

    return lst[rnd] # Random element from list


def lst_fisher_yates_shuffle(lst, level=1):
    '''Function shuffles normal and with a Fisher Yates Algorithm'''
    lst, max = list(lst), len(lst)
    if max > 0:
        while level > 0: # Repeat level times
            random.shuffle(lst) # Normal shuffle
            for i in range(max): # Walkthrough all elements
                rnd = random.randrange(max) # Get a random key
                mem = lst[i]; lst[i] = lst[rnd]; lst[rnd] = mem # Swap values elements
            level -= 1

    return lst


# Function compresses a gif image
def compress_gif(
        path, # Name of image to compress
        verbose=cfg.verbose
    ):
    '''Function compressess a gif image.
       Python libraries used: pygifsicle, imageio
       Install command imageio: python3 -m pip install imageio
       Install command: python3 -m pip install pygifsicle
       Application gifsicle is needed for the compression of a gif-image
       Instal gifsicle on your OS too
       Example linux debian: install command: sudo apt-get install gifsicle
    '''
    ok = False
    cnsl.log(f'Start compress file {ymd.now()}', verbose)

    if os.path.isfile(path):
        cnsl.log(f'Filename is {path}')
        try: # Check for pygifsicle
            import pygifsicle
        except:
            cnsl.log('Python library pygifsicle is not installed', verbose)
            cnsl.log('Install library with command: python3 -m pip install pygifsicle', verbose)
            cnsl.log('Install on your os the following programm: gifsicle', verbose)
        else:
            fcopy = f'{path}.bck'
            shutil.copyfile(path, fcopy)
            try:
                pygifsicle.optimize(path)
            except Exception as e:
                cnsl.log(f'Error compressing \n{e}', cfg.error)
                shutil.copyfile(fcopy, path) # Put original file back
            else:
                ok = True
                cnsl.log('Compress successfull', verbose)
            fio.rm_file(fcopy, False) # Always remove the copy
    else:
        cnsl.log(f'Path - {path} - is not file', verbose)

    cnsl.log('End compress file', verbose)
    return ok
