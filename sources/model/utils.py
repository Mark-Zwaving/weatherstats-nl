# -*- coding: utf-8 -*-
'''Library for supportive divers functions'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.1.8'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import sources.control.fio as fio
import sources.model.ymd as ymd
import sources.model.validate as validate
import sources.view.console as cnsl
import datetime, math, time, os, sys, random, math, webbrowser, subprocess
from datetime import datetime, timedelta
from dateutil import rrule
from pytz import timezone
from urllib.parse import urlparse

l0          = lambda s, n=1: str(s).zfill(n) # Add leading zeros
add_l0      = lambda s, n=1: l0(s,n)
var_dump    = lambda v: print( f'Dump {id(v)} {type(v)} {v}' )
url_name    = lambda url: urlparse(url).netloc.split('.')[-2].lower()
name_ext    = lambda path: os.path.splitext(os.path.basename(path))
lst_unique  = lambda lst: list(set(lst))
lst_to_s    = lambda lst, sep=', ': sep.join(lst)
rnd_digit   = lambda min, max: random.randint(min, max)
abspath     = lambda path: os.path.abspath(path)
mk_path     = lambda dir, f: abspath(os.path.join(dir, f))

def add_lst(lst, el, key=0):
    '''Must return the list'''
    lst.insert(key, el)
    return lst

def datetime_plus_minutes_rounded( minute=15 ):
    '''Get a default datetime minutes af the current datetime'''
    dt_plus_MM = datetime.now() + timedelta(minutes=minute)
    yyyymmdd, hhmmss = dt_plus_MM.strftime('%Y%m%d-%H%M%S').split('-')
    yyyy, mm, dd, HH, MM, _ = ymd.split_yyyymmdd_hhmmss(yyyymmdd, hhmmss)
    SS = '00'

    # Return type MySQL string
    return f'{yyyy}-{mm}-{dd} {HH}:{MM}:{SS}' 

def replace_char(s, chars, char):
    '''Function replaces in a str all the chars in string with a given string '''
    for c in chars:
        s = s.replace(c, char)
    return s

def str_max(s, startlen=18, maxlen=78, brk='..'):
    '''Function chops of n characters in the middle to not exceed a given length'''
    if len(s) > maxlen:
        startlen -= len(brk)
        st = f'{s[0:startlen]}'
        while len(s) >= (maxlen - startlen + 1): 
            s = f'{s[1:]}'

        return f'{st}{brk}{s[startlen:maxlen]}'
    
    return s

def lst_to_col(lst, align='left', col=5, width=16, ln='\n'):
    # Overrule width if its too short
    for el in lst:
        if len(el) >= width:
            width = len(el) + 1 # Make width bigger, add one space 

    t = ''
    for ndx, el in enumerate(lst):
        # Long text Break off anyway
        el = el[:width]

        if   align ==   'left': 
            t += f'{el:{width}}'
        elif align ==  'right': 
            t += f'{el:>{width}}'
        elif align == 'center': 
            t += f'{el:^{width}}'

        ndx += 1
        if ndx % col == 0 and ndx != len(lst):
            t = t.strip() + ln

    return t

def max_chars_in_lst(lst):
    maxx = 0
    for el in lst:
        cnt = len(str(el))
        if cnt > maxx:
            maxx = cnt
    return maxx

def remove_chars(s, l):
    if type(l) != list:
        l = [l]
    for rm in l:
        s = s.replace(rm,cfg.e)
    return s

def l_years(ys, ye):
    return range( int(ys), int(ye) + 1 )

def to_int(s):
    s = s if type(s) == str else str(s)
    while s[0] == '0': s = s[1:] # Remove leading zero's
    s = int(s) # Make int
    return s

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
    t =  loc_date_now().strftime('%Y%m%d-%H%M%S')
    return t

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
        end_time  = cfg.e,  # Time with format <HH:MM:SS> or <HHMMSS> to pause untill to.
                            # Minutes and seconds can be omitted then 00 wiil be used
        end_date  = cfg.e,  # <optional> Date to start. Format <yyyymmdd> or <yyyy-mm-dd>
                            # If omitted current date will be used.
        output    = 'programm will continue at', # <optional> Output text second substring
        verbose   = cfg.verbose 
    ):
    '''Functions pauses untill a certain date and time is reached and then
       continues the executing of programm.'''
    
    # Check if there is a time anyway
    if end_time == cfg.e: return # We don't need to wait
    if end_date == cfg.e: end_date = ymd.yyyymmdd_now() # Get current date if not given 

    # Get start date time
    ok, hhmmss = validate.hhmmss(end_time) # Fill in the possible missing parts
    ok, yymmdd = validate.yyyymmdd(end_date) # Fill in the missing part with the current date

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

    cnsl.log_r(f'[{ymd.now()}] {t}\n\n', verbose)

def process_time_ext_ns(t=cfg.e, delta_ns = 0):
    '''Function gives a time string from nano seconds till days '''
    # Convert to seconds
    delta_ns = delta_ns / cfg.sec_nano 

    # Calculate from seconds
    rest, total_sec = math.modf( delta_ns )
    rest, milli_sec = math.modf( rest * 1000 )
    rest, micro_sec = math.modf( rest * 1000 )
    rest, nano_sec  = math.modf( rest * 1000 )
    mill, micr, nano = int(milli_sec), int(micro_sec), int(nano_sec)

    # Calculate from seconds
    d = int(total_sec // cfg.sec_day) # Calculate days
    r = total_sec % cfg.sec_day       # Leftover nano seconds
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

def process_time_ns(t=cfg.e, start_ns=0, ln=''):
    delta_ns = time.time_ns() - start_ns
    t = process_time_ext_ns(t, delta_ns)
    return t + ln

def process_time_delta_ns(t=cfg.e, delta_ns=0, ln=''):
    t = process_time_ext_ns(t, delta_ns)
    return t + ln

def process_time(t=cfg.e, start_sec=0, ln=''):
    delta_ns = start_sec * cfg.sec_nano
    t = process_time_ext_ns(t, delta_ns) # Update to nano seconds
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

lst_shuffle = lambda lst, lev=3: lst_fisher_yates_shuffle(lst, lev) # ERR, TODO

def exec_with_app(path, verbose=cfg.verbose):
    '''Function opens a file with an default application'''
    ok, err = False, cfg.e
    cnsl.log(f'Start open file with an app {ymd.now()}', verbose)

    if fio.check(path, verbose):
        cnsl.log(f'File {path}', verbose)

        # Linux
        if sys.platform.startswith('linux'):
            try:
                subprocess.call( ['xdg-open', path] )
            except Exception as e:
                err += f'Error in utils exec_with_app(). Linux, xdg-open {path}\n{e}\n'
                try:
                    os.system(f'start {path}')
                except Exception as e:
                    err += f'Error in utils exec_with_app(). Linux, start {path}\n{e}\n'
                    err += f'{e}\n'
                else:
                    ok = True
            else:
                ok = True

        # OS X
        elif sys.platform.startswith('darwin'): # ?
            try: 
                os.system( f'open "{path}"' )
            except Exception as e: 
                err += f'Error in utils exec_with_app(). OSX, darwin {path}\n{e}\n'
            else: 
                ok = True

        # Windows
        elif sys.platform in ['cygwin', 'win32']:
            try: # Should work on Windows
                os.startfile(path)
            except Exception as e:
                err += f'Error in utils exec_with_app(). Windows, os.startfile {path}\n{e}\n'
                try:
                    os.system( f'start "{path}"' )
                except Exception as e:
                    err += f'{e}\n'
                else:
                    ok = True
            else:
                ok = True

        # Possible fallback, use the webbrowser
        if not ok:
            try: webbrowser.open(path, new=2, autoraise=True)
            except Exception as e: 
                err += f'Error in utils exec_with_app(). Fallback, webbrowser.open {path}\n{e}\n'
            else: 
                ok = True

    else:
        cnsl.log(f'File not found', cfg.error)

    if ok: 
        cnsl.log('Open file with an app successfull', verbose)
    else: 
        cnsl.log(f'Error open file with an app\n{err}', cfg.error)

    return ok
