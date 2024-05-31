##########################################################################################
# KNMI
# Source: https://developer.dataplatform.knmi.nl/open-data-api

import config as cfg
import sources.control.fio as fio
import sources.model.utils as utils
import sources.model.stations as stations
import sources.model.ymd as ymd 
import sources.model.convert as convert
import sources.model.check as chk
import sources.view.console as cnsl 
import requests, xmltodict
import xarray as xr, pandas as pd, h5py

class OpenDataAPI:
    '''Open API class from knmi to request the weather datasets from the knmi'''
    def __init__(self, api_token:str = cfg.knmi_api_key):
        self.base_url = 'https://api.dataplatform.knmi.nl/open-data/v1'
        self.headers  = { 'Authorization': api_token } # Default token from config.py

    def __get_data(self, url, params=None):
        return requests.get(
                    url, headers=self.headers, params=params
               ).json()

    def list_files(self, dataset_name: str, dataset_version: str, params: dict):
        return self.__get_data(
            f'{self.base_url}/datasets/{dataset_name}/versions/{dataset_version}/files',
            params=params, 
        )

    def get_file_url(self, dataset_name: str, dataset_version: str, file_name: str):
        return self.__get_data(
            f'{self.base_url}/datasets/{dataset_name}/versions/{dataset_version}/files/{file_name}/url'
        )

def request_dataset(dataset, version, param, typ):
    '''Request a specific dataset and return the result'''
    # Init vars
    ok, bdata = True, b'' 
    
    # Init a new knmi API object
    api = OpenDataAPI()

    # Get a list of current files for the dataset 
    # with the correct version and params
    response = api.list_files(dataset, version, param)
    if 'error' in response: # Check for an error
        cnsl.log(f"Unable to retrieve list of files: {response['error']}", cfg.error)
        ok = False

    if ok:
        # Get the latest file for the file typ is typ
        file_name = response['files'][typ].get('filename')

        # Get the data with the (latest) xml url based on the latest file name
        # Will be automaticly converted to jso
        json_data = api.get_file_url(dataset, version, file_name)

        # Get the temporary download url out of the json data 
        download_url = json_data['temporaryDownloadUrl'] 

        # print('download url')
        # input(download_url)

        try:
            # Download the dataset. No params for this url.
            with requests.get(download_url, stream=True) as req:
                req.raise_for_status()
                for chunk in req.iter_content(chunk_size=8192):
                    bdata += chunk
                
        except Exception as e:
            cnsl.log(f'Error in knmi.request_dataset(){cfg.ln}{e}', cfg.error)
            ok = False
    
    return ok, bdata

def short_term_weather_forecast():
    '''Function to download the - short_term_weather_forecast - dataset
       and return the result'''
    # Example url for weatherforecast
    # url = f'https://api.dataplatform.knmi.nl/open-data/v1/datasets/{short_term_weather_forecast}/versions/{1.0}/files' 
    # Init variables
    ok, t = True, ''

    # Dataset credentials
    dataset = 'short_term_weather_forecast'
    version = 1.0                    # Version of dataset
    param = { 'maxKeys': 4,          # First 3 files, json, xml, text
              'orderBy': 'created',  # Order by time created
              'sorting': 'desc' }    # Sort dscending from new to old
    
    # File types format from knmi for this dataset
    typ_json_html, typ_txt, typ_html, typ_xml = 0, 1, 2, 3
    
    # Get the current weather data for the dataset, typ is text
    ok, bdata = request_dataset(dataset, version, param, typ_txt)

    if ok:
        # Get correct decoding charset
        charset = utils.get_encoding_of_binary(bdata)

        # Convert binary data to string
        t = bdata.decode(charset, errors="ignore") # 'utf-8' ? 

        # Replace too much enters (3 or more) with 2 enters
        t = t.replace('\n\n\n', '\n\n')

        # Replace weird char errors (why not use utf-8?) 
        # and strip surrounding whitespace
        t = t.replace('\'C', '°C').strip()

    return ok, t

