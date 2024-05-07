# -*- coding: utf-8 -*-
'''Library contains functions for building html'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.1.6'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg, os
import sources.control.fio as fio
import sources.control.dayvalues.read as dayval_read
import sources.model.dayvalues.broker_period as broker
import sources.model.dayvalues.data as data
import sources.model.utils as utils
import sources.model.ymd as ymd
import sources.view.console as cnsl
import sources.view.html as html
import sources.view.text as text

def save_txt_file(path, fname, main, verbose=False):
    ''' Class to make a text page based on given entities'''
    dt = ymd.text(ymd.yyyymmdd_now())
    fname = f'{fname}-{dt}.txt'
    path = os.path.join(path, fname)
    l = lambda x, s : x * s + '\n'

    header = l(80,'#') + 'DAYVALUES'
    main = main
    footer  = cfg.knmi_dayvalues_notification 
    footer += text.created_by_notification + ' '
    footer += ymd.text_datetime_now()
    content = header + content + footer 

    ok = fio.write(path, content, verbose=verbose)

    return ok, path

def process(options, verbose=True):
    ok = True
    # Output file type
    ftyp = options[text.ask_file_type]
    # Col num ymd 
    col_ymd = data.column('yyyymmdd')

    # Path index to open the result file
    path_ndx = ''

    for station in options[text.ask_lst_stations]:
        t = f'[{ymd.now()}] Show day(s) for {station.wmo} {station.place}'
        cnsl.log(t, verbose)

        # Read data stations
        ok, np_lst_days = dayval_read.weatherstation(station)

        # Get the correct period 
        period = options[text.ask_period]

        # Get Days object with correct days for the given period
        ok, np_lst_period = broker.process(np_lst_days, period)

        # Make the correct wmo map. To save the file in
        base_dir = cfg.e
        if ftyp in text.lst_output_htm: 
            base_dir = cfg.dir_dayvalues_htm
        elif ftyp in text.lst_output_txt: 
            base_dir = cfg.dir_dayvalues_txt
        wmo_dir = fio.mk_path(base_dir, station.wmo)

        # Walk through all days in the given period
        for np_day in np_lst_period:
            # Get year, month and day of np day  
            y, m, d = ymd.split_yyyymmdd(ymd.symd(np_day[col_ymd]))

            # Make correct path based on year/month
            ym_dir = fio.mk_path(wmo_dir, f'{y}/{m}') 

            # Make filename
            fname = f'dayvalues-{station.wmo}-{y}-{m}-{d}{text.file_extension(ftyp)}'
            fpath = fio.mk_path(ym_dir, fname)

            # Skip if its add only and the file already exists
            if options[text.ask_write_dayval] == 'add':

                # Check if the file is already there
                if fio.check(fpath, verbose=False):

                    # Give skip text
                    t  = f'[{ymd.now()}] Skipped {options[text.ask_file_type]} '
                    t += f'dayvalues for {station.place} {utils.str_max(fpath)}'
                    cnsl.log_r(t, verbose)

                    # If file is already there, skip rest to go to the next file 
                    continue 
    
            # Give a text to say that a file will be written
            t  = f'[{ymd.now()}] Write {options[text.ask_file_type]} '
            t += f'dayvalues for {station.place} {utils.str_max(fpath)}'
            cnsl.log_r(t, verbose)

            # Get all data elements from th given np day
            stn, yyyymmdd, ddvec, fhvec, fg, fhx, fhxh, fhn, fhnh, \
            fxx, fxxh, tg, tn, tnh, tx, txh, t10n, t10nh, sq, sp, \
            q, dr, rh, rhx, rhxh, pg, px, pxh, pn, pnh, vvn, vvnh, \
            vvx, vvxh, ng, ug, ux, uxh, un, unh, ev24 = data.ents(np_day)

            # Get the correct text or html for the specific entitie given 
            # in the list 'lst-sel-cells'
            htm, txt = cfg.e, cfg.e
            for cell in options[text.ask_select_cells]:
                # Make HTML
                if ftyp in text.lst_output_htm:
                    if   cell == 'tx':    htm += html.day_value_tx(tx,txh)
                    elif cell == 'tg':    htm += html.day_value_tg(tg)
                    elif cell == 'tn':    htm += html.day_value_tn(tn,tnh)
                    elif cell == 't10n':  htm += html.day_value_t10n(t10n,t10nh)
                    elif cell == 'ddvec': htm += html.day_value_ddvec(ddvec)
                    elif cell == 'fhvec': htm += html.day_value_fhvec(fhvec)
                    elif cell == 'fg':    htm += html.day_value_fg(fg)
                    elif cell == 'fhx':   htm += html.day_value_fhx(fhx, fhxh)
                    elif cell == 'fhn':   htm += html.day_value_fhn(fhn, fhnh)
                    elif cell == 'fxx':   htm += html.day_value_fxx(fxx, fxxh)
                    elif cell == 'sq':    htm += html.day_value_sq(sq) 
                    elif cell == 'sp':    htm += html.day_value_sp(sp) 
                    elif cell == 'rh':    htm += html.day_value_rh(rh)
                    elif cell == 'rhx':   htm += html.day_value_rhx(rhx, rhxh)
                    elif cell == 'dr':    htm += html.day_value_dr(dr)
                    elif cell == 'px':    htm += html.day_value_px(px, pxh)
                    elif cell == 'pg':    htm += html.day_value_pg(pg)
                    elif cell == 'pn':    htm += html.day_value_pn(pn, pnh)
                    elif cell == 'ux':    htm += html.day_value_ux(ux, uxh)
                    elif cell == 'ug':    htm += html.day_value_ug(ug)
                    elif cell == 'un':    htm += html.day_value_un(un, unh)
                    elif cell == 'vvx':   htm += html.day_value_vvx(vvx, vvxh)
                    elif cell == 'vvn':   htm += html.day_value_vvn(vvn, vvnh)
                    elif cell == 'ng':    htm += html.day_value_ng(ng)
                    elif cell == 'q':     htm += html.day_value_q(q)
                    elif cell == 'ev24':  htm += html.day_value_ev24(ev24)

            # Check if a directory exists
            # If it's not there make the map
            ok = os.path.isdir(ym_dir) 
            if ok: 
                # Year/month map already exists
                cnsl.log(f'Create map {ym_dir} successful', False)
            else:
                # Map does not exist. Make necessary map
                ok = fio.mk_dir(ym_dir, verbose=False)
                if not ok: 
                    t = f'Error in dayvalues process(). Make a map {ym_dir}'
                    cnsl.log(t, cfg.error)

            # Make html output
            if ftyp in text.lst_output_htm: 
                datestring = ymd.yyyymmdd_to_text( np_day[col_ymd] )
                header  = f'<i class="text-info fas fa-home"></i> '
                header += f'{station.wmo} - {station.place} '
                header += f'{station.province} - {datestring} '

                # Unused HTML
                # foot  = f'{cfg.knmi_dayvalues_notification}<br>'
                # foot += f'Made by WeatherstatsNL on {ymd.txt_datetime_now()}'

                # Path (empthy) js file
                path_js = f'{cfg.path_to_html_root}js/default.js'

                # Descriptions (meta tag)
                meta_description = f'Dayvalues for {station.wmo} {station.place} on {datestring}' 

                # Page title html/meta tag
                page_title = f'{station.wmo} {station.place} {datestring}'

                # Create HTML object
                page = html.Template()
                page.add_js_file(path_js) # Add own content
                page.template = cfg.html_template_dayvalues
                page.verbose = False
                page.strip = True
                page.path_to_file = fpath
                page.path_to_root = cfg.path_to_html_root
                page.path_to_thirdparty = cfg.path_to_thirdparty
                page.add_description(meta_description)
                page.title  = page_title
                page.header = header
                page.main   = htm

                # Save HTML page
                ok = page.save()
                if not ok:
                    t = 'Error in dayvalues process(). Failed to save html file'
                    cnsl.log(t, cfg.error)

                # Default index html file
                path_ndx = fio.mk_path(cfg.dir_dayvalues_htm, f'index.html')

            # TODO
            elif ftyp in text.lst_output_txt:
                main  = ''
                ok, path_ndx = save_txt_file(fpath, fname, main, verbose=False)

        cnsl.log(f'\n[{ymd.now()}] Dayvalues {station.wmo} {station.place} done!', verbose)

    return ok, path_ndx # Make link html only. 
