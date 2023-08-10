# -*- coding: utf-8 -*-
'''Library contains functions for writing output to screen or to a file'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 3 - GPLv3'
__version__    =  '0.1.9'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg, stations
import numpy as np, math, time, re, shutil 
import sources.model.daydata as daydata
import sources.model.utils as utils
import sources.model.weather_stations as weather_stations
import sources.model.convert as convert

cli_colls, cli_rows = shutil.get_terminal_size()

def A0(d): return f'0{d}' if int(d) < 10 else str(d) # Add zero < 10
def line(s): return str(s) * (shutil.get_terminal_size()[0] - 1)
def line_hashtag(): return line('#')
def line_hyphen(): return line('-')
def head(t='Header'): return f'{line_hashtag()}\n##  {t}\n{line_hashtag()}'
def foot(t='Footer'): return f'{line_hashtag()}\n##  {t}\n{line_hashtag()}\n'

def lines_spacer( cnt=1 ):
    '''Function print enters to the screen'''
    t = ''
    while cnt >= 0: 
        t += '\n'; cnt -= 1
    return t

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

type_in = 'Type in something...'
next_n  = "Press 'n' to move to the next..."
next_press_enter = "Press <enter> to move to the next..."
back_main = "Press a 'key' to go back to the main menu..."

# Answers option lists
lst_quit = ['q','quit','stop','ho', 'x','X','exit','get out']
lst_yess = ['y','yes','yess','j','ja','ok','oke','oké','yee','jee', 'yep', 'yup', 'oui']
lst_no   = ['n','no','nope','not','nee','nada','nein','non','neet','njet','neen']
lst_prev = ['p', 'last', 'prev', 'previous']
lst_back = ['b', 'back', 'return']

# Quick txt lists
lst_m = ['1','2','3','4','5','6','7','8','9','10','11','12']
lst_mm = ['01','02','03','04','05','06','07','08','09','10','11','12']
lst_mmm = ['jan','feb','mar','apr','mai','jun','jul','aug','sep','okt','nov','dec']
lst_mmmm = ['january','februari','march','april','mai','june','july',
            'august','september','oktober','november','december']
lst_months_all = lst_m + lst_mm + lst_mmm + lst_mmmm

dd_01, dd_02, dd_03, dd_04, dd_05, dd_06 = 31, 29, 31, 30, 31, 30
dd_07, dd_08, dd_09, dd_10, dd_11, dd_12 = 31, 31, 30, 31, 30, 31
lst_dd = [ dd_01, dd_02, dd_03, dd_04, dd_05, dd_06,
           dd_07, dd_08, dd_09, dd_10, dd_11, dd_12 ]

lst_dd_01 = [ f'01{A0(d)}' for d in range(1,dd_01+1) ]
lst_dd_02 = [ f'02{A0(d)}' for d in range(1,dd_02+1) ]
lst_dd_03 = [ f'03{A0(d)}' for d in range(1,dd_03+1) ]
lst_dd_04 = [ f'04{A0(d)}' for d in range(1,dd_04+1) ]
lst_dd_05 = [ f'05{A0(d)}' for d in range(1,dd_05+1) ]
lst_dd_06 = [ f'06{A0(d)}' for d in range(1,dd_06+1) ]
lst_dd_07 = [ f'07{A0(d)}' for d in range(1,dd_07+1) ]
lst_dd_08 = [ f'08{A0(d)}' for d in range(1,dd_08+1) ]
lst_dd_09 = [ f'09{A0(d)}' for d in range(1,dd_09+1) ]
lst_dd_10 = [ f'10{A0(d)}' for d in range(1,dd_10+1) ]
lst_dd_11 = [ f'11{A0(d)}' for d in range(1,dd_11+1) ]
lst_dd_12 = [ f'12{A0(d)}' for d in range(1,dd_12+1) ]

# lst_mmdd = [ str( f'{A0(i+1)}{A0(d)}' for d in range(1, dd + 1) ) for i, dd in enumerate(lst_dd) ]
lst_mmdd  = lst_dd_01 + lst_dd_02 + lst_dd_03 + lst_dd_04 + lst_dd_05 + lst_dd_06
lst_mmdd += lst_dd_07 + lst_dd_08 + lst_dd_09 + lst_dd_10 + lst_dd_11 + lst_dd_12

# File extensions
extension_htm = '.html'
extension_txt = '.txt'
extension_csv = '.csv'
extension_excel = '.xlsx'

# Output options
lst_output_options = ['X console TODO', 'X text file TODO', 'html', 'X csv TODO', 'X excel TODO', 'X all types TODO']
lst_output_cnsl = ['cmd', 'console', 'command', 'command line', 'console only']
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
lst_output_files = lst_output_txt + lst_output_htm + lst_output_csv_excel + lst_output_img
lst_output_all = lst_output_cnsl + lst_output_files

# MENU 
title_menu_diy_stats = 'DIY cells statistics'
title_menu_winter_stats = 'Winter statistics'
title_menu_summer_stats = 'Summer statistics' 
title_menu_winter_summer_stats = 'Winter & summer statistics'
title_menu_default_extremes = 'Default extremes (see config.py)'
title_menu_default_counts = 'Default counts (see config.py)'

menu_knmi_dayvalues_all        = 'knmi_dayvalues_all'
menu_knmi_dayvalues_select     = 'knmi_dayvalues_select'
menu_anim_download_images      = 'download_images'
menu_anim_download_animation   = 'download_animation'
menu_anim_images_fom_map       = 'animation_from_images_from_dir'

menu_buienradar_forecast       = 'weather_buienradar_forecast'
menu_buienradar_act_values     = 'weather_buienradar_current'
menu_knmi_forecast             = 'weather_knmi_forecast'
menu_knmi_forecast_model       = 'weather_knmi_model'
menu_knmi_forecast_guidance    = 'weather_knmi_guidance'
menu_knmi_act_values           = 'weather_knmi_current'

menu_table_stats_diy           = 'table_stats_diy'
menu_table_stats_winter        = 'table_stats_winter'
menu_table_stats_summer        = 'table_stats_summer'
menu_table_stats_winter_summer = 'table_stats_winter_summer'
menu_table_stats_extremes      = 'table_stats_extremes'
menu_table_stats_counts        = 'table_stats_counts'
menu_table_stats_default_1     = 'table_stats_default_1'
menu_table_stats_id_1          = 'table_stats_ID-1'

menu_table_stats_per2_in_per1  = 'table_stats_per2_in_per1'
menu_table_stats_compare       = 'table_stats_compare'

menu_make_dayvalues            = 'make_dayvalues'
menu_see_dayvalues             = 'see_dayvalues'
menu_search_for_days           = 'search_for_days'

menu_graph_period              = 'graph_period'

lst_menu_download = [ 'DOWNLOAD', [ 
    [ 'Download all dayvalues knmi stations',        menu_knmi_dayvalues_all        ],
    [ 'Download selected dayvalues knmi stations',   menu_knmi_dayvalues_select     ],
] ]

lst_menu_animation = [ 'DOWNLOAD IMAGES AND MAKE ANIMATIONS', [ 
    [ 'Download (weather) images only',              menu_anim_download_images      ],
    [ 'Download and make an animation',              menu_anim_download_animation   ],
    # [ 'Make an animation from images in a map', menu_anim_images_fom_map ]
] ]

lst_menu_statistics = [ 'STATISTICS TABLES', [  
    [ 'DIY cells statistics',                        menu_table_stats_diy           ],
    [ 'Winter statistics',                           menu_table_stats_winter        ],
    [ 'Summer statistics',                           menu_table_stats_summer        ],
    [ 'Winter & summer statistics',                  menu_table_stats_winter_summer ],
    [ 'Default statistics (see config.py)',          menu_table_stats_default_1     ],
    [ 'Default extremes (see config.py)',            menu_table_stats_extremes      ],
    [ 'Default counts (see config.py)',              menu_table_stats_extremes      ],
    [ 'Day, month & period statistics in a period',  menu_table_stats_per2_in_per1  ],
    [ 'Compare (day, month, year and season)',       menu_table_stats_compare       ],

    ####################################################################################
    ## Do you want to add more default lists with statistics in the menu ? 

    # See -> control > menu.py for the functions
    #     fn: select_menu_option(option)    # Broker between menu and python functions
    #     fn: table_stats_id_1()            # Function for your statistics list 

    # For an example list with statistics
    # see -> config.py -> lst_cells_id_1 = [... ...]
    # You can update the list with your own statistics cells

    # ID-1 is the connection ID between the text menu and the python function 
    
    # Uncomment next row, to let it show up in the menu
    # [ 'My stats ID-1 (see config.py)',   menu_table_stats_id_1 ], 
    ####################################################################################
] ]

lst_menu_days = [ 'DAYVALUES', [ 
    [ 'Make dayvalues',                     menu_make_dayvalues         ],
    [ 'See dayvalues',                      menu_see_dayvalues          ],
    [ 'Search for days',                    menu_search_for_days        ],
] ]

lst_menu_graphs = [ 'GRAPHS', [ 
    [ 'DIY period',                         menu_graph_period           ],
] ]

lst_menu_weather = [ 'WEATHER (dutch)', [ 
    [ 'Buienradar Forecast',                menu_buienradar_forecast    ],
    [ 'Buienradar Stations NL',             menu_buienradar_act_values  ],
    [ 'KNMI Forecast weather',              menu_knmi_forecast          ],
    [ 'KNMI Forecast guidance short term',  menu_knmi_forecast_guidance ],
    [ 'KNMI Forecast model long term',      menu_knmi_forecast_model    ],
    [ 'KNMI Stations NL',                   menu_knmi_act_values        ],
] ]

# TODO
lst_menu_database = [ 'DATABASES SQLITE TODO', [ 
    [ 'Update database', 'process_database_update' ],
    [ 'Input Query', 'process_database_query'      ],
    [ 'Delete database', 'process_delete_database' ],
] ]

# Ask options
ask_title          = 'title'
ask_colspan        = 'colspan'
ask_other_menu     = 'other-menu'
ask_start_date     = 'start-datetime'
ask_end_date       = 'end-datetime'
ask_period         = 'period'
ask_per1           = ask_period
ask_per2           = 'periode-2'
ask_per_compare    = 'period-cmp'
ask_file_type      = 'file-type'
ask_filename       = 'file-name'
ask_download       = 'download'
ask_download_url   = 'image-download-url'
ask_download_interval = 'interval-download'
ask_animation_name = 'animation-name'
ask_animation_time = 'animation-time' 
ask_rm_downloads   = 'remove-downloads' 
ask_gif_compress   = 'gif-compress'
ask_stations       = 'lst-stations'
ask_select_cells   = 'lst-sel-cells'
ask_diy_cells      = 'lst-diy-cells'
ask_write_dayval   = 'write-dayvalues'
ask_s4d_query      = 's4d-query'
ask_clima_period   = 'clima-period'
ask_verbose        = 'verbose'
ask_graph_title    = 'graph-title'
ask_graph_ylabel   = 'graph-y-label'
ask_graph_default  = 'graph-default'
ask_graph_width    = 'graph-width'
ask_graph_height   = 'graph-height'
ask_graph_cummul_val = 'graph-cummul-val'
ask_graph_type     = 'graph-type'
ask_graph_dpi      = 'graph-dpi'
ask_graph_entities = 'graph-lst-entities-types'

# Questions to ask
lst_ask_stats           = [ask_stations, ask_period, ask_file_type, ask_filename]
lst_ask_stats_diy       = [ask_stations, ask_period, ask_select_cells, ask_file_type, ask_filename]
lst_ask_stats_p1_p2_diy = [ask_stations, ask_per1, ask_per2, ask_select_cells, ask_file_type, ask_filename]
lst_ask_stats_compare   = [ask_stations, ask_period, ask_per_compare, ask_select_cells, ask_file_type, ask_filename]
lst_ask_download        = [ask_download_url, ask_start_date, ask_end_date, ask_download_interval]
lst_ask_animation       = [ask_animation_name, ask_animation_time, ask_rm_downloads, ask_gif_compress]
lst_ask_make_dayval     = [ask_stations, ask_period, ask_file_type, ask_write_dayval]
lst_ask_see_dayval      = [ask_stations, ask_period, ask_file_type, ask_write_dayval]
lst_ask_search_4_day    = [ask_stations, ask_period, ask_s4d_query, ask_file_type, ask_filename]

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

menu_image_download_examples = '''
DOWNLOAD IMAGES EXAMPLES
# KNMI
https://cdn.knmi.nl/knmi/map/page/weer/actueel-weer/windkracht.png 
https://cdn.knmi.nl/knmi/map/page/weer/actueel-weer/windsnelheid.png 
https://cdn.knmi.nl/knmi/map/page/weer/actueel-weer/maxwindkm.png 
https://cdn.knmi.nl/knmi/map/page/weer/actueel-weer/temperatuur.png 
https://cdn.knmi.nl/knmi/map/page/weer/actueel-weer/relvocht.png 
https://cdn.knmi.nl/knmi/map/page/weer/actueel-weer/zicht.png 
# Weerplaza 
https://oud.weerplaza.nl/gdata/10min/GMT_T10C_latest.png'  # Temp 10cm
https://oud.weerplaza.nl/gdata/10min/nl_10min.jpg'         # Weather
https://oud.weerplaza.nl/gdata/10min/GMT_TTTT_latest.png'  # Temp 2 meter
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
{lst_to_col(lst_mmdd, 'left', 15)}
'''

menu_info_select_a_month = f'''
MONTH INFO
{lst_to_col(lst_months_all, 'left', 6)}
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
TABLE CELLS INFO

