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
import sources.model.dayvalues.data as data
import sources.model.utils as utils
import sources.model.ymd as ymd
import sources.model.dayvalues.broker_period as broker
import sources.model.dayvalues.s4d_query as s4d_query
import sources.view.text as text
import sources.view.icon as icon
import sources.view.html as html
import sources.view.column.condition_cnt as condit_cnt
import sources.view.column.indexes as col_ndx
import sources.view.column.sum as col_sum
import sources.view.column.mean as col_mean
import sources.view.column.inf as col_inf
import sources.view.column.extreme as col_extreme
import sources.view.column.clima as col_clima
import sources.view.column.fixed_day as col_fixed_day
import sources.view.console as cnsl

def process(options, type='normal'):
    '''Function calculates all statistics'''
    cnsl.log(f'[{ymd.now()}] {options[text.ask_title].upper()}', True)

    # The main body rows with the data columns for the body (2D matrix)
    body_htm, body_txt, body_csv, options, cnt = body_rows_columns(options)

    # Count the cells in row
    options[text.ask_colspan] = len(options[text.ask_select_cells])

    # The header row with the columns for the table (2D matrix)
    head_htm, head_txt, head_csv, script = header_row(options)

    # The footer row with the column for the table (2D matrix)
    foot_htm, foot_txt, foot_csv = footer_row(options)

    # Remove separator (csv) at the end if there
    if len(head_csv) > 0 and head_csv[-1] == cfg.csv_sep: head_csv = head_csv[:-1]
    if len(body_csv) > 0 and body_csv[-1] == cfg.csv_sep: body_csv = body_csv[:-1]
    if len(foot_csv) > 0 and foot_csv[-1] == cfg.csv_sep: foot_csv = foot_csv[:-1]

    # Merge header, body and footer
    htm = f'{head_htm}{body_htm}{foot_htm}{script}' # HTML data
    txt = f'{head_txt}\n{body_txt}{foot_txt}' # Text data
    csv = f'{head_csv}\n{body_csv}\n{foot_csv}' # Csv data

    # Output to screen or file(s) 
    ok, path_to_file = mk_output(htm, txt, csv, options)

    return ok, path_to_file

def header_row(options):
    '''Makes the header'''
    head_htm, head_txt, head_csv = cfg.e, cfg.e, cfg.e

    # Sorting script vars
    col_num    = 0     # Start column num is 0 increment at start
    descending = '+'   # Identifier sort direction: large to small
    ascending  = '-'   # Identifier sort direction: small to high
    sort_num   = 'num' # Identifier sort num-based
    sort_txt   = 'txt' # Identifier sort txt-based
    row_num    = 2     # Row tr num for click to sort
    # Add a script with a Javascript object for sorting with columns
    script     = cfg.e 
    file_type  = options[text.ask_file_type]

    if file_type in text.lst_output_htm:
        head_htm += f'''
        <table class="rounded shadow border" id="stats"><thead><tr>
            <th colspan="{options[text.ask_colspan]}">
                {icon.weather_all()} 
                {options[text.ask_title]} 
                {icon.wave_square()} 
                {options[text.ask_period]} 
                {icon.cal_period()}                 
            </th></tr><tr>
        '''

    if file_type in text.lst_output_txt_cnsl:
        pass # head_txt += '#' * 80 + '\n'

    for option in options[text.ask_select_cells]:
        txt, htm, csv = '', '', '' # Init reset
        # Sort options. 
        # Defaults: sort is True, numeric and descending. Add 1 to col_num
        sort_type, sort_dir, col_num = sort_num, descending, col_num + 1

        # Make list from cell id. Exemple: tx_>=_10 : entity sign value
        lst_col = option.split(cfg.cells_separator) 

        # Get base values for cell
        stats, entity = lst_col[0], lst_col[1]

        # Info texts
        if stats in text.lst_info:
            txt, htm, csv = col_inf.header(lst_col, file_type)

            # Update sort type for geo places
            if entity in text.lst_geo_places:
                sort_type = sort_txt  # Text sort

        # Fixed day values
        elif stats in text.lst_day:
            txt, htm, csv = col_fixed_day.header(lst_col, file_type)

        # Max extreme
        elif stats in text.lst_extremes:
            txt, htm, csv = col_extreme.header(lst_col, file_type)

        # Average
        elif stats in text.lst_ave:
            txt, htm, csv = col_mean.header(lst_col, file_type)

        # Sum
        elif stats in text.lst_sum:
            txt, htm, csv = col_sum.header(lst_col, file_type)

        # Indexes
        elif stats in text.lst_ndx:
            txt, htm, csv = col_ndx.header(lst_col, file_type)

        # Counters
        elif stats in text.lst_count:
            txt, htm, csv = condit_cnt.header(lst_col, file_type)

        # Climate
        elif stats in text.lst_clima:
            txt, htm, csv = col_clima.header(lst_col, file_type)

        # Add Sort Script
        if file_type in text.lst_output_htm:
            col_id = text.strip_all_whitespace(f'{entity}_col_{col_num}'.replace('-','_')).upper()
            script += js_script_fn( col_id, sort_type, sort_dir, row_num, col_num )

        # Add (cells) to head (row) output
        head_txt = head_txt + txt
        head_htm = head_htm + htm
        head_csv = head_csv + csv 

    # Close all for html
    if file_type in text.lst_output_htm: 
        head_htm += '</tr></thead><tbody>'

    # Make JS script
    js  = ' <script> ' 
    js += 'let col_titles = { ' 
    js += script.strip()[:-1]  # Remove comma
    js += ' }; </script> '     # Close JS object and script tag

    # Return headers
    return head_htm, head_txt.upper(), head_csv, js

