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
import sources.model.ymd as ymd
import sources.view.console as cnsl
import sources.model.dayvalues.broker_period as broker
import sources.model.dayvalues.data as data

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
    np_lst_days = update_low_values__1(np_lst_days)

    return ok, np_lst_days  # OK

def update_low_values__1( np_lst_days ):
    '''Function updates the -1 raw value in the data. 
       Note: -1 raw value in lst is 0.1 for real
       The -1 raw value is used for small values between 0.1 and 0.0 
       The weatherdata is given in integers. 
       That way it is not possible to have floating point values
    ''' 
    find_low_val = -1.0  # Lower dan 1 value, -1 raw is -> -0.1
    replace_val  = cfg.knmi_dayvalues_low_measure_val # Sustitute value

    # Columns to replace -1.0 for
    col_rh, col_rhx, col_sq = data.column('RH'), data.column('RHX'), data.column('SQ')

    # Loop days and update if -1 value for the spicific data is found 
    for ndx, value in np.ndenumerate(np_lst_days):
        row, col = ndx # Get current indices

        # Check rh
        if col == col_rh: # If col is rh col, Check if rh value is -1
            if value == find_low_val: # If rh == -1
                np_lst_days[row,col] = replace_val # Update rh value to replace value

        # Check rhx
        elif col == col_rhx: # If col is rhx col, Check if rhx value is -1
            if value == find_low_val: # If rhx == -1
                np_lst_days[row,col] = replace_val # Update rhx value to replace value

        # Check sq
        elif col == col_sq: # If col is sq col, Check if sq value is -1
            if value == find_low_val: # If sq == -1
                np_lst_days[row,col] = replace_val   # Update ss value to replace value

        

    return np_lst_days

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
