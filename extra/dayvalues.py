# -*- coding: utf-8 -*-
'''Library contains functions for auto downloading files and updating the day values.'''
__author__ = 'Mark Zwaving'
__email__ = 'markzwaving@gmail.com'
__copyright__ = 'Copyright (C) Mark Zwaving. All rights reserved.'
__license__ = 'GNU Lesser General Public License (LGPL)'
__version__ = '0.0.8'
__maintainer__ = 'Mark Zwaving'
__status__ = 'Development'

# To get access to all the code from weathersstats,
# add the root map from weatherstats to sys.path.
import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))

# Import weatherstats libraries
import config as cfg, datetime
import sources.model.stations as stations 
import sources.view.dayvalues as dayvalues 
import sources.model.ymd as ymd 

if __name__ == '__main__':
    verbose = cfg.verbose = False                                 # See all the files made or checked
    yyyy, mm, dd, HH, MM, SS = ymd.y_m_d_h_m_s_now()   # Get current date time
    init     = False                                    # First time init all data. (Re-)write all
    ed_ymd   = f'{yyyy}{mm}{dd}'                       # End date is today
    st_ymd   = ymd.yyyymmdd_minus_day(ed_ymd, 100)     # Start date is X=100 days back, only last 100 days
    period   = f'{st_ymd}-{ed_ymd}'                    # Default period
    day_of_week = datetime.datetime.today().weekday()  # Monday is 0 and Sunday is 6
    update   = 'add'                                   # Default update is add onle
    download = True                                    # Default download

    # Stations list to update
    lst_stations = [
        stations.wmo_to_station('260'),
        stations.wmo_to_station('280'),
        stations.wmo_to_station('235'),
        stations.wmo_to_station('310'),
        stations.wmo_to_station('380')
    ]

    # Update options for updating data and period
    if init:                     # Init all data
        update = 'rewrite'       # (Re-)write files
        period = '*'             # All time
    else:
        if int(HH) >= 12:        # Second/third day check
            pass                 # Only add and download always
        elif dd == '01':         # First day of month
            update = 'rewrite'   # (Re-)write all 
            period = '*'         # All data
        elif day_of_week == 6:   # Sunday
            update = 'rewrite'   # Rewrite last X days

    # Option list to make dayvalues
    options = {
        'init': init,                   # First time True or False
        'title': 'dayvalues',           # Title for verbose options
        'lst-stations': lst_stations,   # Selected stations
        'period': period,               # Period to make dayvalues, default is only last 100 days
        'file-type': 'html',            # Output type file
        'write-dayvalues': update,                # Rewrite 'rewrite' all or just just 'add'
        'lst-sel-cells': cfg.lst_cells_dayvalues,  # Entities for the day. Use all.
        'download': download,           # Download data first
    }

    dayvalues.calculate(options, verbose) # Make vayvalues
