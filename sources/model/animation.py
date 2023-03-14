# -*- coding: utf-8 -*-
'''Library contains functions for converting elements'''
__author__     = 'Mark Zwaving'
__email__      = 'markzwaving@gmail.com'
__copyright__  = 'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    = 'GNU General Public License version 3 - GPLv3'
__version__    = '0.0.3'
__maintainer__ = 'Mark Zwaving'
__status__     = 'Development'

import config as cfg
import sources.control.fio as fio
import sources.model.ymd as ymd
import sources.model.utils as utils
import sources.model.validate as validate
import sources.view.console as cnsl
import os, imageio, re, time, datetime

# Function creates an image animation
def create(
        path,          # File name for the animation image
        lst_images,    # List with all the images for the animation
        animation_time = cfg.animation_time,  # Interval time for the image
        verbose        = cfg.verbose # Show output on screen
    ):
    '''Function create an anmiation file, using imageio'''
    ok = False
    if not path:
        y, m, d, H, M, S = ymd.y_m_d_h_m_s_now() # Get current date and time
        animation_name = f'{cfg.animation_name}-{y}{m}{d}-{H}{M}{S}.{cfg.animation_ext}'
        animation_map = os.path.join(cfg.dir_animation, f'{y}/{m}/{d}')
        path = os.path.join(animation_map, animation_name)
    else:
        animation_map = os.path.dirname(path)

    cnsl.log(f'[{ymd.now()}] Start make animation', verbose)
    cnsl.log(f'Animation file: {path}', verbose)
    cnsl.log(f'Animation interval time: {animation_time} seconds', verbose)

    if lst_images:
        fio.mk_dir(animation_map, verbose) # Always make path before saving
        try: # Read imageio data in data lst from paths list
            data = [imageio.imread(img) for img in lst_images if os.path.exists(img)]
            imageio.mimsave(
                path,                   # Result animation file
                data,                   # Images data list for animation
                duration=float(animation_time) # Animation time
            ) 
        except Exception as e:
            cnsl.log(f'Error making an animation\n{e}', cfg.error)
        else:
            cnsl.log('Make animation success', verbose)
            ok = True
    else:
        cnsl.log('No images given to create an animation.', verbose)
    cnsl.log('End make animation\n', verbose)

    return ok, path

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
    lst_images = [] # List for the downloaded files with their name
    submap = utils.url_name(url)
    basename, ext = os.path.splitext(os.path.basename(url))
    y, m, d = ymd.yyyy_mm_dd_now()
    download_map = utils.mk_path(cfg.dir_download, f'{y}/{m}/{d}/{submap}')

    cnsl.log(f'[{ymd.now()}] Start interval download', verbose)
    cnsl.log(f'Internet url: {url}', verbose)
    cnsl.log(f'Download map: {download_map}', verbose)
    cnsl.log(f'Start date time: {start_datetime}', verbose)
    cnsl.log(f'End date time: {end_datetime}', verbose)
    cnsl.log(f'Interval time: {interval} minutes\n', verbose)

    # Get end date time
    ed_date, ed_time = end_datetime.split(' ')
    ok, ed_hms = validate.hhmmss(ed_time)
    ok, ed_ymd = validate.yyyymmdd_1(ed_date)
    i_end_time = int(f'{ed_ymd}{ed_hms}') # Make int for comparison
    num_act   = 1 # This is used to number the files
    fail_cnt  = 1  # Count failures
    fail_try  = 5 # How many tries
    fail_next = 60 # Wait for next try
    sec_interval = interval * 60 # Interval time in seconds

    # Start download loop
    while True:
        dt_next = datetime.datetime.fromtimestamp(ymd.epoch_act() + sec_interval)
        dt_date_next = dt_next.strftime('%Y%m%d')
        dt_time_next = dt_next.strftime('%H:%M:%S')
        ok, hms_next = validate.hhmmss(dt_time_next)
        ok, ymd_next = validate.yyyymmdd_1(dt_date_next)
        i_next_time = int(f'{ymd_next}{hms_next}')
        if i_end_time < i_next_time:
            break # Done

        # Make path
        y, m, d, H, M, S = ymd.y_m_d_h_m_s_now() # Get current date and time
        map  = utils.mk_path(cfg.dir_download, f'{y}/{m}/{d}/{submap}')
        name = f'{basename}-{y}{m}{d}-{H}{M}{S}_{num_act}{ext}'
        path = utils.mk_path(map, name) # Download path

        # Try to download image
        while fail_cnt <= fail_try:
            ok = fio.download(url, path, check, verbose) # Download image and always show
            if ok: # If download is a succes
                lst_images.append(path) # Add image to downloaded images list
                num_act += 1 # Update num for next file only if download is a success
                break
            else: # Downdt_time_nextload failed.
                t  = f'Download failed {fail_cnt} time(s), '
                t += f'next try in {fail_next} seconds'
                cnsl.log(t, cfg.error) # Only once
                fail_cnt += 1 # Increase fails
                time.sleep(fail_next)
        fail_cnt = 1 # Try next image, next time
        cnsl.log(' ', verbose) # Spacer
        utils.pause(dt_time_next, dt_date_next, f'next ({num_act}) download at', verbose)

    cnsl.log(f'[{ymd.now()}] End interval download\n', verbose)
    return lst_images


