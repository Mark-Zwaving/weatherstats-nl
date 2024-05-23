# -*- coding: utf-8 -*-
'''Library contains a broker function for the weather forecasts'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.0.3'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import sources.control.fio as fio
import sources.view.console as cnsl
import sources.model.forecast.buienradar as buienradar
import sources.model.forecast.knmi as knmi

def process(title, verbose=cfg.verbose):
    ok = False

    if fio.check_for_internet_connection(verbose):

        # Select fn for the specific forecasts
        if title == 'buienradar-forecast':
            ok, t = buienradar.weather_forecast(verbose)
        elif title == 'buienradar-stations': 
            ok, t = buienradar.weather_stations(verbose)
        elif title == 'knmi-forecast':
            ok, t = knmi.weather_forecast()
        elif title == 'knmi-stations':
            ok, t = knmi.weather_stations()

        if ok:
            # Remove enter for and after text
            t = t.strip() 

            # Write to screen (always)
            cnsl.log(t, True) 

            # Must we save the texts to a file?
            if cfg.save_forecasts:
                # Make download path with dates and times
                path = fio.path_with_act_date(cfg.dir_forecasts, title) 

                # Save the file
                ok = fio.write(path, t, verbose=verbose)

            # # Remove already saved files (knmi)
            # else: 
            #     if fio.check(path, verbose=verbose):
            #         fio.remove_file_and_empthy_maps_reverse(path, verbose)

        else:
            cnsl.log('Error in forecast broker().', cfg.error)
    else:
        cnsl.log('No internet connection available to download weather forecasts.', cfg.error)