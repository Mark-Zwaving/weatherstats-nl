# -*- coding: utf-8 -*-
'''Library contains classes and functions for calculating statistics'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 3 - GPLv3'
__version__    =  '0.1.2'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

from importlib.resources import path
from pkgutil import read_code
import pandas as pd
import sources.view.text as text
import sources.view.icon as icon
import sources.view.html as html
import sources.view.console as cnsl
import sources.model.stats as stats
import sources.model.daydata as daydata
import sources.model.utils as utils
import sources.model.validate as valid
import sources.model.ymd as ymd
import sources.model.convert as convert
import sources.model.cell.cnt as cell_cnt
import sources.model.cell.ndx as cell_ndx
import sources.model.cell.sum as cell_sum
import sources.model.cell.mean as cell_mean
import sources.model.cell.inf as cell_inf
import sources.model.cell.extreme as cell_extreme
import sources.model.cell.clima as cell_clima
import sources.control.fio as fio
import config as cfg

def calculate(options, type='normal'):
    '''Function calculates all statistics'''
    cnsl.log(f'[{ymd.now()}] {options[text.ask_title].upper()}', True)

    body_htm, body_txt, body_csv, options, cnt = body(options)
    options[text.ask_colspan] = len(options[text.ask_select_cells])

    head_htm, head_txt, head_csv, script = head(options)
    foot_htm, foot_txt, foot_csv = foot(options)

    htm = f'{head_htm}{body_htm}{foot_htm}{script}' # HTML data
    txt = f'{head_txt}\n{body_txt}{foot_txt}' # Text data

    # Remove separator at the end if there
    if len( head_csv) > 0: 
        if head_csv[-1] == cfg.csv_sep: 
            head_csv = head_csv[:-1]
    if len(body_csv) > 0: 
        if body_csv[-1] == cfg.csv_sep: 
            body_csv = body_csv[:-1]
    if len(foot_csv) > 0: 
        if foot_csv[-1] == cfg.csv_sep: 
            foot_csv = foot_csv[:-1]

    csv = f'{head_csv}\n{body_csv}\n{foot_csv}' # Csv data

    # Output to screen or file(s) 
    ok, path_to_file = output(htm, txt, csv, options)

    return ok, path_to_file

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

def head(options):
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
                {icon.weather_all()} {options[text.ask_title]} 
                {icon.wave_square()} 
                {options[text.ask_period]} 
                {icon.cal_period()}                 
            </th></tr><tr>'''

    if file_type in text.lst_output_txt_cnsl:
        pass # head_txt += '#' * 80 + '\n'

    for option in options[text.ask_select_cells]:
        txt, htm, csv = '', '', '' # Init reset
        # Sort options. 
        # Defaults: sort is True, numeric and descending. Add 1 to col_num
        sort_type, sort_dir, col_num = sort_num, descending, col_num + 1

        # Make list from cell id. Exemple: tx_>=_10 : entity sign value
        lst_cell = option.split(cfg.cells_separator) 

        # Get base values for cell
        typ, entity = lst_cell[0], lst_cell[1]

        # Info texts
        if typ in text.lst_info:
            txt, htm, csv = cell_inf.head(lst_cell, file_type)

            # Update sort type for geo places
            if entity in text.lst_geo_places:
                sort_type = sort_txt  # Text sort

        # Fixed day values
        elif typ in text.lst_day:
            txt = text.padding(entity, 'center', text.pad_day)[:text.pad_day]
            ico = html.entity_to_icon(entity, size='fa-sm', color=cfg.e, extra=cfg.e) # Icon
            if file_type in text.lst_output_htm: 
                htm = f'<th title="{html.attr_title(entity)}">{ico}{entity}</th>'
            elif file_type in text.lst_output_csv_excel:
                csv = f'{entity}{cfg.csv_sep}'

        # Max extreme
        elif typ in text.lst_extremes:
            txt, htm, csv = cell_extreme.head(lst_cell, file_type)

        # Average
        elif typ in text.lst_ave:
            txt, htm, csv = cell_mean.head(lst_cell, file_type)

        # Sum
        elif typ in text.lst_sum:
            txt, htm, csv = cell_sum.head(lst_cell, file_type)

        # Indexes
        elif typ in text.lst_ndx:
            txt, htm, csv = cell_ndx.head(lst_cell, file_type)

        # Counters
        elif typ in text.lst_count:
            txt, htm, csv = cell_cnt.head(lst_cell, file_type)

        # Climate
        elif typ in text.lst_clima:
            txt, htm, csv = cell_clima.head(lst_cell, file_type)

        # Add Sort Script
        if file_type in text.lst_output_htm:
            col_id = text.strip_all_whitespace(f'{entity}_col_{col_num}'.replace('-','_')).upper()
            script += js_script_fn( col_id, sort_type, sort_dir, row_num, col_num )

        # Add to total head output
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

    return head_htm, head_txt.upper(), head_csv, js


