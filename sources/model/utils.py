# -*- coding: utf-8 -*-
'''Library for supportive divers functions'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 3 - GPLv3'
__version__    =  '0.1.1'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import sources.model.validate as validate
import sources.model.ymd as ymd
import sources.control.answer as answer
import sources.control.fio as fio
import sources.control.ask as ask
import sources.view.console as cnsl
import datetime, time, math, os, sys, random, math, shutil, webbrowser, subprocess
import numpy as np
from datetime import datetime
from dateutil import rrule
from pytz import timezone
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
abspath     = lambda path: os.path.abspath(path)
mk_path     = lambda dir, f: abspath(os.path.join(dir, f))

def name_with_act_date(base_name, ext='txt'):
    H, M, S = ymd.hh_mm_ss_now()
    return f'{base_name}-{H}-{M}-{S}.{ext}'

def dir_with_act_date(base_dir):
    y, m, d = ymd.yyyy_mm_dd_now()
    return mk_path(base_dir, f'{y}/{m}/{d}')

def path_with_act_date(base_dir, base_name):
    return mk_path(dir_with_act_date(base_dir), name_with_act_date(base_name))

def max_chars_in_lst(lst):
    maxx = 0
    for el in lst:
        cnt = len(str(el))
        if cnt > maxx:
            maxx = cnt
    return maxx

def mk_path_with_dates(base_dir, fname):
    yyyy, mm, dd = ymd.yyyy_mm_dd_now()
    dir  = fio.mk_path( base_dir, f'{yyyy}/{mm}/{dd}' )
    name = fname.replace( '*', 'x' ).replace( ' ', '-' )
    path = fio.mk_path( dir, name )

    return path, dir, name

def remove_chars(s, l):
    if type(l) != list:
        l = [l]
    for rm in l:
        s = s.replace(rm,'')
    return s

def l_years(ys, ye):
    return range( int(ys), int(ye) + 1 )

def to_int(s):
    s = s if type(s) == str else str(s)
    while s[0] == '0': s = s[1:] # Remove leading zero's
    s = int(s) # Make int
    return s

def make_dirs_app(verbose=False):
    l = [ cfg.dir_data, cfg.dir_winterstats, cfg.dir_summerstats, cfg.dir_dayvalues,
          cfg.dir_search4days, cfg.dir_allstats, cfg.dir_thirdparty , cfg.dir_img,
          cfg.dir_pdf, cfg.dir_txt, cfg.dir_forecasts, cfg.dir_templates, cfg.dir_period,
          cfg.dir_static, cfg.dir_dayextremes, cfg.dir_monthextremes, cfg.dir_yearextremes,
          cfg.dir_dayvalues_zip, cfg.dir_dayvalues_txt, cfg.dir_forecasts_txt,
          cfg.dir_period_img, cfg.dir_templates_html, cfg.dir_quick_calc,
          cfg.dir_quick_calc_txt ]
    for dir in l:
        if not os.path.exists(dir):
            fio.mk_dir(dir, verbose)

def is_nan( val ):
    ok = False
    try:
        if val != val:
            ok = True
        elif val == np.isnan:
            ok = True
        elif np.isnan(val):
            ok = True
        elif math.isnan(val):
            ok = True
    except Exception as e:
        pass

    return ok

def is_float( val ):
    ok = True
    try:
        if val is None:
            ok = False
        elif is_nan(val):
            ok = False
        else:
            f = float(val)
    except Exception as e:
        cnsl.log(f'Digit {val} is no float.')
        ok = False

    return ok

def is_date( dt ):
    try:
        datetime.strptime(dt, '%Y%m%d')
    except ValueError:
        return False
    else:
        return True

def unique_list(l):
    unique = list()
    for el in l:
        if el not in unique:
            unique.append(el)
    return unique

def shuffle_list(l, level=1):
    max = len(l) - 1
    if max > 0:
        while level > 0:
            i = 0
            while i <= max:
                rnd = rnd_digit(0, max)  # Get random key

                # Swap values elements
                mem    = l[i]
                l[i]   = l[rnd]
                l[rnd] = mem

                i += 1  # Next element

            level -= 1
    return l

def rnd_from_list( l ):
    l = shuffle_list(l)  # Shuffle list
    rnd = rnd_digit( 0, len(l)-1 ) # Get a random number from list
    return l[rnd]

def loc_date_now():
    dt = datetime.now() # UTC ?
    dt_loc = dt.replace(tzinfo=timezone(cfg.timezone)) # Now local

    return dt_loc.now() # return local

def now_for_file():
    t =  loc_date_now().strftime('%Y%m%d%H%M%S')
    return t

def ymd_to_txt( yyyymmdd ):
    yyyymmdd = yyyymmdd if type(yyyymmdd) is str else fl_to_s(yyyymmdd)
    return datetime.strptime(yyyymmdd, '%Y%m%d').strftime('%A, %d %B %Y')

def mk_name( base='x', period='x', places=[], entities=[] ):
    st = base + '-' + period.replace('*', 'x')
    for s in places:
        st += f'-{s.wmo}-'
    for e in entities:
        st += f'-{e}-'
    return st[:-1]

def mk_name_type( base='x', period='x', places=[], entities=[], type='txt' ):
    return mk_name( base, period, places, entities ) + f'.{type}'

# TODO testing
def add_zero_less_x(d, x):
    s = str(d)
    n = x - len(s)
    while n > 0:
        s = f'0{s}'
    return s

def add_zero_less_ten(d):
    if int(d) < 10:
        return f'0{d}'
    else:
        return f'{d}'

def add_zero_less_1000(d):
    s = str(d)
    n = len(s)
    if n == 1:
        return f'00{s}'
    elif n == 2:
        return f'0{s}'
    return s

def list_dates_range( sd, ed ):
    l = []
    sd = datetime.strptime(sd, '%Y%m%d')
    ed = datetime.strptime(ed, '%Y%m%d')
    for date in rrule.rrule( rrule.DAILY, dtstart=sd, until=ed ):
        l.append( date.strftime('%Y%m%d') )

    return l

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
            cnsl.log('Python library pygifsicle is not installed', cfg.error)
            cnsl.log('Install library with command: python3 -m pip install pygifsicle', cfg.error)
            cnsl.log('Install on your os the following programm: gifsicle', cfg.error)
            cnsl.log('Example install debian: sudo apt-get install gifsicle', cfg.error)
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
            fio.delete(fcopy, False) # Always remove the copy
    else:
        cnsl.log(f'Path - {path} - is not a file', verbose)

    cnsl.log('End compress file', verbose)
    return ok

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

def pause(
        end_time, # Time with format <HH:MM:SS> or <HHMMSS> to pause untill to.
                  # Minutes and seconds can be omitted then 00 wiil be used
        end_date, # <optional> Date to start. Format <yyyymmdd> or <yyyy-mm-dd>
                  # If omitted current date will be used.
        output = 'programm will continue at', # <optional> Output text second substring
        verbose = cfg.verbose 
    ):
    '''Functions pauses untill a certain date and time is reached and then
       continues the executing of programm.'''
    cnsl.log('Start pause programm', verbose)
    # Check if there is a time anyway
    if not end_time: 
        return # We dont need to wait

    # Get start date time
    ok, hhmmss = validate.hhmmss(end_time) # Fill in the possible missing parts
    ok, yymmdd = validate.yyyymmdd_1(end_date) # Fill in the missing part with the current date

    if not ok:
        return 
    
    end_ymdhms = int(f'{yymmdd}{hhmmss}')
    act_ymdhms = int(ymd.ymdhms_now())

    # Make a nice output
    y, m, d, H, M, S = ymd.split_yyyymmdd_hhmmss(yymmdd, hhmmss)
    t = f'{output} {y}-{m}-{d} {H}:{M}:{S}'
    cnsl.log_r(f'[{ymd.now()}] {t}', verbose)   

    while act_ymdhms < end_ymdhms:
        time.sleep(1) # Wait a second
        cnsl.log_r(f'[{ymd.now()}] {t}', verbose)       
        act_ymdhms = int(ymd.ymdhms_now()) # New time act

    cnsl.log_r(f'[{ymd.now()}] {t}\n', verbose)
    cnsl.log('End pause programm\n', verbose)

def process_time_ext(t='', delta_sec = 0):
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

def process_time(t='', st=time.time_ns(), ln='\n'):
    delta = time.time_ns() - st
    t = process_time_ext(t, delta)
    return t + ln

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

def exec_with_app(fname, verbose=cfg.verbose):
    '''Function opens a file with an default application'''
    ok, err = False, ''
    cnsl.log(f'Start open file with an app {ymd.now()}', verbose)

    if fio.check(fname, verbose):
        cnsl.log(f'File {fname}', verbose)

        # Linux
        if sys.platform.startswith('linux'):
            try:
                subprocess.call( ['xdg-open', fname] )
            except Exception as e:
                err += f'{e}\n'
                try:
                    os.system(f'start {fname}')
                except Exception as e:
                    err += f'{e}\n'
                else:
                    ok = True
            else:
                ok = True

        # OS X
        elif sys.platform.startswith('darwin'): # ?
            try: 
                os.system( f'open "{fname}"' )
            except Exception as e: 
                err += f'{e}\n'
            else: 
                ok = True

        # Windows
        elif sys.platform in ['cygwin', 'win32']:
            try: # Should work on Windows
                os.startfile(fname)
            except Exception as e:
                err += f'{e}\n'
                try:
                    os.system( f'start "{fname}"' )
                except Exception as e:
                    err += f'{e}\n'
                else:
                    ok = True
            else:
                ok = True

        # Possible fallback, use the webbrowser
        if not ok:
            try: webbrowser.open(fname, new=2, autoraise=True)
            except Exception as e: err += e
            else: 
                ok = True

    else:
        cnsl.log(f'File not found', cfg.error)

    if ok: 
        cnsl.log('Open file with an app successfull', verbose)
    else: 
        cnsl.log(f'Error open file with an app\n{err}', cfg.error)

    return ok

def open_with_default_app(path, options):
    t = f'\nOpen the file <type={ options["file-type"] }> with your default application ?'
    fopen = ask.open_with_app(t, default='', back=True, exit=True, spacer=True)
    if answer.is_quit(fopen):
        return fopen
    elif fopen:
        exec_with_app(path)
        
    return True
