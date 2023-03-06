# -*- coding: utf-8 -*-
'''Library contains functions for writing output to screen or to a file'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU Lesser General Public License (LGPL)'
__version__    =  '0.1.3'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import math, time, re
import numpy as np
import stations
import sources.model.daydata as daydata
import sources.model.utils as utils
import sources.view.translate as tr
import sources.control.menu as ctrl_menu

# Menu

# Quick txt lists
lst_wmo = lambda: [el.wmo for el in stations.lst]
lst_name = lambda: [el.place for el in stations.lst]
lst_wmo_name = lambda: [ f'{el[0]} {el[1]}' for el in zip( lst_wmo(), lst_name() ) ]
lst_m = ['1','2','3','4','5','6','7','8','9','10','11','12']
lst_mm = ['01','02','03','04','05','06','07','08','09','10','11','12']
lst_mmm = ['jan','feb','mar','apr','mai','jun','jul','aug','sep','okt','nov','dec']
lst_mmmm = ['january','februari','march','april','mai','june','july',
            'august','september','oktober','november','december']
lst_months_all = lst_m + lst_mm + lst_mmm + lst_mmmm

# TXT strings
enter_default = lambda default: f'Press <enter> for default (={default})...'
enter_back_to = lambda t: f"Press 'q' to go back to the {t} menu... "
type_more_info = lambda i: f"Type '{i}' for more info..."

# Answers option lists
answer_quit = ['q','quit','stop']
answer_yes  = ['y','yes','yess','j','ja','ok','oke','oké','yee','jee']
answer_no   = ['n','no','nope','nee','nada','nein','non','neet']

# Check answ short fn
is_empty = lambda answ: is_answ_empty(answ)
is_no    = lambda answ: is_answ_no(answ)
is_yes   = lambda answ: is_answ_yes(answ)
is_quit  = lambda answ: is_answ_quit(answ)

# Makes versatile answers possible (list or string)
def answer_lst_to_str(answ):
    if type(answ) == list:
        answ = str(answ[0]) if len(answ) > 0 else ''

    return answ

# Check answer functions. Answ can be list or str
def is_answ_quit(answ):
    if type(answ) == list:
        if answ == answer_quit:
            return True
        else:
            answ = answer_lst_to_str(answ)
    else:
        answ = str(answ).lower()

    return answer_lst_to_str(answ) in answer_quit

def is_answ_yes(answ):
    if type(answ) == list:
        if answ == answer_yes:
            return True
        else:
            answ = answer_lst_to_str(answ)
    else:
        answ = str(answ).lower()

    return answer_lst_to_str(answ) in answer_yes

def is_answ_no(answ):
    if type(answ) == list:
        if answ == answer_no:
            return True
        else:
            answ = answer_lst_to_str(answ)
    else:
        answ = str(answ).lower()

    return answer_lst_to_str(answ) in answer_no

def is_answ_empty(answ):
    if type(answ) == list:
        if answ == []:
            return True
        else:
             answ = answer_lst_to_str(answ)
    else:
        answ = answ.strip()

    return False if answ else True

def separator( cnt=0 ):
    t = ' '
    while cnt > 0:
        t += '\n'
        cnt -= 1

    return t

def error(t, err):
    t = f'{t} failed.\nError {err}'
    return t

def succes(t):
    t = f'{t} success.'
    return t

def strip_all(s):
    t = re.sub('\t|\r|\n| |\s', '', t)
    return t

def clean_up( t ):
    t = t.strip()
    t = re.sub(r'(\n\n)\n+', '\n\n', t)
    t = re.sub('\t|  ', ' ', t)
    return t

def padding(t, align='center', spaces=35):
    spaces -= len(str(t))
    spaces = 2 if spaces < 0 else spaces
    if   align == 'center': t = f'{t:^{spaces}}'
    elif align == 'left':   t = f'{t:<{spaces}}'
    elif align == 'right':  t = f'{t:>{spaces}}'

    return t

def lst_el_maxwidth(l):
    max = 0
    for el in l:
        if len(el) > max:
            max = len(el)
    return max

def lst_to_col(l, align='left', sep=' ', col=10, width=10):
    t, lst = '', list(l)
    cnt = len(lst)
    if cnt > 0:
        for ndx, el in enumerate(lst):
            if   align ==   'left': t += f'{el:{width}}'
            elif align ==  'right': t += f'{el:>{width}}'
            elif align == 'center': t += f'{el:^{width}}'

            ndx += 1
            if ndx % col == 0 and ndx != cnt:
                t += '\n'

    return t

def style(t='', style='none'):
    t = tr.t( t.strip().replace('  ', ' '))
    if   style in ['cap','capitalize']: t = t.capitalize()
    elif style in ['up','upper']: t = t.upper()
    elif style in ['low','lower']: t = t.lower()
    elif style in ['tit', 'title']: t = t.title()

    return t

ave_tg    = lambda s='cap': style('average temperature', s)
ave_tx    = lambda s='cap': style('average maximum temperature', s)
ave_tn    = lambda s='cap': style('average minumum temperature', s)
ave_sq    = lambda s='cap': style('average sunshine duration', s)
ave_rh    = lambda s='cap': style('average rain precipiation', s)
max_tx    = lambda s='cap': style('highest maximum temperatur, warmest day', s)
max_tg    = lambda s='cap': style('highest mean temperature', s)
max_tn    = lambda s='cap': style('highest minimum temperature. warmest night', s)
min_tx    = lambda s='cap': style('lowest maximum temperature, coldest day', s)
min_tg    = lambda s='cap': style('lowest mean temperature', s)
min_tn    = lambda s='cap': style('lowest minumum temperature, coldest night', s)
max_t10n  = lambda s='cap': style('highest ground minimum temperature', s)
min_t10n  = lambda s='cap': style('lowest ground minimum temperature', s)
max_sq    = lambda s='cap': style('highest sunshine duration, most sunny day', s)
max_rh    = lambda s='cap': style('highest rain, most wet day', s)

tot_hour_sun    = lambda s='cap': style('total hours of sunshine', s)
tot_rain_sum    = lambda s='cap': style('total rain sum in mm', s)
sum_rh          = lambda s='cap': tot_rain_sum()
sum_sq          = lambda s='cap': tot_hour_sun()

days_tg_gt_18   = lambda s='cap': style('days mean temperature higher than 18 degrees celsius (heat index)' , s)
days_tg_gte_18  = lambda s='cap': style('days mean temperature higher and equal to 18 degrees celsius (heat index)' , s)
days_tg_gte_20  = lambda s='cap': style('days mean temperature higher and equal to 20 degrees celsius (heat index)' , s)
days_tn_gte_20  = lambda s='cap': style('tropical nights minium temperature higher and equal to 20 degrees celsius' , s)
days_tx_gte_20  = lambda s='cap': style('warm days maximum temperature higher and equal to 20 degrees celsius' , s)
days_tx_gte_25  = lambda s='cap': style('summer days maximum temperature higher and equal to 25 degrees celsius' , s)
days_tx_gte_30  = lambda s='cap': style('tropical days maximum temperature higher and equal to 30 degrees celsius' , s)
days_tx_gte_35  = lambda s='cap': style('tropical days maximum temperature higher and equal to 35 degrees celsius' , s)
days_tx_gte_40  = lambda s='cap': style('tropical days maximum temperature higher and equal to 40 degrees celsius' , s)
days_sq_gte_10  = lambda s='cap': style('sunny days with more than 10 hours of sunshine', s)
days_rh_gte_10  = lambda s='cap': style('days with more than 10 mm of rain' , s)
days_hellman    = lambda s='cap': style('hellmann days mean temperature less than 0 degress celsius', s)

hellmann        = lambda s='cap': style('hellmann cold number', s)
ijnsen          = lambda s='cap': style('ijnsen cold number', s)
frostsum        = lambda s='cap': style('frostsum cold number', s)
heat_ndx        = lambda s='cap': style('heat number', s)

days_tx_lt_0    = lambda s='cap': style('days with a maximum temperature below 0 degrees celsius' , s)
days_tg_lt_0    = lambda s='cap': style('days with an mean temperature below 0 degrees celsius', s)
days_tn_lt_0    = lambda s='cap': style('days with a minimum temperature below 0 degrees celsius' , s)
days_tn_lt__5   = lambda s='cap': style('days with a minimum temperature below -5 degrees celsius', s)
days_tn_lt__10  = lambda s='cap': style('days with a minimum temperature below -10 degrees celsius', s)
days_tn_lt__15  = lambda s='cap': style('days with a minimum temperature below -15 degrees celsius', s)
days_tn_lt__20  = lambda s='cap': style('days with a minimum temperature below -20 degrees celsius', s)
days_tn_lt__25  = lambda s='cap': style('days with a minimum temperature below -25 degrees celsius', s)
days_tn_lt__30  = lambda s='cap': style('days with a minimum temperature below -30 degrees celsius', s)

days_t10n_lt_0    = lambda s='cap': style('days with a ground minimum temperature below 0 degrees celsius' , s)
days_t10n_lt__5   = lambda s='cap': style('days with a ground minimum temperature below -5 degrees celsius', s)
days_t10n_lt__10  = lambda s='cap': style('days with a ground minimum temperature below -10 degrees celsius', s)
days_t10n_lt__15  = lambda s='cap': style('days with a ground minimum temperature below -15 degrees celsius', s)
days_t10n_lt__20  = lambda s='cap': style('days with a ground minimum temperature below -20 degrees celsius', s)
days_t10n_lt__25  = lambda s='cap': style('days with a ground minimum temperature below -25 degrees celsius', s)
days_t10n_lt__30  = lambda s='cap': style('days with a ground minimum temperature below -30 degrees celsius', s)

def stations_inf():
    l  = [f'{s.wmo} {s.place}' for s in stations.lst_stations_in_map()]
    w  = lst_el_maxwidth(l) # Max column width
    t  = 'STATIONS INFO \n'
    t += lst_to_col(l, 'left', ' ', 5, w)
    return t

def quick_calc_inf():
    t  = 'CALCULATION INFO\n'
    t += 'Default format: ENT(STATISTIC) \n'
    t += 'Options ENT: TX, RH, SQ, TN et cetera \n'
    t += 'Options STATISTIC: MIN -, MAX +, mean ~, SUM Σ, hellmann hmann, frostsum fsum, ijnsen, heatndx hndx\n'
    t += 'EXAMPLES: \n'
    t += 'TX+ (=maximum temperature TX)  TG~ (=average temperature TG)  TN- (=minimum temperature TN)\n'
    t += 'RHΣ (=total rain sum)          RH+ (=maximum rain in a day)   HELLMANN (=hellmann winter score) \n'
    t += 'FSUM (=frostsum winter score)  IJNSEN (=ijnsen winter score)  HNDX (=sum heat index score) \n'

    return t

def period_inf():
    t  = 'PERIOD INFO\n'
    t += 'Format yyyymmdd-yyyymmdd     ie. 20200510-20200520 \n'
    t += 'Examples with a wild card * (--- in development ---) \n'
    t += '  ********            selects all the available data (=8x*)\n'
    t += '  ****                selects (current) year (=4x*)\n'
    t += '  **                  selects (current) month (=2x*)\n'
    t += '  yyyy****            selects the whole year yyyy\n'
    t += '  yyyymm**            selects the month mm in the year yyyy\n'
    t += '  ****mm**            selects a month mm for every year \n'
    t += '  ****mmdd            selects a monthday mmdd for every year \n'
    t += '  yyyy****-yyyy****   selects a full year from yyyy untill yyyy \n'
    t += '  yyyymmdd-yyyymmdd*  selects a day mmdd in a year from start day to endyear\n'
    t += '  yyyymmdd-yyyy*mmdd* selects a certain period from mmdd=mmdd* in a year from yyyy to yyyy\n'
    t += '  2015**** or 2015    selects the year 2015 \n'
    t += '  201101**-202001**   selects all januarys from 2011 unto 2020 \n'
    t += '  ****07**            selects all julys from avalaible data \n'
    t += '  ****1225            selects all 25 decembers from avalaible data'
    return t

def ent_inf():
    t  = 'ENTITIES INFO\n'
    t += 'DDVEC = Vector mean wind direction (degrees)      FHVEC = Vector mean windspeed (m/s)\n'
    t += 'FG    = Daily mean windspeed (in 0.1 m/s)         FHX   = Maximum hourly mean windspeed (m/s)\n'
    t += 'FHN   = Minimum hourly mean windspeed (m/s)       FXX   = Maximum wind gust (m/s)\n'
    t += 'TG    = Daily mean temperature in (°C)            TN    = Minimum temperature (°C)\n'
    t += 'TX    = Maximum temperature (°C)                  T10N  = Minimum temperature at 10 cm (°C)\n'
    t += 'SQ    = Sunshine duration (hour)                  SP    = % of maximum sunshine duration\n'
    t += 'Q     = Global radiation (J/cm2)                  DR    = Precipitation duration (hour)\n'
    t += 'RH    = Daily precipitation amount (mm)           RHX   = Maximum hourly precipitation (mm)\n'
    t += 'PG    = Daily mean sea level pressure (hPa)       PX    = Maximum hourly sea level pressure (hPa)\n'
    t += 'PN    = Minimum hourly sea level pressure (hPa)   EV24  = Potential evapotranspiration (mm)\n'
    t += 'NG    = Mean daily cloud cover (octants)          UG    = Daily mean relative atmospheric humidity (%)\n'
    t += 'UX    = Maximum atmospheric humidity (%)          UN    = Minimum relative atmospheric humidity (%)\n'
    t += 'VVN   = Minimum visibility 0: <100m, 1:100-200m, 2:200-300m,..., 49:4900-5000m, 50:5-6 km, \n'
    t += '        56:6-7km, 57:7-8km,..., 79:29-30km, 80:30-35km, 81:35-40km,..., 89: >70km)\n'
    t += 'VVX   = Maximum visibility 0: <100 m, 1:100-200 m, 2:200-300 m,..., 49:4900-5000 m, 50:5-6 km, \n'
    t += '        56:6-7km, 57:7-8km,..., 79:29-30km, 80:30-35km, 81:35-40km,..., 89: >70km)'
    return t

def query_inf():
    t  = 'QUERY INFO\n'
    t += "' gt', '> '         = greater than             ie. TG >  20  Warm nights\n"
    t += "' ge', '>=', ' ≥'   = greater than and equal   ie. TX >= 30  Tropical days\n"
    t += "' lt', '< '         = less than                ie. TN <   0  Frosty days\n"
    t += "' le', '<=', ' ≤'   = less than equal          ie. TX <=  0  Icy days\n"
    t += "' eq', '=='         = equal                    ie. DDVEC == 90  A day with a wind from the east\n"
    t += "' ne', '!=', '<>'   = not equal                ie. RH !=  0  A day with rain\n"
    t += "' or', '||'  'or '  ie SQ > 10  or TX >= 25    Sunny and warm days\n"
    t += "'and', '&&'  'and'  ie RH > 10 and TX <  0     Most propably a day with snow"
    return t

def quick_stats_all_inf():
    t  = period_inf() + '\n\n'
    t += stations_inf() + '\n\n'
    t += ent_inf() + '\n\n'
    t += quick_calc_inf() + '\n'
    return t

def month_num_to_name( n ):
    l = ['januari', 'februari', 'march', 'april', 'may', 'june', 'july',
          'august', 'september', 'oktober', 'november', 'december']
    return tr.t( l[int(n)-1] )

def month_to_num( mm ):
    if mm in [ '1', '01', 'january',  'jan']:  return '01'
    if mm in [ '2', '02', 'februari', 'feb']:  return '02'
    if mm in [ '3', '03', 'march',    'mar']:  return '03'
    if mm in [ '4', '04', 'april',    'apr']:  return '04'
    if mm in [ '5', '05', 'mai',      'may']:  return '05'
    if mm in [ '6', '06', 'june',     'jun']:  return '06'
    if mm in [ '7', '07', 'july',     'jul']:  return '07'
    if mm in [ '8', '08', 'august',   'aug']:  return '08'
    if mm in [ '9', '09', 'september','sep']:  return '09'
    if mm in [ '10',      'oktober',  'okt']:  return '10'
    if mm in [ '11',      'november', 'nov']:  return '11'
    if mm in [ '12',      'december', 'dec']:  return '12'
    return '??'

def ent_to_txt(ent):
    e = ent.strip().upper()
    if   e == 'TX':    return tr.t('maximum temperature')
    elif e == 'TG':    return tr.t('mean temperature')
    elif e == 'TN':    return tr.t('minimum temperature')
    elif e == 'T10N':  return tr.t('minimum temperature (10cm)')
    elif e == 'DDVEC': return tr.t('wind direction')
    elif e == 'FG':    return tr.t('mean windspeed (daily)')
    elif e == 'RH':    return tr.t('precipitation amount')
    elif e == 'SQ':    return tr.t('sunshine duration (hourly)')
    elif e == 'PG':    return tr.t('mean pressure')
    elif e == 'UG':    return tr.t('mean atmospheric humidity')
    elif e == 'FXX':   return tr.t('maximum wind (gust)')
    elif e == 'FHVEC': return tr.t('mean windspeed (vector)')
    elif e == 'FHX':   return tr.t('maximum mean windspeed (hourly)')
    elif e == 'FHN':   return tr.t('minimum mean windspeed (hourly)')
    elif e == 'SP':    return tr.t('sunshine duration (maximum potential)')
    elif e == 'Q':     return tr.t('radiation (global)')
    elif e == 'DR':    return tr.t('precipitation duration')
    elif e == 'RHX':   return tr.t('maximum precipitation (hourly)')
    elif e == 'PX':    return tr.t('maximum pressure (hourly)')
    elif e == 'PN':    return tr.t('minimum pressure (hourly)')
    elif e == 'VVN':   return tr.t('minimum visibility')
    elif e == 'VVX':   return tr.t('maximum visibility')
    elif e == 'NG':    return tr.t('mean cloud cover')
    elif e == 'UX':    return tr.t('maximum humidity')
    elif e == 'UN':    return tr.t('minimum humidity')
    elif e == 'EV24':  return tr.t('evapotranspiration (potential)')
    return tr.t(e)

def option_lst( npl, sep=',', col_cnt = False, col_spaces = False ):
    # Possible update none values
    max_len, max_char = 0, 60
    for e in npl:
        char_len = len( str(e) )
        if char_len > max_len:
            max_len = char_len

    # Update the values
    if col_cnt == False: col_cnt = math.floor( max_char / max_len )
    if col_spaces == False or col_spaces < max_len: col_spaces = max_len

    # Make txt list with colls en newlines
    txt, n, max = '', 1, npl.size
    for e in npl:
        txt += f'{e:{col_spaces}}'
        txt += f'{sep} ' if n % col_cnt != 0 and n != max else '\n' # comma or newline
        n   += 1

    return txt

def day_ent_lst(sep=',', kol = False, kol_width = False):
    '''Functions prints a list with available entities'''
    l = daydata.entities
    for rem in np.array( [ 'FHXH', 'FHNH', 'FXXH', 'TNH', 'TXH', 'T10NH',\
                           'RHXH', 'PXH',  'PNH', 'VVNH', 'VVXH',  'UXH',\
                           'UNH' ] ):
        l = l[l != rem] # Remove time ent

    txt = optionlist( l, '', kol, kol_width )
    return txt

def txt_main( day ):
    stn, ymd, ddvec, fhvec, fg, fhx,\
    fhxh, fhn, fhnh, fxx, fxxh, tg,\
    tn, tnh, tx, txh, t10n, t10nh,\
    sq, sp, q, dr, rh, rhx,\
    rhxh, pg, px, pxh, pn, pnh,\
    vvn, vvnh, vvx, vvxh, ng, ug,\
    ux, uxh, un, unh, ev24 = ents( day )

    txt, title1, title2, title3, main1, main2, main3 = '', '', '', '', '', '', ''

    title1 += ent_to_txt('TX') if tx else ''
    title1 += ent_to_txt('TG') if tg else ''
    title1 += ent_to_txt('TN') if tn else ''
    title1 += ent_to_txt('T10N') if t10n else ''
    title1 += ent_to_txt('DDVEC') if ddvec else ''
    title1 += ent_to_txt('FG') if fg else ''
    title1 += ent_to_txt('RH') if rh else ''
    title1 += ent_to_txt('SQ') if sq else ''
    title1 += ent_to_txt('PG') if pg else ''
    title1 += ent_to_txt('UG') if ug else ''

    title2 += ent_to_txt('FXX') if fxx else ''
    title2 += ent_to_txt('FHX') if fhx else ''
    title2 += ent_to_txt('FHN') if fhn else ''
    title2 += ent_to_txt('FHVEC') if fhvec else ''
    title2 += ent_to_txt('DR') if dr else ''
    title2 += ent_to_txt('SP') if sp else ''
    title2 += ent_to_txt('Q') if q else ''
    title2 += ent_to_txt('RHX') if rhx else ''
    title2 += ent_to_txt('PX') if px else ''
    title2 += ent_to_txt('PN') if pn else ''

    title3 += ent_to_txt('VVX') if vvx else ''
    title3 += ent_to_txt('VVN') if vvn else ''
    title3 += ent_to_txt('NG') if ng else ''
    title3 += ent_to_txt('UX') if ux else ''
    title3 += ent_to_txt('UN') if un else ''
    title3 += ent_to_txt('EV24') if ev24  else ''

    main1 = ''
    main1 += tx if tx else ''
    main1 += tg if tg else ''
    main1 += tn if tn else ''
    main1 += t10n  if t10n  else ''
    main1 += ddvec if ddvec else ''
    main1 += fg    if fg    else ''
    main1 += rh    if rh    else ''
    main1 += sq    if sq    else ''
    main1 += pg    if pg    else ''
    main1 += ug    if ug    else ''

    main2 += fhvec if fhvec else ''
    main2 += fhx   if fhx   else ''
    main2 += fhn   if fhn   else ''
    main2 += fxx   if fxx   else ''
    main2 += sp    if sp    else ''
    main2 += q     if q     else ''
    main2 += dr    if dr    else ''
    main2 += rhx   if rhx   else ''
    main2 += px    if px    else ''
    main2 += pn    if pn    else ''

    main3 += vvn   if vvn   else ''
    main3 += vvx   if vvx   else ''
    main3 += ng    if ng    else ''
    main3 += ux    if ux    else ''
    main3 += un    if un    else ''
    main3 += ev24  if ev24  else ''

    txt += f'{title1}\n{main1}\n'
    txt += f'{title2}\n{main2}\n'
    txt += f'{title3}\n{main3}\n'

    return f'{txt}\n'

def process_time_ext(t='', delta_ns=0):
    '''Function gives a time string from nano seconds till days '''
    dag_sec, uur_sec, min_sec = 86400, 3600, 60
    delta_sec = delta_ns / 1000000000

    rest, total_sec = math.modf( delta_sec )
    rest, milli_sec = math.modf( rest * 1000 )
    rest, micro_sec = math.modf( rest * 1000 )
    rest, nano_sec  = math.modf( rest * 1000 )
    mill, micr, nano = int(milli_sec), int(micro_sec), int(nano_sec)

    # Calculate from seconds
    dag  = int(total_sec // dag_sec) # Calculate days
    rest = total_sec  % dag_sec      # Leftover seconds
    uur  = int(rest // uur_sec)      # Calculate hours
    rest = rest  % uur_sec           # Leftover seconds
    min  = int(rest // min_sec)      # Calculate minutes
    rest = rest  % min_sec           # Leftover seconds
    sec  = int(rest)                 # Calculate seconds

    # Make nice output. Give emthpy string if 0
    # Only print to screen when counted amount > 0
    if dag > 0: t += str(dag) + ( f' {tr.t("days")} '    if dag > 1 else f' {tr.t("day")} ' )
    if uur > 0: t += str(uur) + ( f' {tr.t("hours")} '   if uur > 1 else f' {tr.t("hour")} ' )
    if min > 0: t += str(min) + ( f' {tr.t("minutes")} ' if min > 1 else f' {tr.t("minute")} ' )

    smile = utils.add_zero_less_1000(mill)
    if sec > 0:
        t += f'{sec}.{smile} ' + ( f'{tr.t("second")} ' if sec == 1 else f'{tr.t("seconds")} ' )
    else:
        t += f'0.{smile} {tr.t("second")} '

    # if micr > 0: txt += f'{micr} {"microseconds" if micr>1 else "microsecond"} '
    # if nano > 0: txt += f'{nano} {"nanoseconds" if nano>1 else "nanosecond"} '

    return t

def process_time(t='', st=time.time_ns()):
    delta = time.time_ns() - st
    t = process_time_ext(t, delta)
    return t
