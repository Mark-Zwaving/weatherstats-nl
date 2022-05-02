# -*- coding: utf-8 -*-
'''Library contains functions for converting data'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.4.4"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import config as cfg
import sources.view.text as text

# Convert temperatures
celsius_to_fahrenheit = lambda c:   float(c) * 1.8 + 32.0
celsius_to_kelvin     = lambda c:   float(c) + 273.15
fahrenheit_to_celsius = lambda f: ( float(f) - 32.0 ) / 1.8
fahrenheit_to_kelvin  = lambda f: ( float(f) + 459.67 ) / 1.8
kelvin_to_celsius     = lambda k:   float(k) - 273.15
kelvin_to_fahrenheit  = lambda k:   float(k) * 1.8 - 459.67

# Convert distance/length
inch_to_cm     = lambda i:   float(i) * 2.54
cm_to_inch     = lambda c:   float(c) / 2.54
feet_to_cm     = lambda f:   float(f) * 30.48
cm_to_feet     = lambda c:   float(c) / 30.48
inc_to_feet    = lambda i:   float(i) / 12.0
feet_to_inch   = lambda f:   float(f) * 12.0
yard_to_feet   = lambda y:   float(y) * 3.0
feet_to_yard   = lambda y:   float(y) / 3.0
mile_to_km     = lambda m:   float(m) * 1.60930
km_to_mile     = lambda k:   float(k) / 1.60930
nautmile_to_km = lambda s:   float(s) * 1.85  # Nautical miles/seamiles
km_to_nautmile = lambda f:   float(f) / 1.85
yard_to_cm     = lambda y:   float(y) * 91.44
cm_to_yard     = lambda c:   float(c) / 91.44

# Default dpi in matplotlib is 100. See cfg.py
pixel_to_inch  = lambda p: float(p) / float(cfg.plot_dpi)

def ms_to_bft( ms ):
    i = int(ms)
    if   i <   3: return '0'
    elif i <  16: return '1'
    elif i <  34: return '2'
    elif i <  55: return '3'
    elif i <  80: return '4'
    elif i < 108: return '5'
    elif i < 139: return '6'
    elif i < 172: return '7'
    elif i < 208: return '8'
    elif i < 245: return '9'
    elif i < 285: return '10'
    elif i < 327: return '11'
    else: return '12'

def octa_to_txt(octa):
    i = int(octa)
    if   0 == i: return text.tr('Onbewolkt')
    elif 1 == i: return text.tr('Vrijwel onbewolkt')
    elif 2 == i: return text.tr('Licht bewolkt')
    elif 3 == i: return text.tr('Half bewolkt')
    elif 4 == i: return text.tr('Half bewolkt')
    elif 5 == i: return text.tr('Half tot zwaar bewolkt')
    elif 6 == i: return text.tr('Zwaar bewolkt')
    elif 7 == i: return text.tr('Vrijwel geheel bewolkt')
    elif 8 == i: return text.tr('Geheel bewolkt')
    elif 9 == i: return text.tr('Bovenlucht onzichtbaar')
    else: return ''

def deg_to_txt(deg):
    i = int(deg)
    if   i ==  0:  return text.tr('stil')
    elif i  < 22:  return text.tr('NOORD')
    elif i  < 30:  return text.tr('NOORDNOORDOOST')
    elif i  < 67:  return text.tr('NOORDOOST')
    elif i  < 112: return text.tr('OOST')
    elif i  < 157: return text.tr('ZUIDOOST')
    elif i  < 202: return text.tr('ZUID')
    elif i  < 247: return text.tr('ZUIDWEST')
    elif i  < 292: return text.tr('WEST')
    elif i  < 337: return text.tr('NOORDWEST')
    elif i  < 360: return text.tr('NOORD')
    elif i == 990: return text.tr('veranderlijk')
    else: return ''

def ms_to_txt( ms ):
    i = int(ms)
    if   i <   3: return text.tr('windstil')
    elif i <  16: return text.tr('zwakke wind')
    elif i <  34: return text.tr('zwakke wind')
    elif i <  55: return text.tr('matige wind')
    elif i <  80: return text.tr('matige wind')
    elif i < 108: return text.tr('vrij krachtige wind')
    elif i < 139: return text.tr('krachtige wind')
    elif i < 172: return text.tr('harde wind')
    elif i < 208: return text.tr('stormachtige wind')
    elif i < 245: return text.tr('storm')
    elif i < 285: return text.tr('zware storm')
    elif i < 327: return text.tr('zeer zware storm')
    else: return text.tr('orkaan')

def vvn_to_txt( vvn ):
    i = int(vvn)
    # 1:100-200 m ... 49:4900-5000 m
    if vvn <= 49:
        return f'{i*100} - {(i+1)*100}' + text.tr('meter')
    # 50:5-6 km
    elif vvn == 50:
        return '5 - 6' + text.tr('km')
    # 56:6-7 km ... 79:29-30 km
    elif vvn <= 79:
        return f'{i-50} - {i-49}' + text.tr('km')
    #  80:30-35 km ... 87:65-70 km
    elif vvn  < 89:
        return '{(i-80)*5+30} - {(i-79)*5+30}' + text.tr('km')
    # 89: >70 km
    elif vvn == 89:
        return '< 70' + text.tr('km')
    else:
        return ''

def timespan1hour(h):
    i = int(h)
    return f'{i-1} - {i}' + text.tr('hour')

def timespan6hour(u):
    i = int(u)
    if   i ==  6:
        s  = '0 - 6'
    elif i == 12:
        s  = '6 - 12'
    elif i == 18:
        s  = '12 - 18'
    elif i == 24:
        s  = '18 - 24'
    else:
        s  = ''

    return s + text.tr('hour')
