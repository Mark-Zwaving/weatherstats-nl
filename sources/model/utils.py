# -*- coding: utf-8 -*-
'''Library for supportive divers functions'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU Lesser General Public License (LGPL)'
__version__    =  '0.1.1'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import datetime, os, re, math
import numpy as np
from datetime import datetime
from dateutil import rrule
from pytz import timezone
import sources.model.daydata as daydata
import sources.view.text as text
import common.model.validate as validate
import common.model.ymd as ymd
import common.control.answer as answer
import common.control.fio as fio
import common.view.console as cnsl
import common.model.util as util
import sources.control.ask as ask

def again(t):
    return ask.again(t, default='', back=True, exit=True, spacer=True)

def open_with_default_app(path, options):
    if options['file-type'] != 'cmd':
        t = f'\nOpen the file <type={ options["file-type"] }> with your default application ?'
        fopen = ask.open_with_app(t, default='', back=True, exit=True, spacer=True)
        if answer.quit(fopen):
            return fopen
        elif fopen:
            fio.open_with_app(path)
    return True


def mk_path_with_dates(base_dir, fname):
    yyyy, mm, dd = ymd.yyyy_mm_dd_now()
    dir  = fio.mk_path( base_dir, f'{yyyy}/{mm}/{dd}' )
    name = fname.replace( '*', 'x' ).replace( ' ', '-' )
    path = fio.mk_path( dir, name )

    return path, dir, name

def query_ok(query):
    # Check the query
    ok, ttt, p = True, '', query.split(' ')
    max = len(p)

    if max < 3 or not (max-3) % 4 == 0:
        ttt = 'Query (possible) incomplete !'
        ok = False
    else:
        i = 0
        while i < max:
            ent, op, val = p[i], p[i+1].lower(), p[i+2]
            if not daydata.is_entity( ent ):            # Must be an entity
                ok, ttt = False, f'Error in "{ent}"! Must be an entity.'
            elif op.lower() not in text.lst_op_relat:   # Must be a relational operator
                ok = False
                ttt  = f'Error in "{op}"! Must be a relational operator!\n'
                ttt += f'Choose one of: {", ".join(text.lst_op_relat)}.'
            elif not validate.is_int(val) or \
                    not validate.is_float(val):       # Must be an number
                ok = False
                ttt  = f'Error in "{val}"! Value "{val}" must be a number.'
            if i+3 < max:
                and_or = p[i+3].lower()
                if and_or not in text.lst_op_logic: # Must be a logical operator
                    ok = False
                    ttt  = f'Error in "{and_or}"! Must be a logical operator!\n'
                    ttt += f'Choose one of: {", ".join(text.lst_op_logic)}.'

            i += 4 # Next set

    return ok, ttt

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

# Fisher Yates Algorithm
def shuffle_list(l, level=1):
    max = len(l) - 1
    if max > 0:
        while level > 0:
            i = 0
            while i <= max:
                rnd = util.rnd_digit(0, max)  # Get random key

                # Swap values elements
                mem    = l[i]
                l[i]   = l[rnd]
                l[rnd] = mem

                i += 1  # Next element

            level -= 1
    return l

def rnd_from_list( l ):
    l = shuffle_list(l)  # Shuffle list
    rnd = util.rnd_digit( 0, len(l)-1 ) # Get a random number from list
    return l[rnd]

def s_to_bytes( s, charset, errors ):
    try:
        b = s.encode(encoding=charset, errors=errors)
    except Exception as e:
        cnsl.log(f'Fail convert to bytes with charset {charset}\nError {e}', True)
    else:
        return b
    return s

def bytes_to_s( b, charset, errors ):
    try:
        s =  b.decode(encoding=charset, errors=errors)
    except Exception as e:
        cnsl.log(f'Fail convert to string with charset {charset}.\nError:{e}', True)
    else:
        return s
    return b

def b_ascii_to_s( b ):
    s = bytes_to_s(b, 'ascii', 'ignore')
    return s

def b_utf8_to_s( b ):
    s = bytes_to_s(b, 'utf-8', 'ignore')
    return s

def download_and_read_file(url, file):
    ok, t = False, ''
    if fio.has_internet():
        ok = fio.download( url, file )
        if ok:
            ok, t = fio.read(file)
    else:
        cnsl.log('No internet connection...', True)

    return ok, t

def loc_date_now():
    dt = datetime.now() # UTC ?
    dt_loc = dt.replace(tzinfo=timezone(cfg.timezone)) # Now local

    return dt_loc.now() # return local

def now_for_file():
    t =  loc_date_now().strftime('%Y%m%d%H%M%S')
    return t

def now_created_notification():
    ds = loc_date_now().strftime('%A, %d %B %Y %H:%M')
    return cfg.created_by_notification % ds

def ymd_to_txt( yyyymmdd ):
    yyyymmdd = yyyymmdd if type(yyyymmdd) is str else f_to_s(yyyymmdd)
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

# Check and sanitize input
def clear( s ):
    s = re.sub('\n|\r|\t', '', s)
    s = re.sub('\s+', ' ', s)
    s = s.strip()
    return s

def clean(s): return clear(s)

def make_query_txt_only(query):
    q = query.lower()
    q = q.replace('ge',  ' ge ')
    q = q.replace('le',  ' le ')
    q = q.replace('eq',  ' eq ')
    q = q.replace('ne',  ' ne ')
    q = q.replace('gt',  ' gt ')
    q = q.replace('lt',  ' lt ')
    q = q.replace('or',  ' or ')
    q = q.replace('and', ' and ')
    q = q.replace('>=',  ' ge ')
    q = q.replace('≥',   ' ge ')
    q = q.replace('<=',  ' le ')
    q = q.replace('≤',   ' le ')
    q = q.replace('==',  ' eq ')
    q = q.replace('!=',  ' ne ')
    q = q.replace('<>',  ' ne ')
    q = q.replace('!=',  ' ne ')
    q = q.replace('>',   ' gt ')
    q = q.replace('<',   ' lt ')
    q = q.replace('||',  ' or ')
    q = q.replace('&&',  ' and ')

    return clear(q)

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