def cells(options, days1, days2=cfg.e, day=cfg.e, cnt=-1):
    '''Process all the data cells types'''
    cell_htm, cell_txt, cell_csv = cfg.e, cfg.e, cfg.e
    days = days2 if days2 else days1
    station = days.station
    file_type = options[text.ask_file_type]

    for option in options[text.ask_select_cells]:  # Check all the available given options
        txt, htm, csv = '', '', '' # Init/reset data vars
        lst_cell = option.split('_')  # Make lst of cell id-options
        typ, entity = lst_cell[0], lst_cell[1]  # At least two must be available

        # Info texts
        if typ in text.lst_info:
            txt, htm, csv = cell_inf.calc(days1, days2, lst_cell, day, cnt, file_type)

        # if not days1.np_period_2d_has_days():
        #     cell_txt += cfg.no_val
        #     cell_htm += f'<td>{cfg.no_val}</t>'
        #     continue

        # Fixed day values
        elif typ in text.lst_day:
            val = text.fix_ent(day[daydata.etk(entity)], entity)
            cell_txt += text.padding(val, 'center', text.pad_day)[:text.pad_day]
            if file_type in text.lst_output_htm:
                cell_htm += f'<td>{html.span(val, "val")}</td>'
            elif file_type in text.lst_output_csv_excel:
                cell_csv += f'{val}{cfg.csv_sep}'

        # Extremes (typ is maximum or minimum)
        elif typ in text.lst_extremes:
            txt, htm, csv = cell_extreme.calc(days, lst_cell, file_type)

        # Average
        elif typ in text.lst_ave:
            txt, htm, csv = cell_mean.calc(days, lst_cell, file_type)

        # Sum
        elif typ in text.lst_sum:
            txt, htm, csv = cell_sum.calc(days, lst_cell, file_type)
            
        # Indexes
        elif typ in text.lst_ndx:
            txt, htm, csv = cell_ndx.calc(days, lst_cell, file_type)

        # Counters (conditional)
        elif typ in text.lst_count:
            txt, htm, csv = cell_cnt.calc(days, lst_cell, file_type) # Make/calculate cells

        # Climate calculations
        # TODO / beta
        # calculate month clima values 
        # for the period for every climate year and month
        elif typ in text.lst_clima:  
            txt, htm, csv = cell_clima.calc(days, lst_cell, file_type) # Make/calculate cells

        # Cell type option not found? Must not. 
        else:
            txt += text.padding(cfg.no_val, 'center', text.pad_default)[:text.pad_default]
            htm += f'<td>{html.span(cfg.no_val, "val")}</td>' 
            csv += f'{cfg.no_val}{cfg.csv_sep}'

        # Add (calculated) results to cells
        cell_txt = cell_txt + txt 
        cell_htm = cell_htm + htm 
        cell_csv = cell_csv + csv 

    return cell_htm, cell_txt, cell_csv

def tr_cells(options, days1, days2=cfg.e, day=cfg.e, cnt=-1):
    body_htm, body_txt, body_csv = cfg.e, cfg.e, cfg.e
    htm, txt, csv = cells(options, days1, days2, day, cnt=cnt)     # Get the cells with data        
    if htm: 
        body_htm += '<tr>'  # Open htm row
        body_htm += htm     # Add to body
        body_htm += '</tr>' # Close htm row
    if txt or csv:
        body_txt += cfg.e      # Open txt row
        body_txt += txt     # Add to body
        body_txt += '\n'    # Close txt row
    if csv:
        body_csv += cfg.e      # Open txt row
        body_csv += csv     # Add to body
        body_csv += '\n'    # Close txt row
    
    return body_htm, body_txt, body_csv

def info_line(txt, options, station):
    t  = f'[{ymd.now()}] {txt} <{options[text.ask_title]}> '
    t += f'for {station.wmo} {station.place} '
    t += f'in period <{options[text.ask_per1]}> '
    t += f'with sub-period <{options[text.ask_per2]}>' if options[text.ask_per2] else cfg.e
    cnsl.log(t, True)

def subject_map( title, map ):
    # TODO
    pass

