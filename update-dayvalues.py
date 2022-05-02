# -*- coding: utf-8 -*-
'''Library contains functions for auto downloading files and updating the day values.'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU Lesser General Public License (LGPL)'
__version__    =  '0.0.1'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import stations
import sources.model.dayvalues as dayvalues
import config as cfg

# Stations to update
lst_stations = [
    stations.from_wmo_to_station('260'),
    stations.from_wmo_to_station('280'),
    stations.from_wmo_to_station('235'),
    stations.from_wmo_to_station('310'),
    stations.from_wmo_to_station('380')
]

options = { 
    'period': '********', 
    'lst-stations': lst_stations, 
    'file-type': 'html', 
    'write': 'add', 
    'download': True
} 

cfg.verbose = False

if __name__ == '__main__':
    dayvalues.calculate( options )