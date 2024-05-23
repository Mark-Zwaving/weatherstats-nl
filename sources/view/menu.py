# -*- coding: utf-8 -*-
'''Library contains the menu options'''
__author__     = 'Mark Zwaving'
__email__      = 'markzwaving@gmail.com'
__copyright__  = 'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    = '0.0.9' 
__maintainer__ = 'Mark Zwaving'
__status__     = 'Development'

import config as cfg
import defaults
import sources.control.menu as ctrl_menu 

lst_downloads = [ 
    'DOWNLOAD', 
    [ 
        [ 'Download all dayvalues knmi stations',      ctrl_menu.download_knmi_dayvalues_all ],
        [ 'Download selected dayvalues knmi stations', ctrl_menu.download_knmi_dayvalues_select ],
    ]   
]

lst_animations = [ 
    'ANIMATIONS', 
    [ 
        [ 'Download only images or files', ctrl_menu.interval_download_files ],
        [ 'Download images and make an animation', ctrl_menu.download_animation ],
    ] 
]

lst_divers_statistics = [ 
    'STATISTICS TABLES', 
    [  
        [ 'DIY statistics', ctrl_menu.table_stats_diy ],
        [ 'Two period statistics (more options) <BETA>', ctrl_menu.table_stats_period_in_period],
        [ 'Compare statistics <BETA>',  ctrl_menu.table_stats_period_compare ],
    ] 
]

# See defaults.py
lst_default_statistics = [ 
    defaults.title_statistics,  
    defaults.lst_menu 
]

lst_dayvalues = [ 
    'DAYVALUES', 
    [ 
        [ 'Make day(s) dayvalues', ctrl_menu.make_days_dayvalues ],
        [ 'See day(s) dayvalues', ctrl_menu.see_days_dayvalues ],
        # [ 'TODO Search for day(s)', ctrl_menu.search_for_days_dayvalues ],
    ] 
]

lst_graphs = [ 
    'GRAPHS', 
    [ 
        [ 'Dayvalues and statistics', ctrl_menu.graph_period ],
    ] 
]

# TODO DAYVALUES
lst_databases = [ 
    'DATABASE SQLITE', 
    [ 
        [ 'TODO Create/(Re)new (sqlite) Database',      ctrl_menu.database_create_renew ],
        [ 'TODO Update (sqlite) Database',              ctrl_menu.database_create_renew ],
        [ 'TODO Execute a (sqlite) Query',              ctrl_menu.database_query        ],
        [ 'TODO Delete the (sqlite) Database',          ctrl_menu.database_create_renew ],
        [ 'TODO Create Database extern (mysql) Server', ctrl_menu.database_create_renew ],
        [ 'TODO Update Database extern (mysql) Server', ctrl_menu.database_create_renew ],
    ] 
]

lst_current_weather = [ 
    'WEATHER (dutch)', 
    [ 
        [ 'Buienradar Forecast',    ctrl_menu.weather_buienradar_forecast ],
        [ 'Buienradar Stations NL', ctrl_menu.weather_buienradar_stations ],
    ] 
]

# Is a knmi Api key activated than add knmi options
if cfg.knmi_api_key:
    lst_current_weather[1].append( ['KNMI Forecast weather', ctrl_menu.weather_knmi_forecast] )
    lst_current_weather[1].append( ['KNMI Stations NL', ctrl_menu.weather_knmi_stations])