INFO format: inf_option
inf_place, inf_province, inf_country, inf_period, inf_num, inf_period-2

STATISTICS format: [ave|sum]_entity
ave_tg, sum_sq, sum_rh

EXTREMES format: [max|min]_entity
max_tx, min_tn, min_t10n, max_rh, max_sq, max_rhx, max_px, min_px, min_pn, max_ux, max_ug, min_un

INDEXES format: ndx_name
ndx_hellmann, ndx_frost-sum, ndx_heat-ndx, ndx_ijnsen

COUNT format: cnt_entity_operator_value
cnt_tx_ge_25, cnt_tx_ge_30, cnt_tg_>=_20, cnt_sq_ge_10, cnt_rh_ge_10, cnt_tx_<_0, cnt_tn_lt_-5, cnt_tn_lt_-20 

CLIMA format: clima_option_entity
clima_ave_tg, clima_sum_sq, clima_sum_rh

Example winter:
inf_place, inf_period, ave_tg, clima_ave_tg, min_tx, min_tn, ndx_hellmann, ndx_frost-sum, sum_rh, 
clima_sum_rh, cnt_rh_ge_10, cnt_tx_<_0, cnt_tg_<_0, cnt_tn_<_0, cnt_tn_<_0, cnt_tn_<_-5, cnt_tn_<_-10

