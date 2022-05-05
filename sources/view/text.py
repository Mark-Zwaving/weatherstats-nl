# -*- coding: utf-8 -*-
'''Library contains functions for writing output to screen or to a file'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU Lesser General Public License (LGPL)'
__version__    =  '0.1.3'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import numpy as np, math, time, re
import sources.view.icon as icon
import sources.model.daydata as daydata
import sources.model.utils as utils
import sources.model.stations as stations
import common.model.convert as cvt
import common.view.txt as txt

##########################################################################################
# MENU 

line = txt.line_hashtag
def head(t='Header'): return f'{line}\n##  {t}\n{line}'
def foot(t='Footer'): return f'{line}\n##  {t}\n{line}'

type_in = 'Type in something...'
next_n  = "Press 'n' to move to the next..."
back_main = "Press a 'key' to go back to the main menu..."

exit = ['x','X','exit','get out','stop']

# Menu texts
menu_no_weather_stations = f'''
No weatherstations found in configuration file !
Add one or more weatherstations in stations.py'
{foot('Press a key to quit...')}
'''

menu_no_internet_no_data = '''
No internet and no data! Not much can be done now.
1)  Try to have a working internet connection.
2)  Press a key to reload the menu or restart the application.
3)  Download weatherdata in the download options in the menu.
'''

menu_info_quick_calculations = '''
CALCULATION INFO
Default format: ENT(STATISTIC) 
Options ENT: TX, RH, SQ, TN et cetera 
Options STATISTIC: MIN -, MAX +, mean ~, SUM Σ, hellmann hmann, frostsum fsum, ijnsen, heatndx hndx

EXAMPLES: 
TX+ (=maximum temperature TX)  TG~ (=average temperature TG)  TN- (=minimum temperature TN)
RHΣ (=total rain sum)          RH+ (=maximum rain in a day)   HELLMANN (=hellmann winter score)
FSUM (=frostsum winter score)  IJNSEN (=ijnsen winter score)  HNDX (=sum heat index score)
'''

menu_info_periods = '''
PERIOD INFO
Format:  yyyymmdd-yyyymmdd     ie. 20200510-20200520

Examples with a wild card * (--- in development ---) 
*                   selects all the available data (=1x*)
**                  selects (current) month (=2x*)
****                selects (current) year (=4x*)
yyyy****            selects the whole year yyyy
yyyymm**            selects the month mm in the year yyyy
****mm**            selects a month mm for every year 
****mmdd            selects a monthday mmdd for every year 
yyyy****-yyyy****   selects a full year from yyyy untill yyyy 
yyyymmdd-yyyymmdd*  selects a day mmdd in a year from start day to endyear
yyyymmdd-yyyy*mmdd* selects a certain period from mmdd=mmdd* in a year from yyyy to yyyy

2015**** or 2015    selects the year 2015 
201101**-202001**   selects all januarys from 2011 unto 2020 
****07**            selects all julys from avalaible data 
****1225            selects all 25 decembers from avalaible data
'''

menu_info_select_a_day = f'''
DAY INFO
{txt.lst_to_col(txt.lst_mmdd, 'left', 16)}
'''

menu_info_select_a_month = f'''
MONTH INFO
{txt.lst_to_col(txt.lst_months_all, 'left', 6)}
'''

menu_info_queries = '''
QUERY INFO
Use only simple queries without parenthesis ()
Always put spaces between the elements
Example for a wet and warm day is: TX > 28 and RH > 20

gt, >          = greater than             ie. TG >  20  Warm nights
ge, >=,  ≥     = greater than and equal   ie. TX >= 30  Tropical days
lt, <          = less than                ie. TN <   0  Frosty days
le, <=,  ≤     = less than equal          ie. TX <   0  Icy days
eq, ==         = equal                    ie. DDVEC == 90  A day with a wind from the east
ne, !=, <>     = not equal                ie. RH !=  0  A day with rain

