# -*- coding: utf-8 -*-
'''Functions to read dayvalues from a file'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.1.5'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import numpy as np, threading
import sources.model.dayvalues.np_days as np_days
import sources.view.console as cnsl
import sources.model.dayvalues.broker_period as broker
import sources.model.ymd as ymd

def weatherstation( 
        weather_station,      # Station object
        verbose = cfg.verbose # Show text overrride
    ):
    '''Reads data dayvalues from a knmi station into a numpy list'''
    ok = False
    np_lst_days = np.array([[]]) 
    cnsl.log(f'[{ymd.now()}] Read {weather_station.wmo} {weather_station.place}', verbose)

    # Read one station at a time
    with threading.Lock(): 
        try:
            np_lst_days = np.genfromtxt( 
                weather_station.data_txt_path,
                dtype          = cfg.data_dtype,  # Float 32
                delimiter      = weather_station.data_delimiter,
                missing_values = weather_station.data_missing,
                filling_values = np.nan,
                skip_header    = weather_station.data_skip_header, # Skip comments at astart
                skip_footer    = weather_station.data_skip_footer,
                comments       = weather_station.data_comments_sign,
                autostrip      = True,
                usemask        = False  # Mask not needed ?
            )
        except Exception as e:
            err = f'[{ymd.now()}] Error in read station()\n Station {weather_station.place}\n{e}'
            cnsl.log(err, cfg.error)
        else:
            err = f'[{ymd.now()}] Success in reading station {weather_station.place}'
            cnsl.log(err, verbose)
            ok = True

    # Update the low -1 values for spcific columns into -> 0.025
    if ok:
        np_lst_days = np_days.update_low_values__1(np_lst_days)

    return ok, np_lst_days  # OK

def weatherstation_period(
        weather_station,      # Station object
        period,               # Period to read
        verbose = cfg.verbose # Show text overrride
    ):
    '''Function reads data from a weather station for a given  period'''
    ok, np_lst_days = weatherstation(weather_station)

    if ok: 
        ok, np_lst_days = broker.process(np_lst_days, period)

    return ok, np_lst_days

# def read_stations_period( stations, period, t='Process data station:', verbose=cfg.verbose ):
#     result = np.array([])
#     for station in stations:
#         cnsl.log(f'[{ymd.now()}] {t} {station.wmo} {station.place}...', verbose)
#         ok, npl = read_period(station, period, verbose)
#         if ok:
#             result = npl if result.size == 0 else np.concatenate( (result, npl), axis=0 )

#     return result # convert to numpy array
