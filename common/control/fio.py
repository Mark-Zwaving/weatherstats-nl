# -*- coding: utf-8 -*-
'''Functions for io file handling.
   Creating, writing, deleting, downloading, unzipping a file'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'MIT License'
__version__    =  '0.1.8'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import common.cmn_cfg as cfg
import common.model.convert as cvt
import common.view.console as cnsl
import common.model.ymd as ymd
import common.model.validate as validate
import common.model.util as util
import threading, urllib, json, os, time, zipfile, webbrowser
import datetime, requests, socket, shutil, subprocess, sys

abspath = lambda path: os.path.abspath(path)
mk_path = lambda dir, f: abspath(os.path.join(dir, f))

def open_with_app(fname, verbose=cfg.verbose):
    '''Function opens a file with an default application'''
    ok, err = False, ''
    cnsl.log(f'Start open file with an app {ymd.now()}', verbose)

    if check(fname, verbose):
        cnsl.log(f'File {fname}', verbose)

        # Linux
        if sys.platform.startswith('linux'):
            try:
                subprocess.call( ['xdg-open', fname] )
            except Exception as e:
                err += f'{e}\n'
                try:
                    os.system(f'start {fname}')
                except Exception as e:
                    err += f'{e}\n'
                else:
                    ok = True
            else:
                ok = True

        # OS X
        elif sys.platform.startswith('darwin'): # ?
            try: 
                os.system( f'open "{fname}"' )
            except Exception as e: 
                err += f'{e}\n'
            else: 
                ok = True

        # Windows
        elif sys.platform in ['cygwin', 'win32']:
            try: # Should work on Windows
                os.startfile(fname)
            except Exception as e:
                err += f'{e}\n'
                try:
                    os.system( f'start "{fname}"' )
                except Exception as e:
                    err += f'{e}\n'
                else:
                    ok = True
            else:
                ok = True

        # Possible fallback, use the webbrowser
        if not ok:
            try: webbrowser.open_new_tab(fname)
            except Exception as e: err += e
            else: ok = True

    else:
        cnsl.log(f'File not found', cfg.error)

    if ok: 
        cnsl.log('Open file with an app successfull', verbose)
    else: 
        cnsl.log(f'Error open file with an app\n{err}', cfg.error)

    return ok


def lst_maps(map, recursive=True, secret=True, verbose=cfg.verbose):
    '''Returns a list with all the (sub) directories'''
    lst = []
    cnsl.log(f'[{ymd.now()}] check for directories', verbose)
    cnsl.log(f'In map {map}', verbose)
    for el in os.listdir(map):
        # skip secret maps
        if not secret: 
            if el[0] == '.': 
                continue  

        path = mk_path(map, el)
        if os.path.isdir(path): # Check paths if is a map
            cnsl.log(f'Map found: {map}', verbose)
            lst.append(path)
            if recursive: # Add subdirectories too
                lst += lst_maps(path)

    return lst

def check(path, verbose=cfg.verbose):
    '''Function checks a file for existence'''
    ok = False
    cnsl.log(f'[{ymd.now()}] check file exists', verbose)
    cnsl.log(f'File {path}', verbose)
    with threading.Lock():
        try:
            if os.path.exists(path):  # Check if is there file
                ok = True
        except Exception as e:
            cnsl.log(f'Error check\n{e}', cfg.error)
        else:
            if ok:
                cnsl.log('File exists', verbose)
            else:
                cnsl.log('File does not exist', verbose)
    return ok

def write(path='dummy.txt', content='', encoding='utf-8', prefix='w', verbose=cfg.verbose):
    '''Function writes content to a file'''
    ok = False
    cnsl.log(f'[{ymd.now()}] write a file', verbose)
    cnsl.log(f'File {path}', verbose)
    with threading.Lock():
        try:
            map = os.path.dirname(path)
            if map: mk_dir(map, verbose) # Make map(s)
            with open(path, encoding=encoding, mode=prefix) as f:
                f.write(content)
        except Exception as e:
            cnsl.log(f'Error writing file\n{e}', cfg.error)
        else:
            cnsl.log('Write file success', verbose)
            ok = True
    return ok

def save(path='dummy.txt', content='', encoding='utf-8', prefix='w', verbose=cfg.verbose):
    '''Function writes content to a file'''
    return write(path, content, encoding, prefix, verbose)

def read(path, encoding='utf-8', verbose=cfg.verbose):
    '''Function reads the content in a file'''
    ok, t, paths = False, '', cvt.to_lst(path)
    cnsl.log(f'[{ymd.now()}] read a file', verbose)
    cnsl.log(f'File(s) {cvt.to_lst(paths)}', verbose)

    for path in paths: # All paths
        with threading.Lock():
            if check(path, verbose):
                try:
                    with open(path, encoding=encoding, mode='r') as f:
                        t = f.read()
                except Exception as e:
                    cnsl.log(f'Error reading a file\n{e}', cfg.error)
                else:
                    cnsl.log('Read file success', verbose)
                    ok = True
    return ok, t

def readlines(path, encoding='utf-8',verbose=cfg.verbose):
    '''Function reads the content from a file into a list'''
    l, ok, t, paths = [], False, '', cvt.to_lst(path)
    cnsl.log(f'[{ymd.now()}] read file(s) to a list', verbose)
    cnsl.log(f'File(s) {cvt.to_lst(paths)}', verbose)

    for path in paths: # All paths
        with threading.Lock():
            if check(path, verbose):
                try:
                    with open(path, encoding=encoding, mode='r') as f:
                        l = f.readlines()
                except Exception as e:
                    cnsl.log(f'Error reading a file\n{e}', cfg.error)
                else:
                    cnsl.log('Read file success', verbose)
                    ok = True
    return ok, l

def delete(path, verbose=cfg.verbose):
    '''Function deletes a file if exists'''
    ok, paths = False, cvt.to_lst(path)
    cnsl.log(f'[{ymd.now()}] delete file(s)', verbose)
    cnsl.log(f'File(s) {cvt.to_lst(paths)}', verbose)

    for path in paths: # All paths
        with threading.Lock():
            if check(path, verbose):
                try:
                    os.remove(path)  # Remove file
                except Exception as e:
                    cnsl.log(f'Error deleting a file\n{e}', cfg.error)
                else:
                    cnsl.log('Delete file success', verbose)
                    ok = True
            else:
                cnsl.log(f'Cannot delete. File does not exist', verbose)
    return ok

def rm(path, verbose=cfg.verbose):
    '''Function removes a file if exists (canonical) for delete()'''
    return delete(path, verbose)

def mk_dir(dir, verbose=cfg.verbose):
    '''Function makes a map if not already exists'''
    ok, paths = False, cvt.to_lst(dir)
    cnsl.log(f'[{ymd.now()}] make directory(s)', verbose)
    cnsl.log(f'File(s) {cvt.to_lst(paths)}', verbose)

    for path in paths: # All paths
        with threading.Lock():
            try:
                if os.path.isdir(path):
                    cnsl.log('Map not made because it already exists.', verbose)
                    ok = True
                else:
                    os.makedirs(path)
            except Exception as e:
                cnsl.log(f'Error make directory\n{e}', cfg.error)
            else:
                cnsl.log(f'Make directory {path} successful', verbose)
                ok = True

    return ok

# Function removes a map, empthy or not
def rm_dir(
        dir, # Map to remove
        verbose=cfg.verbose
    ):
    '''Function deletes an directory empty or not'''
    ok, paths = False, cvt.to_lst(dir)
    cnsl.log(f'[{ymd.now()}] remove directory(s)', verbose)
    cnsl.log(f'Dir(s) {cvt.to_lst(paths)}', verbose)

    for path in paths: # All paths
        with threading.Lock():
            if os.path.exists(path):
                try:
                    shutil.rmtree(path)
                except Exception as e:
                    cnsl.log(f'Error removing map\n{e}', cfg.error)
                else:
                    cnsl.log('Remove map {path} successful', verbose)
                    ok = True
            else:
                cnsl.log('Cannot remove {path}.\nMap does not exist.', verbose)
    return ok

def is_dir_empthy(dir, verbose=cfg.verbose):
    ok = False
    cnsl.log(f'[{ymd.now()}] check empty dir', verbose)
    cnsl.log(f'Dir {dir}', verbose)

    if os.path.exists(dir):
        ok = True if len(os.listdir(dir)) == 0 else False
    else:
        cnsl.log('Map does not exist.', verbose)
        ok = True

    return ok

def unzip(zip, txt, verbose=cfg.verbose):
    '''Function unzips a zipfile'''
    ok = False
    cnsl.log(f'[{ymd.now()}] unzip a file', verbose)
    cnsl.log(f'From {zip}\nTo {txt}', verbose) # TODO force to txt file
    with threading.Lock():
        try:
            dir_txt = os.path.dirname(txt)
            with zipfile.ZipFile(zip, 'r') as z:
                z.extractall(dir_txt)
        except Exception as e:
            cnsl.log(f'Error unzip\n{e}', cfg.error)
        else:
            cnsl.log('Unzip success', verbose)
            ok = True
    return ok

def download(
        url,  # Url to download
        path, # Path to download the file to
        check   = False,  # <optional> Check file True will not overwrite the file if exists
        verbose = cfg.verbose  # <optional> Overwrite default value verbose -> see config.py
    ):
    '''Function downloads a file from an internet url'''
    ok = False
    cnsl.log(f'[{ymd.now()}] download', verbose)
    cnsl.log(f'From {url}\nTo {path}', verbose)

    # Check if image is already downloaded
    if check and os.path.exists(path):
        cnsl.log(f'Download skipped, file already exists', verbose)
        ok = True
    else:
        with threading.Lock():
            if url_exists(url, verbose): # Check if a url exists
                try:
                    mk_dir(os.path.dirname(path), verbose) # Make map if not exists
                    urllib.request.urlretrieve( url, path ) # Download file
                except Exception as e:
                    cnsl.log(f'Error in download {e}', cfg.error)
                else:
                    cnsl.log('Download success', verbose)
                    ok = True
            else:
                cnsl.log(f'Url {url} does not exist', True)
        # Do not flood server protection
        wait = cfg.download_interval_time
        time.sleep(0.2 if wait < 0.2 else wait)
    return ok

def download_read_file(url, file, verbose=cfg.verbose):
    '''Function downloads a file, read the file and return the content of the file'''
    ok, t = False, ''
    cnsl.log(f'[{ymd.now()}] download and read', verbose)
    cnsl.log(f'Url: {url}', verbose)
    cnsl.log(f'To file: {url}', verbose)
    if has_internet(verbose):
        ok = download( url, file, verbose )
        if ok: 
            ok, t = read(file)
    else:
        t = 'Cannot download file. There is no internet connection'
        cnsl.log(t, cfg.error)
    return ok, t

def request(url, type='txt', verbose=cfg.verbose):
    '''Function makes the request based on the url given as parameter
       The return values are: ok, True if success else False... And the text From
       the request.'''
    ok, t = False, ''
    cnsl.log(f'[{ymd.now()}] {type} - request', verbose)
    cnsl.log(f'Url: {url}', verbose)
    with threading.Lock():
        try:
            resp = urllib.request.urlopen( url )
            data = resp.read()
            if type == 'text':
                t = data
            elif type == 'json':
                t = json.loads(data)
        except Exception as e:
            cnsl.log(f'Error request\n{e}', cfg.error)
        else:
            cnsl.log('Request success', verbose)
            ok = True
    return ok, t

def request_text(url, verbose=cfg.verbose):
    '''Function makes an online request for a text file'''
    return request(url, 'txt', verbose)

def request_json( url, verbose=cfg.verbose):
    '''Function makes an online request for a json file'''
    return request(url, 'json', verbose)

def has_internet(verbose=cfg.verbose):
    '''Function checks if there is a internet connection available'''
    ok = False
    cnsl.log(f'[{ymd.now()}] check internet connection', verbose)
    cnsl.log(f'Url {cfg.check_internet_url}', verbose)
    with threading.Lock():
        try:
            sock = socket.create_connection((cfg.check_internet_url, 53))
            if sock: sock.close()
        except Exception as e:
            cnsl.log(f'Check failed\n{e}', verbose)
        else:
            cnsl.log('Check succes', verbose)
            ok = True
    return ok

# Function checks if a url exists
def url_exists(url, verbose=cfg.verbose):
    '''Function checks if a url exists. Return True or False'''
    cnsl.log(f'[{ymd.now()}] check url existence', verbose)
    cnsl.log(f'Url {url}', verbose)
    with threading.Lock():
        try:
            resp = requests.head(url)
            ok = True if resp.status_code == 200 else False
        except Exception as e:
            cnsl.log(f'Error url exist\n{e}', cfg.error)
        else:
            cnsl.log('Url exists', verbose)
            ok = True
    return ok

# Function get files in a dir. Filering can be done based on keywords and extenions
def lst_files_dir(
        dir,             # Dir to search for files
        extensions = '', # <optional> List of extensions or one string ext to search the map for
        keywords   = '', # <optional> List of keyword or one string to search the directory for
        case_insensitive = True, # <optional> Search case insensitive. True by default.
        verbose = cfg.verbose  # <optional> Overwrite verbose option
    ):
    '''Function list files in a directory. The list can be filtered by keywords
       and extensions.'''
    paths = cvt.to_lst(dir)
    cnsl.log(f'[{ymd.now()}] list files directory(s)', verbose)
    cnsl.log(f'Dir(s) {cvt.to_lst(paths)}', verbose)

    results = [] # List with found paths
    for path in paths: # All paths
        if not os.path.exists(path): # Check map
            cnsl.log(f'Path {path} does not exist', verbose)
        else:
            # Check types and add to an (empty) list element if needed
            len_ext, len_key = 0, 0
            if extensions:
                extensions = cvt.to_lst(extensions)
                len_ext = len(extensions)
            if keywords:
                keywords = cvt.to_lst(keywords)
                len_key = len(keywords)
    
            filter_on = True if (len_key + len_ext) > 0 else False # Filter on ?
    
            if len_key > 0: 
                cnsl.log(f'Search words { cvt.lst_to_s(keywords,", ") }', verbose)
            if len_ext > 0: 
                cnsl.log(f'Search extensions { cvt.lst_to_s(extensions,", ") }', verbose)

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
                fname, ext =  os.path.splitext(f)

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
                    else: # All words are True
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
                    cnsl.log(f'File found {path}', verbose)
                    results.append(path)

    return results


# Function downloads in interval for a period of time and returns a list with
# the images
def download_interval(
       url,          # Url for the files on the web
       map           = cfg.dir_download, # Map for the downloads
       interval      = 10,    # Interval time for downloading Images (minutes)
       duration      = 1*60,  # Total time for downloading all the images (minutes)
       date_submap   = False, # Set True to the possible given date submaps
       date_subname  = False, # Add date and time to downloaded files
       check         = True,  # No double downloads check
       verbose       = cfg.verbose  # With output to screen
    ):
    '''Download files from the web in interval for a period of time.
       Returns a list with the names of the downloaded files.'''
    # Update map
    base_map, submap = map, util.url_name(url)
    y, m, d = ymd.yyyy_mm_dd_now()
    map = mk_path(base_map, f'{y}/{m}/{d}/{submap}') if date_submap else base_map
    cnsl.log(f'[{ymd.now()}] interval download', verbose)
    cnsl.log(f'Internet url is {url}', verbose)
    cnsl.log(f'Download map is {map}', verbose)
    cnsl.log(f'Interval time is {interval} minutes', verbose)
    cnsl.log(f'Duration time is {duration} minutes', verbose)

    num_act   = 1 # This is used to number the files
    num_max   = 10000 # Maximum number files for interval downloads
    fail_cnt  = 1  # Count failures
    fail_try  = 10 # How many tries
    fail_next = 60 # Wait for next try
    lpaths    = [] # List for the downloaded files with their name

    # Get name and extension of downloaded file
    name, ext = os.path.splitext(os.path.basename(url))
    ext = validate.extension(ext) # Check extension

    # Calculate end time (in seconds) for downloading files
    time_end = int(round(duration * 60)) + time.time()
    time_interval = int(round(interval * 60)) # Calculate interval seconds
    time_download = 0 # Epoch seconds. Set to 0 to always start a download for the first time

    cnsl.log(' ', verbose) # Spacer
    # Start download loop
    while True:
        time_act = time.time() # Get current time (epoch seconds)

        # Extern time shift (eg. wintertime). Wait untill we are at last time
        while time_download > time_act: time_act = time.time()

        y, m, d, hh, mm, ss = ymd.y_m_d_h_m_s_now() # Get current date and time
        yyyymmdd_act = f'{y}{m}{d}' # Make current date

        # Update map only if date_submaps is True
        map = mk_path(base_map, f'{y}/{m}/{d}/{submap}') if date_submap else base_map

        # Make a download file name
        fname = f'{name}_{num_act}'
        if date_subname: fname += f'_{y}{m}{d}_{hh}{mm}{ss}'
        fpath = mk_path(map, f'{fname}{ext}') # Download path

        # Try to download image
        while fail_cnt <= fail_try:
            ok = download(url, fpath, check, verbose) # Download image and always show
            if ok: # If download is a succes
                lpaths.append(fpath) # Add image to downloaded images list
                num_act += 1 # Update num for next file only if download is a success
                break
            else: # Download failed.
                for i in range(fail_next):
                    t  = f'Download failed {fail_cnt} time(s), '
                    t += f'next try in {fail_next-i} seconds'
                    if cfg.timer: cnsl.log_r(t, cfg.error)
                    elif i == 0: cnsl.log(t, cfg.error) # Only once
                    time.sleep(1)

                fail_cnt += 1 # Increase fails

        # Check time to stop or too much files reached
        if time_act >= time_end or num_act >= num_max: break  # Done

        # Update vars
        time_download = time_act # Update last_download time
        fail_cnt = 1 # Try next image, next time

        # Wait untill next download
        dt = datetime.datetime.fromtimestamp(time_download + time_interval)
        util.pause( dt.strftime('%H:%M:%S'), dt.strftime('%Y%m%d'),
                    f'next ({num_act}) download {name} at' )
    return lpaths

def rm_lst(lst = [], remove_empty=False, verbose=cfg.verbose):
    '''Function tries to remove all files in the list.'''
    cnsl.log(f'[{ymd.now()}] remove files in list', verbose)
    for path in list(set(lst)): # Make list unique and walkthrough paths
        if delete(path, verbose): # Remove file from disk
            dir = os.path.dirname(path) # Get map from path
            # Remove maps only empty maps and remove_empty is True
            while is_dir_empthy(dir, verbose) and remove_empty:
                rm_dir(dir, verbose) # Remove empty map
                dir = os.path.dirname(dir) # Go to upper dir

# Function downloads a list of files uries on the web to a local path list
def lst_download(
        uries = [],     # List with download urls
        paths = [],     # <optional> List with names for the files from the download urls
        check = True,   # Already download check. Do not overwrite download file
        verbose=cfg.verbose # Output to screen
    ):
    '''Downloads images based on two lists. It combines an uries list with a path list'''
    cnsl.log(f'[{ymd.now()}] download list', verbose)
    if not paths: # If no paths, make them based on the uries
        for url in uries:
            locnet = util.url_name(url) # Get name url
            name, ext = util.name_ext(path) # Get name and extension
            ext = validate.extension(ext) # Handle dot.
            path = mk_path(cfg.dir_download, f'{locnet}_{name}{ext}') # Make image path
            paths.append(path) # Add to list

    res_urie, res_path, max = [], [], cfg.download_max_num
    # Combine/zip the two lists (with download paths and web urls) into one list
    for path, url in tuple(zip(paths[:max], uries[:max])): # Loop through img and url objects
        ok = download(url, path, check, verbose) # Download file
        if ok: # Success add to lists
            res_urie.append(url)
            res_path.append(path)

    return res_urie, res_path # Return correct paths
