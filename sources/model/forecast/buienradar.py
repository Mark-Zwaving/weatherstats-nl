# -*- coding: utf-8 -*-
'''Library contains classes and functions showing actual weather from buienradar'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.1.0'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import sources.control.fio as fio
import sources.view.text as text

def table_stations(lst, cols=8, spaces=33):
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
            t += el_t + cfg.ln
        t += cfg.ln
        ndx, end = ndx + cols, end + cols
        # Check end
        if ndx >= max:
            break
        elif ndx < max:
            if end >= max:
                end = max # Correct max endkey
    return t

def table_forecast(lst, spaces=30):
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
        el_t = cfg.e # Always one space separator
        for day in lst:
            el = str(day[enties])
            el = cfg.no_val if el == cfg.e else el + post_fix

            if enties == 'day': el = el[:10]
            el_t += text.padding(el, align='center', spaces=value_pad)

        t += el_t + cfg.ln

    return t

def weather_stations(verbose=cfg.verbose):
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

        t  = f'Waarnemingen NL' + cfg.ln
        t += table_stations(lst, cols=cfg.buienradar_json_cols, spaces=36)
        t += js['buienradar']['copyright'] + cfg.ln

    return ok, t

def weather_forecast(verbose=cfg.verbose):
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
                tt += sentence + cfg.ln + cfg.ln # Add white row
                sentence = cfg.e # Reset sentence
                cnt = 1 # Reset counter
            elif len(sentence) > max_len: # Not (much) longer than X chars
                tt += sentence + cfg.ln # Add enter
                sentence = cfg.e # Reset sentence
                cnt += 1 # Count rows 
        tt += sentence # Add left over   

        t  = 'Weerbericht van buienradar.nl' + cfg.ln
        t += 'Gepubliceerd op: '
        t += report['published'].replace('T', ' ') + cfg.ln + cfg.ln
        t += report['title'] + cfg.ln + cfg.ln
        t += text.sanitize(tt) + cfg.ln + cfg.ln
        t += 'Auteur: ' + report['author'] + cfg.ln + cfg.ln
        t += 'Vooruitzichten:' + cfg.ln 
        t += table_forecast(js['forecast']['fivedayforecast']) + cfg.ln
        t += js['buienradar']['copyright'] + cfg.ln + cfg.ln

    return ok, t