# Makes a animation of downloaded images
def download_images_and_make_animations(
        url,                                     # Url for the files on the web
        animation_name  = '',                    # Name of animation file   
        start_datetime  = 'yyyy-mm-dd hh:mm:ss', # Start time
        end_datetime    = 'yyyy-mm-dd hh:mm:ss', # End datetime
        interval        = 10,     # Interval time for downloading Images (minutes)
        check           = True,                  # No double downloads check
        animation_time  = cfg.animation_time,    # Animation interval time for gif animation
        remove_download = cfg.remove_download,   # Remove the downloaded images
        gif_compress    = cfg.gif_compress,      # Compress the size of the animation
        verbose         = cfg.verbose            # With output to screen
    ):
    '''Function download images for a given time and interval and creates an
       animation from the downloaded images'''
    cnsl.log(f'[{ymd.now()}] Start interval download and make an animation', verbose)
    cnsl.log(f'Url: {url}', verbose)
    cnsl.log(f'Start time: {start_datetime}', verbose)
    cnsl.log(f'End time: {end_datetime}', verbose)
    cnsl.log(f'Download interval: {interval} minutes', verbose)
    cnsl.log(f'Compress animation: {gif_compress}', verbose)
    cnsl.log(f'Remove downloaded images: {remove_download}\n', verbose)

    # Pause till start
    date_start, time_start = start_datetime.split(' ')
    utils.pause(time_start, date_start, 'download will start at', verbose)

    # Start interval downloads
    lst_images = download_interval(url, start_datetime, end_datetime, interval, check, verbose)

    # Animation name
    y, m, d, H, M, S = ymd.y_m_d_h_m_s_now() # Get current date and time
    animation_map = os.path.join(cfg.dir_animation, f'{y}/{m}/{d}')
    if not animation_name:
        animation_name = f'{cfg.animation_name}-{y}{m}{d}-{H}{M}{S}.{cfg.animation_ext}'
    path = utils.mk_path(animation_map, animation_name) # Make animation path

    # Make animation
    ok, path = create(path, lst_images, animation_time)

    if ok:
        if gif_compress: 
            ok = utils.compress_gif(path, verbose) # Compress animation
            if not ok:
                cnsl.log(f'Error in compressing animation file\nFile: {path}', cfg.error)
    else:
        cnsl.log(f'Error in make animation file\nFile: {path}', cfg.error)

    if remove_download: 
        fio.remove_files_in_list(lst_images, verbose) # Remove downloaded images

    cnsl.log(f'[{ymd.now()}] End download images and make an animation\n', verbose)
    return path