def outlook_weather_forecast():
    ok, t = True, ''
    # Credentials for the dataset 
    dataset = 'outlook_weather_forecast'
    version = 1.0                    # Version of dataset
    param = { 'maxKeys': 2,          # Get the two file options
              'orderBy': 'created',  # Order by time created
              'sorting': 'desc' }    # Sort dscending from new to old   

    # File types format from knmi for this dataset
    typ_xml, typ_html = 0, 1 # XML or HTML only?

    # Get weather binary data
    ok, bdata = request_dataset(dataset, version, param, typ_xml)

    if ok:
        # Get correct decoding charset
        charset = utils.get_encoding_of_binary(bdata)

        # Convert binary data to string
        data = bdata.decode(charset, errors="ignore") # 'utf-8', 

        # Change xml data to a dictionary
        dict = xmltodict.parse(data)

        # date_created  = dict['dataroot']['@generated'].replace('T' , ' ')[:-3]
        verwachting   = dict['dataroot']['Middellange_x0020_en_x0020_lange_x0020_Termijn']
        meerdaagse    = verwachting['verwachting_meerdaagse']
        lange_termijn = verwachting['verwachting_lange_termijn_tekst']

        # Lists for data with 6 days forecast dictionary
        lst_days = range(1, 7)
        space_title, space_value = 20, 12
        sep = '/'

        # Make weather texts
        t = f'Vooruitzichten:{cfg.ln}'
        t += 'Datum '.rjust(space_title)
        for n in lst_days: 
            ddd  = verwachting[f'dag{n}_ddd']
            dd   = verwachting[f'dag{n}_dd']
            mmm  = ymd.mm_to_mmm(verwachting[f'dag{n}_mm'])
            mmdd = f'{ddd} {dd} {mmm}'
            t += f'{mmdd: ^{space_value}}'
        t = t.rstrip() + cfg.ln

        t += 'Maximum temperatuur '.rjust(space_title)
        for n in lst_days: 
            max_temp_min = verwachting[f'maximumtemperatuur_min_dag{n}'] 
            max_temp_max = verwachting[f'maximumtemperatuur_max_dag{n}']
            if int(max_temp_min) == int(max_temp_max):
                max_temp = f'{max_temp_max}°C' 
            else:
                max_temp = f'{max_temp_min}{sep}{max_temp_max}°C' 
            t += f'{max_temp: ^{space_value}}'
        t = t.rstrip() + cfg.ln

        t += 'Minimum temperatuur '.rjust(space_title)
        for n in lst_days: 
            min_temp_min = verwachting[f'minimumtemperatuur_min_dag{n}']
            min_temp_max = verwachting[f'minimumtemperatuur_max_dag{n}']
            if int(min_temp_min) == int(min_temp_max):
                min_temp = f'{min_temp_max}°C' 
            else:
                min_temp = f'{min_temp_min}{sep}{min_temp_max}°C' 
            t += f'{min_temp: ^{space_value}}'
        t = t.rstrip() + cfg.ln

        t += 'Percentage zon '.rjust(space_title)
        for n in lst_days: 
            zon = verwachting[f'zonneschijnkans_dag{n}'] + '%'
            t += f'{zon: ^{space_value}}'
        t = t.rstrip() + cfg.ln

        t += 'Percentage regen '.rjust(space_title)
        for n in lst_days: 
            regen = verwachting[f'neerslagkans_dag{n}'] + '%'
            t += f'{regen: ^{space_value}}'
        t = t.rstrip() + cfg.ln

        t += 'Hoeveelheid regen '.rjust(space_title)
        for n in lst_days: 
            regen = verwachting[f'neerslaghoeveelheid_max_dag{n}'] + 'mm'
            t += f'{regen: ^{space_value}}'
        t = t.rstrip() + cfg.ln

        t += 'Windrichting '.rjust(space_title)
        for n in lst_days:
            wind = verwachting[f'windrichting_dag{n}'].upper()
            t += f'{wind: ^{space_value}}'
        t = t.rstrip() + cfg.ln

        t += 'Windkracht '.rjust(space_title)
        for n in lst_days:
            wind = verwachting[f'windkracht_dag{n}'] + 'bft'
            t += f'{wind: ^{space_value}}'
        t = t.rstrip() + cfg.ln + cfg.ln

        t += f'Meerdaagse:{cfg.ln}{meerdaagse}{cfg.ln + cfg.ln}'
        t += f'Lange termijn:{cfg.ln}{lange_termijn}'
        # t += f'DATUM <{date_created}>'

        # Remove unnecessary whitespace
        t = t.strip()

    return ok, t