def footer_row(options):
    '''Makes the footer'''
    foot_htm, foot_txt, foot_csv, ftyp = cfg.e, cfg.e, cfg.e, options[text.ask_file_type]

    if ftyp in text.lst_output_htm:
        foot_htm += f'''
        </tbody><tfoot>
        <tr><td class="text-muted" colspan="{options[text.ask_colspan]}">
        <small> {text.create_by_notification_html().replace("<br>", " ")} </small>
        </td></tr>
        </tfoot></table>'''

    if ftyp in text.lst_output_txt_cnsl:
        foot_txt += cfg.knmi_dayvalues_notification

    return foot_htm, foot_txt, foot_csv

def body_columns(options, np_days1, np_days2=cfg.e, day=cfg.e, cnt=-1):
    '''Process all the data cells types'''
    col_htm, col_txt, col_csv = cfg.e, cfg.e, cfg.e
    np_days = np_days2 if np_days2 else np_days1
    file_type = options[text.ask_file_type]

    # input(options)

    for cell in options[text.ask_select_cells]: # Check all the available given options
        txt, htm, csv = '', '', '' # Init/reset data vars
        lst_cell_typ = cell.split('_')  # Example: ave_tg. Make a lst of cell id type
        stats = lst_cell_typ[0]  # At least two must be available
 
        if np_days1.size == 0: 
            col_txt += cfg.no_val 
            col_htm += f'<td>{cfg.no_val}</td>' 
            col_csv += cfg.no_val 

            # Skip calculating values, because there are no values
            continue 

        # Info texts
        if stats in text.lst_info:
            txt, htm, csv = col_inf.body(np_days1, np_days2, lst_cell_typ, day, cnt, file_type)

        # Fixed day values
        elif stats in text.lst_day: 
            txt, htm, csv = col_fixed_day.body(np_days, lst_cell_typ, file_type) 

        # Extremes (stats is maximum or minimum) 
        elif stats in text.lst_extremes: 
            txt, htm, csv = col_extreme.body(np_days, lst_cell_typ, file_type) 

        # Average
        elif stats in text.lst_ave: 
            txt, htm, csv = col_mean.body(np_days, lst_cell_typ, file_type) 

        # Sum
        elif stats in text.lst_sum:
            txt, htm, csv = col_sum.body(np_days, lst_cell_typ, file_type) 

        # Indexes
        elif stats in text.lst_ndx:
            txt, htm, csv = col_ndx.body(np_days, lst_cell_typ, file_type) 

        # Counters (conditional)
        elif stats in text.lst_count:
            txt, htm, csv = condit_cnt.body(np_days, lst_cell_typ, file_type) # Make/calculate cells

        # Climate calculations
        elif stats in text.lst_clima:  
            txt, htm, csv = col_clima.body(np_days, lst_cell_typ, file_type) # Make/calculate cells

        # Cell type option not found?
        else:
            cnsl.log(f"Entity type option {cell} not found", cfg.verbose) 
            txt += text.padding(cfg.no_val, 'center', text.pad_default)[:text.pad_default] 
            htm += f'<td>{html.span(cfg.no_val,"val")}</td>' 
            csv += f'{cfg.no_val}{cfg.csv_sep}' 

        # Add (calculated) results to cells
        col_txt = col_txt + txt 
        col_htm = col_htm + htm 
        col_csv = col_csv + csv 

    return col_htm, col_txt, col_csv 

