# -*- coding: utf-8 -*-
'''Library contains the menu options'''
__author__     = 'Mark Zwaving'
__email__      = 'markzwaving@gmail.com'
__copyright__  = 'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    = '0.0.8' 
__maintainer__ = 'Mark Zwaving'
__status__     = 'Development'

import defaults
import sources.control.menu as ctrl_menu 

lst_downloads = [ 
    'DOWNLOAD', 
    [ 
        [ 'OK Download all dayvalues knmi stations',      ctrl_menu.download_knmi_dayvalues_all ],
        [ 'OK Download selected dayvalues knmi stations', ctrl_menu.download_knmi_dayvalues_select ],
    ]   
]

lst_animations = [ 
    'ANIMATIONS', 
    [ 
        [ 'OK Download only images or files', ctrl_menu.interval_download_files ],
        [ 'OK Download and make an animation', ctrl_menu.download_animation ],
    ] 
]

lst_divers_statistics = [ 
    'STATISTICS TABLES', 
    [  
        [ 'OK DIY statistics', ctrl_menu.table_stats_diy ],
        [ 'TODO Day, month, year or period in a period', ctrl_menu.todo],
        [ 'TODO Compare two periods day, month, year and season',  ctrl_menu.todo ],
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
        [ 'OK Make day(s) dayvalues', ctrl_menu.make_days_dayvalues ],
        [ 'OK See day(s) dayvalues', ctrl_menu.see_days_dayvalues ],
        [ 'TODO Search for day(s)', ctrl_menu.search_for_days_dayvalues ],
    ] 
]

lst_graphs = [ 
    'GRAPHS', 
    [ 
        [ 'TODO DIY period',  ctrl_menu.graph_period ],
    ] 
]

# TODO DAYVALUES
lst_databases = [ 
    'DATABASE SQLITE', 
    [ 
        [ 'TODO Create/(Re)new (sqlite) Database',      ctrl_menu.database_create_renew ],
        [ 'TODO Update (sqlite) Database',              ctrl_menu.database_create_renew ],
        [ 'TODO Execute a (sqlite) Query',              ctrl_menu.database_query ],
        [ 'TODO Delete the (sqlite) Database',          ctrl_menu.database_create_renew ],
        [ 'TODO Create Database extern (mysql) Server', ctrl_menu.database_create_renew ],
        [ 'TODO Update Database extern (mysql) Server', ctrl_menu.database_create_renew ],
    ] 
]

lst_current_weather = [ 
    'WEATHER (dutch)', 
    [ 
        [ 'OK Buienradar Forecast',  ctrl_menu.weather_buienradar_forecast ],
        [ 'OK Buienradar Stations NL', ctrl_menu.weather_buienradar_stations ],

    # Jammer, ftp pub knmi opgeheven
    # [ 'KNMI Forecast weather',              menu_knmi_forecast          ],
    # [ 'KNMI Forecast guidance short term',  menu_knmi_forecast_guidance ],
    # [ 'KNMI Forecast model long term',      menu_knmi_forecast_model    ],
    # [ 'KNMI Stations NL',                   menu_knmi_act_values        ],
    ] 
]
