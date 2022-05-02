# -*- coding: utf-8 -*-
'''Library contains texts for output to screen or to a file'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'MIT License'
__version__    =  '0.1.4'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import re
import common.cmn_cfg as cfg
import common.model.util as util

line_hashtag = '#' * cfg.txt_line_width
line_hyphen  = '-' * cfg.txt_line_width

# Answers option lists
lst_quit = ['q','quit','stop','ho']
lst_yess = ['y','yes','yess','j','ja','ok','oke','oké','yee','jee', 'yep', 'yup', 'oui']
lst_no   = ['n','no','nope','not','nee','nada','nein','non','neet','njet','neen']
yes, no, quit = lst_yess[0], lst_no[0], lst_quit[0]
lst_prev = ['p', 'last', 'prev', 'previous']

# Quick txt date lists
lst_m    = ['1','2','3','4','5','6','7','8','9','10','11','12']
lst_mm   = ['01','02','03','04','05','06','07','08','09','10','11','12']
lst_mmm  = ['jan','feb','mar','apr','mai','jun','jul','aug','sep','okt','nov','dec']
lst_mmmm = ['january','februari','march','april','mai','june','july',
            'august','september','oktober','november','december']
lst_months_all = lst_m + lst_mm + lst_mmm + lst_mmmm

lst_dd   = [ '31', '29', '31', '30', '31', '30', '31', '31', '30', '31', '30', '31' ]

dd_01, dd_02, dd_03, dd_04, dd_05, dd_06 = 31, 29, 31, 30, 31, 30
dd_07, dd_08, dd_09, dd_10, dd_11, dd_12 = 31, 31, 30, 31, 30, 31

lst_dd_01 = [ f'01{util.l0(d,2)}' for d in range(1,dd_01+1) ]
lst_dd_02 = [ f'02{util.l0(d,2)}' for d in range(1,dd_02+1) ]
lst_dd_03 = [ f'03{util.l0(d,2)}' for d in range(1,dd_03+1) ]
lst_dd_04 = [ f'04{util.l0(d,2)}' for d in range(1,dd_04+1) ]
lst_dd_05 = [ f'05{util.l0(d,2)}' for d in range(1,dd_05+1) ]
lst_dd_06 = [ f'06{util.l0(d,2)}' for d in range(1,dd_06+1) ]
lst_dd_07 = [ f'07{util.l0(d,2)}' for d in range(1,dd_07+1) ]
lst_dd_08 = [ f'08{util.l0(d,2)}' for d in range(1,dd_08+1) ]
lst_dd_09 = [ f'09{util.l0(d,2)}' for d in range(1,dd_09+1) ]
lst_dd_10 = [ f'10{util.l0(d,2)}' for d in range(1,dd_10+1) ]
lst_dd_11 = [ f'11{util.l0(d,2)}' for d in range(1,dd_11+1) ]
lst_dd_12 = [ f'12{util.l0(d,2)}' for d in range(1,dd_12+1) ]

lst_mmdd  = lst_dd_01 + lst_dd_02 + lst_dd_03 + lst_dd_04 + lst_dd_05 + lst_dd_06
lst_mmdd += lst_dd_07 + lst_dd_08 + lst_dd_09 + lst_dd_10 + lst_dd_11 + lst_dd_12

def month_num_to_mmmm( n ):
    return lst_mmmm[int(n)-1]

def month_to_mm( mm ):
    m = mm.lower()
    if m in [  1,  '1', '01', 'january',  'jan']:  return '01'
    if m in [  2,  '2', '02', 'februari', 'feb']:  return '02'
    if m in [  3,  '3', '03', 'march',    'mar']:  return '03'
    if m in [  4,  '4', '04', 'april',    'apr']:  return '04'
    if m in [  5,  '5', '05', 'mai',      'may']:  return '05'
    if m in [  6,  '6', '06', 'june',     'jun']:  return '06'
    if m in [  7,  '7', '07', 'july',     'jul']:  return '07'
    if m in [  8,  '8', '08', 'august',   'aug']:  return '08'
    if m in [  9,  '9', '09', 'september','sep']:  return '09'
    if m in [ 10, '10',       'oktober',  'okt']:  return '10'
    if m in [ 11, '11',       'november', 'nov']:  return '11'
    if m in [ 12, '12',       'december', 'dec']:  return '12'
    return -1

def month_name_to_num ( name ):
    ndx = 0
    for mmm, mmmm in zip(lst_mmm, lst_mmmm):
        if name in [mmm,mmmm]:
            return ndx
        ndx += 1
    else:
        return -1 # Name not found

# Check and sanitize input
def sanitize( s ):
    s = re.sub( '\t+|\s+',' ', str(s) )
    s = re.sub( '\n|\r', '', s.strip() )
    return s

def remove_dumb_whitespace( t ):
    '''Function removes excessive whitespaces from a text string'''
    t = re.sub('\n|\r|\t', '', str(t))
    t = re.sub('\s+', ' ', t)
    return t.strip()

def strip_all_whitespace(t):
    '''Function removes all whitespace from a text string'''
    return re.sub( '\t|\r|\n| |\s', '', str(t) )

def cleanup_whitespaces( t ):
    '''Function civilizes long text output with too much enters e.g.'''
    t = re.sub(r'\n+', '\n\n', t)
    t = re.sub('\t+|\s+', ' ', t)
    return t.strip()

def padding(t, align='center', spaces=0):
    '''Function aligns text on the screen'''
    t = str(t)
    if   align == 'center': t = f'{t:^{spaces}}'
    elif align == 'left':   t = f'{t:<{spaces}}'
    elif align == 'right':  t = f'{t:>{spaces}}'
    return t

def line_spacer( cnt=1 ):
    '''Function print enters to the screen'''
    t = ''
    while cnt >= 0: t += '\n'; cnt -= 1
    return t

def style( t='', type='none'):
    t = t.strip().replace('  ', ' ')
    if   type in ['c','cap','capitalize']: t = t.capitalize()
    elif type in ['u','up','upper']: t = t.upper()
    elif type in ['l','low','lower']: t = t.lower()
    elif type in ['t','tit', 'title']: t = t.title()
    return t

def lst_el_maxwidth(l):
    max = 0
    for el in l:
        if len(el) > max:
            max = len(el)
    return max

def lst_to_col(lst, align='left', col=5, width=2, ln='\n'):
    # Overrule width if its too short
    for el in lst:
        if len(el) >= width:
            width = len(el) + 1 # Make width bigger, add one space 

    t, cnt = '', len(lst) 
    if cnt > 0:
        for ndx, el in enumerate(lst):
            if   align ==   'left': t += f'{el:{width}}'
            elif align ==  'right': t += f'{el:>{width}}'
            elif align == 'center': t += f'{el:^{width}}'

            ndx += 1
            if ndx % col == 0 and ndx != cnt:
                t += ln

    return t