def body(options):
    '''Makes the body'''
    body_htm, body_txt, body_csv, cnt = cfg.e, cfg.e, cfg.e, 0

    # Walkthrough stations and calculate statistics and add to table
    for station in options[text.ask_stations]:
        info_line('Start', options, station)

        ok, np_data_2d = daydata.read(station, verbose=False)  # Read data stations
        if not ok: 
            continue 

        # Get days from a station for the given period
        days1, days2 = stats.Days( station, np_data_2d, options[text.ask_period] ), cfg.e
    
        # Compare periods
        if options[text.ask_per_compare]: # More periods to calculate
            typ, val = options[text.ask_per_compare][0], options[text.ask_per_compare][1]
            lst_yyyy = [ str(yymmdd)[:4] for yymmdd in range( int(days1.ymd_start), int(days1.ymd_end), 10000 ) ]
            
            # Add period-2 to list cell to show in table, if not there yet
            if utils.key_from_lst(options[text.ask_select_cells], 'inf_period-2') == -1:
                lst = options[text.ask_select_cells]
                key = utils.key_from_lst( options[text.ask_select_cells], 'inf_period' ) # Get key value
                key = 0 if key == -1 else key + 1 # input(key)
                lst_2 = lst[:key] # Add period-2 to lst to show in table
                lst_2.append('inf_period-2')
                options[text.ask_select_cells] = lst_2 + lst[key:] 
                # Now remove period 1 from lst
                if 'inf_period' in options[text.ask_select_cells]:
                    options[text.ask_select_cells].remove('inf_period')

            for yyyy in lst_yyyy[::-1]: # Reverse lst
                if   typ in text.lst_year:  options[text.ask_per2] = f'{yyyy}****'
                elif typ in text.lst_month: options[text.ask_per2] = f'{yyyy}{val}**'
                elif typ in text.lst_day:   options[text.ask_per2] = f'{yyyy}{val}'
                elif typ in text.lst_season:
                    if   val == 'winter': options[text.ask_per2] = f'{int(yyyy)-1}1201-{yyyy}{"0229" if valid.is_leap(yyyy) else "0228"}'
                    elif val == 'spring': options[text.ask_per2] = f'{yyyy}0301-{yyyy}0531'
                    elif val == 'summer': options[text.ask_per2] = f'{yyyy}0601-{yyyy}0831'
                    elif val == 'autumn': options[text.ask_per2] = f'{yyyy}0901-{yyyy}1130'
                elif typ in text.lst_period_1:
                    mmdd1, mmdd2 = val.split('-')
                    if int(mmdd1) <= int(mmdd2): options[text.ask_per2] = f'{yyyy}{mmdd1}-{yyyy}{mmdd2}'
                    else: options[text.ask_per2] = f'{int(yyyy)-1}{mmdd1}-{yyyy}{mmdd2}'

                info_line('Calculate', options, station)
                days2 = stats.Days(station, days1.np_period_2d, options[text.ask_per2])
                if not days2.np_period_2d_has_days(): 
                    continue # Skip whole day/row

                cnt += 1  # Count the days
                htm, txt, csv = tr_cells( options, days1, days2, day=cfg.e, cnt=cnt ) # Get the cells with data
                body_htm, body_txt, body_csv = body_htm + htm, body_txt + txt, body_csv + csv # Add to body

            info_line('End', options, station)
            continue

        # Search for days table
        if options[text.ask_s4d_query]:  # Update days
            days = days2 if days2 else days1
            np_2d_search, _ = days.query(options[text.ask_s4d_query])
            if not days.np_period_2d_has_days():
                continue  # Skip whole day/row
            else:
                for day in np_2d_search:
                    cnt += 1  # Count the days
                    htm, txt, csv = tr_cells(options, days1, days2, day=day, cnt=cnt) # Get the cells with data
                    body_htm, body_txt, body_csv = body_htm + htm, body_txt + txt, body_csv + csv # Add to body
            info_line('End', options, station)
            continue

        # Period in period
        if options[text.ask_per2]:  # Get days2 for calculation of statistics
            days2 = stats.Days(station, days1.np_period_2d, options[text.ask_per2])
            
            # Add period-2 to list cell to show in table, if not there yet
            if utils.key_from_lst(options[text.ask_select_cells], 'inf_period-2') == -1:
                lst = options[text.ask_select_cells]
                key = utils.key_from_lst( options[text.ask_select_cells], 'inf_period' ) # Get key value
                key = 0 if key == -1 else key + 1 # input(key)
                lst_2 = lst[:key] # Add period-2 to lst to show in table
                lst_2.append('inf_period-2')
                options[text.ask_select_cells] = lst_2 + lst[key:] 

        # Statistics table
        cnt += 1  # Count the days
        htm, txt, csv = tr_cells(options, days1, days2, day=cfg.e, cnt=cnt) # Get the tr cells with data
        body_htm, body_txt, body_csv = body_htm + htm, body_txt + txt, body_csv + csv # Add to body
        info_line('End', options, station)

    return body_htm, body_txt, body_csv, options, cnt

def foot(options):
    '''Makes the footer'''
    foot_htm, foot_txt, foot_csv, ftyp = cfg.e, cfg.e, cfg.e, options[text.ask_file_type]

    if ftyp in text.lst_output_htm:
        foot_htm += f'''
        </tbody><tfoot>
        <tr><td class="text-muted" colspan="{options[text.ask_colspan]}">
            {text.now_created_notification()}
            {cfg.knmi_dayvalues_notification.lower()}
        </td></tr>
        </tfoot></table>'''

    if ftyp in text.lst_output_txt_cnsl:
        foot_txt += cfg.knmi_dayvalues_notification

    return foot_htm, foot_txt, foot_csv

def output(htm, txt, csv, options):
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

        path_to_file, map, _ = utils.mk_path_with_dates(map, fname) # Update dir with date maps
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
