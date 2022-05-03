# -*- coding: utf-8 -*-
'''Library contains classes and functions showing actual weather'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.0.6"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import config as cfg, wget, os
import sources.view.text as text
import sources.model.utils as utils
import common.control.fio as fio
import common.view.txt as txt
import common.model.ymd as ymd
import common.view.console as cnsl


def full_dir():
    y, m, d = ymd.yyyy_mm_dd_now()
    return fio.mk_path( cfg.dir_forecasts, f'{y}/{m}/{d}' )

def full_name(fname):
    H, M, S = ymd.hh_mm_ss_now()
    return f'{fname}-{H}-{M}-{S}.txt'

def full_path(fname):
    return fio.mk_path(full_dir(), full_name(fname))


# Buienradar
def buienradar_table_current_weather_stations(l, cols=8, spaces=33):
    entities = [ 'stationname', 'timestamp', 'weatherdescription', 'temperature',
                 'feeltemperature', 'windspeedBft', 'winddirection',
                 'precipitation', 'humidity', 'airpressure', 'sunpower' ]
                 # 'winddirectiondegrees',
    t, ndx, end, max = '', 0, cols, len(l)
    while True:
        part = l[ndx:end]
        for enties in entities:
            if enties == 'weatherdescription':
                enties = enties.replace('weather', '')

            title = enties + ' '
            post_fix = ''
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

            t += text.padding( title, align='right', spaces=33 )

            el_t = ''
            for station in part:
                if enties in station:
                    el = str(station[enties])
                    if el == '':
                        el = '....'
                    else:
                        if enties == 'timestamp':
                            el = el.replace('T', ' ')[:-3]
                        elif enties == 'stationname':
                            el = el.replace('Meetstation','')

                        el += post_fix
                else:
                    el = '....'

                el_t += text.padding( el, align='center', spaces=spaces )

            t += el_t + '\n'

        t += '\n'
        ndx, end = ndx + cols, end + cols
        # Check end
        if ndx >= max:
            break
        elif ndx < max:
            if end >= max:
                end = max # Correct max endkey

    t += '\n'

    return t

def buienradar_stations(verbose=cfg.verbose):
    ok, js = fio.request_json( cfg.buienradar_json_data, verbose=verbose)

    if ok: # If download is oke, prepare the results
        stations = js['actual']['stationmeasurements']
        if cfg.buienradar_json_places != -1: # Print only stations in list
            l = []
            for select in cfg.buienradar_json_places:
                for station in stations:
                    name = str(station['stationname']).replace('Meetstation',' ').strip()
                    if name == str(select):
                        l.append(station)
        else:
            l = stations # Print all stations

        t  = f'Waarnemingen NL\n\n'
        t += buienradar_table_current_weather_stations(
                    l, cols=cfg.buienradar_json_cols, spaces=36
                )
        t += js['buienradar']['copyright'] + '\n'

        if cfg.save_forecasts:
            ok = fio.write(full_path('buienradar-weather-stations'), t, verbose=verbose)

    return ok, t

def buienradar_table_forecast(l, spaces=30):
    entities = [ 'day', 'maxtemperature', 'mintemperature', 'rainChance',
                 'sunChance', 'windDirection', 'wind' ] #'weatherdescription'
    t = ''
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

        t += text.padding( title, align='right', spaces=spaces )

        el_t = ''
        for day in l:
            el = str(day[enties])
            el = '....' if el == '' else el + post_fix

            if enties == 'day':
                el = el[:10]

            el_t += text.padding( el, align='center', spaces=24 )

        t += el_t + '\n'

    return t

def buienradar_weather(verbose=cfg.verbose):
    ok, js = fio.request_json(cfg.buienradar_json_data, verbose=verbose)
    if ok:
        report = js['forecast']['weatherreport']

        # Clean up text
        t = report['text'].replace('.', '. ').replace('&agrave;', 'à')
        t = t.replace('&rsquo;', '\'').replace('&euml;', 'ë')
        t = t.replace('&nbsp;', ' ')
        t = txt.sanitize(t)

        tt, sentence, cnt, max_sentence, max_len = '', '', 1, 8, 64  # Count words
        for word in t.split(' '):
            sentence += word + ' ' # Make sentences of words
            if word[-1] == '.' and cnt >= max_sentence: # End of paragraph
                tt += sentence + '\n\n' # Add white row
                sentence = '' # Reset sentence
                cnt = 1 # Reset counter
            elif len(sentence) > max_len: # Not (much) longer than X chars
                tt += sentence + '\n' # Add enter
                sentence = '' # Reset sentence
                cnt += 1 # Count rows 
        tt += sentence # Add left over   

        t  = 'Weerbericht van buienradar.nl\n'
        t += 'Gepubliceerd op: '
        t += report['published'].replace('T', ' ') + '\n\n'
        t += report['title']  + '\n\n'
        t += tt + '\n\n'
        t += 'Auteur: ' + report['author'] + '\n\n'

        l_days_forecast = js['forecast']['fivedayforecast']

        t += 'Vooruitzichten:\n'
        t += buienradar_table_forecast(l_days_forecast) + '\n\n'
        t += js['buienradar']['copyright'] + '\n\n'

        if cfg.save_forecasts:
            ok = fio.write(full_path('buienradar-weather-forecast'), t, verbose=verbose)

    return ok, t

# KNMI
def knmi_table_current_weather(l, cols=8, spaces=33):
    entities = [ 'station', 'overcast', 'temperature', 'windchill',
                 'humidity', 'wind_direction', 'wind_strength',
                 'visibility', 'air_pressure' ]

    t, ndx, end, max = '', 0, cols, len(l)
    while True:
        part = l[ndx:end]
        for enties in entities:

            title = enties.replace('_','') + ' '
            post_fix = ''
            if enties in ['temperature', 'windchill']: post_fix = '°C'
            elif enties == 'humidity':      post_fix = '%'
            elif enties == 'wind_strength': post_fix = 'bft'
            elif enties == 'visibility':    post_fix = 'm'
            elif enties == 'air_pressure':  post_fix = 'hPa'

            t += text.padding( title, align='right', spaces=28 )

            el_t = ''
            for station in part:
                el = ''
                if enties in station:
                    el = str(station[enties])
                el = '....' if el == '' else el + post_fix
                el_t += text.padding( el[:22], align='center', spaces=spaces )

            t += el_t + '\n'

        t += '\n'
        ndx, end = ndx + cols, end + cols
        # Check end
        if ndx >= max:
            break
        elif ndx < max:
            if end >= max:
                end = max # Correct max endkey

    t += '\n'
    return t

def knmi_stations(verbose=cfg.verbose):
    t = ''
    url = cfg.knmi_json_data_10min
    ok, js = fio.request_json( url, verbose=verbose)

    if ok: # If download is oke, prepare the results

        stations = js['stations']
        if cfg.knmi_json_places != -1: # Print only stations in list
            l = list()
            for select in cfg.knmi_json_places:
                for station in stations:
                    name = station['station'].strip()
                    if name == select:
                        l.append(station)
        else:
            l = stations # Print all stations

        t += f'Waarnemingen: {js["date"]}\n\n'
        t += knmi_table_current_weather( l, cols=cfg.knmi_json_cols, spaces=40 )
        t += cfg.knmi_dayvalues_notification.lower() + '\n'

        if cfg.save_forecasts:
            ok = fio.write(full_path('knmi-weather-stations'), t, verbose=verbose)

    return ok, t


def process_knmi(url, fname, verbose=cfg.verbose):
    ok, t = False, ''
    dir, fname = full_dir(), full_name(fname)
    path = fio.mk_path(dir, fname)

    ok = fio.mk_dir(dir, verbose=verbose) # Make map
    wget.download(url, path, bar=None)  # Download

    ok, t = fio.read(path, encoding="ISO-8859-1", verbose=verbose)
    t = text.clean_up(t)
    cnsl.log(t, True)

    if not cfg.save_forecasts:
        ok = fio.delete(path, verbose=verbose)
        for _ in range(3): # Clean up maps if empthy
            path = os.path.dirname( path )
            if fio.is_dir_empthy( path, verbose=verbose): # Remove only empthy maps
                fio.rm_dir( path, verbose=verbose)


    return ok, t 


def process(option, verbose=cfg.verbose):
    ok = False
    if fio.has_internet(verbose):
        if   option == 'buienradar-weather':  ok, t = buienradar_weather(verbose)
        elif option == 'knmi-stations':       ok, t = knmi_stations(verbose)
        elif option == 'buienradar-stations': ok, t = buienradar_stations(verbose)

        if ok:
            cnsl.log(text.clean_up(t), True)
        else:
            cnsl.log('Not ok. Something went wrong along the way.', cfg.error)
    else:
        cnsl.log('No internet connection.', cfg.error)
