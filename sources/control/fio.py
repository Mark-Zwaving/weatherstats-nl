# -*- coding: utf-8 -*-
'''Functions for io file handling.
   Creating, writing, deleting, downloading, unzipping a file'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.2.6'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import sources.model.convert as convert
import sources.model.ymd as ymd
import sources.model.validate as validate
import sources.model.utils as utils
import sources.view.console as cnsl
import sources.view.text as text
import threading, urllib, json, os
import time, zipfile, requests, shutil
import urllib.request, socket, datetime
from urllib.parse import urlparse

# Minimum interval time for saving or downloading files
minimum_interval_time = 0.1

abspath = lambda path: os.path.abspath(path)
mk_path = lambda dir, f: abspath(os.path.join(dir, f))

def flood_protection():
    # Flood server protection
    if cfg.download_flood_protection_active:
        wait = cfg.download_interval_time
        if wait < minimum_interval_time: 
            wait = minimum_interval_time
        time.sleep(wait)

def sanitize_file_name(fname):
    # Sanitize file name
    fname = fname.replace('*', 'x')
    fname = utils.replace_char(fname, " .", '-')
    fname = utils.replace_char(fname, cfg.lst_forbidden_file_chars, '')
    fname = fname.lower()

    return fname

def sanitize_map_name(map):
    '''Function makes a string valid to be used as directory name'''
    map = utils.replace_char(map, cfg.lst_forbidden_file_chars, 'x')

    return map

def mk_path_with_dates(base_dir, fname):
    yyyy, mm, dd = ymd.yyyy_mm_dd_now()
    dir  = mk_path( base_dir, f'{yyyy}/{mm}/{dd}' )
    fname = fname.lower()
    path = mk_path(dir, fname)

    return path, dir, fname

def name_with_act_date(base_name, ext='txt'):
    H, M, S = ymd.hh_mm_ss_now()
    return f'{base_name}-{H}-{M}-{S}.{ext}'

def dir_with_act_date(base_dir):
    y, m, d = ymd.yyyy_mm_dd_now()
    return mk_path(base_dir, f'{y}/{m}/{d}')

def path_with_act_date(base_dir, base_name):
    return mk_path(dir_with_act_date(base_dir), name_with_act_date(base_name))

def check(path, verbose=cfg.verbose):
    '''Function checks a file for existence'''
    ok = False
    cnsl.log(f'[{ymd.now()}] Check if a file exists', verbose)
    cnsl.log(f'[{ymd.now()}] File {utils.str_max(path)}', verbose)
    with threading.Lock():
        try:
            if os.path.exists(path):  # Check if is there file
                ok = True
        except Exception as e:
            cnsl.log(f'[{ymd.now()}] Error check\n{e}', cfg.error)
        else:
            if ok:
                cnsl.log(f'[{ymd.now()}] File exists', verbose)
            else:
                cnsl.log(f'[{ymd.now()}] File does not exist', verbose)
    return ok

def write(path='dummy.txt', content=cfg.e, encoding='utf-8', prefix='w', verbose=cfg.verbose):
    '''Function writes content to a file'''
    ok = False
    cnsl.log(f'[{ymd.now()}] Write a file', verbose)
    cnsl.log(f'[{ymd.now()}] File {utils.str_max(path)}', verbose)
    with threading.Lock():
        try:
            map = os.path.dirname(path)
            if map: mk_dir(map, verbose) # Make map(s)
            with open(path, encoding=encoding, mode=prefix) as f:
                f.write(content)
        except Exception as e:
            cnsl.log(f'[{ymd.now()}] Error writing file\n{e}', cfg.error)
        else:
            cnsl.log(f'[{ymd.now()}] Write file success', verbose)
            ok = True

    # Flood protection
    # flood_protection()

    return ok

def save(path='dummy.txt', content=cfg.e, encoding='utf-8', prefix='w', verbose=cfg.verbose):
    '''Function writes content to a file'''
    return write(path, content, encoding, prefix, verbose)

def read(path, encoding='utf-8', verbose=cfg.verbose):
    '''Function reads the content in a file'''
    ok, t, paths = False, cfg.e, convert.to_lst(path)
    cnsl.log(f'[{ymd.now()}] Read a file', verbose)
    cnsl.log(f'[{ymd.now()}] File(s)', verbose)
    for  ndx, p in enumerate(paths):
         cnsl.log(f'[{ymd.now()}] {ndx+1}. {utils.str_max(p)}', verbose)

    for path in paths: # All paths
        with threading.Lock():
            if check(path, verbose):
                try:
                    with open(path, encoding=encoding, mode='r') as f:
                        t = f.read()
                except Exception as e:
                    cnsl.log(f'[{ymd.now()}] Error in fio read()\n{e}', cfg.error)
                else:
                    cnsl.log(f'[{ymd.now()}] Read file success', verbose)
                    ok = True
    return ok, t

def readlines(path, encoding='utf-8',verbose=cfg.verbose):
    '''Function reads the content from a file into a list'''
    l, ok, t, paths = [], False, cfg.e, convert.to_lst(path)
    cnsl.log(f'[{ymd.now()}] Read file(s) into a list', verbose)
    for  ndx, p in enumerate(paths):
         cnsl.log(f'[{ymd.now()}] {ndx+1}. {utils.str_max(p)}', verbose)

    for path in paths: # All paths
        with threading.Lock():
            if check(path, verbose):
                try:
                    with open(path, encoding=encoding, mode='r') as f:
                        l = f.readlines()
                except Exception as e:
                    cnsl.log(f'[{ymd.now()}] Error in fio readlines()\n{e}', cfg.error)
                else:
                    cnsl.log(f'[{ymd.now()}] Read file success', verbose)
                    ok = True
    return ok, l

def delete(path, verbose=cfg.verbose):
    '''Function deletes a file if exists'''
    ok, paths = False, convert.to_lst(path)
    cnsl.log(f'[{ymd.now()}] Delete file(s)', verbose)
    for  ndx, p in enumerate(paths):
         cnsl.log(f'[{ymd.now()}] {ndx+1}. {utils.str_max(p)}', verbose)

    for path in paths: # All paths
        with threading.Lock():
            if check(path, verbose):
                try:
                    os.remove(path)  # Remove file
                except Exception as e:
                    cnsl.log(f'[{ymd.now()}] Error in fio delete()\n{e}', cfg.error)
                else:
                    cnsl.log(f'[{ymd.now()}] Delete file success', verbose)
                    ok = True
            else:
                cnsl.log(f'[{ymd.now()}] Cannot delete. File does not exist', verbose)
    return ok

def rm(path, verbose=cfg.verbose):
    '''Function removes a file if exists (canonical) for delete()'''
    return delete(path, verbose)

def mk_dir(dir, verbose=cfg.verbose):
    '''Function makes a map if not already exists'''
    ok, paths = False, convert.to_lst(dir)
    cnsl.log(f'[{ymd.now()}] Make directory(s)', verbose)
    for  ndx, p in enumerate(paths):
         cnsl.log(f'[{ymd.now()}] {ndx+1}. {utils.str_max(p)}', verbose)

    for path in paths: # All paths
        with threading.Lock():
            try:
                if os.path.isdir(path):
                    cnsl.log(f'[{ymd.now()}] Map not made because it already exists.', verbose)
                    ok = True
                else:
                    os.makedirs(path)
            except Exception as e:
                cnsl.log(f'[{ymd.now()}] Error in fio mk_dir()\n{e}', cfg.error)
            else:
                cnsl.log(f'[{ymd.now()}] Make directory {path} successful', verbose)
                ok = True

    return ok

def rm_dir(
        dir, # Map to remove
        verbose=cfg.verbose
    ):
    '''Function deletes an directory empty or not'''
    ok, paths = False, convert.to_lst(dir)
    cnsl.log(f'[{ymd.now()}] Remove directory(s)', verbose)
    cnsl.log(f'[{ymd.now()}] # TODO force to txt fileDir(s)', verbose)
    for  ndx, p in enumerate(paths):
         cnsl.log(f'[{ymd.now()}] {ndx+1}. {utils.str_max(p)}', verbose)

    for path in paths: # All paths
        with threading.Lock():
            if os.path.exists(path):
                try:
                    shutil.rmtree(path)
                except Exception as e:
                    cnsl.log(f'[{ymd.now()}] Error removing map\n{e}', cfg.error)
                else:
                    cnsl.log(f'[{ymd.now()}] Remove map {path} successful', verbose)
                    ok = True
            else:
                cnsl.log(f'[{ymd.now()}] Cannot remove {path}.\nMap does not exist.', verbose)
    return ok

def is_dir_empthy(dir, verbose=cfg.verbose):
    ok = False
    cnsl.log(f'[{ymd.now()}] Check if dir is empty', verbose)
    cnsl.log(f'[{ymd.now()}] Dir {utils.str_max(dir)}', verbose)

    if os.path.exists(dir):
        ok = True if len(os.listdir(dir)) == 0 else False
    else:
        cnsl.log(f'[{ymd.now()}] Map does not exist.', verbose)
        ok = True

    return ok

def unzip(zip, txt, verbose=cfg.verbose):
    '''Function unzips a zipfile'''
    ok = False
    cnsl.log(f'[{ymd.now()}] Unzip a file', verbose)
    cnsl.log(f'[{ymd.now()}] From {utils.str_max(zip)}', verbose)
    cnsl.log(f'[{ymd.now()}] To {utils.str_max(txt)}', verbose)
    with threading.Lock():
        try:
            dir_txt = os.path.dirname(txt)
            with zipfile.ZipFile(zip, 'r') as z:
                z.extractall(dir_txt)
        except Exception as e:
            cnsl.log(f'[{ymd.now()}] Error in fio unzip()\n{e}', cfg.error)
        else:
            cnsl.log(f'[{ymd.now()}] Unzip success', verbose)
            ok = True
    return ok

def download(
        url,    # Url to download
        path,   # Path to download the file to
        check   = False, # <optional> Check file True will not overwrite the file if exists
        verbose = cfg.verbose # <optional> Overwrite default value verbose -> see config.py
    ):
    '''Function downloads a file from an internet url'''
    ok = False
    cnsl.log(f'[{ymd.now()}] Download a file', verbose)
    cnsl.log(f'[{ymd.now()}] From {utils.str_max(url)}', verbose)
    cnsl.log(f'[{ymd.now()}] To {utils.str_max(path)}', verbose)

    # Check if image is already downloaded
    if check and os.path.exists(path):
        cnsl.log(f'[{ymd.now()}] Download skipped, file already exists', verbose)
        ok = True
    else:
        with threading.Lock():
            if url_exists(url, False): # Check if a url exists
                try:
                    mk_dir(os.path.dirname(path), False) # Make map if not exists
                    urllib.request.urlretrieve( url, path ) # Download file
                except Exception as e:
                    cnsl.log(f'[{ymd.now()}] Error in fio download()\n{e}', cfg.error)
                else:
                    cnsl.log(f'[{ymd.now()}] Download success', verbose)
                    ok = True
            else:
                cnsl.log(f'[{ymd.now()}] Url {url} does not exist', verbose)

        # Flood server protection
        flood_protection()

    return ok

def download_read_file(url, file, verbose=cfg.verbose):
    '''Function downloads a file, read the file and return the content of the file'''
    ok, t = False, cfg.e
    cnsl.log(f'[{ymd.now()}] Download and read', verbose)
    cnsl.log(f'[{ymd.now()}] Url: {utils.str_max(url)}', verbose)
    cnsl.log(f'[{ymd.now()}] To: {utils.str_max(file)}', verbose)
    if check_for_internet_connection():
        ok = download( url, file, verbose )
        if ok: 
            ok, t = read(file)
    else:
        t = 'Cannot download file. There is no internet connection'
        cnsl.log(f'[{ymd.now()}] {t}', cfg.error)
    return ok, t

def request(url, type='txt', verbose=cfg.verbose):
    '''Function makes the request based on the url given as parameter
       The return values are: ok, True if success else False... And the text From
       the request.'''
    ok, t = False, cfg.e
    cnsl.log(f'[{ymd.now()}] Request {type}', verbose)
    cnsl.log(f'[{ymd.now()}] Url: {utils.str_max(url)}', verbose)
    with threading.Lock():
        try:
            resp = urllib.request.urlopen( url )
            data = resp.read()
            if type == 'text':
                t = data
            elif type == 'json':
                t = json.loads(data)
        except Exception as e:
            cnsl.log(f'[{ymd.now()}] Error in fio request()\n{e}', cfg.error)
        else:
            cnsl.log(f'[{ymd.now()}] Request success', verbose)
            ok = True
    return ok, t

def request_text(url, verbose=cfg.verbose):
    '''Function makes an online request for a text file'''
    return request(url, 'txt', verbose)

def request_json( url, verbose=cfg.verbose):
    '''Function makes an online request for a json file'''
    return request(url, 'json', verbose)

def has_internet(ip=cfg.check_ip_1, port=cfg.check_port_80, verbose=cfg.verbose):
    '''Function checks if there is a internet connection available'''
    cnsl.log(f'[{ymd.now()}] Check internet connection', verbose)
    cnsl.log(f'[{ymd.now()}] IP {ip}', verbose)

    ok, wait = False, 0.1
    with threading.Lock():
        try:
            address = (ip, port)
            sock = socket.create_connection(address=address)
        except Exception as e:
            cnsl.log(f'[{ymd.now()}] Error in fio has_internet()\n{e}', verbose)
        else:
            cnsl.log(f'[{ymd.now()}] Check succes', verbose)
            sock.close()
            ok = True

        time.sleep(wait)

        # try:
        #     requests.head(ip, timeout=cfg.check_timeout)
        # except Exception as e:
        #     cnsl.log(f'Check failed\n{e}', True)
        # else:
        #     cnsl.log('Check succes', verbose)
        #     ok = True

        # time.sleep(wait)

        # try:
        #     urllib.request.urlopen( ip ) #Python 3.x
        # except Exception as e:
        #     cnsl.log(f'Check failed\n{e}', verbose)
        # else:
        #     cnsl.log('Check succes', verbose)
        #     ok = True

    return ok

def check_for_internet_connection(verbose=cfg.verbose):
    '''Function checks for multiple ip's and port for a internte connection'''
    if has_internet( ip=cfg.check_ip_4,
                     port=cfg.check_port_dns,
                     verbose=verbose ):
        return True
    elif has_internet( ip=cfg.check_ip_1, 
                       port=cfg.check_port_80, 
                       verbose=verbose ):
        return True
    elif has_internet( ip=cfg.check_ip_2,
                       port=cfg.check_port_80,
                       verbose=verbose ):
        return True
    elif has_internet( ip=cfg.check_ip_3,
                       port=cfg.check_port_dns,
                       verbose=verbose ):
        return True
    return False

