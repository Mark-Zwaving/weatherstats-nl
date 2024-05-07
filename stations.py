# -*- coding: utf-8 -*-
''' Library contains class to store knmi data
    Here you can make your own data lst
    Function for handlin stationsdata
'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright 2020 (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.1.8'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import os, numpy as np

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
        self.min_date = ''
        self.max_date = ''
        self.data_download = True

        if self.format == 'knmi':
            self.data_format        = cfg.knmi_data_format     # For data standards
            self.data_skip_header   = cfg.knmi_dayvalues_skip_header
            self.data_skip_footer   = cfg.knmi_dayvalues_skip_footer
            self.data_dummy         = cfg.knmi_dayvalues_dummy_val
            self.data_missing       = cfg.knmi_dayvalues_missing_val
            self.data_notification  = cfg.knmi_dayvalues_notification
            self.data_delimiter     = cfg.knmi_dayvalues_delimiter
            self.data_zip_file      = f'etmgeg_{self.wmo}.zip'
            self.data_txt_file      = f'etmgeg_{self.wmo}.txt'
            self.data_url = cfg.knmi_dayvalues_url.format(self.wmo)

        elif self.format == 'dwd': # TODO
            pass

        self.data_zip_path      = os.path.join(cfg.dir_dayvalues_zip, self.data_zip_file)
        self.data_txt_path      = os.path.join(cfg.dir_dayvalues_txt, self.data_txt_file)
        self.data_comments_sign = cfg.data_comment_sign

# Make list with stations
lst = []
# Add KNMI weatherstations
# Extended example ie Maastricht,
Maastricht = Station('380', 'Maastricht', 'Limburg', 'Netherlands')  # Create Station
Maastricht.data_skip_header  = cfg.knmi_dayvalues_skip_header  # (=49, KNMI)
Maastricht.data_dummy        = cfg.knmi_dayvalues_dummy_val
Maastricht.data_missing      = cfg.knmi_dayvalues_missing_val
Maastricht.data_notification = cfg.knmi_dayvalues_notification
Maastricht.data_format       = cfg.knmi_data_format
Maastricht.data_zip_path     = os.path.join( cfg.dir_dayvalues_zip, 'etmgeg_380.zip' )
Maastricht.data_txt_path     = os.path.join( cfg.dir_dayvalues_txt, 'etmgeg_380.txt' )
Maastricht.data_url          = r'https://cdn.knmi.nl/knmi/map/page/klimatologie/gegevens/daggegevens/etmgeg_380.zip'
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

# Sort station list on place name, using numpy
lst = np.array( sorted( np.array(lst), key=lambda station: station.place ) ).tolist()

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
