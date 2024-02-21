# -*- coding: utf-8 -*-
'''Library contains functions for building html'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 3 - GPLv3'
__version__    =  '0.1.3'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg, os
import sources.model.daydata as daydata
import sources.model.stats as stats
import sources.model.utils as utils
import sources.view.html as html
import sources.view.text as text
import sources.control.fio as fio
import sources.view.console as cnsl
import sources.model.ymd as ymd

def calculate(options):
    ok = True
    ftyp = options[text.ask_file_type]

    cnsl.log(f'[{ymd.now()}] Start {options[text.ask_title]}', True)
    path_ndx_html = fio.mk_path(cfg.dir_dayvalues_htm, f'index.html')
    # input(ftyp)

    for station in options[text.ask_stations]:
        cnsl.log(f'[{ymd.now()}] Make dayvalues for {station.wmo} {station.place}', True)

        if options[text.ask_download]:
            daydata.process_data( station )

        ok, np_data_2d = daydata.read(station) # Read data stations
        days = stats.Days(station, np_data_2d, options[text.ask_period]) # Get Days object with correct days

        # Make base path and wmo dir
        base_dir = cfg.e
        if   ftyp in text.lst_output_htm: base_dir = cfg.dir_dayvalues_htm
        elif ftyp in text.lst_output_txt: base_dir = cfg.dir_dayvalues_txt
        wmo_dir = fio.mk_path(base_dir, station.wmo)

        # Walk all dates
        for day in days.np_period_2d:

            # print(f'day -> {day}')

            # Make path. Get year, month and day
            y, m, d = ymd.split_yyyymmdd(day[daydata.etk('yyyymmdd')])
            ym_dir = fio.mk_path(wmo_dir, f'{y}/{m}') # Make path year/month
            path_to_file = fio.mk_path(ym_dir, f'dayvalues-{station.wmo}-{y}-{m}-{d}{text.file_extension(ftyp)}')

            # input(path_to_file)

            # Skip ?
            if options[text.ask_write_dayval] == 'add':
                if fio.check(path_to_file, verbose=False):  # Check if there is a file
                    t  = f'[{ymd.now()}] Skipped {options[text.ask_file_type]} dayvalues for {station.place} ...{path_to_file[-57:]}'
                    cnsl.log_r(t, True)
                    continue # If already there skip 
    
            t  = f'[{ymd.now()}] Write {options[text.ask_file_type]} dayvalues for {station.place} ...{path_to_file[-57:]}'
            cnsl.log_r(t, True)

            # Get all data elements from a dayc
            stn, yyyymmdd, ddvec, fhvec, fg, fhx, fhxh, fhn, fhnh, fxx, fxxh, tg, tn,\
            tnh, tx, txh, t10n, t10nh, sq, sp, q, dr, rh, rhx, rhxh, pg, px, pxh,\
            pn, pnh, vvn, vvnh, vvx, vvxh, ng, ug, ux, uxh, un, unh, ev24 = daydata.ents(day)

            # input(stn)

            # Make text or htm for entities given in 'lst-sel-cells'
            htm, txt = cfg.e, cfg.e
            for cell in options[text.ask_select_cells]:
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
                elif ftyp in text.lst_output_txt:
                    # TODO
                    pass

            # Check and make directories
            ok = os.path.isdir(ym_dir)
            if not ok: # Check and make necessary maps
                ok = fio.mk_dir(ym_dir, verbose=False)

            if ok: # Month map exists
                cnsl.log(f'Map to make {ym_dir} is done!', False)
            else:
                cnsl.log(f'Error make map {ym_dir}', cfg.error)

            # Make output
            datestring = ymd.text(day[daydata.etk('yyyymmdd')])
            header  = f'<i class="text-info fas fa-home"></i> '
            header += f'{station.wmo} - {station.place} '
            header += f'{station.province} - {datestring} '

            foot  = f'{cfg.knmi_dayvalues_notification}<br>'
            foot += f'Made by WeatherstatsNL on {ymd.txt_datetime_now()}'

            # HTML object
            page = html.Template()
            page.add_js_file(f'{cfg.path_to_html_root}js/default.js') # Add own content
            page.template = cfg.html_template_dayvalues
            page.verbose = False
            page.strip = True
            page.path_to_file = path_to_file
            page.path_to_root = cfg.path_to_html_root
            page.path_to_thirdparty = cfg.path_to_thirdparty
            page.add_description(f'Dayvalues for {station.wmo} {station.place} on {datestring}' )
            page.title  = f'{station.wmo} {station.place} {datestring}'
            page.header = header
            page.main   = htm
            page.footer = foot
            ok = page.save()

            if not ok:
                cnsl.log('\nFailed!\n', cfg.error)

        cnsl.log(f'\n[{ymd.now()}] Dayvalues {station.wmo} {station.place} done!', True)

    return ok, path_ndx_html # Make link html only. 