def url_exists(url, verbose=cfg.verbose):
    '''Function checks if a url exists. Return True or False'''
    ok = False
    cnsl.log(f'[{ymd.now()}] Check url for existence', verbose)
    cnsl.log(f'[{ymd.now()}] Url {utils.str_max(url)}', verbose)
    with threading.Lock():
        try:
            resp = requests.head(url)
            ok = True if resp.status_code == 200 else False
        except Exception as e:
            cnsl.log(f'[{ymd.now()}] Error in fio url_exists()\n{e}', cfg.error)
        else:
            cnsl.log(f'[{ymd.now()}] Url exists', verbose)
            ok = True
    return ok

def rm_lst(lst = [], remove_empty=False, verbose=cfg.verbose):
    '''Function tries to remove all files in the list.'''
    cnsl.log(f'[{ymd.now()}] Remove files in list', verbose)
    for path in list(set(lst)): # Make list unique and walkthrough paths
        if delete(path, verbose): # Remove file from disk
            dir = os.path.dirname(path) # Get map from path
            # Remove maps only empty maps and remove_empty is True
            while is_dir_empthy(dir, verbose) and remove_empty:
                rm_dir(dir, verbose) # Remove empty map
                dir = os.path.dirname(dir) # Go to upper dir

def lst_download(
        uries = [],     # List with download urls
        paths = [],     # <optional> List with names for the files from the download urls
        check = True,   # Already download check. Do not overwrite download file
        verbose=cfg.verbose # Output to screen
    ):
    '''Downloads images based on two lists. It combines an uries list with a path list'''
    cnsl.log(f'[{ymd.now()}] Download list', verbose)
    if not paths: # If no paths, make them based on the uries
        for url in uries:
            locnet = urlparse(url).netloc.split('.')[-2].lower()# Get name url
            name, ext = os.path.splitext(os.path.basename(url)) # Get name and extension
            ext = validate.extension(ext) # Handle dot.
            path = mk_path(cfg.dir_data, f'{locnet}_{name}{ext}') # Make image path
            paths.append(path) # Add to list

    res_urie, res_path, max = [], [], cfg.download_max_num
    # Combine/zip the two lists (with download paths and web urls) into one list
    for path, url in tuple(zip(paths[:max], uries[:max])): # Loop through img and url objects
        ok = download(url, path, check, verbose) # Download file
        if ok: # Success add to lists
            res_urie.append(url)
            res_path.append(path)

    return res_urie, res_path # Return correct paths

