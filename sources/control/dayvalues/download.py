# -*- coding: utf-8 -*-
'''Functions to process download and unzip dayvalues from the knmi '''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.1.5'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg, stations
import time
import sources.control.fio as fio
import sources.model.ymd as ymd
import sources.model.utils as utils
import sources.view.console as cnsl

def process( 
        weatherstation,  # Weatherstation object
        verbose = cfg.verbose 
    ):
    '''Function processes (downloading en unzipping) a knmi data file'''
    ok = False

    if weatherstation.data_download: # Only downloadable stations
        t = f'[{ymd.now()}] Process data for station: {weatherstation.wmo} {weatherstation.place}...'
        cnsl.log(t, verbose)

        url = weatherstation.data_url
        if not url:
            cnsl.log(f'[{ymd.now()}] Download skipped...', verbose)

        elif weatherstation.data_format == cfg.knmi_data_format:
            zip = weatherstation.data_zip_path
            txt = weatherstation.data_txt_path

            # Download
            ns_download = time.time_ns() 
            ok = fio.download(url, zip, check=False, verbose=verbose)
            if ok:
                delta_download = time.time_ns() - ns_download
                t = utils.process_time_delta_ns(f'[{ymd.now()}] Download in ', delta_download)
                cnsl.log(t, verbose)

                # Unzip
                ns_zip = time.time_ns()
                ok = fio.unzip(zip, txt, verbose)
                if ok:
                    delta_unzip = time.time_ns() - ns_zip
                    t = utils.process_time_delta_ns(f'[{ymd.now()}] Unzip in ', delta_unzip)
                    cnsl.log(t, verbose)
                else:
                    err = f'[{ymd.now()}] Error in download process unzip {zip}'
                    cnsl.log(err, cfg.error)
            else:
                err = f'[{ymd.now()}] Error in download processdownload {url}'
                cnsl.log(err, cfg.error)

            if ok:
                t = f'[{ymd.now()}] Process data {weatherstation.place} success'
            else:
                t = f'[{ymd.now()}] Process data {weatherstation.place} failed'

            cnsl.log(t, True)

        else:
            # TODO
            # Stations with other Formats
            # Needs to converted to knmi data format format first
            pass

    return ok

def process_lst(lst, verbose=cfg.verbose):
    '''Function downloads, unzipped knmi stations in a given list'''
    start_ns = time.time_ns()
    for station in lst: 
        process(station, verbose)
    delta_ns = time.time_ns() - start_ns

    t = utils.process_time_delta_ns(f'[{ymd.now()}] Total processing time is ', delta_ns)
    cnsl.log(t, cfg.verbose)

def process_all(verbose=cfg.verbose):
    '''Function processes (downloading en unzipping) files from the 
      selected stations in the given lst at stations.py'''
    process_lst( stations.lst, verbose )
