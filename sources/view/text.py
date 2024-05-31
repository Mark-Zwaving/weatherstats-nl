# -*- coding: utf-8 -*-
'''Library contains functions for writing output to screen or to a file'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.2.8'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg, defaults
import numpy as np, math, re, shutil 
import sources.model.dayvalues.data as data
import sources.model.utils as utils
import sources.model.stations as stations
import sources.model.convert as convert
import sources.model.ymd as ymd

cli_colls, cli_rows = shutil.get_terminal_size()

def line(s): return str(s) * (shutil.get_terminal_size()[0] - 1)
def line_hashtag(): return line('#')
def line_hyphen(): return line('-')
def head(t='Header'): return f'{line_hashtag()}\n##  {t}\n{line_hashtag()}'
def foot(t='Footer'): return f'{line_hashtag()}\n##  {t}\n{line_hashtag()}\n'

def lines_spacer( cnt=1 ):
    '''Function print enters to the screen'''
    t = ''
    for _ in range(cnt):
        t += cfg.ln 
    return t

# Txt question strings
enter_back_menu = lambda t='main', c='b':  f"# Press '{c}' to go back to the {t} menu... " 
enter_back_main = enter_back_menu('main', 'a key') 
enter_default   = lambda default, c='enter': f"# Press '{c}' for default (='{default}')..." 
enter_previous  = lambda c='p':     f"# Press '{c}' to go to the previous question..." 
enter_exit      = lambda c='q':     f"# Press '{c}' to quit the program..." 
enter_next      = lambda c='enter': f"# Press '{c}' to move to the next..." 
enter_y_or_n    = lambda y='y', n='n': f"# Type in '{y}' for yes or '{n}' for no..."
type_more_info  = lambda c='i':     f"# Type '{c}' for more info..." 
error           = lambda t, err:    f'{t} failed.\nError {err}...' 
succes          = lambda t:         f'{t} success...' 
type_in         = 'Type in something...' 
press_enter_continue = 'Press <enter> to continue...'

# Answers option lists
lst_quit = ['q','quit','stop','ho', 'x','X','exit','get out']
lst_yes  = ['y','yes','yess','j','ja','ok','oke','oké','yee','jee', 'yep', 'yup', 'oui']
lst_no   = ['n','no','nope','not','nee','nada','nein','non','neet','njet','neen']
lst_prev = ['p', 'last', 'prev', 'previous']
lst_back = ['b', 'back', 'return']

# File extensions
extension_htm = '.html'
extension_txt = '.txt'
extension_csv = '.csv'
extension_excel = '.xlsx'

# Output options
lst_output_options = [
    'console (text)', 
    'html', 
    # 'X csv TODO', 
    # 'X excel TODO', 
    #'X all types TODO'
]
lst_output_cnsl = ['cmd', 'console', 'command', 'command line', 'console only', 'console (text)']
lst_output_htm = ['html', 'htm', 'html file', 'htm file']
lst_output_txt = ['txt', 'text', 'text file', 'txt file']
lst_output_csv = ['csv', 'csv file']
lst_output_excel = ['excel', 'excel file', 'excell', 'excell file']
lst_output_gif = ['gif']
lst_output_jpg = ['jpg', 'jpeg']
lst_output_png = ['png']
lst_output_webm = ['webm']
lst_output_img = lst_output_gif + lst_output_jpg + lst_output_png + lst_output_webm 
lst_output_all = ['*', 'all', 'all file types']
lst_output_txt_cnsl = lst_output_txt + lst_output_cnsl
lst_output_csv_excel = lst_output_csv + lst_output_excel
lst_output_files = lst_output_htm + lst_output_csv + lst_output_excel + lst_output_img
lst_output_all = lst_output_cnsl + lst_output_files

# Ask options
ask_title             = 'title'
ask_colspan           = 'colspan'
ask_other_menu        = 'other-menu'
ask_start_datetime    = 'start-datetime'
ask_end_datetime      = 'end-datetime'
ask_lst_see_days      = 'lst-select-yyyymmdd'
ask_lst_period_1      = 'lst-period-1'
ask_lst_period_2      = 'lst-period-2'
ask_period            = 'period-1'
ask_period_1          = ask_period
ask_period_2          = 'periode-2'
ask_per_compare       = 'period-cmp'
ask_file_type         = 'file-type'
ask_filename          = 'file-name'
ask_save_txt_file     = 'save-txt-file'
ask_download          = 'download'
ask_download_knmi     = 'download-knmi-one-or-more'
ask_download_url      = 'image-download-url'
ask_download_interval = 'interval-download'
ask_animation_name    = 'animation-name'
ask_animation_time    = 'animation-time' 
ask_rm_downloads      = 'remove-downloads' 
ask_gif_compress      = 'gif-compress'
ask_lst_stations      = 'lst-stations'
ask_select_cells      = 'lst-sel-cells'
ask_select_all_cells  = 'lst-sel-all-cells'
ask_diy_cells         = 'lst-diy-cells'
ask_write_dayval      = 'write-dayvalues'
ask_s4d_query         = 's4d-query'
ask_clima_period      = 'clima-period'
ask_lst_entities      = 'lst-entities'
ask_verbose           = 'verbose'
ask_sqlite_query      = 'sqlite-query'

# Graph specific
ask_graph_title       = 'graph-title'
ask_graph_ylabel      = 'graph-y-label'
ask_graph_default     = 'graph-default'
ask_graph_width       = 'graph-width'
ask_graph_height      = 'graph-height'
ask_graph_cummul_val  = 'graph-cummul-val'
ask_graph_type        = 'graph-type'
ask_graph_dpi         = 'graph-dpi'
ask_graph_extension   = 'graph-extension'

ask_lst_graph_entities                  = 'graph-entities-lst'
ask_lst_graph_entities_options          = 'graph-entities-lst-options'
ask_graph_entity_name                   = 'graph_entity'
ask_graph_entity_type                   = 'graph_type'
ask_graph_entity_line_width             = 'graph_line-width'
ask_graph_entity_marker_size            = 'graph_marker-size'
ask_graph_entity_marker_text            = 'graph_marker-text'
ask_graph_entity_min_max                = 'graph_min-max-period'
ask_graph_entity_climate_ave            = 'graph_climate-ave'
ask_graph_entity_climate_ave_marker_txt = 'graph_climate-ave-marker-txt'
ask_graph_entity_climate_yyyy_start     = 'graph_climate-yyyy-start'
ask_graph_entity_climate_yyyy_end       = 'graph_climate-yyyy-end'
ask_graph_entity_climate_period         = 'graph_climate-periode'

# Questions to ask
lst_ask_stats = [ 
    ask_period_1, ask_lst_stations, 
    ask_file_type, ask_filename
]

lst_ask_stats_diy = [ 
    ask_period_1, ask_lst_stations, ask_select_cells, 
    ask_file_type, ask_filename
]

lst_ask_stats_p1_p2_diy = [ 
    ask_period_1, ask_period_2, ask_lst_stations, 
    ask_select_all_cells, ask_file_type, ask_filename
]

lst_ask_stats_compare = [ 
    ask_period_1, ask_per_compare, ask_lst_stations, 
    ask_select_cells, ask_file_type, ask_filename
]

lst_ask_download_knmi = [ 
    ask_lst_stations 
]

lst_ask_download_files = [ 
    ask_download_url, ask_start_datetime, 
    ask_end_datetime, ask_download_interval 
] 

lst_ask_animation = [ 
    ask_animation_name, ask_animation_time, 
    ask_rm_downloads, ask_gif_compress
]

lst_ask_make_dayval = [ 
    ask_period_1, ask_lst_stations, 
    ask_file_type, ask_write_dayval
]

lst_ask_see_dayval = [ 
    ask_lst_period_1, ask_lst_stations, ask_lst_entities
]

lst_ask_search_4_day = [ 
    ask_lst_period_1, ask_lst_stations, ask_s4d_query, 
    ask_file_type, ask_filename 
]

# Graphs
lst_ask_graph = [ 
    ask_period_1, ask_lst_stations, ask_lst_graph_entities, 
    ask_graph_title, ask_graph_ylabel, 
    ask_graph_default, ask_graph_width, ask_graph_height, 
    # ask_graph_dpi, 
    ask_lst_graph_entities_options,
    ask_filename
]

lst_ask_graph_entities = [
    ask_graph_entity_type, 
    ask_graph_entity_marker_text, 
    ask_graph_entity_min_max, 
    ask_graph_entity_climate_ave, 
    ask_graph_entity_climate_ave_marker_txt
]

# Database
lst_ask_db_fill = [ask_lst_stations]
lst_ask_sqlite_query = [ask_sqlite_query]

# 'lst-stations', 'period', 'lst-entities', 'file-name', 'graph-type',
# 'graph-title', 'graph-y-label', 'graph-default','graph-width',
# 'graph-height', 'graph-cummul-val','graph-dpi', 'graph-lst-entities-types'

# [ 'QUICK IO <TODO>',
#     [ [ 'Quick statistics', cquick_stats_io ],
#       [ 'Quick graphs', cquick_graphs_io ],
#     ]
# ],

# Menu texts
menu_no_weather_stations = f'''
No weatherstations found in stations file !
Add one or more weatherstations in stations.py
'''

menu_no_internet_no_data = '''
No internet and no data! Not much can be done now.
1)  Try to have a working internet connection.
2)  Press a key to reload the menu or restart the application.
3)  Download weatherdata in the download options in the menu.
'''

menu_image_download_examples = f'''
{head('DOWNLOAD URLS')}
Examples KNMI
Temperature:  https://cdn.knmi.nl/knmi/map/page/weer/actueel-weer/temperatuur.png  
Windforce:    https://cdn.knmi.nl/knmi/map/page/weer/actueel-weer/windkracht.png 
Windspeed:    https://cdn.knmi.nl/knmi/map/page/weer/actueel-weer/windsnelheid.png 
Windblast:    https://cdn.knmi.nl/knmi/map/page/weer/actueel-weer/maxwindkm.png 
Moisture:     https://cdn.knmi.nl/knmi/map/page/weer/actueel-weer/relvocht.png 
View:         https://cdn.knmi.nl/knmi/map/page/weer/actueel-weer/zicht.png 
{line_hashtag()}
'''

# # Weerplaza 
# Temperature:         https://oud.weerplaza.nl/gdata/10min/GMT_TTTT_latest.png
# Temperature (10cm):  https://oud.weerplaza.nl/gdata/10min/GMT_T10C_latest.png
# Current weather:     https://oud.weerplaza.nl/gdata/10min/nl_10min.jpg
# Windforce:           https://oud.weerplaza.nl/gdata/10min/GMT_FFFF_latest.png 
# Windblast:           https://oud.weerplaza.nl/gdata/10min/GMT_FXFF_latest.png
# Cloud cover:         https://oud.weerplaza.nl/gdata/10min/GMT_NNNN_latest.png 
# Moisture:            https://oud.weerplaza.nl/gdata/10min/GMT_RHRH_latest.png
# View:                https://oud.weerplaza.nl/gdata/10min/GMT_VVVV_latest.png 

menu_info_quick_calculations = f'''
{head('CALCULATION INFO')}
Default format: ENT(STATISTIC) 
Options ENT: TX, RH, SQ, TN et cetera 
Options STATISTIC: MIN -, MAX +, mean ~, SUM Σ, hellmann hmann, frostsum fsum, ijnsen, heatndx hndx
EXAMPLES: 
TX+ (=maximum temperature TX)  TG~ (=average temperature TG)  TN- (=minimum temperature TN)
RHΣ (=total rain sum)          RH+ (=maximum rain in a day)   HELLMANN (=hellmann winter score)
FSUM (=frostsum winter score)  IJNSEN (=ijnsen winter score)  HNDX (=sum heat index score)
{line_hashtag()}
'''

menu_info_periods = f'''
{head('PERIOD INFO')}
One period:
    Format:  yyyymmdd-yyyymmdd     E.g: 20200510-20200520
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
For multiple periods, use a comma to separate the periods
    E.g: 20230101-20230131, 20240101-02 
