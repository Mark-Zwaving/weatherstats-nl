# -*- coding: utf-8 -*-
'''Library contains functions for handling quick io'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.0.6"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import config as cfg
import stations
import sources.model.utils as utils
import sources.model.daydata as daydata
import common.control.fio as fio
import common.view.console as cnsl

# Input options
l_inp_min  = ['min', '-']
l_inp_max  = ['max', '+']
l_inp_mean = ['mean', 'ave', 'average', '~']
l_inp_sum  = ['sum', 'total', 'tot', 'Σ']
l_inp_hman = ['hellmann', 'hmann']
l_inp_fsum = ['frostsum', 'fsum', 'frostsom', 'fsom']
l_inp_ijns = ['ijnsen']
l_inp_hndx = ['heatndx', 'hndx']
l_inp_stat = l_inp_min  + l_inp_max  + l_inp_mean + l_inp_sum
l_inp_indx = l_inp_hman + l_inp_fsum + l_inp_ijns + l_inp_hndx
l_inp_all  = l_inp_stat + l_inp_hman + l_inp_fsum + l_inp_ijns + l_inp_hndx
l_no_dates = l_inp_mean + l_inp_sum  + l_inp_indx
l_rm_chars = [' ', '(', ')','{','}','[', ']']


def correct_ent_statis(inp_usr):
    '''Function returns the correct entity (tg, sq, rh, fsum ) and
       the correct statistical part (min,max) from input from the user'''
    # Remove unecessary chars
    inp_usr = utils.remove_chars(inp_usr, l_rm_chars).lower()
    result = {'statis': '', 'entity': ''} # Result dictionary
    for inp_stat in l_inp_stat: # Check the stats: min, max, mean, sum
        if inp_usr in l_inp_indx: # Always skip possible index values
            continue
        if inp_usr.find(inp_stat) != -1: # Find correct input
            # Remove the statistical part (like: min, max et cetera)
            # Leftover is tg, tg, tn, sq et cetera
            result['entity'] = utils.remove_chars(inp_usr, l_inp_stat)
            # Remove the entity part (like: tg, rh, sq et cetera)
            # Leftover is the statistical part
            result['statis'] = utils.remove_chars(inp_usr, result['entity'])
            break # else will now not be executed
    else:
        # Not the stats: min, max, mean, sum
        if inp_usr not in l_inp_stat:
            # Check the index values like: hellmann, frostsum, heatndx, ijnsen
            if   inp_usr in l_inp_hman: result['statis'] = l_inp_hman[0]
            elif inp_usr in l_inp_fsum: result['statis'] = l_inp_fsum[0]
            elif inp_usr in l_inp_hndx: result['statis'] = l_inp_hndx[0]
            elif inp_usr in l_inp_ijns: result['statis'] = l_inp_ijns[0]
            # Both statis and ent are the same
            result['entity'] = result['statis']

    return result

def calc_stats_txt(data, st, ent):
    '''Function resolves output text and calculates the correct
       statistical value'''
    ok, t, val = False, '', ''
    if   st in l_inp_min:  ok, t, val = True, 'minimum', calc_stats.min(data,ent)
    elif st in l_inp_max:  ok, t, val = True, 'maximum', calc_stats.max(data,ent)
    elif st in l_inp_sum:  ok, t, val = True, 'sum',     calc_stats.sum(data,ent)
    elif st in l_inp_mean: ok, t, val = True, 'mean',    calc_stats.average(data,ent)
    elif st in l_inp_hman: ok, t, val = True, 'hellmann',calc_stats.hellmann(data)
    elif st in l_inp_fsum: ok, t, val = True, 'frostsum',calc_stats.frost_sum(data)
    elif st in l_inp_ijns: ok, t, val = True, 'ijnsen',  calc_stats.ijnsen(data)
    elif st in l_inp_hndx: ok, t, val = True, 'heatndx', calc_stats.heat_ndx(data)

    return ok, t, val

def mk_period(period):
    '''Update period'''
    return period.replace(' ', ' ') # Remove whitespace

def mk_stations(inp_places):
    '''From user input make a list with all the stations'''
    result = [] # Result lst
    # Make a list with stations who are available in the data map
    stations_in_map = stations.lst_stations_in_map()

    # Remove unecessary whitespaces
    inp_places = inp_places.replace('  ', ' ').strip()
    # Check for wild card
    if inp_places == '*':
        return stations_in_map # Return all stations

    lplaces = inp_places.split(',') # Split up in station names or wmo
    for wmo_place in lplaces: # Check all Input
        # Station name can be a wmo number or a name
        wmo_place = wmo_place.replace(' ','')
        if stations.name_wmo_in_lst(wmo_place):
            station = stations.wmo_name_to_station(wmo_place)
            if station != False:
                cnsl.log(f'Found -> {wmo_place}') # Verbose output
                result.append(station) # Add station to result lst

    return result # List with stations

# We want to know the entitity (tx,tn, hmann)
# and what to calculate (max,mean,fsum)
def mk_statistics(statistics):
    result = [] # Result lst
    # Remove unecessary chars and whitespace and make lowercase
    statistics = utils.remove_chars(statistics, l_rm_chars).lower()
    l_inp_usr = statistics.split(',') # Split up in parts
    for inp_usr in l_inp_usr: # Input from user
        for inp in l_inp_all: # Check all possible statistical input
            if inp_usr.find(inp) != -1: # Found correct element
                # Get the correct statistical and entity part
                res_dict = correct_ent_statis(inp_usr)
                cnsl.log(f'Found -> {str(res_dict)}', True) # Verbose output
                result.append(res_dict) # Add dictionary to lst
    return result

def mk_fname(period, lstations, ldict_st_ent):
    '''Function makes a file name based on input'''
    def replace_signs(s):
        s = s.replace('-', 'min')
        s = s.replace('+', 'max')
        s = s.replace('~', 'mean')
        s = s.replace('Σ', 'sum')
        return s

    # If all is selected use -> x else get al the wmo names from the stations
    lplaces = ['x'] if len(lstations) == len(stations.lst_stations_in_map()) else \
              [ station.wmo for station in lstations ] # List names wmo stations

    l_st_ent = [] # Result list with statis and entities
    for st_ent in ldict_st_ent:
        entity = st_ent['entity'] # Get entity part
        statis = st_ent['statis'] # Get statistical part
        ent_st = ''
        # No entity name in name output file, because is double with statis name
        if entity not in l_inp_indx:
            ent_st += entity # Add entity to result lst
        # Replace -, + with min, plus etcetera and add statis to result string
        ent_st += replace_signs(statis)
        l_st_ent.append(ent_st) # Add statis to result lst

    # Make base name, length no more than 80 chars
    base  = f'quick-{period}-{"_".join(lplaces)}-{"-".join(l_st_ent)}'[:80]
    fname = f'{base}.txt'.lower() # Make name an no uppercase
    return fname

def get_date_txt(data, val, entity=''):
    '''Function makes a date with a date txt if a date is there'''
    symd, ymd = '', ''
    if entity:
        ymd = daydata.date_by_val(data, val, entity)
        if ymd:
            symd = f'{ymd}  {ymd.text(ymd)}'

    return symd

def calculate(command):
    cmd_output = utils.clean(command) # Cleanup command for output
    # Split command calc in three parts
    period, places, statistics = cmd_output.split('->')
    period = mk_period(period) # Make string period
    lplaces = mk_stations(places) # Make a list of all places
    # Make a list with dictionaries with the correct entities and statistical part
    ldict_st_ent = mk_statistics(statistics) # Get dictionary
    fname = mk_fname(period, lplaces, ldict_st_ent) # Get a file name
    path = utils.mk_path(cfg.dir_quick_calc_txt, fname) # Get path

    cnsl.log(' ', True)
    t = f'Command given\n{cmd_output}\n' # For output to file
    for place in lplaces:
        wmo_place = f'{place.wmo} {place.place}'.title()
        # Output to console
        cnsl.log(f'Process data period <{period}> for station: {wmo_place}...', True)
        # Read the data from station for a given period
        ok, data = daydata.read_period(place, period) # Get data stations
        if ok:
            # Output to file
            t += f'\nStation {wmo_place} for period {period}\n'

            # Walkthrough statistical list with dictionaries
            for st_ent in ldict_st_ent:
                statis = st_ent['statis']
                entity = st_ent['entity']

                # Verbose output
                tc = f'For station {wmo_place} calculate {statis} '
                if entity: tc += f'for {entity}'
                cnsl.log(tc)

                # Calculate correct results
                ok, txt, val = calc_stats_txt(data, statis, entity)

                if ok:
                    ent  = entity.upper() # Make upper for output
                    rent = txt # Statistical value, like mean, sum, max, heatndx
                    # Add ent to output only if it is not an index value (like hellmann, heatndx)
                    if entity not in l_inp_indx: rent += f' {ent}'
                    # Add correct postfixes bft, °C et cetera
                    sval = fix.ent(val, entity)

                    # Output to file
                    t += f'{rent:>12}  {sval:<8} '
                    # No date added for mean, sum and index values
                    if entity not in l_no_dates:
                        t += get_date_txt(data, val, entity)
                    t += '\n'
                else:
                    cnsl.log(f'Error reading data...', True)

    # Output result to console
    cnsl.log(f'\n{t}', True) # Output to console

    # Save result to file
    ok = fio.save(path, t)
    if not ok:
        cnsl.log(f'Error in saving {path}...', True)

    return path