def weather_stations():
    '''Make a knmi stations text makes use of the dataset
       Dataset: Actuele10mindataKNMIstation
    '''
    # Example url for Actuele10mindataKNMIstation
    # url = f'https://api.dataplatform.knmi.nl/open-data/v1/datasets/{Actuele10mindataKNMIstation}/versions/{2}/files' 
    # Info: https://english.knmidata.nl/open-data/actuele10mindataknmistations

    # Init variables
    ok, t = True, ''

    # Dataset credentials
    dataset = 'Actuele10mindataKNMIstations'
    version = 2   # Version of dataset
    param = { 'maxKeys': 1,          # Get the one file options
              'orderBy': 'created',  # Order by time created
              'sorting': 'desc' }    # Sort dscending from new to old
    typ = 0 # Only one type -> nc (xarray)
 
    # Get data from knmi
    ok, xr_data = request_dataset(dataset,version,param,typ)

    if ok:
        # File name and path
        # Make download path with dates and times
        path = fio.path_with_act_date(cfg.dir_forecasts, 
                                      cfg.knmi_stations_name_nc, 
                                      extension='nc')

        # Save the file
        ok = fio.write(path, xr_data, encoding='', prefix='wb', verbose=True)

        # Now read dataset from file
        ds = xr.open_dataset(path, engine="h5netcdf")

        # Make lists with values for all the files
        lst_places, lst_dates = [], []
        lst_ta, lst_tb2, lst_dd = [], [], []
        lst_ps, lst_n, lst_vv = [], [], []
        for place in cfg.lst_knmi_stations_show: 

            # Get town name from data x array
            xr_town = ds.sel(station=place)

            # Place
            station = stations.wmo_to_station(place[2:])
            lst_places.append(station.place)

            # Tact
            ta = float(xr_town["ta"])
            ta = cfg.no_val if chk.is_nan(ta) else f'{ta}°C'
            lst_ta.append(ta)

            # Temp 10CM
            tb2 = float(xr_town["tb2"])
            tb2 = cfg.no_val if chk.is_nan(tb2) else f'{tb2}°C'
            lst_tb2.append(tb2)

            # View
            vv = float(xr_town["vv"])
            vv = cfg.no_val if chk.is_nan(vv) else f'{int(round(vv))}m'
            lst_vv.append(vv)
            
            # Pressure
            ps = float(xr_town["ps"])
            ps = cfg.no_val if chk.is_nan(ps) else f'{int(round(ps))}hPa'
            lst_ps.append(ps)

            # Wind direction and speed 
            bft, dir = float(xr_town["ff"]), float(xr_town["dd"])
            bft = cfg.no_val if chk.is_nan(bft) else convert.ms_to_bft(bft) + 'bft'
            dir = cfg.no_val if chk.is_nan(dir) else convert.wind_deg_to_txt_short(dir)
            wind = f'{dir} {bft}'
            lst_dd.append(wind)

            # Cloud
            n = float(xr_town["n"])
            n = cfg.no_val if chk.is_nan(n) else convert.octa_to_txt(n)
            lst_n.append(n)

        # Start at first key
        col_start, col_end = 0, cfg.knmi_station_cols
        spc_title, spc_val = 14, 20

        t = f'Waarnemingen NL' + cfg.ln + cfg.ln
        while col_end != len(cfg.lst_knmi_stations_show):
            t += 'Weerstation '.rjust(spc_title)[:spc_title]
            for place in lst_places[col_start:col_end]: 
                t += f'{place[:spc_val]:^{spc_val}}'
            t = t.rstrip() + cfg.ln

            t += 'Bewolking '.rjust(spc_title)[:spc_title]
            for n in lst_n[col_start:col_end]: 
                t += f'{n[:spc_val]:^{spc_val}}'
            t = t.rstrip() + cfg.ln

            t += 'Temperatuur '.rjust(spc_title)[:spc_title]
            for ta in lst_ta[col_start:col_end]: 
                t += f'{ta[:spc_val]:^{spc_val}}'
            t = t.rstrip() + cfg.ln

            # t += 'Temperature 10cm '.rjust(spc_title)[:spc_title]
            # for tb2 in lst_tb2[col_start:col_end]: t += f'{tb2[:spc_val]:^{spc_val}}'
            # t = t.rstrip() + cfg.ln

            t += 'Wind '.rjust(spc_title)[:spc_title]
            for dd in lst_dd[col_start:col_end]: 
                t += f'{dd[:spc_val]:^{spc_val}}'
            t = t.rstrip() + cfg.ln

            t += 'Luchtdruk '.rjust(spc_title)[:spc_title]
            for ps in lst_ps[col_start:col_end]: 
                t += f'{ps[:spc_val]:^{spc_val}}'
            t = t.rstrip() + cfg.ln

            t += 'Zicht '.rjust(spc_title)[:spc_title]
            for vv in lst_vv[col_start:col_end]: 
                t += f'{vv[:spc_val]:^{spc_val}}'
            t = t.rstrip() + cfg.ln + cfg.ln

            # Move cols up
            col_start += cfg.knmi_station_cols
            col_end += cfg.knmi_station_cols

    return ok, t

