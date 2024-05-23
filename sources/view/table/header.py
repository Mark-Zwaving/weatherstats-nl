# -*- coding: utf-8 -*-
'''Library contain functions to make the header for a 2d matrix table.'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.0.5'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import sources.view.text as text
import sources.view.icon as icon
import sources.view.table.cell.condition_cnt as condit_cnt
import sources.view.table.cell.indexes as col_ndx
import sources.view.table.cell.sum as col_sum
import sources.view.table.cell.mean as col_mean
import sources.view.table.cell.inf as col_inf
import sources.view.table.cell.extreme as col_extreme
import sources.view.table.cell.clima as col_clima
import sources.view.table.cell.fixed_day as col_fixed_day

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

def row(options):
    '''Makes the header'''
    # Init vars
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

    # File type
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

        if len(lst_col) < 2: # This cannot, wrong cell id
            continue

        # Get base values for cell
        opt, entity = lst_col[0], lst_col[1]

        # Info texts
        if opt in text.lst_info:
            txt, htm, csv = col_inf.header(lst_col, file_type)

            # Update sort type for geo places
            if entity in text.lst_geo_places:
                sort_type = sort_txt  # Text sort

        # Fixed day values
        elif opt in text.lst_day:
            txt, htm, csv = col_fixed_day.header(lst_col, file_type)

        # Max extreme
        elif opt in text.lst_extremes:
            txt, htm, csv = col_extreme.header(lst_col, file_type)

        # Average
        elif opt in text.lst_ave:
            txt, htm, csv = col_mean.header(lst_col, file_type)

        # Sum
        elif opt in text.lst_sum:
            txt, htm, csv = col_sum.header(lst_col, file_type)

        # Indexes
        elif opt in text.lst_ndx:
            txt, htm, csv = col_ndx.header(lst_col, file_type)

        # Counters
        elif opt in text.lst_count:
            txt, htm, csv = condit_cnt.header(lst_col, file_type)

        # Climate
        elif opt in text.lst_clima:
            txt, htm, csv = col_clima.header(lst_col, file_type)

        # Add Sort Script
        if file_type in text.lst_output_htm:
            col_id = text.strip_all_whitespace(
                f'{entity}_col_{col_num}'.replace('-','_')
            ).upper()
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