Example spring:
inf_place, inf_province, inf_period, ave_tg, clima_ave_tg, ndx_heat, max_tx, min_tx, min_tn, sum_sq, clima_sum_sq, 
cnt_sq_ge_8, sum_rh, clima_sum_rh, cnt_rh_ge_10, cnt_tx_>=_20, cnt_tx_>=_25, cnt_tn_<_0

Example summer:
inf_place, inf_period, ave_tg, clima_ave_tg, max_tx, max_tn, ndx_heat, sum_sq, clima_sum_sq, cnt_sq_ge_10, 
sum_rh, clima_sum_rh, cnt_rh_ge_10, cnt_tx_>=_25, cnt_tx_>=_30, cnt_tx_>=_30, cnt_tn_>=_20
'''

quick_calc_inf = '''
CALCULATION INFO
Default format: ENT(STATISTIC)
Options ENT: TX, RH, SQ, TN et cetera
Options STATISTIC: MIN -, MAX +, mean ~, SUM Σ, hellmann hmann, frostsum fsum, ijnsen, heatndx hndx
EXAMPLES:
TX+ (=maximum temperature TX)  TG~ (=average temperature TG)  TN- (=minimum temperature TN)
RHΣ (=total rain sum)          RH+ (=maximum rain in a day)   HELLMANN (=hellmann winter score)
FSUM (=frostsum winter score)  IJNSEN (=ijnsen winter score)  HNDX (=sum heat index score)
'''

period_inf = '''
PERIOD INFO
Format yyyymmdd-yyyymmdd     ie. 20200510-20200520 
Examples with a wild card * (--- in development ---)
  ********            selects all the available data (=8x*)
  ****                selects (current) year (=4x*)
  **                  selects (current) month (=2x*)
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