def lst_maps(map, recursive=True, secret=True, verbose=cfg.verbose):
    '''Returns a list with all the (sub) directories'''
    lst = []
    cnsl.log(f'[{ymd.now()}] Check directories', verbose)
    cnsl.log(f'[{ymd.now()}] Map {utils.str_max(map)}', verbose)
    for el in os.listdir(map):
        # skip secret maps
        if not secret: 
            if el[0] == '.': 
                continue  

        path = mk_path(map, el)
        if os.path.isdir(path): # Check paths if is a map
            cnsl.log(f'[{ymd.now()}] Map found: {map}', verbose)
            lst.append(path)
            if recursive: # Add subdirectories too
                lst += lst_maps(path)

    return lst

def lst_files_dir(
        dir,             # Dir to search for files
        extensions = cfg.e, # <optional> List of extensions or one string ext to search the map for
        keywords   = cfg.e, # <optional> List of keyword or one string to search the directory for
        case_insensitive = True, # <optional> Search case insensitive. True by default.
        verbose = cfg.verbose  # <optional> Overwrite verbose option
    ):
    '''Function list files in a directory. The list can be filtered by keywords
       and extensions.'''
    results = [] # List with found paths
    paths = convert.to_lst(dir)
    cnsl.log(f'[{ymd.now()}] List files directory(s)', verbose)
    for  ndx, p in enumerate(paths):
         cnsl.log(f'[{ymd.now()}] {ndx+1}. {utils.str_max(p)}', verbose)


    for path in paths: # All paths
        if not os.path.exists(path): # Check map
            cnsl.log(f'[{ymd.now()}] Path {path} does not exist', verbose)
        else:
            # Check types and add to an (empty) list element if needed
            len_ext, len_key = 0, 0
            if extensions:
                extensions = convert.to_lst(extensions)
                len_ext = len(extensions)
            if keywords:
                keywords = convert.to_lst(keywords)
                len_key = len(keywords)
    
            filter_on = True if (len_key + len_ext) > 0 else False # Filter on ?
    
            if len_key > 0: 
                cnsl.log(f'[{ymd.now()}] Search words { str(keywords) }', verbose)
            if len_ext > 0: 
                cnsl.log(f'[{ymd.now()}] Search extensions { str(extensions) }', verbose)

            # Validate extensions, add point if needed
            if len_key > 0: 
                extensions = [validate.extension(ext) for ext in extensions]

            # Get all the files in the directory
            files = [f for f in os.listdir(path) if os.path.isfile( mk_path(path,f) )]

            # Make search lists case in-sensitive if set
            if case_insensitive:
                extensions, keywords = [e.lower() for e in extensions], [k.lower() for k in keywords]

            # Filter files based on extensions and keywordsfname =
            for f in files:
                # Get name and extension
                fname, ext = os.path.splitext(f)

                # Make case insensitive if needed
                if case_insensitive: 
                    fname, ext = fname.lower(), ext.lower()

                found = True
                if filter_on: # Check to filter
                    found_word, found_ext = False, False # Found is False by default
                    # Check words and extensions
                    if len_key > 0: # Check only if there are words to check
                        # Check if keywords are in name
                        if len([w for w in keywords if w in fname]) > 0:
                            found_word = True # Part word is found
                    else: # All words are Truelst_files_dirlst_files_dir
                        found_word = True

                    if len_ext > 0: # Check only if there are extensions to check
                        # Check if extension is found
                        if len([e for e in extensions if e == ext]) > 0:
                            found_ext = True # Extension is found
                    else: # All extensions are True
                        found_ext = True

                    # Both must True
                    found = found_word or found_ext

                if found: # If found add file path to results
                    path = mk_path(dir, f)
                    cnsl.log(f'[{ymd.now()}] File found {path}', verbose)
                    results.append(path)

    return results