def weather_forecast():
    '''Make a knmi weather forecast makes use of two datasets
       1) outlook_weather_forecast
       2) short_term_weather_forecast
    '''
    ok1, t1 = short_term_weather_forecast()
    ok2, t2 = outlook_weather_forecast()
    ok = ok1 and ok2
    t = t1 + cfg.ln + cfg.ln + t2 if ok else ''

    return ok, t

# lst_ents = [
#     'D1H','dd','dn','dr','dsd', 'dx','ff', 'ffs', 'fsd', 'fx', 'fxs', 
#     'gff', 'gffs', 'h', 'h1', 'h2', 'h3', 'hc', 'hc1', 
#     'hc2', 'hc3', 'n', 'n1', 'n2', 'n3', 'nc', 'nc1', 
#     'nc2', 'nc3', 'p0', 'pp', 'pg', 'pr', 'ps', 'pwc', 
#     'Q1H', 'Q24H', 'qg', 'qgn', 'qgx', 'qnh', 'R12H', 'R1H', 
#     'R24H', 'R6H', 'rg', 'rh', 'rh10', 'Sav1H', 'Sax1H', 'Sax3H', 
#     'Sax6H', 'sq', 'ss', 'Sx1H','Sx3H', 'Sx6H', 't10', 'ta', 
#     'tb', 'tb1', 'Tb1n6', 'Tb1x6', 'tb2', 'Tb2n6', 'Tb2x6', 'tb3', 
#     'tb4', 'tb5', 'td', 'td10', 'tg', 'tgn', 'Tgn12', 'Tgn14', 
#     'Tgn6', 'tn', 'Tn12', 'Tn14', 'Tn6', 'tsd', 'tx', 'Tx12',  
#     'Tx24', 'Tx6', 'vv', 'W10', 'W10-10', 'ww', 'ww-10', 'zm'
# ] 

# D1H: 0.0
# dd: 101.4
# dn: 38.0
# dr: 0.0
# dsd: 22.5
# dx: 164.5
# ff: 2.33
# ffs: 2.33
# fsd: 0.63
# fx: 4.92
# fxs: 4.92
# gff: 4.1
# gffs: 4.1
# h: 6584.92
# h1: 6584.92
# h2: 0.0
# h3: 0.0
# hc: 6584.92
# hc1: 6584.92
# hc2: 0.0
# hc3: 0.0
# n: 8.0
# n1: 8.0
# n2: 0.0
# n3: 0.0
# nc: 8.0
# nc1: 8.0
# nc2: 0.0
# nc3: 0.0
# p0: 1007.19
# pp: 1007.57
# pg: 0.0
# pr: 0.0
# ps: 1007.0
# pwc: 0.0
# Q1H: 177.72
# Q24H: 1839.54
# qg: 360.0
# qgn: 282.0
# qgx: 492.0
# qnh: 1007.58
# R12H: 0.017
# R1H: 0.0
# R24H: 2.62267
# R6H: 0.0
# rg: 0.0
# rh: 46.0
# rh10: nan
# Sav1H: 2.66467
# Sax1H: 3.63
# Sax3H: 5.38
# Sax6H: 5.38
# sq: 0.0
# ss: 0.68898
# Sx1H: 5.75
# Sx3H: 9.57
# Sx6H: 9.57
# t10: nan
# ta: 23.2
# tb: 15.7718
# tb1: nan
# Tb1n6: nan
# Tb1x6: nan
# tb2: nan
# Tb2n6: nan
# Tb2x6: nan
# tb3: nan
# tb4: nan
# tb5: nan
# td: 10.9
# td10: nan
# tg: 23.7
# tgn: 23.7
# Tgn12: 7.0
# Tgn14: 7.0
# Tgn6: 19.2
# tn: 23.1
# Tn12: 9.7
# Tn14: 9.7
# Tn6: 18.4
# tsd: nan
# tx: 23.4
# Tx12: 23.7
# Tx24: 23.7
# Tx6: 23.7
# vv: 37000.0
# W10: 0.0
# W10-10: 0.0
# ww: 3.0
# ww-10: 3.0
# zm: 37000.0
