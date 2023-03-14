# -*- coding: utf-8 -*-
'''Library contains functions for auto downloading files and updating the day values.'''
__author__ = 'Mark Zwaving'
__email__ = 'markzwaving@gmail.com'
__copyright__ = 'Copyright (C) Mark Zwaving. All rights reserved.'
__license__ = 'GNU Lesser General Public License (LGPL)'
__version__ = '0.0.3'
__maintainer__ = 'Mark Zwaving'
__status__ = 'Development'

# To get access to all the code from weathersstats,
# add the root map from weatherstats to sys.path.
import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))

# Import weatherstats libraries
import config as cfg
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

# No need to update it all (everytime)
# Period for last X days
days = 31 # days to go back
end_ymd = ymd.yyyymmdd_now()
start_ymd = ymd.yyyymmdd_minus_day(end_ymd, days)
per_last_X_days = f'{start_ymd}-{end_ymd}'

# Make dayvalues
def make(lst_stations, period):
    # Option list to make dayvalues
    options = {
        'title': 'dayvalues',          # Title for verbose options
        'lst-stations': lst_stations,  # Selected stations
        'period': period,              # All times
        'file-type': 'html',           # html files
        'write': 'rewrite',            # Rewrite 'rewrite' all or just just 'add'
        'lst-sel-cells': cfg.lst_cells_dayvalues,  # Entities for the day. Use all.
        'download': True               # Download data first
    }
    dayvalues.calculate(options)

if __name__ == '__main__':
    # Example all days for lst stations
    make(lst_stations, '*')