def body_row(options, days1, days2=cfg.e, day=cfg.e, cnt=-1):
    '''Put all the data columns in one body row'''
    # Init empthy vars
    body_htm, body_txt, body_csv = cfg.e, cfg.e, cfg.e

    # Get the column cells with data  
    htm, txt, csv = body_columns(options, days1, days2, day, cnt=cnt)      
    if htm: 
        body_htm += '<tr>'  # Open htm row
        body_htm += htm     # Add columns to row
        body_htm += '</tr>' # Close htm row
    if txt or csv:
        body_txt += cfg.e   # Open txt row
        body_txt += txt     # Add columns to row
        body_txt += '\n'    # Close txt row
    if csv:
        body_csv += cfg.e   # Open txt row
        body_csv += csv     # Add columns to row
        body_csv += '\n'    # Close txt row
    
    return body_htm, body_txt, body_csv

def body_rows_columns(options):
    '''Makes all the body rows'''
    body_htm, body_txt, body_csv, cnt = cfg.e, cfg.e, cfg.e, 0

    # Walkthrough stations and calculate statistics and add to table
    for station in options[text.ask_lst_stations]:
        info_line('Start', options, station)

        # Read data station
        ok, np_lst_days = dayval_read.weatherstation(station, verbose=False)  
        if not ok: 
            err  = f'Error in table body_row_columns()\ndata.read()\n'
            err += f'Options {options}\nStation {station}\n{np_lst_days}'
            cnsl.log(err, cfg.error)
            continue 

        # Get the days for a given period
        period_1 = options[text.ask_period_1]
        ok, np_lst_period_1 = broker.process( np_lst_days, period_1 )

        if not ok:
            err  = f'Error in table body_row_columns()\ndata.read()\n'
            err += f'Options {options}\nPeriod 1 {period_1}\n{np_lst_period_1}'
            cnsl.log(err, cfg.error)
            continue 

        # Get start and end date for period 1, make string 
        col_ymd = data.column('yyyymmdd') # Column date
        symd_1 = str(int(np_lst_period_1[0,col_ymd])) # Start date period 1
        eymd_1 = str(int(np_lst_period_1[-1,col_ymd])) # End date period 1

        # Get the days for the second period 2 (if given)
        period_2 = options[text.ask_period_2]
        np_lst_period_2 = np.array([])
        if period_2:
            ok, np_lst_period_2 = broker.process( np_lst_days, period_2 )
            if not ok:
                err  = f'Error in table body_row_columns()\ndata.read()\n'
                err += f'Options {options}\Period 2 {period_2}\n{np_lst_period_2}'
                cnsl.log(err, cfg.error)
                continue

            symd_2 = str(int(np_lst_period_2[0,col_ymd])) # Start date period 2
            eymd_2 = str(int(np_lst_period_2[-1,col_ymd])) # End date period 2
    
        # Compare periods TODO
        if options[text.ask_per_compare]: # More periods to calculate
            typ, val = options[text.ask_per_compare][0], options[text.ask_per_compare][1]
            lst_yyyy = [ str(yymmdd)[:4] for yymmdd in range( int(symd_1), int(eymd_1), 10000 ) ]
            
            # Add period-2 to list cell to show in table, if not there yet
            if utils.key_from_lst(options[text.ask_select_cells], 'inf_period-2') == -1:
                lst = options[text.ask_select_cells]
                key = utils.key_from_lst( options[text.ask_select_cells], 'inf_period-1' ) # Get key value
                key = 0 if key == -1 else key + 1 # input(key)
                lst_2 = lst[:key] # Add period-2 to lst to show in table
                lst_2.append('inf_period-2')
                options[text.ask_select_cells] = lst_2 + lst[key:] 

                # Now remove period 1 from lst
                if 'inf_period-1' in options[text.ask_select_cells]:
                    options[text.ask_select_cells].remove('inf_period-1')

            for yyyy in lst_yyyy[::-1]: # Reverse lst
                if   typ in text.lst_year:
                    options[text.ask_period_2] = f'{yyyy}****'
                elif typ in text.lst_month:
                    options[text.ask_period_2] = f'{yyyy}{val}**'
                elif typ in text.lst_day:
                    options[text.ask_period_2] = f'{yyyy}{val}'
                elif typ in text.lst_season:
                    if   val == 'winter': 
                        options[text.ask_period_2] = f'{int(yyyy)-1}1201-{yyyy}{"0229" if ymd.is_leap(yyyy) else "0228"}'
                    elif val == 'spring': 
                        options[text.ask_period_2] = f'{yyyy}0301-{yyyy}0531'
                    elif val == 'summer': 
                        options[text.ask_period_2] = f'{yyyy}0601-{yyyy}0831'
                    elif val == 'autumn': 
                        options[text.ask_period_2] = f'{yyyy}0901-{yyyy}1130'
                elif typ in text.lst_period_1:
                    mmdd1, mmdd2 = val.split('-')
                    if int(mmdd1) <= int(mmdd2): 
                        options[text.ask_period_2] = f'{yyyy}{mmdd1}-{yyyy}{mmdd2}'
                    else: 
                        options[text.ask_period_2] = f'{int(yyyy)-1}{mmdd1}-{yyyy}{mmdd2}'

                info_line('Calculate', options, station)

                if period_2: # no data
                    continue # Skip whole day/row

                cnt += 1  # Count the days
                htm, txt, csv = body_row( options, np_lst_period_1, np_lst_period_2, day=cfg.e, cnt=cnt ) # Get the cells with data
                body_htm, body_txt, body_csv = body_htm + htm, body_txt + txt, body_csv + csv # Add to body

            info_line('End', options, station)
            continue

        # TODO Search for days table
        if options[text.ask_s4d_query]: # Update days
            ok, np_lst_res = s4d_query.calculate(np_lst_days, options[text.ask_s4d_query]) 
            if not ok:
                continue
            else:
                for day in np_lst_res:
                    cnt += 1  # Count the days
                    htm, txt, csv = body_row(options, np_lst_res, np_lst_res, day=day, cnt=cnt) # Get the cells with data
                    body_htm, body_txt, body_csv = body_htm + htm, body_txt + txt, body_csv + csv # Add to body

            info_line('End', options, station)
            continue

        # TODO Period-1 in period-2 
        if options[text.ask_period_2]:  # Get days2 for calculation of statistic
            
            # Add period-2 to list cell to show in table, if not there yet
            if utils.key_from_lst(options[text.ask_select_cells], 'inf_period-2') == -1:
                lst = options[text.ask_select_cells]
                key = utils.key_from_lst( options[text.ask_select_cells], 'inf_period-1' ) # Get key value
                key = 0 if key == -1 else key + 1 # input(key)
                lst_2 = lst[:key] # Add period-2 to lst to show in table
                lst_2.append('inf_period-2')
                options[text.ask_select_cells] = lst_2 + lst[key:] 

        # Statistics table
        cnt += 1  # Count the days
        htm, txt, csv = body_row(options, np_lst_period_1, np_lst_period_2, day=cfg.e, cnt=cnt) # Get the tr cells with data
        body_htm, body_txt, body_csv = body_htm + htm, body_txt + txt, body_csv + csv # Add to body

        info_line('End', options, station)

    return body_htm, body_txt, body_csv, options, cnt

