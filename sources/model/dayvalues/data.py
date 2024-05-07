# -*- coding: utf-8 -*-
'''Processes data dayvalues from the knmi'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.1.5'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import numpy as np
import sources.view.text as text
import sources.model.check as chk
import sources.model.convert as convert

# Dayvalues data KNMI / Keys for dayvalues
STN      =  0 # WMO number for nl weatherstation
YYYYMMDD =  1 # Date (YYYY=year MM=month DD=day)
DDVEC    =  2 # Vector mean wind direction in degrees (360=north, 90=east, 180=south, 270=west, 0=calm/variable)
FHVEC    =  3 # Vector mean windspeed (in 0.1 m/s)
FG       =  4 # Daily mean windspeed (in 0.1 m/s)
FHX      =  5 # Maximum hourly mean windspeed (in 0.1 m/s)
FHXH     =  6 # Hourly division in which FHX was measured
FHN      =  7 # Minimum hourly mean windspeed (in 0.1 m/s)
FHNH     =  8 # Hourly division in which FHN was measured
FXX      =  9 # Maximum wind gust (in 0.1 m/s)
FXXH     = 10 # Hourly division in which FXX was measured
TG       = 11 # Daily mean temperature in (0.1 degrees Celsius)
TN       = 12 # Minimum temperature (in 0.1 degrees Celsius)
TNH      = 13 # Hourly division in which TN was measured
TX       = 14 # Maximum temperature (in 0.1 degrees Celsius)
TXH      = 15 # Hourly division in which TX was measured
T10N     = 16 # Minimum temperature at 10 cm above surface (in 0.1 degrees Celsius)
T10NH    = 17 # 6-hourly division in which T10N was measured; 6=0-6 UT, 12=6-12 UT, 18=12-18 UT, 24=18-24 UT
SQ       = 18 # Sunshine duration (in 0.1 hour) calculated from global radiation (-1 for <0.05 hour)
SP       = 19 # Percentage of maximum potential sunshine duration
Q        = 20 # Global radiation (in J/cm2)
DR       = 21 # Precipitation duration (in 0.1 hour)
RH       = 22 # Daily precipitation amount (in 0.1 mm) (-1 for <0.05 mm)
RHX      = 23 # Maximum hourly precipitation amount (in 0.1 mm) (-1 for <0.05 mm)
RHXH     = 24 # Hourly division in which RHX was measured
PG       = 25 # Daily mean sea level pressure (in 0.1 hPa) calculated from 24 hourly values
PX       = 26 # Maximum hourly sea level pressure (in 0.1 hPa)
PXH      = 27 # Hourly division in which PX was measured
PN       = 28 # Minimum hourly sea level pressure (in 0.1 hPa)
PNH      = 29 # Hourly division in which PN was measured
VVN      = 30 # Minimum visibility; 0: <100 m, 1:100-200 m, 2:200-300 m,..., 49:4900-5000 m, 50:5-6 km, 56:6-7 km, 57:7-8 km,..., 79:29-30 km, 80:30-35 km, 81:35-40 km,..., 89: >70 km)
VVNH     = 31 # Hourly division in which VVN was measured
VVX      = 32 # Maximum visibility; 0: <100 m, 1:100-200 m, 2:200-300 m,..., 49:4900-5000 m, 50:5-6 km, 56:6-7 km, 57:7-8 km,..., 79:29-30 km, 80:30-35 km, 81:35-40 km,..., 89: >70 km)
VVXH     = 33 # Uurvak waarin VVX is gemeten / Hourly division in which VVX was measured
NG       = 34 # Mean daily cloud cover (in octants, 9=sky invisible)
UG       = 35 # Daily mean relative atmospheric humidity (in percents)
UX       = 36 # Maximum relative atmospheric humidity (in percents)
UXH      = 37 # Hourly division in which UX was measured
UN       = 38 # Minimum relative atmospheric humidity (in percents)
UNH      = 39 # Hourly division in which UN was measured
EV24     = 40 # Potential evapotranspiration (Makkink) (in 0.1 mm)

knmi_entities = [
    'STN', 'YYYYMMDD', 'DDVEC', 'FHVEC', 'FG', 'FHX', 'FHXH', 'FHN', 'FHNH', 'FXX',
    'FXXH', 'TG', 'TN', 'TNH', 'TX', 'TXH', 'T10N', 'T10NH', 'SQ', 'SP',
    'Q', 'DR', 'RH', 'RHX', 'RHXH', 'PG', 'PX', 'PXH', 'PN', 'PNH',
    'VVN', 'VVNH', 'VVX', 'VVXH', 'NG', 'UG', 'UX', 'UXH', 'UN', 'UNH',
    'EV24'
]

knmi_time_entities = [
    'TXH', 'TNH', 'T10NH', 'FHXH', 'FHNH', 'FXXH', 'RHXH', 
    'PXH', 'PNH', 'VVNH', 'VVXH', 'UXH', 'UNH'
]

def correct(value, entity, format='knmi'):
    '''Old fn: df'''
    f, e = float(value), entity.upper()
    if format == 'knmi':
        if e in ['TX', 'TG', 'TN', 'FG', 'FHX', 'FHN', 'FXX', 'DR',
                'FHVEC', 'SQ', 'RH', 'RHX', 'PG', 'PX', 'PN', 'EV24' ]:
            return f * 10.0
        elif e in ['YYYYMMDD', 'STN', 'DDVEC', 'SP', 'Q', 'VVN', 'VVX', 'NG', 'UG',
                'UX', 'UN', 'FHXH', 'FHNH', 'FXXH', 'TNH', 'TXH', 'T10NH',
                'RHXH', 'PXH', 'PNH', 'VVNH', 'VVXH', 'UXH', 'UNH' ]:
            return f
    return f

def is_time_entity(entity, format='knmi'):
    entity = entity.upper()
    if entity in knmi_time_entities:
        return True 
    return False 

def entity_to_t_entity(entity):
    e, t_entity = entity.upper(), cfg.e
    if   e == 'TX': t_entity = 'TXH'
    elif e == 'TN': t_entity = 'TNH'
    elif e == 'T10N': t_entity = 'T10NH'
    elif e == 'FHX': t_entity = 'FHXH'
    elif e == 'FHN': t_entity = 'FHNH'
    elif e == 'FXX': t_entity = 'FXXH'
    elif e == 'RHX': t_entity = 'RHXH'
    elif e == 'PX': t_entity = 'PXH'
    elif e == 'PN': t_entity = 'PNH'
    elif e == 'VVN': t_entity = 'VVNH'
    elif e == 'VVX': t_entity = 'VVXH'
    elif e == 'UX': t_entity = 'UXH'
    elif e == 'UN': t_entity = 'UNH'

    return t_entity.lower()

def check(val):
    ok = True
    if not chk.is_float(val):
        ok = False
    elif chk.is_nan(val):
        ok = False
    elif val == cfg.knmi_dayvalues_dummy_val:
        ok = False
    return ok

def user_to_raw(val, entity):
    '''Function turns data from input to raw values'''
    if check(val) == False: return val
    f, e = float(val), entity.strip().lower()

    # Exception for -1 in rh,rhx and sq
    if f == -1.0 and (e in ['rh', 'rhx', 'sq']):  return cfg.knmi_dayvalues_low_measure_val * 10.0
    # Indexes
    elif e in text.lst_helmmann + text.lst_heat_ndx + text.lst_frost_sum: return f * 10.0
    elif e in text.lst_ijnsen: return f
    # Temperatures
    elif e in [ 'tx', 'tn', 'tg', 't10n' ]: return f * 10.0
    # Airpressure
    elif e in [ 'pg', 'pn', 'px' ]: return f * 10.0
    # Radiation
    elif e in [ 'q' ]: return f * 10.0
    # Percentages
    elif e in [ 'ug', 'ux', 'un', 'sp' ]: return f
    # Time hours
    elif e in [ 'fhxh', 'fhnh', 'fxxh', 'tnh', 'txh', 'rhxh',
                'pxh', 'vvnh', 'vvxh', 'uxh', 'unh', 'pnh' ]: return f
    # Time 6 hours
    elif e in [ 't10nh' ]: return f
    # CLouds cover/octants
    elif e in [ 'ng' ]: return f
    # Wind
    elif e in [ 'fhvec','fg','fhx','fhn','fxx' ]: return f * 10.0
    # Evapotranspiration
    elif e in [ 'ev24', 'rh', 'rhx' ]: return f * 10.0
    # Duration hours
    elif e in [ 'sq', 'dr' ]: return f * 10.0
    # Wind direction
    elif e in  [ 'ddvec' ]:  return f
    # View distance
    elif e in [ 'vvn', 'vvx' ]:  return f
    return f  # No need to correct

def process_value(val, entity):
    '''Function turns data from etmgeg into the real values'''
    if not check(val):
        return val

    f = float(val)
    e = entity.strip().lower()

    # Exception for -1 in rh,rhx and sq
    if f == -1.0 and (e in ['rh', 'rhx', 'sq']):
        return cfg.knmi_dayvalues_low_measure_val

    # Indexes
    elif e in text.lst_helmmann + text.lst_heat_ndx + text.lst_frost_sum:
        return round(f / 10.0, 1)

    elif e in text.lst_ijnsen:
        return round(f)

    # Temperatures
    elif e in [ 'tx', 'tn', 'tg', 't10n' ]:
        return round(f / 10.0, 1)

    # Airpressure
    elif e in [ 'pg', 'pn', 'px' ]:
        return round(f / 10.0, 1)

    # Radiation
    elif e in [ 'q' ]:
        return round(f / 10.0, 1)

    # Percentages
    elif e in [ 'ug', 'ux', 'un', 'sp' ]:
        return round(f)

    # Time hours
    elif e in [ 'fhxh', 'fhnh', 'fxxh', 'tnh', 'txh', 'rhxh',
                'pxh', 'vvnh', 'vvxh', 'uxh', 'unh', 'pnh' ]:
        return round(f)

    # Time 6 hours
    elif e in [ 't10nh' ]:
        return round(f)

    # CLouds cover/octants
    elif e in [ 'ng' ]:
        return round(f)

    # Wind
    elif e in [ 'fhvec','fg','fhx','fhn','fxx' ]:
        return round(f / 10.0, 1)

    # Evapotranspiration
    elif e in [ 'ev24', 'rh', 'rhx' ]:
        return round(f / 10.0, 1)

    # Duration hours
    elif e in [ 'sq', 'dr' ]:
        return round(f / 10.0, 1)

    # Wind direction
    elif e in  [ 'ddvec' ]:
        return round(f)

    # View distance
    elif e in [ 'vvn', 'vvx' ]:
        return round(f)

    # Happens for dummy values
    return f  

def is_operator(op):
    return op.lower() in text.lst_op 

def is_entity( entity, format='knmi'):
    '''Check if a value is a dayvalue entity'''
    lst = [] 
    if format.lower() == 'knmi': 
        lst = knmi_entities

    return entity.upper() in lst

def key_to_entity(key, format='knmi'):
    if format.lower() == 'knmi': 
        lst = knmi_entities

    return lst[key]

def column(entity, format='knmi'):
    '''Get index by text from the array entities'''
    lst, ent = [], entity.upper()

    if format.lower() == 'knmi':
        lst = knmi_entities

    for key, el in enumerate(lst):
        if el == ent:
            return key 

    return -1

def list_ent( data, ent ):
    col = column(ent)
    return data[:,col]

def ents( day, format='knmi' ):
    stn   = convert.fl_to_s( day[STN] )
    ymd   = convert.fl_to_s( day[YYYYMMDD] )
    ddvec = text.fix_for_entity(day[DDVEC], key_to_entity(DDVEC))
    fhvec = text.fix_for_entity(day[FHVEC], key_to_entity(FHVEC))
    fg    = text.fix_for_entity(day[FG],  key_to_entity(FG))
    fhx   = text.fix_for_entity(day[FHX], key_to_entity(FHX))
    fhxh  = text.fix_for_entity(day[FHXH], key_to_entity(FHXH))
    fhn   = text.fix_for_entity(day[FHN], key_to_entity(FHN))
    fhnh  = text.fix_for_entity(day[FHNH], key_to_entity(FHNH))
    fxx   = text.fix_for_entity(day[FXX], key_to_entity(FXX))
    fxxh  = text.fix_for_entity(day[FXXH], key_to_entity(FXXH))
    tg    = text.fix_for_entity(day[TG], key_to_entity(TG))
    tn    = text.fix_for_entity(day[TN], key_to_entity(TN))
    tnh   = text.fix_for_entity(day[TNH], key_to_entity(TNH))
    tx    = text.fix_for_entity(day[TX], key_to_entity(TX))
    txh   = text.fix_for_entity(day[TXH], key_to_entity(TXH))
    t10n  = text.fix_for_entity(day[T10N], key_to_entity(T10N))
    t10nh = text.fix_for_entity(day[T10NH], key_to_entity(T10NH))
    sq    = text.fix_for_entity(day[SQ], key_to_entity(SQ))
    sp    = text.fix_for_entity(day[SP], key_to_entity(SP))
    q     = text.fix_for_entity(day[Q], key_to_entity(Q))
    dr    = text.fix_for_entity(day[DR], key_to_entity(DR))
    rh    = text.fix_for_entity(day[RH], key_to_entity(RH))
    rhx   = text.fix_for_entity(day[RHX], key_to_entity(RHX))
    rhxh  = text.fix_for_entity(day[RHXH], key_to_entity(RHXH))
    pg    = text.fix_for_entity(day[PG], key_to_entity(PG))
    px    = text.fix_for_entity(day[PX], key_to_entity(PX))
    pxh   = text.fix_for_entity(day[PXH], key_to_entity(PXH))
    pn    = text.fix_for_entity(day[PN], key_to_entity(PN))
    pnh   = text.fix_for_entity(day[PNH], key_to_entity(PNH))
    vvn   = text.fix_for_entity(day[VVN], key_to_entity(VVN))
    vvnh  = text.fix_for_entity(day[VVNH], key_to_entity(VVNH))
    vvx   = text.fix_for_entity(day[VVX], key_to_entity(VVX))
    vvxh  = text.fix_for_entity(day[VVXH], key_to_entity(VVXH))
    ng    = text.fix_for_entity(day[NG], key_to_entity(NG))
    ug    = text.fix_for_entity(day[UG], key_to_entity(UG))
    ux    = text.fix_for_entity(day[UX], key_to_entity(UX))
    uxh   = text.fix_for_entity(day[UXH], key_to_entity(UXH))
    un    = text.fix_for_entity(day[UN], key_to_entity(UN))
    unh   = text.fix_for_entity(day[UNH], key_to_entity(UNH))
    ev24  = text.fix_for_entity(day[EV24], key_to_entity(EV24))

    return ( stn, ymd, ddvec, fhvec, fg, fhx,
             fhxh, fhn, fhnh, fxx, fxxh, tg,
             tn, tnh, tx, txh, t10n, t10nh,
             sq, sp, q, dr, rh, rhx,
             rhxh, pg, px, pxh, pn, pnh,
             vvn, vvnh, vvx, vvxh, ng, ug,
             ux, uxh, un, unh, ev24 )

def normalize( day, format='knmi' ):
    stn   = int( day[STN] )
    ymd   = int( day[YYYYMMDD] )
    ddvec = day[DDVEC] / 10.0
    fhvec = day[FHVEC] / 10.0
    fg    = day[FG] / 10.0
    fhx   = day[FHX] / 10.0
    fhxh  = day[FHXH]
    fhn   = day[FHN] / 10.0
    fhnh  = day[FHNH]
    fxx   = day[FXX] / 10.0
    fxxh  = day[FXXH]
    tg    = day[TG] / 10.0
    tn    = day[TN] / 10.0
    tnh   = day[TNH]
    tx    = day[TX] / 10.0
    txh   = day[TXH] / 10.0
    t10n  = day[T10N] / 10.0
    t10nh = day[T10NH]
    sq    = day[SQ] / 10.0
    sp    = day[SP]
    q     = day[Q]
    dr    = day[DR]
    rh    = day[RH]
    rhx   = day[RHX]
    rhxh  = day[RHXH]
    pg    = day[PG] / 10.0
    px    = day[PX] / 10.0
    pxh   = day[PXH]
    pn    = day[PN] / 10.0
    pnh   = day[PNH]
    vvn   = day[VVN] / 10.0
    vvnh  = day[VVNH]
    vvx   = day[VVX] / 10.0
    vvxh  = day[VVXH]
    ng    = day[NG]
    ug    = day[UG]
    ux    = day[UX]
    uxh   = day[UXH]
    un    = day[UN]
    unh   = day[UNH]
    ev24  = day[EV24] / 10.0

    return ( stn, ymd, ddvec, fhvec, fg, fhx,
             fhxh, fhn, fhnh, fxx, fxxh, tg,
             tn, tnh, tx, txh, t10n, t10nh,
             sq, sp, q, dr, rh, rhx,
             rhxh, pg, px, pxh, pn, pnh,
             vvn, vvnh, vvx, vvxh, ng, ug,
             ux, uxh, un, unh, ev24 )

def date_by_val(data, val, ent):
    ymd, row, col, key_ent = cfg.e, 0, 1, column(ent)

    for ndx, el in np.ndenumerate(data):  # ndx (0,0)
        if ndx[col] == key_ent: # Check only searched indexes
            if el == val: # Check for correct value
                ymd = str(int(data[ndx[row]][YYYYMMDD]))
                break

    return ymd
