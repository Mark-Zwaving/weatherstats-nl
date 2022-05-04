# -*- coding: utf-8 -*-
''' Library contains class to store knmi data
    Here you can make your own data lst
    Function for handlin stationsdata
'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright 2020 (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU Lesser General Public License (LGPL)'
__version__    =  '0.1.8'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import os, numpy as np, threading
import common.control.fio as fio

class Station:
    '''Class defines a (knmi) weatherstation'''
    def __init__(self, wmo = ' ', place = ' ', province = ' ', country='', info = ' ', format='knmi'):
        self.wmo      = wmo
        self.place    = place
        self.province = province
        self.state    = province
        self.country  = country
        self.info     = info
        self.format   = format

        if self.format == 'knmi':
            self.data_format        = cfg.knmi_data_format     # For data standards
            self.data_skip_header   = cfg.knmi_dayvalues_skip_header
            self.data_skip_footer   = cfg.knmi_dayvalues_skip_footer
            self.data_dummy_val     = cfg.knmi_dayvalues_dummy_val
            self.data_missing       = cfg.knmi_dayvalues_missing_val
            self.data_notification  = cfg.knmi_dayvalues_notification
            self.data_delimiter     = cfg.knmi_dayvalues_delimiter
            self.data_zip_file      = f'etmgeg_{self.wmo}.zip'
            self.data_txt_file      = f'etmgeg_{self.wmo}.txt'
            self.data_url = cfg.knmi_dayvalues_url.format(self.wmo)
        elif self.format == 'dwd':
            pass

        self.data_zip_path      = os.path.join(cfg.dir_dayvalues_zip, self.data_zip_file)
        self.data_txt_path      = os.path.join(cfg.dir_dayvalues_txt, self.data_txt_file)
        self.data_comments_sign = cfg.data_comment_sign
        self.data_download      = True

# Make list with stations
lst = []
# Add KNMI weatherstations
# Extended example ie Maastricht,
Maastricht = Station('380', 'Maastricht', 'Limburg', 'Netherlands')  # Create Station
Maastricht.data_skip_header  = cfg.knmi_dayvalues_skip_header  # (=49, KNMI)
Maastricht.data_dummy_val    = cfg.knmi_dayvalues_dummy_val
Maastricht.data_empthy_val   = cfg.knmi_dayvalues_missing_val
Maastricht.data_notification = cfg.knmi_dayvalues_notification
Maastricht.data_format       = cfg.knmi_data_format
Maastricht.data_zip_path     = os.path.join( cfg.dir_dayvalues_zip, 'etmgeg_380.zip' )
Maastricht.data_txt_path     = os.path.join( cfg.dir_dayvalues_txt, 'etmgeg_380.txt' )
Maastricht.data_dayvalus_url = r'https://cdn.knmi.nl/knmi/map/page/klimatologie/gegevens/daggegevens/etmgeg_380.zip'
lst.append( Maastricht ) # Add to list

# For the rest the url and the files and the rest are automaticly updated
# Just put in the right WMO number for the station or make one for yourself
lst.append(Station('215', 'Voorschoten', 'Zuid-Holland', ''))
lst.append(Station('235', 'De Kooy', 'Noord-Holland', ''))
lst.append(Station('240', 'Schiphol', 'Noord-Holland', ''))
lst.append(Station('249', 'Berkhout', 'Noord-Holland', ''))
lst.append(Station('251', 'Hoorn Terschelling', 'Friesland', ''))
lst.append(Station('257', 'Wijk aan Zee', 'Noord-Holland', ''))
lst.append(Station('260', 'De Bilt', 'Utrecht', ''))
# list.append(Station('265', 'Soesterberg', 'Utrecht', '')) # Read error
lst.append(Station('267', 'Stavoren','Friesland', ''))
lst.append(Station('269', 'Lelystad','Flevoland', ''))
lst.append(Station('270', 'Leeuwarden','Friesland', ''))
lst.append(Station('273', 'Marknesse', 'Flevoland', ''))
lst.append(Station('275', 'Deelen', 'Gelderland', ''))
lst.append(Station('277', 'Lauwersoog', 'Groningen', ''))
lst.append(Station('278', 'Heino', 'Overijssel', ''))
lst.append(Station('279', 'Hoogeveen', 'Drenthe', ''))
lst.append(Station('280', 'Eelde', 'Drenthe', ''))
lst.append(Station('283', 'Hupsel', 'Gelderland', ''))
lst.append(Station('286', 'Nieuw Beerta', 'Groningen', ''))
lst.append(Station('290', 'Twenthe', 'Overijssel', ''))
lst.append(Station('310', 'Vlissingen', 'Zeeland', ''))
lst.append(Station('319', 'Westdorpe', 'Zeeland', ''))
lst.append(Station('323', 'Wilhelminadorp', 'Zeeland', ''))
lst.append(Station('330', 'Hoek van Holland', 'Zuid-Holland', ''))
lst.append(Station('340', 'Woensdrecht', 'Noord-Brabant', ''))
lst.append(Station('344', 'Rotterdam', 'Zuid-Holland', ''))
lst.append(Station('348', 'Cabauw Mast', 'Utrecht', ''))
lst.append(Station('350', 'Gilze-Rijen', 'Noord-Brabant', ''))
lst.append(Station('356', 'Herwijnen', 'Gelderland', ''))
lst.append(Station('370', 'Eindhoven', 'Noord-Brabant', ''))
lst.append(Station('375', 'Volkel', 'Noord-Brabant', ''))
lst.append(Station('377', 'Ell', 'Limburg', ''))
lst.append(Station('391', 'Arcen', 'Limburg', ''))
lst.append(Station('242', 'Vlieland', 'Friesland', ''))

# Below an example how to add your your (own) station
# Rules for your data file.
# 1. Keep knmi structure and order. So restructure data in a KNMI way
# 2. '     ' = 5 spaces or data_dummy_value = 99999 for unregistered data
#  KNMI DATA Structure:
#  STN,YYYYMMDD,DDVEC,FHVEC,   FG,  FHX, FHXH,  FHN, FHNH,  FXX, FXXH,   TG,   TN,  TNH,
#   TX,  TXH, T10N,T10NH,   SQ,   SP,    Q,   DR,   RH,  RHX, RHXH,   PG,   PX,  PXH,
#   PN,  PNH,  VVN, VVNH,  VVX, VVXH,   NG,   UG,   UX,  UXH,   UN,  UNH, EV24
# Borkum = Station()  # Create Station
# Borkum.wmo                    =  '-1'
# Borkum.place                  =  'Emden'
# Borkum.province               =  'Niedersaksen'
# Borkum.country                =  'Deutschland'
# Borkum.dayvalues_skip_rows    =  1
# Borkum.dayvalues_dummy_val    =  knmi_dayvalues_dummy_val
# Borkum.dayvalues_empthy_val   =  knmi_dayvalues_empthy_val
# Borkum.dayvalues_notification =  'source copyright @ Borkum'
# Borkum.dayvalues_dir_dayvalues =  os.path.join( dir_data, 'borkum' ) # ie. Create map borkum in the data map
# Borkum.dayvalues_file_zip      =  os.path.join( Borkum.dir_dayvalues, 'tag.zip' )
# Borkum.dayvalues_file_txt      =  os.path.join( Borkum.dir_dayvalues, 'tag.txt' )
# Borkum.data_url                =  r'https://my.borkum.de/data/tag.zip'
# lst.append( Borkum ) # Add to list

# Sort station list on place name, using numpy
lst = np.array( sorted( np.array(lst), key=lambda station: station.place ) ).tolist()

################################################################################
# Functions

lst_wmo  = lambda: [station.wmo  for station in lst]
lst_name = lambda: [station.name for station in lst]

def lst_wmo_check():
    pass

def lst_stations_in_map():
    '''Get all the stations available in the data dayvalues text map'''
    lst_result, dir = [], cfg.dir_dayvalues_txt
    with threading.Lock():
        if os.path.exists(dir):
            lst_files = fio.lst_files_dir(dir, extensions=['txt'], verbose=False)
            for station in lst:
                # Extra check if in selected default list too
                if station.data_txt_path in lst_files:
                        lst_result.append(station)
    return lst_result

def wmo_to_station(wmo):
    '''Get station object based on wmo'''
    if wmo_in_lst(wmo, lst):
        for station in lst:
            if station.wmo == wmo:
                return station
    return False

def name_to_station(name):
    if name_in_lst(name):
        name = name.lower()
        for station in lst:
            if station.name.lower() == name:
                return station
    return False

def wmo_name_to_station(wmo_name):
    if name_in_lst(wmo_name):
        name = wmo_name.lower()
        for station in lst:
            if station.place.lower() == name:
                return station
    if wmo_in_lst(wmo_name):
        for station in lst:
            if station.wmo == wmo_name:
                return station
    return False

def wmo_to_name(wmo, l=False):
    if wmo_in_lst(wmo):
        if l == False:
            l = lst_stations_in_map()
        for s in l:
            if s.wmo == wmo:
                return s.place
    return wmo

def wmo_to_province(wmo, l=False):
    if wmo_in_lst(wmo):
        if l == False:
            l = lst_stations_in_map()
        for s in l:
            if s.wmo == wmo:
                return s.province
    return wmo

def name_in_lst(name, l=False):
    if name:
        name = name.lower()
        if l == False:
            l = lst_stations_in_map()
        for s in l:
            if s.place.lower() == name:
                return True
    return False

def wmo_in_lst(wmo, l=False):
    if wmo:
        if l == False:
            l = lst_stations_in_map()
        for s in l:
            if s.wmo == wmo:
                return True
    return False

def name_wmo_in_lst(wmo_name, l=False):
    if wmo_name:
        if l == False:
            l = lst_stations_in_map()
        for s in l:
            if wmo_name.lower() in [s.wmo, s.place.lower()]:
                return True
    return False

def find_by_name(name, l=False):
    if name:
        n = name.lower()
        if l == False:
            l = lst_stations_in_map()
        for s in l:
            if s.place.lower() == n:
                return s
    return False

def find_by_wmo( wmo, l=False):
    if wmo:
        n = wmo.lower()
        if l == False:
            l = lst_stations_in_map()
        for s in l:
            if s.wmo.lower() == n:
                return s
    return False

def find_by_wmo_or_name(name_or_wmo, l=False):
    if name_or_wmo:
        name = find_by_name( name_or_wmo, l )
        if name != False:
            return name

        wmo = find_by_wmo( name_or_wmo, l )
        if wmo != False:
            return wmo

    return False

def check_if_station_already_in_list( station, l ):
    return station.wmo in l
    