or,  ||  or    ie. SQ > 10  or TX >= 25   Sunny and warm days
and, &&  and   ie. RH > 10 and TX <  0    Most propably a day with snow
'''

menu_info_entities = '''
ENTITIES INFO
DDVEC = Vector mean wind direction (degrees)      FHVEC = Vector mean windspeed (m/s)
FG    = Daily mean windspeed (in 0.1 m/s)         FHX   = Maximum hourly mean windspeed (m/s)
FHN   = Minimum hourly mean windspeed (m/s)       FXX   = Maximum wind gust (m/s)
TG    = Daily mean temperature in (°C)            TN    = Minimum temperature (°C)
TX    = Maximum temperature (°C)                  T10N  = Minimum temperature at 10 cm (°C)
SQ    = Sunshine duration (hour)                  SP    = % of maximum sunshine duration
Q     = Global radiation (J/cm2)                  DR    = Precipitation duration (hour)
RH    = Daily precipitation amount (mm)           RHX   = Maximum hourly precipitation (mm)
PG    = Daily mean sea level pressure (hPa)       PX    = Maximum hourly sea level pressure (hPa)
PN    = Minimum hourly sea level pressure (hPa)   EV24  = Potential evapotranspiration (mm)
NG    = Mean daily cloud cover (octants)          UG    = Daily mean relative atmospheric humidity (%)
UX    = Maximum atmospheric humidity (%)          UN    = Minimum relative atmospheric humidity (%)
VVN   = Minimum visibility 0: <100m, 1:100-200m, 2:200-300m,..., 49:4900-5000m, 50:5-6 km,
        56:6-7km, 57:7-8km,..., 79:29-30km, 80:30-35km, 81:35-40km,..., 89: >70km)
VVX   = Maximum visibility 0: <100 m, 1:100-200 m, 2:200-300 m,..., 49:4900-5000 m, 50:5-6 km,
        56:6-7km, 57:7-8km,..., 79:29-30km, 80:30-35km, 81:35-40km,..., 89: >70km)
'''

menu_info_td_cells = '''
CELL STATISTICS
INFO - format: inf_<option>
Examples: inf_place, inf_province, inf_country, inf_period, inf_num, inf_period-2

STATISTICS - format: <ave|sum>_<entity>
Examples: ave_tg, sum_sq, sum_rh

EXTREMES - format: <max|min>_<entity>
Examples: max_tx, min_tn, min_t10n, max_rh, max_sq, max_rhx,
max_px, min_px, min_pn, max_ux, max_ug, min_un

INDEXES - format: ndx_<name>
Examples: ndx_hellmann, ndx_frost-sum, ndx_heat-ndx, ndx_ijnsen

COUNT DAYS - format: cnt_<entity>_<operator>_<value>
Examples: cnt_tx_ge_25, cnt_tx_ge_30, cnt_tg_ge_20, cnt_sq_ge_10, 
cnt_rh_ge_10, cnt_tx_lt_0, cnt_tn_lt_0, cnt_tn_lt_-5, 
cnt_tn_lt_-20 

Example: average temperature, maximum temperature, minimum temperature, total sum rain, 
the tropical and the ice days: 
inf_place, inf_period, ave_tg, max_tx, min_tn, sum_sq, sum_rh, cnt_tx_>_30, cnt_tx_<_0
Example: winter
inf_place, inf_period, ave_tg, min_tx, min_tn, ndx_hellmann, ndx_frost-sum, cnt_tx_<_0, cnt_tg_<_0, cnt_tn_<_0
Example: summer
inf_place, inf_period, ave_tg, max_tx, max_tn, ndx_heat, sum_sq, sum_rh, cnt_tx_>_25, cnt_tx_>_30, cnt_tn_>_20
Example short:
inf_place, inf_period, ave_tg, max_tx, min_tn, sum_sq, sum_rh, cnt_tx_>=_20, cnt_tn_<_0
'''

def menu_info_stations():
    l = [f'{s.wmo} {s.place}' for s in stations.lst_stations_map()]
    return  f'''
STATIONS INFO
{txt.lst_to_col(l, 'left', 4)}
'''

menu_allAvailable_info = f'''
{ menu_info_periods }

{ menu_info_stations() }

{ menu_info_entities }

