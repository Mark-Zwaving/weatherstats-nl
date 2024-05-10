# -*- coding: utf-8 -*-
'''Library has functions for downloading data.'''
__author__ = 'Mark Zwaving'
__email__ = 'markzwaving@gmail.com'
__copyright__ = 'Copyright (C) Mark Zwaving. All rights reserved.'
__license__ = 'GNU Lesser General Public License (LGPL)'
__version__ = '0.0.2'
__maintainer__ = 'Mark Zwaving'
__status__ = 'Development'
# To get access to all the code from weathersstats,
# add the root map from weatherstats to sys.path.
import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))

# Import weatherstats libraries
import sources.model.ymd as ymd 
import sources.view.console as cnsl
import sources.model.dayvalues.data as data
import sources.model.stations as stations

################################################################################
# Stations lists

# List with stations for download
lst_sel_stations = [
    stations.wmo_to_station('260'),
    stations.wmo_to_station('280'),
    stations.wmo_to_station('235'),
    stations.wmo_to_station('310'),
    stations.wmo_to_station('380')
]

# All available weather stations
lst_all_stations = stations.lst 


################################################################################
# Download functions

def download(lst):
    cnsl.log(f'[{ymd.now()}] Start download', True)
    data.process_lst(lst)
    cnsl.log(f'[{ymd.now()}] End download', True)


if __name__ == '__main__':
    download(lst_all_stations)