ent_inf = '''
ENTITIES INFO\n'
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

query_inf = '''
QUERY INFO
' gt', '> '         = greater than             ie. TG >  20  Warm nights
' ge', '>=', ' ≥'   = greater than and equal   ie. TX >= 30  Tropical days
' lt', '< '         = less than                ie. TN <   0  Frosty days
' le', '<=', ' ≤'   = less than equal          ie. TX <=  0  Icy days
' eq', '=='         = equal                    ie. DDVEC == 90  A day with a wind from the east
' ne', '!=', '<>'   = not equal                ie. RH !=  0  A day with rain
' or', '||'  'or '  ie SQ > 10  or TX >= 25    Sunny and warm days
'and', '&&'  'and'  ie RH > 10 and TX <  0     Most propably a day with snow
'''

menu_info_stations =  f'''
STATIONS INFO
{lst_to_col([f'{s.wmo} {s.place}' for s in weather_stations.lst_stations_map()], 'left', 4)}
'''

quick_stats_all_inf = period_inf + '\n\n' + menu_info_stations + '\n\n' + ent_inf + '\n\n' + quick_calc_inf + '\n'

menu_allAvailable_info = f'''
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
lst_home = ['home', 'place'] 
lst_states = ['province', 'country'] 
lst_geo_places = lst_states + lst_home
lst_period_1 = ['period', 'periode', 'period1', 'period-1']
lst_period_2 = ['period2', 'period-2', 'periode-2']
lst_temp = ['temperature', 'temp', 'tx', 'tg', 'tn', 't10n']
lst_heat_ndx = ['heatindex', 'heat-index', 'heat-ndx', 'heatndx', 'hndx', 'heat'] 
lst_helmmann = ['hmann', 'hellmann', 'hellman']
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
lst_season = ['season']

