# -*- coding: utf-8 -*-
'''Library contains functions select one or more days and print he results onth screen'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.0.5'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg, os
import pprint
import sources.control.fio as fio
import sources.control.davalues.read as dayval_read
import sources.model.dayvalues.np_days as np_days
import sources.model.dayvalues.broker_period as broker
import sources.model.dayvalues.data as data
import sources.model.ymd as ymd
import sources.view.console as cnsl
import sources.view.text as text

def save_txt_file(path, fname, main, verbose=False):
    ''' Class to make a text page based on given entities'''
    dt = ymd.text(ymd.yyyymmdd_now())
    fname = f'{fname}-{dt}.txt'
    path = os.path.join(path, fname)
    l = lambda x, s : x * s + '\n'

    header = l(80,'#') + 'DAYVALUES'
    main = main
    footer  = cfg.knmi_dayvalues_notification 
    footer += text.created_by_notification + ' '
    footer += ymd.text_datetime_now()
    content = header + content + footer 

    ok = fio.write(path, content, verbose=verbose)

    return ok, path

def process(options, verbose=True): 
    '''Print the day on the screen'''
    # Init list stations
    lst_dict_stations = []
    for station in options[text.ask_lst_stations]:
        # Dictionary for the staiion init and reset
        dict_result_station = {}
        dict_result_station['station'] = station 
        dict_result_station['lst-dict-period'] = [] 

        # Read the weatherdata for the stations
        ok, np_lst_days = dayval_read.weatherstation(station)
        if ok: 
            # Walkthrough every day in the lst
            for period in options[text.ask_lst_period_1]: 
                # Get the day (period) from the data
                ok, np_lst_period = broker.process(np_lst_days, period)
                if ok: # Days found in period
                    # Walkthrough the days in given period
                    for np_ymd in np_lst_period: 
                        # Get date
                        yyyymmdd = str(int( np_ymd[data.YYYYMMDD] )) 
                        # Dictionary for the days (yyyymmdd) init and reset
                        dict_result_yyyymmdd = {} 
                        dict_result_yyyymmdd['yyyymmdd'] = yyyymmdd
                        dict_result_yyyymmdd['lst-dict-entities'] = [] 

                        # Walkthrough the entities
                        for entity in options[text.ask_lst_entities]:
                            # Make dictionary with entity and dummy value
                            dict_ent_val = {}
                            dict_ent_val['entity'] = entity 
                            dict_ent_val['raw-val'] = cfg.no_val 

                            # Get the day in the period
                            ok, np_lst_day = broker.process(np_lst_period, yyyymmdd)
                            if ok:
                                # Get only valid values, remove NAN values from np lst
                                ok, np_lst_valid = np_days.rm_nan(np_lst_day, entity) 
                                if ok: 
                                    # There is a valid value for tshe day in the data
                                    col_ent = data.column(entity) # Data col of entity
                                    raw_val = np_lst_valid[0, col_ent] # Raw data values

                                    # Update dictionary with a correct value
                                    dict_ent_val['raw-val'] = raw_val

                            # Add dictionary current entity and value to lst entities
                            dict_result_yyyymmdd['lst-dict-entities'].append(dict_ent_val)

                        # Add the dictionary yyyymmdd to the lst 
                        dict_result_station['lst-dict-period'].append(dict_result_yyyymmdd)

        # Add the station dictionary with the days with entites and values lst stations
        lst_dict_stations.append(dict_result_station)

    # pprint.pp(lst_dict_stations)

    # Init txt for output
    txt = ''
    # Write stations with the days with the entities to the screen
    for dict_station in lst_dict_stations: 
        # Grap station and ststion info
        station = dict_station['station']
        info_station = f'{station.wmo} {station.place}'
        
        # Get lst of dictionary
        for lst_yyyymmdd in dict_station['lst-dict-period']:
            # Get date
            yyyymmdd = lst_yyyymmdd['yyyymmdd']
            ymd_txt = ymd.yyyymmdd_to_text(yyyymmdd)
            txt += f'{info_station} <{yyyymmdd}>\n{ymd_txt}' + cfg.ln

            # Walkthrough entities
            for dict_entity in lst_yyyymmdd['lst-dict-entities']:
                entity  = dict_entity['entity'].upper()
                raw_val = dict_entity['raw-val'] 
                ent_txt = text.ent_to_txt(entity) 
                ent_val = text.fix_for_entity(raw_val, entity) 
                txt += f'{entity:^6} {ent_val:^18} <{ent_txt}>' + cfg.ln

    # Print to screen
    cnsl.log(text.head('See see days'), verbose)
    cnsl.log(txt.rstrip(), True)
    cnsl.log(text.foot('End see days'), verbose)

    path_ndx = ''
    return True, path_ndx, txt 
