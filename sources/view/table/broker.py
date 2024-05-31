# -*- coding: utf-8 -*-
'''Library contain functions to make a 2d matrix table.
   Output can be tables html, texts et cetera'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.1.9'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import pandas as pd
import numpy as np
import sources.control.fio as fio
import sources.control.dayvalues.read as dayval_read
import sources.model.dayvalues.np_days as np_days
import sources.model.ymd as ymd
import sources.model.dayvalues.broker_period as broker
import sources.model.dayvalues.s4d_query as s4d_query
import sources.view.text as text
import sources.view.html as html
import sources.view.console as cnsl
import sources.view.table.header as header
import sources.view.table.body as body
import sources.view.table.footer as footer
import sources.view.table.compare as compare

def process(options, type='normal'):
    '''Function calculates all statistics'''
    cnsl.log(f'[{ymd.now()}] {options[text.ask_title].upper()}', True)

    # The main body rows with the data columns for the body (2D matrix)
    body_htm, body_txt, body_csv, options, cnt = body_rows_columns(options)

    # Count the cells in row
    options[text.ask_colspan] = len(options[text.ask_select_cells])

    # The header row with the columns for the table (2D matrix)
    head_htm, head_txt, head_csv, script = header.row(options)

    # The footer row with the column for the table (2D matrix)
    foot_htm, foot_txt, foot_csv = footer.row(options)

    # Remove separator (csv) at the end if there
    if len(head_csv) > 0 and head_csv[-1] == cfg.csv_sep: 
        head_csv = head_csv[:-1]
    if len(body_csv) > 0 and body_csv[-1] == cfg.csv_sep: 
        body_csv = body_csv[:-1]
    if len(foot_csv) > 0 and foot_csv[-1] == cfg.csv_sep: 
        foot_csv = foot_csv[:-1]

    # Merge header, body and footer
    htm = f'{head_htm}{body_htm}{foot_htm}{script}' # HTML data
    txt = f'{head_txt}\n{body_txt}{foot_txt}' # Text data
    csv = f'{head_csv}\n{body_csv}\n{foot_csv}' # Csv data

    # Output to screen or file(s) 
    ok, path = mk_output(htm, txt, csv, options)

    return ok, path

def body_rows_columns(options):
    '''Makes all the body rows'''
    body_htm, body_txt, body_csv, cnt = cfg.e, cfg.e, cfg.e, 0
    np_dummy = np_days.new()

    # Walkthrough stations and calculate statistics and add to table
    for station in options[text.ask_lst_stations]:
        t = text.info_line('Start', options, station)
        cnsl.log(t, True)

        err = cfg.e      
        period1 = options[text.ask_period_1]
        period2 = options[text.ask_period_2]

        # Read data station
        ok, np_lst_station = dayval_read.weatherstation(station, verbose=True)  

        # Check for values in period 1
        if np.size(np_lst_station) == 0: # No stations found.
            body_htm = body_htm + body.no_data_row_htm(station, options, 'all')
            body_txt = body_txt + cfg.no_val
            body_csv = body_csv + cfg.no_val
            continue

        if not ok: 
            err  = f'Error in table body_row_columns(){cfg.ln}data.read(){cfg.ln}'
            err += f'Options {options}{cfg.ln}Station {station}{cfg.ln}{np_lst_station}'
            cnsl.log(err, cfg.error)
            continue 

        # Period 2 empthy
        np_lst_period_2 = cfg.e

        # Get days period1
        ok, np_lst_period_1 = broker.process(np_lst_station, period1)

        # This must not happen.
        if not ok:
            err += f'Error in table body_row_columns(){cfg.ln}FN: broker.process(){cfg.ln}'
            err += f'np lst period 1 {period1}{cfg.ln}Options{cfg.ln}{options}'
            cnsl.log(err, cfg.error) 
            continue 

        # Check for values in period 1 
        # If there are no data  in this period put in an: no_value
        elif np.size(np_lst_period_1) == 0: 
            body_htm = body_htm + body.no_data_row_htm(station, options,  period1)
            body_txt = body_txt + cfg.no_val
            body_csv = body_csv + cfg.no_val
            continue

        # Check for data
        if ok: 
            # Check for the second period
            # !!! TODO NOT for compare (because second period needs to be calculated yet)
            if not options[text.ask_per_compare]:
                if period2 != cfg.e:
                    ok, np_lst_period_2 = broker.process(np_lst_period_1, period2)

                    # There is a critical error
                    if not ok:
                        err += f'Error in table body_row_columns(){cfg.ln}FN: broker.process(){cfg.ln}'
                        err += f'np lst period 2 {period2}{cfg.ln}Options{cfg.ln}{options}'
                        cnsl.log(err, cfg.error) 
                        continue 

                    # Check for values in period 1
                    # If there is no data for a given period give the no_value
                    if np.size(np_lst_period_2) == 0: 
                        body_htm = body_htm + body.no_data_row_htm(station, options,  period2)
                        body_txt = body_txt + cfg.no_val
                        body_csv = body_csv + cfg.no_val

                        continue

        # Make the rows for the table compare
        if options[text.ask_per_compare]: 
            htm, txt, csv, cnt = compare.process(station, options, np_lst_period_1, cnt)
            body_htm = body_htm + htm
            body_txt = body_txt + txt
            body_csv = body_csv + csv # Add to body

            t = text.info_line('End', options, station)
            cnsl.log(t, True)

            # Skip
            continue

        # TODO Search for days table
        if options[text.ask_s4d_query]: # Update days
            ok, np_lst_res = s4d_query.calculate(np_lst_period_1, options[text.ask_s4d_query]) 
            if not ok:
                continue
            else:
                for day in np_lst_res:
                    cnt += 1  # Count the days
                    htm, txt, csv = body.row(station, options,
                                             np_lst_res, np_lst_res, 
                                             day=day, cnt=cnt) # Get the cells with data
                    body_htm = body_htm + htm
                    body_txt = body_txt + txt
                    body_csv = body_csv + csv # Add to body

            t = text.info_line('End', options, station)
            cnsl.log(t, True )
            continue

        # Statistics table
        cnt += 1  # Count the days
        htm, txt, csv = body.row(station, options, np_lst_period_1, np_lst_period_2, 
                                 day=cfg.e, cnt=cnt) # Get the tr cells with data
        body_htm = body_htm + htm
        body_txt = body_txt + txt
        body_csv = body_csv + csv # Add to body

        t = text.info_line('End', options, station)
        cnsl.log(t, True)

    return body_htm, body_txt, body_csv, options, cnt

def mk_output(htm, txt, csv, options):
    '''Make output to screen or file(s)'''
    ok, path, ftyp = True, cfg.e, options[text.ask_file_type] 

    # Write output to console
    if cfg.console:
        cnsl.log(cfg.ln + text.head(f'{options[text.ask_title]} <console output>'), True)
        cnsl.log(txt, True) 
        cnsl.log(text.line('#') + cfg.ln, True)

    # Write to file
    if cfg.save_console_output and ftyp in text.lst_output_cnsl:
        # File name (base)
        fname_base = fio.sanitize_file_name(options[text.ask_title])
        # Make path with dates and times
        path = fio.path_with_act_date(cfg.dir_stats_cnsl, fname_base, extension='txt')
        # Write to file
        ok = fio.save(path, txt, verbose=cfg.debug)

    if ftyp in text.lst_output_files:
        # File name
        fname = options[text.ask_filename] + text.file_extension(ftyp) 

        # Data and dir 
        data, map = '.', cfg.dir_data 
        if   ftyp in text.lst_output_txt:
            data, map = txt, cfg.dir_stats_txt
        elif ftyp in text.lst_output_htm:
            data, map = htm, cfg.dir_stats_htm
        elif ftyp in text.lst_output_csv:
            data, map = csv, cfg.dir_stats_csv
        elif ftyp in text.lst_output_excel:
            data, map = csv, cfg.dir_stats_excel

        # Update dir with date maps
        path, map, _ = fio.mk_path_with_dates(map, fname) 

        # Make dir if not there yet 
        fio.mk_dir( map, verbose=False ) 

        # Create html file
        if ftyp in text.lst_output_htm: 
            page = html.Template()
            page.template = cfg.html_template_statistics
            page.verbose = False
            page.path_to_file = path
            page.path_to_root = cfg.path_to_html_root
            page.path_to_thirdparty = cfg.path_to_thirdparty
            page.title = options[text.ask_title]
            page.add_description(f'{options[text.ask_title]} {", ".join(options[text.ask_select_cells])}')
            page.main = data
            ok = page.save()  # Save page
            if not ok: 
                cnsl.log( f'Save {ftyp} file failed!', cfg.error )

        # text, csv option
        elif text.lst_output_csv:
            # Schrijf naar bestand
            ok = fio.save(path, data, verbose=True)

        # TODO Convert csv to excel 
        elif ftyp in text.lst_output_excel: 
            # Read the csv data with panda
            csv_data = pd.read_table(data, sep=cfg.csv_sep ) 

            # Write excel file
            csv_data.to_excel(path, index = None, header=True) 

    return ok, path