# Padding text values for text output
pad_default = 10
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
pad_cnt = 10
pad_day = 10
pad_max = 10 + 12
pad_min = 10 + 12
pad_extreme = 10 + 12
pad_home = 15
pad_states = 15
pad_place = 15
pad_province = 15
pad_country = 15
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
pad_clima = 10 
pad_view = 4 
pad_evaporation = 4 

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

def month_num_to_name( m, lang='en' ):
    lst, key = [], 0
    if lang == 'en': key = 0
    if lang == 'nl': key = 1

    if    m in ['01','1', 1]: lst = ['january','januari']
    elif  m in ['02','2', 2]: lst = ['february','februari']
    elif  m in ['03','3', 3]: lst = ['march','maart']
    elif  m in ['04','4', 4]: lst = ['april','april']
    elif  m in ['05','5', 5]: lst = ['mai','mei']
    elif  m in ['06','6', 6]: lst = ['june','juni']
    elif  m in ['07','7', 7]: lst = ['july','juli']
    elif  m in ['08','8', 8]: lst = ['august','augustus']
    elif  m in ['09','9', 9]: lst = ['september','september']
    elif  m in ['10', 10]:    lst = ['october','october']
    elif  m in ['11', 11]:    lst = ['nobemver','november']
    elif  m in ['12', 12]:    lst = ['december','december']

    return  lst[key]