def info_line(txt, options, station):
    t  = f'[{ymd.now()}] {txt} <{options[text.ask_title]}> '
    t += f'for {station.wmo} {station.place} '
    t += f'in period <{options[text.ask_period_1]}> '
    t += f'with sub-period <{options[text.ask_period_2]}>' if options[text.ask_period_2] else cfg.e
    cnsl.log(t, True)

def subject_map( title, map ):
    # TODO
    pass

def js_script_fn( option, sort_type, sort_dir, row_num, col_num ):
    '''Function makes an JavaScript object to handle a function call for sorting the table column'''
    # Option    : type coll TX, province, ... 
    # Sort_type : 'num' or 'txt' (numeric of alfa)
    # Sort_dir  : '+' (descending: large to small), '-' (ascending: small to high)
    # Row_num   : 2 (num of row in table)
    # Col_num   : 1..end (colum num in table)

    # Sort object 
    return f'\n{option}' + ': { ' + f''' 
        name: '{option}',
        doc: document.querySelector('table#stats>thead>tr:nth-child({row_num})>th:nth-child({col_num})'),
        type: '{sort_type}', dir: '{sort_dir}', row: {row_num}, col: {col_num-1}
    ''' + ' },'

def mk_output(htm, txt, csv, options):
    '''Make output to screen or file(s)'''
    ok, path_to_file, ftyp = True, cfg.e, options[text.ask_file_type] 
    # input(ftyp)

    if ftyp in text.lst_output_cnsl or cfg.console:  # For console
        cnsl.log(f'\n{txt}', True)  # Add 1 spacer/enter around console output

    if ftyp in text.lst_output_files:
        fname = options[text.ask_filename] + text.file_extension(ftyp)  # File name
        data, map = '.', cfg.dir_data # Data and dir
        if   ftyp in text.lst_output_txt:   data, map = txt, cfg.dir_stats_txt
        elif ftyp in text.lst_output_htm:   data, map = htm, cfg.dir_stats_htm
        elif ftyp in text.lst_output_csv:   data, map = csv, cfg.dir_stats_csv
        elif ftyp in text.lst_output_excel: data, map = csv, cfg.dir_stats_excel

        path_to_file, map, _ = fio.mk_path_with_dates(map, fname) # Update dir with date maps
        fio.mk_dir( map, verbose=False ) # Make dir if not there yet 

        if ftyp in text.lst_output_htm: # Create html file
            page = html.Template()
            page.template = cfg.html_template_statistics
            page.verbose = False
            page.path_to_file = path_to_file
            page.path_to_root = cfg.path_to_html_root
            page.path_to_thirdparty = cfg.path_to_thirdparty
            page.title = options[text.ask_title]
            page.add_description(f'{options[text.ask_title]} {", ".join(options[text.ask_select_cells])}')
            page.main = data
            ok = page.save()  # Save page
            if not ok: 
                cnsl.log( f'Save {ftyp} file failed!', cfg.error )

        elif ftyp in text.lst_output_txt + text.lst_output_csv: # text, csv
            ok = fio.save( path_to_file, data, verbose=True )  # Schrijf naar bestand

        elif ftyp in text.lst_output_excel: # Convert csv to excel 
            csv_data = pd.read_table(data, sep=cfg.csv_sep ) # Read the csv data with panda
            csv_data.to_excel(path_to_file, index = None, header=True) # Write excel file

    return ok, path_to_file