def remove_file_and_empthy_maps_reverse(path, verbose=cfg.verbose):
    ok = delete(path, verbose=verbose) # Remove file
    if ok:
        while True: # Delete maps if empthy
            path = os.path.dirname(path) # Get map
            if is_dir_empthy( path, verbose=verbose): # Remove only empthy maps
                rm_dir( path, verbose=verbose) # remove map
            else:
                break # Not empthy do not delete

def remove_files_in_list( lst = [], verbose=cfg.verbose):
    '''Function tries to remove all downloaded images in the list.
       Removes a direcory if empty too.'''
    cnsl.log(f'[{ymd.now()}] Start remove files in list', verbose)
    lst = list(set(lst)) # Make list unique
    for path in lst:     # Walkthrough paths
        remove_file_and_empthy_maps_reverse(path, verbose)

    cnsl.log(f'[{ymd.now()}] End remove files from list\n', verbose)


# Function downloads in interval for a period of time and returns a list with the images
def download_interval(
       url,                                    # Url for the files on the web
       start_datetime = 'yyyy-mm-dd hh:mm:ss', # Start time
       end_datetime   = 'yyyy-mm-dd hh:mm:ss', # End datetime
       interval       = 10,                    # Interval time for downloading Images (minutes)
       check          = True,                  # No double downloads check
       verbose        = cfg.verbose            # With output to screen
    ):
    '''Download files from the web in interval for a period of time.
       Returns a list with the names of the downloaded files'''
    # List for the downloaded files with their name
    lst_images = [] 
    submap = sanitize_map_name(utils.url_name(url)) # Used to create an extra submap name 
    basename, ext = os.path.splitext( os.path.basename(url) ) 
    y, m, d = ymd.yyyy_mm_dd_now()  # Get current year, month and day
    download_map = mk_path(cfg.dir_download, f'{y}/{m}/{d}/{submap}')
    cnsl.log( text.head(f'Start interval download'), verbose )
    cnsl.log(f'[{ymd.now()}] Download url: {utils.str_max(url)}', verbose)
    cnsl.log(f'[{ymd.now()}] Download map: {utils.str_max(download_map)}', verbose)
    cnsl.log(f'[{ymd.now()}] Start download datetime: {start_datetime}', verbose)
    cnsl.log(f'[{ymd.now()}] End download datetime: {end_datetime}', verbose)
    cnsl.log(f'[{ymd.now()}] Interval time: {interval} minutes\n', verbose)

    ed_date, ed_time = end_datetime.split(' ') # Get end date time
    ok, ed_hms = validate.hhmmss(ed_time)
    ok, ed_ymd = validate.yyyymmdd(ed_date)
    num_act   = 1  # This is used to number the files
    fail_cnt  = 1  # Count failures
    fail_try  = 5  # How many tries
    fail_next = 60 # Wait for next try
    sec_interval = interval * 60 # Make interval time in seconds
    i_end_dt  = int(f'{ed_ymd}{ed_hms}') # Make end time

    # Start download loop
    while True:
        # Next download date and time
        dt_next = datetime.datetime.fromtimestamp( ymd.epoch_act() + sec_interval )
        ymd_next = dt_next.strftime('%Y%m%d')
        hms_next = dt_next.strftime('%H%M%S')

        # Make path
        y, m, d, H, M, S = ymd.y_m_d_h_m_s_now( )  # Get current date and time
        map  = mk_path(cfg.dir_download, f'{y}/{m}/{d}/{submap}')
        name = f'{basename}-{y}{m}{d}-{H}{M}{S}_{num_act}{ext}'
        path = mk_path(map, name) # Download path

        # Try to download image
        while fail_cnt <= fail_try:

            ok = download(url, path, check, verbose) # Download image and always show
            if ok: # If download is a succes
                lst_images.append(path) # Add image to downloaded images list
                num_act += 1 # Update num for next file only if download is a success
                break 

            else: # Download failed
                t  = f'[{ymd.now()}] Download failed {fail_cnt} time(s), '
                t += f'next try in {fail_next} seconds'
                cnsl.log(t, cfg.error) # Only once
                fail_cnt += 1 # Increase fails
                time.sleep(fail_next)
    
        fail_cnt = 1 # Try next image, next time

        cnsl.log(' ', verbose) # Spacer

        # Check for end of time
        if int(ymd.ymdhms_now()) > i_end_dt or \
           int(f'{ymd_next}{hms_next}') > i_end_dt: 
            break # Times out. No more downloads
        else:
            utils.pause(hms_next, ymd_next, f'Next download ({num_act}) at', verbose)

    cnsl.log( text.foot( f'End interval download' ), verbose )

    return lst_images