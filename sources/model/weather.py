# -*- coding: utf-8 -*-
'''Library contains classes and functions showing actual weather'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 3 - GPLv3'
__version__    =  '0.0.8'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg, wget, os
import sources.control.fio as fio
import sources.view.text as text
import sources.view.console as cnsl
import sources.model.utils as utils

# Buienradar
def buienradar_table_stations(lst, cols=8, spaces=33):
    entities = [ 'stationname', 'timestamp', 'weatherdescription', 'temperature',
                 'feeltemperature', 'windspeedBft', 'winddirection',
                 'precipitation', 'humidity', 'airpressure', 'sunpower' ]
                 # 'winddirectiondegrees',
    title_pad, value_pad = 16, 18
    t, ndx, end, max = cfg.e, 0, cols, len(lst)
    
    while True:
        part = lst[ndx:end]
        for enties in entities:
            if enties == 'weatherdescription':
                enties = enties.replace('weather', cfg.e)
            title = enties + ' '
            post_fix = cfg.e
            if enties in ['temperature', 'feeltemperature']:
                post_fix = '°C'
            elif enties == 'humidity':
                post_fix = '%'
            elif enties == 'windspeedBft':
                post_fix = 'bft'
            elif enties == 'visibility':
                post_fix = 'm'
            elif enties == 'airpressure':
                post_fix = 'hPa'
            elif enties == 'precipitation':
                post_fix = 'mm'

            t += text.padding( title, align='right', spaces=title_pad )
            el_t = cfg.e
            for station in part:
                if enties in station:
                    el = str(station[enties])
                    if el == cfg.e:
                        el = '....'
                    else:
                        if enties == 'timestamp':
                            el = el.replace('T', ' ')[:-3]
                        elif enties == 'stationname':
                            el = el.replace('Meetstation',cfg.e)
                        el += post_fix
                else:
                    el = '....'
                el_t += text.padding(el, align='center', spaces=value_pad)
            t += el_t + '\n'
        t += '\n'
        ndx, end = ndx + cols, end + cols
        # Check end
        if ndx >= max:
            break
        elif ndx < max:
            if end >= max:
                end = max # Correct max endkey
    return t

def buienradar_table_forecast(lst, spaces=30):
    entities = [ 'day', 'maxtemperature', 'mintemperature', 'rainChance',
                 'sunChance', 'windDirection', 'wind' ] #'weatherdescription'
    title_pad, value_pad = 15, 12
    t = cfg.e
    for enties in entities:
        # Make title and post fix
        title, post_fix = enties + ' ', ' '
        if enties in ['maxtemperature', 'mintemperature']:
            post_fix = '°C'
        elif enties in ['rainChance', 'sunChance']:
            post_fix = '%'
        elif enties == 'wind':
            post_fix = 'bft'
        elif enties == 'visibility':
            post_fix = 'm'
        elif enties == 'air_pressure':
            post_fix = 'hPa'

        t += text.padding( title, align='right', spaces=title_pad )
        el_t = cfg.e # Alsways one space separator
        for day in lst:
            el = str(day[enties])
            el = cfg.no_val if el == cfg.e else el + post_fix

            if enties == 'day': el = el[:10]
            el_t += text.padding(el, align='center', spaces=value_pad)

        t += el_t + '\n'

    return t

def buienradar_stations_json(verbose=cfg.verbose):
    ok, js = fio.request_json( cfg.buienradar_json_data, verbose=verbose)

    if ok: # If download is oke, prepare the results
        stations = js['actual']['stationmeasurements']
        if cfg.buienradar_json_places != -1: # Print only stations in list
            lst = []
            for select in cfg.buienradar_json_places:
                for station in stations:
                    name = str(station['stationname']).replace('Meetstation',' ').strip()
                    if name == str(select):
                        lst.append(station)
        else:
            lst = stations # Print all stations

        t  = f'Waarnemingen NL\n\n'
        t += buienradar_table_stations(lst, cols=cfg.buienradar_json_cols, spaces=36)
        t += js['buienradar']['copyright'] + '\n'

    return ok, t

def buienradar_weather_json(verbose=cfg.verbose):
    ok, js = fio.request_json(cfg.buienradar_json_data, verbose=verbose)
    if ok:
        report = js['forecast']['weatherreport']

        # Clean up text
        t = report['text'].replace('.', '. ').replace('&agrave;', 'à')
        t = t.replace('&rsquo;', '\'').replace('&euml;', 'ë')
        t = t.replace('&nbsp;', ' ')
        t = text.clean(t)

        tt, sentence, cnt, max_sentence, max_len = cfg.e, cfg.e, 1, 8, 64  # Count words
        for word in t.split(' '):
            sentence += word + ' ' # Make sentences of words
            if word[-1] == '.' and cnt >= max_sentence: # End of paragraph
                tt += sentence + '\n\n' # Add white row
                sentence = cfg.e # Reset sentence
                cnt = 1 # Reset counter
            elif len(sentence) > max_len: # Not (much) longer than X chars
                tt += sentence + '\n' # Add enter
                sentence = cfg.e # Reset sentence
                cnt += 1 # Count rows 
        tt += sentence # Add left over   

        t  = 'Weerbericht van buienradar.nl\n'
        t += 'Gepubliceerd op: '
        t += report['published'].replace('T', ' ') + '\n\n'
        t += report['title']  + '\n\n'
        t += text.sanitize(tt) + '\n\n'
        t += 'Auteur: ' + report['author'] + '\n\n'
        t += 'Vooruitzichten:\n'
        t += buienradar_table_forecast(js['forecast']['fivedayforecast']) + '\n'
        t += js['buienradar']['copyright'] + '\n\n'

    return ok, t

# KNMI
def knmi_table_stations(lst, cols=8, spaces=33):
    entities = [ 'station', 'overcast', 'temperature', 'windchill',
                 'humidity', 'wind_direction', 'wind_strength',
                 'visibility', 'air_pressure' ]
    title_pad, value_pad = 14, 16
    t, ndx, end, max = cfg.e, 0, cols, len(lst)
    while True:
        part = lst[ndx:end]
        for enties in entities:

            title = enties.replace('_',cfg.e) + ' '
            post_fix = cfg.e
            if enties in ['temperature', 'windchill']: post_fix = '°C'
            elif enties == 'humidity':      post_fix = '%'
            elif enties == 'wind_strength': post_fix = 'bft'
            elif enties == 'visibility':    post_fix = 'm'
            elif enties == 'air_pressure':  post_fix = 'hPa'

            t += text.padding(title, align='right', spaces=title_pad)
            el_t = cfg.e
            for station in part:
                el = cfg.e
                if enties in station:
                    el = str(station[enties])
                el = cfg.no_val if el == cfg.e else el + post_fix
                el_t += text.padding(el[:value_pad-2], align='center', spaces=value_pad)
            t += el_t + '\n'
        t += '\n'
        ndx, end = ndx + cols, end + cols
        # Check end
        if ndx >= max:
            break
        elif ndx < max:
            if end >= max:
                end = max # Correct max endkey
                
    return t

def knmi_stations_json(verbose=cfg.verbose):
    t = cfg.e
    url = cfg.knmi_json_data_10min
    ok, js = fio.request_json( url, verbose=verbose)
    if ok: # If download is oke, prepare the results
        stations = js['stations']
        if cfg.knmi_json_places != -1: # Print only stations in list
            lst = []
            for select in cfg.knmi_json_places:
                for station in stations:
                    name = station['station'].strip()
                    if name == select:
                        lst.append(station)
        else:
            lst = stations # Print all stations

        t += f'Waarnemingen: {js["date"]}\n\n'
        t += knmi_table_stations(lst, cols=cfg.knmi_json_cols, spaces=40)
        t += cfg.knmi_dayvalues_notification.lower() + '\n'

    return ok, t

def process_knmi(url, path, verbose=cfg.verbose):
    ok, t = False, cfg.e
    ok = fio.mk_dir(dir, verbose=verbose) # Make map
    wget.download(url, path, bar=None)  # Download

    ok, t = fio.read(path, encoding='ISO-8859-1', verbose=verbose)
    t = text.sanitize(t)

    return ok, t

def process(option, verbose=cfg.verbose):
    ok = False
    if fio.check_for_internet_connection(verbose):
        path = utils.path_with_act_date(cfg.dir_forecasts, option) # Make download path
        if   option == 'buienradar-weather':  ok, t = buienradar_weather_json(verbose)
        elif option == 'buienradar-stations': ok, t = buienradar_stations_json(verbose)
        elif option == 'knmi-weather':        ok, t = process_knmi(cfg.knmi_forecast_global_url, path, verbose)
        elif option == 'knmi-model':          ok, t = process_knmi(cfg.knmi_forecast_model_url, path, verbose)
        elif option == 'knmi-guidance':       ok, t = process_knmi(cfg.knmi_forecast_guidance_url, path, verbose)
        elif option == 'knmi-stations':       ok, t = knmi_stations_json(verbose)

        if ok:
            t = t.strip() # Remove enter for and after text
            cnsl.log(t, True) # Write to screen (always)
            if cfg.save_forecasts:
                ok = fio.write(path, t, verbose=verbose)
            else: # Remove already saved files (knmi)
                if fio.check(path, verbose=verbose):
                    fio.remove_file_and_empthy_maps_reverse(path, verbose)
        else:
            cnsl.log('Not ok. Something went wrong along the way.', cfg.error)
    else:
        cnsl.log('No internet connection.', cfg.error)