def month_num_to_mmmm( n ):
    return lst_mmmm[int(n)-1]

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

def month_name_to_num ( name ):
    ndx = 0
    for mmm, mmmm in zip(lst_mmm, lst_mmmm):
        if name in [mmm,mmmm]:
            return ndx
        ndx += 1
    else:
        return -1 # Name not found

def m_to_mmmm ( m ):
    return lst_mmmm[int(m)-1] if str(m) in lst_m else -1

def m_to_mmm ( m ):
    return lst_mmm[ int(m)-1] if str(m) in lst_m else -1

def mm_to_mmmm( mm ): 
    return lst_mmmm[int(mm)-1] if mm in lst_mm else -1

def mm_to_mmm( mm ): 
    return lst_mmm[ int(mm)-1] if mm in lst_mm else -1

def mmm_to_m( mmm ): 
    return str(month_name_to_num(mmm))

def mmm_to_mm( mmm ): 
    return f'{month_name_to_num(mmm):0>2}'

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
    '''Replce wrong chars for use in file name'''
    q = query.replace('>','gt')
    q = q.replace('>=|≥','ge')
    q = q.replace('<','lt')
    q = q.replace('==','eq')
    q = q.replace('ne|!=|<>','not')
    q = q.replace('\|\|','or')
    q = q.replace('&&','and')
    
    return q

def style(t='', style='none'):
    t = tr( t.strip().replace('  ', ' '))
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
    l = daydata.knmi_entities
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

def process_time_ext(t='', delta_ns=0):
    '''Function gives a time string from nano seconds till days'''
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
    if dag > 0: t += str(dag) + ( ' days '    if dag > 1 else ' day ' )
    if uur > 0: t += str(uur) + ( ' hours '   if uur > 1 else ' hour ' )
    if min > 0: t += str(min) + ( ' minutes ' if min > 1 else ' minute ' )

    smile = utils.add_zero_less_1000(mill)
    if sec > 0:
        t += f'{sec}.{smile} ' + ( ' second ' if sec == 1 else ' seconds ' )
    else:
        t += f'0.{smile} second '

    # if micr > 0: txt += f'{micr} {"microseconds" if micr>1 else "microsecond"} '
    # if nano > 0: txt += f'{nano} {"nanoseconds" if nano>1 else "nanosecond"} '

    return t

def process_time(t='', st=time.time_ns()):
    delta = time.time_ns() - st
    t = process_time_ext(t, delta)
    return t

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

def day_ent_lst(sep=',', kol = False, kol_width = False):
    '''Functions prints a list with available entities'''
    l = daydata.entities
    for rem in np.array( [ 'FHXH', 'FHNH', 'FXXH', 'TNH', 'TXH', 'T10NH',\
                           'RHXH', 'PXH',  'PNH', 'VVNH', 'VVXH',  'UXH',\
                           'UNH' ] ):
        l = l[l != rem] # Remove time ent

    t = option_lst( l, '', kol, kol_width )
    return t

def fix_ent( val, entity ):
    '''Function adds correct post/prefixes for weather entities'''
    # No measurement or false measurement
    if not daydata.check(val):
        return cfg.no_val # Return '.'

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
        bft = convert.ms_to_bft(val)
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

def ent_to_txt(entity):
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

enter_default  = lambda default: f'Press <enter> for default (={default})...'
enter_back_to  = lambda t: f"Press 'b' to go back to the {t} menu... "
type_more_info = lambda i: f"Type '{i}' for more info..."

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

# TXT strings
enter_default = lambda default: f'Press <enter> for default (={default})...'
enter_back = lambda t: f"Press 'b' to go back to the {t} menu... "
enter_previous = lambda s='':f"Press 'p' to go to the previous question..."
enter_exit = "Press 'x' to exit the program..."
type_more_info = lambda i: f"Type '{i}' for more info..."

error  = lambda t, err: f'{t} failed.\nError {err}'
succes = lambda t: f'{t} success.'

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

##########################################################################################
# TRANSLATIONS 
# TODO 
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
