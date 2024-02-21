# -*- coding: utf-8 -*-
'''Processes data dayvalues from the knmi'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 3 - GPLv3'
__version__    =  '0.1.4'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg, stations
import threading, time, numpy as np
import sources.view.text as text
import sources.model.select as select
import sources.model.utils as utils
import sources.view.console as cnsl
import sources.control.fio as fio
import sources.model.validate as validate
import sources.model.ymd as ymd
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
    if not utils.is_float(val):
        ok = False
    elif val == cfg.knmi_dayvalues_dummy_val:
        ok = False
    return ok

def process_value(val, entity):
    '''Function turns data from etmgeg into the real values'''
    if check(val) == False:
        return val

    f = float(val)
    e = entity.strip().lower()

    # Exception for -1 in rh,rhx and sq
    if f == -1.0 and (e in ['rh', 'rhx', 'sq']):
        return cfg.knmi_dayvalues_low_measure_val

    # Indexes
    elif e in text.lst_helmmann + text.lst_heat_ndx + text.lst_frost_sum:
        return f / 10.0

    elif e in text.lst_ijnsen:
        return f

    # Temperatures
    elif e in [ 'tx', 'tn', 'tg', 't10n' ]:
        return f / 10.0

    # Airpressure
    elif e in [ 'pg', 'pn', 'px' ]:
        return f / 10.0

    # Radiation
    elif e in [ 'q' ]:
        return f / 10.0

    # Percentages
    elif e in [ 'ug', 'ux', 'un', 'sp' ]:
        return f

    # Time hours
    elif e in [ 'fhxh', 'fhnh', 'fxxh', 'tnh', 'txh', 'rhxh',
                'pxh', 'vvnh', 'vvxh', 'uxh', 'unh', 'pnh' ]:
        return f

    # Time 6 hours
    elif e in [ 't10nh' ]:
        return f

    # CLouds cover/octants
    elif e in [ 'ng' ]:
        return f

    # Wind
    elif e in [ 'fhvec','fg','fhx','fhn','fxx' ]:
        return f / 10.0

    # Evapotranspiration
    elif e in [ 'ev24', 'rh', 'rhx' ]:
        return f / 10.0

    # Duration hours
    elif e in [ 'sq', 'dr' ]:
        return f / 10.0

    # Wind direction
    elif e in  [ 'ddvec' ]:
        return f

    # View distance
    elif e in [ 'vvn', 'vvx' ]:
        return f

    return f  # Happens for dummy values

def rounding(val, entity):
    '''Function turns data from etmgeg into the real values'''
    if check(val) == False:
        return val

    e = entity.strip().lower()
    f = process_value(val, e)

    # Indexes
    if e in ['heat_ndx', 'heatndx', 'hndx', 'hmann', 'hellmann', 'ijnsen',
             'frost_sum', 'frostsum', 'fsum', 'frost_som', 'frostsom', 'fsom']:
        return round(f,1)

    # Temperatures
    elif e in [ 'tx', 'tn', 'tg', 't10n' ]:
        return round(f,1)

    # Airpressure
    elif e in [ 'pg', 'pn', 'px' ]:
        return round(f,1)

    # Radiation
    elif e in [ 'q' ]:
        return round(f,1)

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
        return round(f,1)

    # Evapotranspiration
    elif e in [ 'ev24', 'rh', 'rhx' ]:
        return round(f,1)

    # Duration hours
    elif e in [ 'sq', 'dr' ]:
        return round(f,1)

    # Wind direction
    elif e in  [ 'ddvec' ]:
        return round(f)

    # View distance
    elif e in [ 'vvn', 'vvx' ]:
        return round(f,1)

    return f  # No need to correct

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

def entity_to_key(entity, format='knmi'):
    '''Get index by text from the array entities'''
    lst, ent = [], entity.upper()

    if format.lower() == 'knmi':
        lst = knmi_entities

    for key, el in enumerate(lst):
        if el == ent:
            return key

    return -1

def etk(entity, format='knmi'):
    return entity_to_key(entity, format)

def key( entity, format='knmi' ):
    '''Function short for ndx_ent '''
    return entity_to_key( entity, format )

def list_ent( data, ent ):
    ndx = entity_to_key(ent)
    return data[:,ndx]

def ents( day, format='knmi' ):
    stn   = convert.fl_to_s( day[STN] )
    ymd   = convert.fl_to_s( day[YYYYMMDD] )
    ddvec = text.fix_ent(day[DDVEC], key_to_entity(DDVEC))
    fhvec = text.fix_ent(day[FHVEC], key_to_entity(FHVEC))
    fg    = text.fix_ent(day[FG],  key_to_entity(FG))
    fhx   = text.fix_ent(day[FHX], key_to_entity(FHX))
    fhxh  = text.fix_ent(day[FHXH], key_to_entity(FHXH))
    fhn   = text.fix_ent(day[FHN], key_to_entity(FHN))
    fhnh  = text.fix_ent(day[FHNH], key_to_entity(FHNH))
    fxx   = text.fix_ent(day[FXX], key_to_entity(FXX))
    fxxh  = text.fix_ent(day[FXXH], key_to_entity(FXXH))
    tg    = text.fix_ent(day[TG], key_to_entity(TG))
    tn    = text.fix_ent(day[TN], key_to_entity(TN))
    tnh   = text.fix_ent(day[TNH], key_to_entity(TNH))
    tx    = text.fix_ent(day[TX], key_to_entity(TX))
    txh   = text.fix_ent(day[TXH], key_to_entity(TXH))
    t10n  = text.fix_ent(day[T10N], key_to_entity(T10N))
    t10nh = text.fix_ent(day[T10NH], key_to_entity(T10NH))
    sq    = text.fix_ent(day[SQ], key_to_entity(SQ))
    sp    = text.fix_ent(day[SP], key_to_entity(SP))
    q     = text.fix_ent(day[Q], key_to_entity(Q))
    dr    = text.fix_ent(day[DR], key_to_entity(DR))
    rh    = text.fix_ent(day[RH], key_to_entity(RH))
    rhx   = text.fix_ent(day[RHX], key_to_entity(RHX))
    rhxh  = text.fix_ent(day[RHXH], key_to_entity(RHXH))
    pg    = text.fix_ent(day[PG], key_to_entity(PG))
    px    = text.fix_ent(day[PX], key_to_entity(PX))
    pxh   = text.fix_ent(day[PXH], key_to_entity(PXH))
    pn    = text.fix_ent(day[PN], key_to_entity(PN))
    pnh   = text.fix_ent(day[PNH], key_to_entity(PNH))
    vvn   = text.fix_ent(day[VVN], key_to_entity(VVN))
    vvnh  = text.fix_ent(day[VVNH], key_to_entity(VVNH))
    vvx   = text.fix_ent(day[VVX], key_to_entity(VVX))
    vvxh  = text.fix_ent(day[VVXH], key_to_entity(VVXH))
    ng    = text.fix_ent(day[NG], key_to_entity(NG))
    ug    = text.fix_ent(day[UG], key_to_entity(UG))
    ux    = text.fix_ent(day[UX], key_to_entity(UX))
    uxh   = text.fix_ent(day[UXH], key_to_entity(UXH))
    un    = text.fix_ent(day[UN], key_to_entity(UN))
    unh   = text.fix_ent(day[UNH], key_to_entity(UNH))
    ev24  = text.fix_ent(day[EV24], key_to_entity(EV24))

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
    fhxh  = int( day[FHXH] )
    fhn   = day[FHN] / 10.0
    fhnh  = int( day[FHNH] )
    fxx   = day[FXX] / 10.0
    fxxh  = int( day[FXXH] )
    tg    = day[TG] / 10.0
    tn    = day[TN] / 10.0
    tnh   = int( day[TNH] )
    tx    = day[TX] / 10.0
    txh   = day[TXH] / 10.0
    t10n  = day[T10N] / 10.0
    t10nh = int( day[T10NH] )
    sq    = day[SQ] / 10.0
    sp    = int( day[SP] ) 
    q     = day[Q]
    dr    = day[DR]
    rh    = day[RH]
    rhx   = day[RHX]
    rhxh  = int( day[RHXH] )
    pg    = day[PG] / 10.0
    px    = day[PX] / 10.0
    pxh   = int(day[PXH])
    pn    = day[PN] / 10.0
    pnh   = int(day[PNH])
    vvn   = day[VVN] / 10.0
    vvnh  = int(day[VVNH])
    vvx   = day[VVX] / 10.0
    vvxh  = int(day[VVXH])
    ng    = int(day[NG])
    ug    = int(day[UG])
    ux    = int(day[UX])
    uxh   = int(day[UXH])
    un    = int(day[UN])
    unh   = int(day[UNH])
    ev24  = day[EV24] / 10.0

    return ( stn, ymd, ddvec, fhvec, fg, fhx,
             fhxh, fhn, fhnh, fxx, fxxh, tg,
             tn, tnh, tx, txh, t10n, t10nh,
             sq, sp, q, dr, rh, rhx,
             rhxh, pg, px, pxh, pn, pnh,
             vvn, vvnh, vvx, vvxh, ng, ug,
             ux, uxh, un, unh, ev24 )


def date_by_val(data, val, ent):
    ymd, row, col, key_ent = cfg.e, 0, 1, etk(ent)

    for ndx, el in np.ndenumerate(data):  # ndx (0,0)
        if ndx[col] == key_ent: # Check only searched indexes
            if el == val: # Check for correct value
                ymd = str(int(data[ndx[row]][YYYYMMDD]))
                break

    return ymd

def day( station, yyyymmdd ):
    '''Function return a list of the dayvalues'''
    ok, data = False, np.array([])
    if validate.yyyymmdd(yyyymmdd):  # Validate date
        ok, data = read(station)
        if ok: # Date is read fine
            ndx = etk('YYYYMMDD')
            ymd, s_ymd, e_ymd = int(yyyymmdd), data[0,ndx], data[-1,ndx]

            # Check ranges and correct anyway
            if ymd < s_ymd:
                ymd = s_ymd
                cnsl.log(f'Date {s_ymd} out range of data. First available date {ymd} used.', True)
            elif ymd > s_ymd:
                ymd = e_ymd
                cnsl.log(f'Date {e_ymd} out range of data. First available date {ymd} used.', True)

            data = data[np.where(data[:,ndx] == ymd)] # Get values correct date

    return ok, data[0]

def update_minus_1( data ):
    spec_val, repl_val = -1.0, cfg.knmi_dayvalues_low_measure_val
    lkey = [etk('RH'), etk('RHX'), etk('SQ')]
    row, col = 0, 1

    for ndx, val in np.ndenumerate(data): # ndx (0,0)
        if ndx[col] in lkey:
            r, c = ndx[row], ndx[col]
            if val == spec_val: data[r][c] = repl_val
            if val == spec_val: data[r][c] = repl_val
            if val == spec_val: data[r][c] = repl_val

    return data

def sel_period( data, period ):
    '''Function selects days by start and end dates'''
    data, lst_period = select.days_period( data, period ) # Get the data for a period
    data = update_minus_1( data ) # Update/correct values -1
    return data

def read( station, verbose=cfg.verbose ):
    '''Reads data dayvalues from the knmi into a list'''
    ok, data, fname = cfg.e, False, station.data_txt_path
    cnsl.log(f'Read {station.wmo} {station.place}', verbose)

    with threading.Lock():
        try:
            data = np.genfromtxt( 
                fname,
                dtype=cfg.data_dtype,
                delimiter=station.data_delimiter,
                missing_values=station.data_missing,
                filling_values=np.nan,
                skip_header=station.data_skip_header,
                skip_footer=station.data_skip_footer,
                comments=station.data_comments_sign,
                autostrip=True,
                usemask=False
            )
        except Exception as e:
            cnsl.log(text.error('Read', e), cfg.error)
        else:
            cnsl.log(text.succes('Read'), verbose)
            ok = True

    return ok, data  # OK

def read_period(station, period):
    ok, data = read(station)
    if ok: 
        data, _ = select.days_period(data, period)
    return ok, data

def read_stations_period( stations, period, t='Process data station:', verbose=cfg.verbose ):
    result = np.array([])
    for station in stations:
        cnsl.log(f'{t} {station.wmo} {station.place}...', verbose)
        ok, npl = read_period(station, period, verbose)
        if ok:
            result = npl if result.size == 0 else np.concatenate( (result, npl), axis=0 )

    return result # convert to numpy array

def process_data( station, verbose=cfg.verbose ):
    '''Function processes (downloading en unzipping) a data file'''
    ok = False
    if station.data_download: # Only downloadable stations
        cnsl.log(f'[{ymd.now()}] Process data for station: {station.wmo} {station.place}...', verbose)

        url = station.data_url
        if not url:
            cnsl.log('Download skipped...', verbose)
        elif station.data_format == cfg.knmi_data_format:
            st = time.time_ns()
            zip = station.data_zip_path
            txt = station.data_txt_path
            ok = fio.download( url, zip, check=False, verbose=verbose )
            if ok:
                cnsl.log(utils.process_time('Download in ', st), verbose)
                st = time.time_ns()
                ok = fio.unzip(zip, txt, verbose)
                if ok:
                    cnsl.log(utils.process_time('Unzip in ', st), verbose)
                else:
                    cnsl.log(f'Failed to unzip {zip}', cfg.error)
            else:
                cnsl.log(f'Failed to download {url}', cfg.error)

            if ok:
                t = f'[{ymd.now()}] Process data {station.place} success.'
            else:
                t = f'[{ymd.now()}] Process data {station.place} failed.'

            cnsl.log(t, True)
        else:
            # Stations with other Formats
            # Needs to converted to knmi data format format
            pass

    return ok

def process_lst(lst_stations, verbose=cfg.verbose):
    '''Function downloads, unzipped knmi stations in the list'''
    st = time.time_ns()
    for station in lst_stations: 
        process_data(station, verbose)
    cnsl.log(utils.process_time('Total processing time is ', st, cfg.e), cfg.verbose)

def process_all(verbose=cfg.verbose):
    '''Function processes (downloading en unzipping) files from the selected stations'''
    process_lst( stations.lst, verbose )
