# -*- coding: utf-8 -*-
'''WeatherStatsNL calculates weather statistics for dutch cities with data from the knmi'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 3 - GPLv3'
__version__    =  '0.1.5'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import sys
import config as cfg

# Add dir (from this) app to system path, if not already there.
if cfg.dir_app not in sys.path: 
    sys.path.append(cfg.dir_app)

# Import libraries
import sources.control.menu as menu
import sources.view.console as cnsl
import stations

# Main programm
if __name__== '__main__':
    cnsl.log('\nWelcome to WeatherStatsNL', True)
    
    if len(stations.lst) == 0:
        menu.error_no_stations_found()
    else:
        menu.main_menu()

    cnsl.log('\nGood bye !', True )
    exit(0)