{ menu_info_quick_calculations }
'''


##########################################################################################
typ_htm = ['html', 'htm']
typ_txt = ['txt','cmd', 'console']

# Quick txt lists
lst_gt  = ['gt', '>'] # , 'greater than'
lst_ge  = ['ge', '>=', '≥', 'gte'] # , 'greater than and equal'
lst_lt  = ['lt', '<'] # , 'less than'
lst_le  = ['le', '<=', '≤', 'lte'] # , 'less than equal'
lst_eq  = ['eq', '==', 'equal']
lst_ne  = ['ne', '!=', '<>', 'not'] # , 'not equal'
lst_or  = ['or', '||']
lst_and = ['and', '&&']
lst_op_relat = lst_gt + lst_ge + lst_lt + lst_le + lst_eq + lst_ne
lst_op_logic =  lst_or + lst_and 
lst_op  = lst_gt + lst_ge + lst_lt + lst_le + lst_eq + lst_ne + lst_or + lst_and 

lst_date = ['date', 'yyyymmdd']
lst_count = ['cnt', 'counter', 'count']
lst_num = ['num']
lst_max = ['max','up','high'] 
lst_plus = ['+']
lst_min = ['min','down','low', '-']
lst_sum = ['sum', 'total', 'tot', 'Σ']
lst_ave = ['ave', 'mean', 'average', '~']
lst_home = ['home', 'place'] 
lst_states = ['province','country'] 
lst_period_1 = ['period','periode','period1','period-1']
lst_period_2 = ['period2','period-2','periode-2']
lst_temp = ['tx','tg','tn','t10n']
lst_heat_ndx = ['heat-ndx','heat_ndx', 'heatndx', 'hndx','heat','fire'] 
lst_helmmann = ['hmann', 'hellmann','hellman']
lst_ijnsen = ['ijnsen', 'ijns']
lst_frost_sum = ['frost-sum', 'frost_sum', 'frostsum', 'fsum', 'frost_som', 'frostsom', 'frost-som', 'fsom']
lst_cold_ndx = lst_helmmann + lst_ijnsen + lst_frost_sum
lst_pressure = ['pg', 'pn', 'px']
lst_copyright = ['copy','copyright']
lst_sun = ['sun', 'sunshine', 'sq','sp']
lst_rain = ['r','dr','rhx']
lst_moist = ['ux', 'un', 'ug']
lst_wind = ['fhvec', 'fg', 'fhx', 'fhn', 'fxx']
lst_wind_direction = ['ddvec']
lst_duration = [ 'sq', 'dr' ]
lst_radiation = ['q'] 
lst_view = ['vvn', 'vvx']
list_fire = ['fire']
lst_cloud = ['ng'] 
lst_evaporation = ['ev24']
lst_yyyymmdd = ['yyyymmdd']
lst_day = ['day', 'mmdd']
lst_month = ['month','mm', 'm', 'mmm', 'mmmm']
lst_year = ['yyyy', 'year', 'yy']
lst_season = ['season']

# TXT strings
enter_default = lambda default: f'Press <enter> for default (={default})...'
enter_back_to = lambda t: f"Press 'q' to go back to the {t} menu... "
enter_previous_question = lambda s='':f"Press 'p' to go to the previous question..."
enter_exit = "Press 'x' to exit the program..."
type_more_info = lambda i: f"Type '{i}' for more info..."


def query_sign_to_text(query):
    '''Replce wrong chars for use in file name'''
    q = query.replace('>','gt')
    q = q.replace('>=|≥','ge')
    q = q.replace('<','lt')
    q = q.replace('==','eq')
    q = q.replace('ne|!=|<>','not')
    q = q.replace('\|\|','or')
    q = q.replace('&&','and')
    
    return q

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


def style(t='', style='none'):
    t = tr( t.strip().replace('  ', ' '))
    if   style in ['cap','capitalize']: t = t.capitalize()
    elif style in ['up','upper']: t = t.upper()
    elif style in ['low','lower']: t = t.lower()
    elif style in ['tit', 'title']: t = t.title()

    return t

def max(entity): 
    return f'highest {entity_to_text(entity)}'

def min(entity):
    return f'lowest {entity_to_text(entity)}'

def ave(entity):
    return f'average {entity_to_text(entity)}'

def sum(entity):
    return f'sum {entity_to_text(entity)}'
    
def hellmann():
    return f'hellmann'

def ijnsen():
    return 'ijnsen'

def frostsum():
    return 'frost_sum'

def heat_ndx():
    return 'heat_ndx'

def title(entity, sign, val):
    return 'title'

def title_mean():
    return 'title mean'

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



def entity_to_text(entity):
    e = entity.lower()
    if   e == 'tx':    return tr('maximum temperature')
    elif e == 'tg':    return tr('mean temperature')
    elif e == 'tn':    return tr('minimum temperature')
    elif e == 't10n':  return tr('minimum temperature (10cm)')
    elif e == 'ddvec': return tr('wind direction')
    elif e == 'fg':    return tr('mean windspeed (daily)')
    elif e == 'rh':    return tr('precipitation amount')
    elif e == 'sq':    return tr('sunshine duration (hourly)')
    elif e == 'pg':    return tr('mean pressure')
    elif e == 'ug':    return tr('mean atmospheric humidity')
    elif e == 'fxx':   return tr('maximum wind (gust)')
    elif e == 'fhvec': return tr('mean windspeed (vector)')
    elif e == 'fhx':   return tr('maximum mean windspeed (hourly)')
    elif e == 'fhn':   return tr('minimum mean windspeed (hourly)')
    elif e == 'sp':    return tr('sunshine duration (maximum potential)')
    elif e == 'q':     return tr('radiation (global)')
    elif e == 'dr':    return tr('precipitation duration')
    elif e == 'rhx':   return tr('maximum precipitation (hourly)')
    elif e == 'px':    return tr('maximum pressure (hourly)')
    elif e == 'pn':    return tr('minimum pressure (hourly)')
    elif e == 'vvn':   return tr('minimum visibility')
    elif e == 'vvx':   return tr('maximum visibility')
    elif e == 'ng':    return tr('mean cloud cover')
    elif e == 'ux':    return tr('maximum humidity')
    elif e == 'un':    return tr('minimum humidity')
    elif e == 'ev24':  return tr('evapotranspiration (potential)')
    return tr(e)


def entity_to_icon(entity, color='', size='', extra=''):
    e = entity.lower()
    if   e == 'tx':    return icon.temp_full(color, extra, size)
    elif e == 'tg':    return icon.temp_half(color, extra, size)
    elif e == 'tn':    return icon.temp_empty(color, extra, size)
    elif e == 't10n':  return icon.temp_empty(color, extra, size)
    elif e == 'ddvec': return icon.wind_dir(color, extra, size)
    elif e == 'fg':    return icon.wind(color, extra, size)
    elif e == 'rh':    return icon.shower_heavy(color, extra, size)
    elif e == 'sq':    return icon.sun(color, extra, size)
    elif e == 'pg':    return icon.compress_alt(color, extra, size)
    elif e == 'ug':    return icon.drop_tint(color, extra, size)
    elif e == 'fxx':   return icon.wind(color, extra, size)
    elif e == 'fhvec': return icon.wind(color, extra, size)
    elif e == 'fhx':   return icon.wind(color, extra, size)
    elif e == 'fhn':   return icon.wind(color, extra, size)
    elif e == 'sp':    return icon.sun(color, extra, size)
    elif e == 'q':     return icon.radiation(color, extra, size)
    elif e == 'dr':    return icon.shower_heavy(color, extra, size)
    elif e == 'rhx':   return icon.shower_heavy(color, extra, size)
    elif e == 'px':    return icon.compress_alt(color, extra, size)
    elif e == 'pn':    return icon.compress_alt(color, extra, size)
    elif e == 'vvn':   return icon.eye(color, extra, size)
    elif e == 'vvx':   return icon.eye(color, extra, size)
    elif e == 'ng':    return icon.cloud(color, extra, size)
    elif e == 'ux':    return icon.drop_tint(color, extra, size)
    elif e == 'un':    return icon.drop_tint(color, extra, size)
    elif e == 'ev24':  return icon.sweat(color, extra, size)
    elif e in lst_day: return icon.day(color, extra, size)
    elif e in lst_max: return icon.arrow_up(color, extra, size)
    elif e in lst_min: return icon.arrow_down(color, extra, size)
    elif e in lst_home: return icon.home(color, extra, size)
    elif e in lst_states: return icon.flag(color, extra, size)
    elif e in lst_states: return icon.flag(color, extra, size)
    elif e in lst_period_1: return icon.cal_period(color, extra, size)
    elif e in lst_period_2: return icon.cal_day(color, extra, size)
    elif e in lst_heat_ndx: return icon.fire(color, extra, size)
    elif e in lst_cold_ndx: return icon.icicles(color, extra, size)
    elif e in ['pg', 'pn', 'px']: return icon.compress_alt(color, extra, size)
    elif e in ['ux', 'un', 'ug']: return icon.drop_tint(color, extra, size)
    elif e in lst_wind: return icon.wind(color, extra, size)
    elif e in lst_rain: return icon.shower_heavy(color, extra, size)
    elif e in lst_wind_direction: return icon.wind_dir(color, extra, size)
    elif e in lst_copyright: return icon.copy(color, extra, size)
    elif e in lst_view: return icon.eye(color, extra, size)
    elif e in ['q']: return icon.radiation(color, extra, size)
    elif e in ['ng']: return icon.cloud(color, extra, size)
    elif e in lst_evaporation: return icon.sweat(color, extra, size)
    elif e in ['sq','sp']: return icon.sun(color, extra, size)
    elif e in lst_sum: return 'Σ'
    elif e in lst_ave: return ''
    elif e in lst_gt: return icon.gt(color, extra, size)
    elif e in lst_ge: return icon.ge(color, extra, size)
    elif e in lst_lt: return icon.lt(color, extra, size)
    elif e in lst_le: return icon.le(color, extra, size)
    elif e in lst_eq: return '=='
    elif e in lst_ne: return '!=' 
    elif e in lst_num: return icon.sort_down(color, extra, size)
    else: 
        return icon.umbrella(color, extra, size)


# def home(color='', extra='', size=''): return i('fas fa-home', color, extra, size)
# def flag(color='', extra='', size=''): return i('fab fa-font-awesome-flag', color, extra, size)
# def : return i('fas fa-fire-alt', color, extra, size)
# def cal_period(color='', extra='', size=''): return i('far fa-calendar-alt', color, extra, size)
# def cal_day(color='', extra='', size=''): return i('fas fa-calendar-day', color, extra, size)
# def sun(color='', extra='', size=''): return i('fas fa-sun', color, extra, size)
# def temp_full(color='', extra='', size=''): return i('fas fa-thermometer-full', color, extra, size)
# def temp_half(color='', extra='', size=''): return i('fas fa-thermometer-half', color, extra, size)
# def temp_empty(color='', extra='', size=''): return i('fas fa-thermometer-empty', color, extra, size)
# def wind(color='', extra='', size=''): return i('fas fa-wind', color, extra, size)
# def wind_dir(color='', extra='', size=''): return i('fas fa-location-arrow', color, extra, size)
# def shower_heavy(color='', extra='', size=''): return i('fas fa-cloud-showers-heavy', color, extra, size)
# def compress(color='', extra='', size=''): return i('fas fa-compress', color, extra, size)
# def compress_alt(color='', extra='', size=''): return i('fas fa-compress-arrows-alt', color, extra, size)
# def cloud(color='', extra='', size=''): return i('fas fa-cloud', color, extra, size)
# def drop_tint(color='', extra='', size=''): return i('fas fa-tint', color, extra, size)
# def eye(color='', extra='', size=''): return i('fas fa-eye', color, extra, size)
# def radiation(color='', extra='', size=''): return i('fas fa-radiation-alt', color, extra, size)
# def sweat(color='', extra='', size=''): return i('far fa-grin-beam-sweat', color, extra, size)
# def icicles(color='', extra='', size=''): return i('fas fa-icicles', color, extra, size)
# def calculator(color='', extra='', size=''): return i('fas fa-calculator', color, extra, size)
# def weather_all(color='', extra='', size=''): return i('fas fa-cloud-sun-rain', color, extra, size)
# def arrow_loc(color='', extra='', size=''): return i('fas fa-location-arrow', color, extra, size)
# def arrow_up(color='', extra='', size=''): return i('fas fa-arrow-up', color, extra, size)
# def arrow_left(color='', extra='', size=''): return i('fas fa-arrow-left', color, extra, size)
# def arrow_down(color='', extra='', size=''): return i('fas fa-arrow-down', color, extra, size)
# def arrow_right(color='', extra='', size=''): return i('fas fas fa-arrow-right', color, extra, size)
# def binoculars(color='', extra='', size=''): return i('fas fa-binoculars', color, extra, size)
# def minus(color='', extra='', size=''): return i('fas fa-minus', color, extra, size)
# def plus(color='', extra='', size=''): return i('fas fa-plus', color, extra, size)
# def wave_square(color='', extra='', size=''): return i('fas fa-wave-square', color, extra, size)
# def copy_light(color='', extra='', size=''): return i('far fa-copyright', color, extra, size)


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
    t, n, max = '', 1, npl.size
    for e in npl:
        t += f'{e:{col_spaces}}'
        t += f'{sep} ' if n % col_cnt != 0 and n != max else '\n' # comma or newline
        n   += 1

    return t

def day_ent_lst(sep=',', kol = False, kol_width = False):
    '''Functions prints a list with available entities'''
    l = daydata.entities
    for rem in np.array( [ 'FHXH', 'FHNH', 'FXXH', 'TNH', 'TXH', 'T10NH',\
                           'RHXH', 'PXH',  'PNH', 'VVNH', 'VVXH',  'UXH',\
                           'UNH' ] ):
        l = l[l != rem] # Remove time ent

    t = option_lst( l, '', kol, kol_width )
    return t

def txt_main( day ):
    stn, ymd, ddvec, fhvec, fg, fhx,\
    fhxh, fhn, fhnh, fxx, fxxh, tg,\
    tn, tnh, tx, txh, t10n, t10nh,\
    sq, sp, q, dr, rh, rhx,\
    rhxh, pg, px, pxh, pn, pnh,\
    vvn, vvnh, vvx, vvxh, ng, ug,\
    ux, uxh, un, unh, ev24 = daydata.ents( day )

    t, title1, title2, title3, main1, main2, main3 = '', '', '', '', '', '', ''

    title1 += entity_to_text('TX') if tx else ''
    title1 += entity_to_text('TG') if tg else ''
    title1 += entity_to_text('TN') if tn else ''
    title1 += entity_to_text('T10N') if t10n else ''
    title1 += entity_to_text('DDVEC') if ddvec else ''
    title1 += entity_to_text('FG') if fg else ''
    title1 += entity_to_text('RH') if rh else ''
    title1 += entity_to_text('SQ') if sq else ''
    title1 += entity_to_text('PG') if pg else ''
    title1 += entity_to_text('UG') if ug else ''
    title2 += entity_to_text('FXX') if fxx else ''
    title2 += entity_to_text('FHX') if fhx else ''
    title2 += entity_to_text('FHN') if fhn else ''
    title2 += entity_to_text('FHVEC') if fhvec else ''
    title2 += entity_to_text('DR') if dr else ''
    title2 += entity_to_text('SP') if sp else ''
    title2 += entity_to_text('Q') if q else ''
    title2 += entity_to_text('RHX') if rhx else ''
    title2 += entity_to_text('PX') if px else ''
    title2 += entity_to_text('PN') if pn else ''
    title3 += entity_to_text('VVX') if vvx else ''
    title3 += entity_to_text('VVN') if vvn else ''
    title3 += entity_to_text('NG') if ng else ''
    title3 += entity_to_text('UX') if ux else ''
    title3 += entity_to_text('UN') if un else ''
    title3 += entity_to_text('EV24') if ev24  else ''

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

    t += f'{title1}\n{main1}\n'
    t += f'{title2}\n{main2}\n'
    t += f'{title3}\n{main3}\n'

    return f'{t}\n'

def fix_entity(val, entity):
    '''Function adds correct post/prefixes for weather entities'''
    # No measurement or false measurement
    if not daydata.check(val):
        return cfg.txt_no_data # Return '.'

    e = entity.strip().lower()
    f = daydata.process_value(val, e) # Format correct for entity

    # Date format: yyyymmddd
    if e in lst_date:
        return f'{f:.0f}'

    # Indexes
    elif e in lst_heat_ndx + lst_frost_sum:
        return f'{f:.1f}'

    elif e in lst_ijnsen:
        return f'{f:.2f}'

    # Counts
    elif e in lst_count: 
        return f'{f:.0f}'

    # Temperatures
    elif e in [ 'tx', 'tn', 'tg', 't10n' ]:
        return f'{f:.1f}°C'

    # Airpressure
    elif e in [ 'pg', 'pn', 'px' ]:
        return f'{f:.0f}hPa'

    # Radiation
    elif e in [ 'q' ]:
        return f'{f:.1f}J/cm2'

    # Percentages
    elif e in [ 'ug', 'ux', 'un', 'sp' ]:
        return f'{f:.0f}%'

    # Time hours
    elif e in [ 'fhxh', 'fhnh', 'fxxh', 'tnh', 'txh', 'rhxh',
                'pxh', 'vvnh', 'vvxh', 'uxh', 'unh', 'pnh' ]:
        f1 = f'{f:.0f}'
        f2 = f'{(f-1):.0f}'
        return f'{f2}-{f1}{tr("hour")}'

    # Time 6 hours
    elif e in [ 't10nh' ]:
        f1 = f'{f:.0f}'
        f2 = f'{(f-6):.0f}'
        return f'{f2}-{f1}{tr("hour")}'

    # CLouds cover/octants
    elif e in [ 'ng' ]:
        return f'{f:.0f}'

    # Wind
    elif e in lst_wind:
        bft = cvt.ms_to_bft(val)
        return f'{f:.1f}m/s {bft}bft'

    # Evapotranspiration
    elif e in [ 'ev24', 'rh', 'rhx' ]:
        return f'{f:.1f}mm'

    # Duration hours
    elif e in lst_duration:
        return f'{f:.1f}{tr("hour")}'

    # Wind direction
    elif e in lst_wind_direction:
        if f == 0.0:
            return f'{f:.0f}° {tr("VAR")}'
        else:
            # From degrees to direction
            # Source: https://www.campbellsci.com/blog/convert-wind-directions
            ldir = [ 'N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S',
                     'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW', 'N' ]
            ndx = int( round( f % 360 / 22.5 ) )
            dir = ldir[ndx]
            return f'{f:.0f}° {tr(dir)}'

    # View distance
    elif e in lst_view:
        if f == 0.0:
            return '<100m'
        else:
            if f < 49.0:
                f1 = f * 100.0
                f2 = (f + 1.0) * 100.0
                return f'{f1:.0f}-{f2:.0f}m'
            elif f == 50.0:
                return '5-6km'
            elif f <= 79.0:
                f1 = f - 50.0
                f2 = f - 49.0
                return f'{f1:.0f}-{f2:.0f}km'
            elif f <= 89.0:
                f1 = f - 50.0
                f2 = f - 45.0
                return f'{f1:.0f}-{f2:.0f}km'
            else:
                return '>70km'

    return f  # Without string casting will give an error with unknowm data entity


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
    if dag > 0: t += str(dag) + ( f' {tr("days")} '    if dag > 1 else f' {tr("day")} ' )
    if uur > 0: t += str(uur) + ( f' {tr("hours")} '   if uur > 1 else f' {tr("hour")} ' )
    if min > 0: t += str(min) + ( f' {tr("minutes")} ' if min > 1 else f' {tr("minute")} ' )

    smile = utils.add_zero_less_1000(mill)
    if sec > 0:
        t += f'{sec}.{smile} ' + ( f'{tr("second")} ' if sec == 1 else f'{tr("seconds")} ' )
    else:
        t += f'0.{smile} {tr("second")} '

    # if micr > 0: t += f'{micr} {"microseconds" if micr>1 else "microsecond"} '
    # if nano > 0: t += f'{nano} {"nanoseconds" if nano>1 else "nanosecond"} '

    return t

def process_time(t='', st=time.time_ns(), ln='\n'):
    delta = time.time_ns() - st
    t = process_time_ext(t, delta)
    return t + ln



##########################################################################################
# TRANSLATIONS TODO
EN = 0
NL = 1

lst_translate =  [
    ['Welcome', 'Welkom'],
    ['Good bye', 'Tot ziens'],
    ['Welcome to WeatherStats NL', 'Welkom bij WeerStats NL'],
    ['No weatherstations found !', 'Geen weerstations gevonden !'],
    ['Add one or more weatherstations in stations.py', 'Voeg één of meer weerstations toe in stations.py'],
    ['Press a key...', 'Druk op een toets...'],
    ['Press a key to quit...', 'Druk op een toets om af te sluiten...'],
    ['MAIN MENU', 'HOOFDMENU'],
    ['Choose one of the following options:', 'Maak een keus uit de volgende opties:'],
    ['Download data all knmi stations', 'Download de gegevens van alle knmi stations'],
    ['Download data of one or more knmi stations', 'Download de gegevens van één of meerdere knmi stations'],
    ['Get weather day values of a day', 'Verkrijg de weergegevens van één dag'],
    ['Calculate summer statistics', 'Bereken zomerstatistieken'],
    ['Calculate heatwaves', 'Bereken hittegolven'],
    ['Calculate winter statistics', 'Bereken winterstatistieken'],
    ["Press 'q' to quit...", "Druk op 'q' om af te sluiten"]
]

def tr(t):
    '''Function translates text from English to other languages'''
    if cfg.translate: # If  translate is active
        LANG = EN # English is default
        if cfg.language == 'NL': 
            LANG = NL

        s = t.lower() # Case insensitive
        for k, l in enumerate(lst_translate): # Search in pool
            if l[EN].lower() == s: # Check on English
                return l[LANG] # return correct language

    return t # Nothing found or translation not activated
