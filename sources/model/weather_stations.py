# -*- coding: utf-8 -*-
''' Library contains functions for handling stations data'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright 2020 (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 3 - GPLv3'
__version__    =  '0.2.0'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg, stations
import threading, os, os.path

################################################################################
# Functions
def lst_wmo():
    lst = [station.wmo   for station in stations.lst]
    return lst

def lst_place():
    lst = [station.place for station in stations.lst]
    return lst

def lst_wmo_place():
    lst = [f'{el[0]} {el[1]}' for el in zip( lst_wmo(), lst_place())]
    return lst 

def wmo_in_map(wmo):
    for station in lst_stations_map():
        if station.wmo == wmo:
            return True
    return False

def wmo_in_lst(wmo):
    for station in stations.lst:
        if station.wmo == wmo:
            return True
    return False

def wmo_to_place(wmo):
    for station in stations.lst:
        if station.wmo == wmo:
            return station.place
    return cfg.no_val

def wmo_to_province(wmo):
    for station in stations.lst:
        if station.wmo == wmo:
            return station.province
    return cfg.no_val

def wmo_to_station(wmo):
    '''Get station object based on wmo'''
    for station in stations.lst:
        if station.wmo == wmo:
            return station
    return station.Station() # Empthy station

def place_in_map(place):
    place = place.lower()
    for station in lst_stations_map():
        if station.place.lower() == place:
            return True
    return False

def place_in_lst(place):
    place = place.lower()
    for station in stations.lst:
        if station.place.lower() == place:
            return True
    return False

def place_to_station(place):
    place = place.lower()
    for station in stations.lst:
        if station.place.lower() == place:
            return station
    return station.Station() # Empthy station

def wmo_or_place_in_map(wmo_or_place):
    wmo_or_place = wmo_or_place.lower()
    for station in lst_stations_map():
        if station.place.lower() == wmo_or_place:
            return True
        elif station.wmo == wmo_or_place:
            return True
    return False

def wmo_or_place_to_station(wmo_or_place):
    wmo_or_place = wmo_or_place.lower()
    for station in stations.lst:
        if station.place.lower() == wmo_or_place:
            return station
        elif station.wmo == wmo_or_place:
            return station
    return station.Station()

def station_in_list( station, lst ):
    for check in lst:
        if check.wmo == station.wmo and \
           check.place.lower() == station.place.lower():
           return True 
    return False 

def lst_stations_map():
    '''Get all the stations available in the data dayvalues text map'''
    lst = []
    with threading.Lock():
        if os.path.exists( cfg.dir_dayvalues_txt ):
            lst_paths = [os.path.join(cfg.dir_dayvalues_txt, f) for f in os.listdir(cfg.dir_dayvalues_txt)]
            for station in stations.lst:
                if station.data_txt_path in lst_paths:  # Extra check if in selected default list too
                    lst.append(station)
    return lst