For one day:
    Format: yyyymmdd   E.g: 20240101
Multiple days, use a comma to separate the days 
    E.g: 20240101, 19630204, 19970707
{line_hashtag()}
'''

menu_info_period2 = f'''
{head('PERIOD 2 INFO')}
Second period, a sub period in a period
 - Period2
 - Month
 - Day
 - Season TODO
{line_hashtag()}
'''

menu_info_select_a_day = f'''
{head('DAY INFO')}
Day date format: mmdd
{utils.lst_to_col(
    utils.add_lst(ymd.lst_mmdd01,'JAN: ') +
    utils.add_lst(ymd.lst_mmdd02,'FEB: ') + 
    utils.add_lst(ymd.lst_mmdd03,'MAI: ') +
    utils.add_lst(ymd.lst_mmdd04,'APR: ') + 
    utils.add_lst(ymd.lst_mmdd05,'MAI: ') +
    utils.add_lst(ymd.lst_mmdd06,'JUN: ') +
    utils.add_lst(ymd.lst_mmdd07,'JUL: ') +
    utils.add_lst(ymd.lst_mmdd08,'AUG: ') +
    utils.add_lst(ymd.lst_mmdd09,'SEP: ') +
    utils.add_lst(ymd.lst_mmdd10,'OCT: ') +
    utils.add_lst(ymd.lst_mmdd11,'NOV: ') +
    utils.add_lst(ymd.lst_mmdd12,'DEC: '), 
    'left', col=15, width=4)}
{line_hashtag()}
'''

menu_info_select_a_month = f'''
{head('MONTH INFO')}
Month day format: mm
{utils.lst_to_col(ymd.lst_months_all, 'left', col=6, width=3)}
{line_hashtag()}
'''

menu_info_queries = f'''
{head('QUERY INFO')}
Use only simple queries without parenthesis ()
Always put spaces between the elements
Example for a wet and warm day is: TX > 28 and RH > 20
gt, >          = greater than             E.g: TG >  20  Warm nights
ge, >=,  ≥     = greater than and equal   E.g: TX >= 30  Tropical days
lt, <          = less than                E.g: TN <   0  Frosty days
le, <=,  ≤     = less than equal          E.g: TX <   0  Icy days
eq, ==         = equal                    E.g: DDVEC == 90  A day with a wind from the east
ne, !=, <>     = not equal                E.g: RH !=  0  A day with rain
or,  ||  or    E.g: SQ > 10  or TX >= 25  Sunny and warm days
and, &&  and   E.g: RH > 10 and TX <  0   Most propably a day with snow
{line_hashtag()}
'''

menu_info_entities = f'''
{head('ENTITIES INFO')}
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
{line_hashtag()}
'''

menu_info_td_cells = f'''
{head('TABLE CELLS INFO')}
INFO format: inf_[place|province|country|period-1|period-2]
E.g: inf_place, inf_province, inf_country, inf_period-1
STATISTICS format: [ave|sum]_entity
E.g: ave_tg, sum_sq, sum_rh
EXTREMES format: [max|min]_entity
E.g: max_tx, min_tn, max_rh, max_sq, max_px, min_px, min_un
INDiCES format: ndx_[name-ndx]
E.g: ndx_hellmann, ndx_frost-sum, ndx_heat-ndx, ndx_ijnsen
COUNTERS format: cnt_[entity]_[operator]_[value]
E.g: cnt_tx_gte_25, cnt_sq_gt_10, cnt_tx_<_0, cnt_tn_lt_-20 
CLIMATE format: clima_[ave|sum]_[entity] | clima_[cnt]_[entity]_[operand]_[value]
E.g: clima_ave_tg, clima_sum_rh, clima_cnt_tn_<_0 
Examples:
E.g winter: inf_place, inf_period-1, ave_tg, clima_ave_tg, min_tn, ndx_hellmann, cnt_tn_<_0
E.g spring: inf_place, inf_period-1, ave_tg, max_tx, min_tx, sum_sq, clima_sum_sq, cnt_tx_>=_25
E.g summer: inf_place, inf_period-1, ave_tg, max_tx, ndx_heat-ndx, sum_rh, cnt_tx_>=_30
See files - examples-cells.txt and cell-available.py - for more info
{line_hashtag()}
'''

menu_info_td_all_type_cells = f'''
{head('TABLE CELLS ALL TYPES INFO')}
DIY statistics: ['add your own statistics cells', 'et cetera', '']
{cfg.ln.join([ f'{l[0]}: {l[1]}' for l in defaults.lst_menu ])}
{line_hashtag()}
'''

menu_info_stations =  f'''
{head('STATIONS INFO')}
{utils.lst_to_col([f'{s.wmo} {s.place}' for s in stations.lst_stations_map()], 'left', col=3)}
{line_hashtag()}
'''

quick_stats_all_inf  = menu_info_periods + cfg.ln + cfg.ln
quick_stats_all_inf += menu_info_stations + cfg.ln + cfg.ln
quick_stats_all_inf += menu_info_entities + cfg.ln + cfg.ln
quick_stats_all_inf += menu_info_quick_calculations + cfg.ln

menu_all_available_info = f'''
{ menu_info_periods }
{ menu_info_stations }
{ menu_info_entities }
{ menu_info_quick_calculations }
'''

##########################################################################################
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

lst_yyyymmdd = lst_date = ['date', 'yyyymmdd']
lst_count = ['cnt', 'counter', 'count']
lst_ndx = ['index', 'ndx', 'idx']
lst_info = ['inf', 'info']
lst_clima = ['clima', 'clim', 'cli']
lst_num = ['num']
lst_max = ['max', 'maximum', 'up', 'high'] 
lst_min = ['min', 'minimum', 'down', 'low', '-', 'minus']
lst_extremes = lst_max + lst_min
lst_plus = ['plus', '+'] 
lst_sum = ['sum', 'total', 'tot', 'Σ']
lst_ave = ['ave', 'mean', 'average', '~']
lst_place = ['place'] 
lst_province = ['province']
lst_country = ['country', 'land']
lst_states = lst_province + lst_country 
lst_geo_places = lst_states + lst_place
lst_period_1 = ['period1', 'period-1', 'periode-1','period', 'periode']
lst_period_2 = ['period2', 'period-2', 'periode-2']
lst_period = lst_period_1 + lst_period_2
lst_temp = ['temperature', 'temp', 'tx', 'tg', 'tn', 't10n']
lst_heat_ndx = ['heatindex', 'heat-index', 'heat-ndx', 'heatndx', 'hndx', 'heat'] 
lst_helmmann = ['hmann', 'hman', 'hellmann', 'hellman', 'helman']
lst_ijnsen = ['ijnsen', 'ijns']
lst_frost_sum = ['frost-sum', 'frostsum', 'fsum', 'frostsom', 'frost-som', 'fsom']
lst_cold_ndx = lst_helmmann + lst_ijnsen + lst_frost_sum
lst_pressure = ['pg', 'pn', 'px']
lst_copyright = ['copy', 'copyright']
lst_sun = ['sun', 'sunshine', 'sq', 'sp']
lst_rain = ['rain', 'rh', 'dr', 'rhx']
lst_moist = ['moist', 'ux', 'un', 'ug']
lst_wind = ['wind', 'fhvec', 'fg', 'fhx', 'fhn', 'fxx']
lst_wind_direction = ['direction', 'ddvec', 'wind-direction']
lst_duration = [ 'duration', 'sq', 'dr' ]
lst_radiation = ['radiation', 'q'] 
lst_view = ['view', 'vvn', 'vvx']
lst_fire = ['fire']
lst_cloud = ['cloud', 'ng'] 
lst_evaporation = ['evaporation', 'ev24']
lst_day = ['day', 'mmdd']
lst_month = ['month','mm', 'm', 'mmm', 'mmmm']
lst_year = ['year', 'yyyy', 'yy']
lst_mmdd_compare = ['days mmdd-mmdd', 'mmdd-mmdd']
lst_season = ['season']
lst_winter = ['winter']
lst_summer = ['summer']
lst_autumn = ['autumn', 'fall']
lst_spring = ['spring']

# Padding text values for text output
pad_default = 8
pad_tx = 5
pad_tg = 5
pad_tn = 5
pad_t10n = 5
pad_ddvec = 5
pad_fg = 5
pad_rh = 5
pad_sq = 5
pad_pg = 5
pad_ug = 5
pad_fxx = 5
pad_fhvec = 5
pad_fhx = 5
pad_fhn = 5
pad_sp = 5
pad_q = 5
pad_dr = 5
pad_rhx = 5
pad_px = 10
pad_pn = 10
pad_vvn = 5
pad_vvx = 5
pad_ng = 3
pad_ux = 5
pad_un = 5
pad_ev24 = 5
pad_cnt = 6
pad_day = 10
pad_max = 15
pad_min = 15
pad_extreme = 18
pad_home = 15
pad_states = 15
pad_place = 15
pad_province = 15
pad_country = 15
pad_period = 19
pad_period_1 = 19
pad_period_2 = 19
pad_month = 3
pad_heat_ndx = 5
pad_hmann = 7
pad_ijns = 7
pad_fsum = 7
pad_cold_ndx = 7
pad_wind = 10
pad_copyright = 3
pad_view = 10
pad_sum = 10
pad_ave = 10
pad_gt = 4
pad_ge = 4
pad_lt = 4
pad_le = 4
pad_eq = 4
pad_ne = 4
pad_num = 4
pad_clima = 14 
pad_view = 4 
pad_evaporation = 4 






# Copyright notification weatherstats 
created_by_notification = 'Created by weatherstats-nl at %s' 
created_by_notification_html = '''
    Created by <a href="https://github.com/Mark-Zwaving/weatherstats-nl" target="_blank">weatherstats-nl</a> at 
