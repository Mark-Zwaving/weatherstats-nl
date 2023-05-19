# -*- coding: utf-8 -*-
'''Library contains functions for auto downloading files and updating the day values.'''
__author__ = 'Mark Zwaving'
__email__ = 'markzwaving@gmail.com'
__copyright__ = 'Copyright (C) Mark Zwaving. All rights reserved.'
__license__ = 'GNU Lesser General Public License (LGPL)'
__version__ = '0.0.6'
__maintainer__ = 'Mark Zwaving'
__status__ = 'Development'

# To get access to all the code from weathersstats,
# add the root map from weatherstats to sys.path.
import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))

# Import weatherstats libraries
import config as cfg, datetime
import sources.model.weather_stations as weather_stations 
import sources.model.dayvalues as dayvalues 
import sources.model.ymd as ymd 

cfg.verbose = True # See all the files made or checked

# Stations list to update
lst_stations = [
    weather_stations.wmo_to_station('260'),
    weather_stations.wmo_to_station('280'),
    weather_stations.wmo_to_station('235'),
    weather_stations.wmo_to_station('310'),
    weather_stations.wmo_to_station('380')
]

# Option list to make dayvalues
options = {
    'title': 'dayvalues',          # Title for verbose options
    'lst-stations': lst_stations,  # Selected stations
    'period': '*',                 # Period to make dayvalues
    'file-type': 'html',           # Output type file
    'write': 'rewrite',            # Rewrite 'rewrite' all or just just 'add'
    'lst-sel-cells': cfg.lst_cells_dayvalues,  # Entities for the day. Use all.
    'download': True               # Download data first
}



# Make dayvalues
def make(lst_stations, init):
    y, m, day, H, M, S = ymd.y_m_d_h_m_s_now() # Get current date time
    day_of_week = datetime.datetime.today().weekday() # Monday is 0 and Sunday is 6.
    days   = 100 # Days to go back. No need to update it all everytime
    ed_ymd = f'{y}{m}{day}'  # End date is today
    st_ymd = ymd.yyyymmdd_minus_day(ed_ymd, days) # Start date is X days back
    period = f'{st_ymd}-{ed_ymd}' # Last X days
    update = 'add' # Default add only new days
    download = True # Always download

    if init: # First time, do all
        period, update = '*', 'rewrite'
    elif day_of_week == 6 : 
        update = 'rewrite' # On sunday rewrite last X days
    elif day == '01': 
        update = 'rewrite' # First day of the month
        period = '*'  # Update period rewrite all data
    else:
        pass
        # Add only
        # Check only last 100 days

    # Make options for update
    options = {
        'title': 'dayvalues',          # Title for verbose options
        'lst-stations': lst_stations,  # Selected stations
        'period': period,              # Period
        'file-type': 'html',           # html files
        'write': update,               # Rewrite 'rewrite' all or just just 'add'
        'lst-sel-cells': cfg.lst_cells_dayvalues,  # Entities for the day. Use all.
        'download': download           # Download data first
    }
    dayvalues.calculate(options) # Process update

if __name__ == '__main__':
    # Example all days for lst stations

    init = False # First time ?
    make(lst_stations, init)