'''

def create_by_notification_html():
    notif = cfg.knmi_dayvalues_notification + '<br>' 
    notif += created_by_notification_html + ' '
    notif += ymd.text_datetime_now()
    return notif.lower()

def clear(s):
    '''Remove double whitespaces'''
    s = str(s).strip()
    s = re.sub(r'\t+',' ', s)
    s = re.sub(' +',' ', s)
    return s.strip()

def clean(s):
    s = clear(s)
    s = re.sub(r'\n|\r', ' ', s )
    s = clear(s)        
    return s.strip()  # No whitespace at start and end

def clean_html(s):
    s = clean(s)
    s = re.sub( '>\s*<', '><', s) # Remove whitespace between html tags
    return s.strip()

def sanitize(s):
    s = clear(s)
    s = re.sub(r'(\n)\n+', '\n\n', s)
    return s.strip()

def strip_all(s):
    s = re.sub('\t|\r|\n| |\s', '', s)
    return s.strip()

def separator( cnt=0 ):
    t = ' '
    while cnt > 0:
        t += cfg.ln
        cnt -= 1

    return t

def error(t, err):
    t = f'{t} failed.\nError {err}'
    return t

def succes(t):
    t = f'{t} success.'
    return t

def padding(t, align='center', spaces=35):
    s = (str(t))
    if   align == 'center': s = f'{s:^{spaces}}'
    elif align == 'left':   s = f'{s:<{spaces}}'
    elif align == 'right':  s = f'{s:>{spaces}}'

    return s

def lst_el_maxwidth(l):
    max = 0
    for el in l:
        if len(el) > max:
            max = len(el)
    return max

def query_sign_to_text(query):
    '''Replace wrong chars for use in file name'''
    q = query.replace('>','gt')
    q = q.replace('>=|≥','ge')
    q = q.replace('<','lt')
    q = q.replace('==','eq')
    q = q.replace('ne|!=|<>','not')
    q = q.replace('\|\|','or')
    q = q.replace('&&','and')
    
    return q

def style(t='', style='none'):
    t = t.strip().replace('  ', ' ')
    if   style in ['cap','capitalize']: t = t.capitalize()
    elif style in ['up','upper']: t = t.upper()
    elif style in ['low','lower']: t = t.lower()
    elif style in ['tit', 'title']: t = t.title()

    return t

def file_extension( typ ):
    if   typ in lst_output_htm:   return extension_htm
    elif typ in lst_output_txt:   return extension_txt
    elif typ in lst_output_csv:   return extension_csv 
    elif typ in lst_output_excel: return extension_excel
    else: return typ

def option_lst(npl, sep=',', col_cnt = False, col_spaces = False):
    # Possible update none values
    max_len, max_char = 0, 60
    for e in npl:
        char_len = len(str(e))
        if char_len > max_len:
            max_len = char_len

    # Update the values
    if col_cnt == False: col_cnt = math.floor( max_char / max_len )
    if col_spaces == False or col_spaces < max_len: col_spaces = max_len

    # Make txt list with colls en newlines
    txt, n, max = '', 1, npl.size
    for e in npl:
        txt += f'{e:{col_spaces}}'
        txt += f'{sep} ' if n % col_cnt != 0 and n != max else cfg.ln # comma or newline
        n   += 1

    return txt

def day_ent_lst(sep=',', kol = False, kol_width = False):
    '''Functions prints a list with available entities'''
    l = data.knmi_entities
    for rem in np.array( [ 'FHXH', 'FHNH', 'FXXH', 'TNH', 'TXH', 'T10NH',\
                           'RHXH', 'PXH',  'PNH', 'VVNH', 'VVXH',  'UXH',\
                           'UNH' ] ):
        l = l[l != rem] # Remove time ent

    t = option_lst( l, '', kol, kol_width )
    return t

def txt_main( day ):
    stn, yymmdd, ddvec, fhvec, fg, fhx,\
    fhxh, fhn, fhnh, fxx, fxxh, tg,\
    tn, tnh, tx, txh, t10n, t10nh,\
    sq, sp, q, dr, rh, rhx,\
    rhxh, pg, px, pxh, pn, pnh,\
    vvn, vvnh, vvx, vvxh, ng, ug,\
    ux, uxh, un, unh, ev24 = data.ents( day )

    t, title1, title2, title3, main1, main2, main3 = '', '', '', '', '', '', ''

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

    t += f'{title1}\n{main1}\n'
    t += f'{title2}\n{main2}\n'
    t += f'{title3}\n{main3}\n'

    return f'{t}\n'

def remove_dumb_whitespace( t ):    
    '''Function removes excessive whitespaces from a text string'''
    t = re.sub('\n|\r|\t', '', str(t))
    t = re.sub('\s+', ' ', t)
    return t.strip()

def strip_all_whitespace(t):
    '''Function removes all whitespace from a text string'''
    s = re.sub( '\t|\r|\n| |\s', '', str(t) )
    s = re.sub(r"\s+", "", s, flags=re.UNICODE)
    return s

def cleanup_whitespaces( t ):
    '''Function civilizes long text output with too much enters e.g.'''
    t = re.sub(r'\n+', '\n\n', t)
    t = re.sub('\t+|\s+', ' ', t)
    return t.strip()

def day_ent_lst(sep=',', kol = False, kol_width = False):
    '''Functions prints a list with available entities'''
    l = data.entities
    for rem in np.array( [ 'FHXH', 'FHNH', 'FXXH', 'TNH', 'TXH', 'T10NH',\
                           'RHXH', 'PXH',  'PNH', 'VVNH', 'VVXH',  'UXH',\
                           'UNH' ] ):
        l = l[l != rem] # Remove time ent

    t = option_lst( l, '', kol, kol_width )
    return t

def fix_for_entity( val, entity ):
    '''Function adds correct post/prefixes for weather entities'''
    # No measurement or false measurement
    if not data.check(val):
        return cfg.no_val # Return '.'

    e = entity.strip().lower()
    f = data.process_value(val, e) # Format correct for entity

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
        return f'{f2}-{f1}{"hour"}'

    # Time 6 hours
    elif e in [ 't10nh' ]:
        f1 = f'{f:.0f}'
        f2 = f'{(f-6):.0f}'
        return f'{f2}-{f1}{"hour"}'

    # CLouds cover/octants
    elif e in [ 'ng' ]:
        return f'{f:.0f}'

    # Wind
    elif e in lst_wind:
        bft = convert.ms_to_bft(val)
        return f'{f:.1f}m/s {bft}bft'

    # Evapotranspiration
    elif e in [ 'ev24', 'rh', 'rhx' ]:
        return f'{f:.1f}mm'

    # Duration hours
    elif e in lst_duration:
        return f'{f:.1f}{"hour"}'

    # Wind direction
    elif e in lst_wind_direction:
        if f == 0.0:
            return f'{f:.0f}° {"VAR"}'
        else:
            # From degrees to direction
            # Source: https://www.campbellsci.com/blog/convert-wind-directions
            ldir = [ 'N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S',
                     'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW', 'N' ]
            ndx = int( round( f % 360 / 22.5 ) )
            dir = ldir[ndx]
            return f'{f:.0f}° {dir}'

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

def ent_to_txt(entity):
    e = entity.lower()
    if   e == 'tx':    return 'maximum temperature'
    elif e == 'tg':    return 'mean temperature'
    elif e == 'tn':    return 'minimum temperature'
    elif e == 't10n':  return 'minimum temperature (10cm)'
    elif e == 'ddvec': return 'wind direction'
    elif e == 'fg':    return 'mean windspeed (daily)'
    elif e == 'rh':    return 'precipitation amount'
    elif e == 'sq':    return 'sunshine duration (hourly)'
    elif e == 'pg':    return 'mean pressure'
    elif e == 'ug':    return 'mean atmospheric humidity'
    elif e == 'fxx':   return 'maximum wind (gust)'
    elif e == 'fhvec': return 'mean windspeed (vector)'
    elif e == 'fhx':   return 'maximum mean windspeed (hourly)'
    elif e == 'fhn':   return 'minimum mean windspeed (hourly)'
    elif e == 'sp':    return 'sunshine duration (maximum potential)'
    elif e == 'q':     return 'radiation (global)'
    elif e == 'dr':    return 'precipitation duration'
    elif e == 'rhx':   return 'maximum precipitation (hourly)'
    elif e == 'px':    return 'maximum pressure (hourly)'
    elif e == 'pn':    return 'minimum pressure (hourly)'
    elif e == 'vvn':   return 'minimum visibility'
    elif e == 'vvx':   return 'maximum visibility'
    elif e == 'ng':    return 'mean cloud cover'
    elif e == 'ux':    return 'maximum humidity'
    elif e == 'un':    return 'minimum humidity'
    elif e == 'ev24':  return 'evapotranspiration (potential)'
    return e

def now_created_notification():
    ds = utils.loc_date_now().strftime('%A, %d %B %Y %H:%M')
    return cfg.created_by_notification % ds

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

lst_wmo = lambda: [el.wmo for el in stations.lst]
lst_name = lambda: [el.place for el in stations.lst]
lst_wmo_name = lambda: [ f'{el[0]} {el[1]}' for el in zip( lst_wmo(), lst_name() ) ]

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

def climate(t=''): 
    return f'climate {t}'

def max(entity): 
    return f'highest {ent_to_txt(entity)}'

def min(entity):
    return f'lowest {ent_to_txt(entity)}'

def ave(entity):
    return f'average {ent_to_txt(entity)}'

def sum(entity):
    return f'sum {ent_to_txt(entity)}'
    
def hellmann():
    return f'hellmann'

def ijnsen():
    return 'ijnsen'

def frostsum():
    return 'frost_sum'

def heat_ndx():
    return 'heat_ndx'

def climate(t=''):
    return f'climate {t}'

def title(entity, sign, val):
    return f'{ent_to_txt(entity)} {sign} {val}'

def title_mean(t=''):
    return f'title mean {t}'


def info_line(txt, options, station):
    t  = f'[{ymd.now()}] {txt} <{options[ask_title]}> '
    t += f'for {station.wmo} {station.place} '
    t += f'in period <{options[ask_period_1]}> '
    t += f'with sub-period <{options[ask_period_2]}>' if options[ask_period_2] else cfg.e
    return t


lst_goodbye_txt = [
'Goodbye!',
'Goodbye my friend! Take good care of yourself!',
'Goodbye! Make me proud!',
'All good things come to an end. Goodbye and farewell!',
"You're one of the best people I've ever met. Best of luck for new life and farewell!",
"Saying goodbye isn't easy, but don't let anything hold you back. You have beautiful days ahead. Farewell, see you soon!",
"It was an honor working under your guidance. My heart is sad to see you go. Farewell to you.", 
"May this goodbye be the beginning of your beautiful life ahead. Stay blessed and keep growing.",
"Saying goodbye is sometimes a part of life. But our memories will always speak for our true friendship wherever we go. Farewell, my friend! Hope to meet again soon.",
"I wish you all the best because that is exactly what you deserve! Goodbye! We will meet again soon. Take care of yourself.",
"Farewell dear. It doesn't matter if you're with us or not, your work will always inspire each and every person. Wish you all the best!",
"No matter where you go, you will always be connected in our hearts. My heartiest good wishes will be with you always. Farewell dear friend!",
"It's tough to say goodbye to you. Your memories will keep you alive. Farewell!"
]