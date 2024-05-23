# -*- coding: utf-8 -*-
'''Library contain functions to make the table rows'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.0.5'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import sources.view.console as cnsl
import sources.model.dayvalues.np_days as np_days
import sources.view.text as text
import sources.view.html as html
import sources.view.table.cell.condition_cnt as condit_cnt
import sources.view.table.cell.indexes as col_ndx
import sources.view.table.cell.sum as col_sum
import sources.view.table.cell.mean as col_mean
import sources.view.table.cell.inf as col_inf
import sources.view.table.cell.extreme as col_extreme
import sources.view.table.cell.clima as col_clima
import sources.view.table.cell.fixed_day as col_fixed_day
import numpy as np

def no_data_row_htm(station, options, period):
    '''Functions prints a correct row if there is no data available'''
    # Init variables
    wmo = station.wmo
    place = station.place
    province = station.province
    country = station.country
    period1 = options[text.ask_period_1]
    period2 = options[text.ask_period_2]
    css = 'class="font-italic text-left"'
    t = f"No data station for {wmo} {place} in period {period}" 

    # Open htm row
    htm = '<tr>' 

    # Make the header cells for no data
    for opt in options[text.ask_select_cells]:
        opt = opt.lower()

        # Put in the info titles anyway
        if opt == 'inf_wmo':
            htm += f'<td {css} title="{t}">{html.span(wmo,"val")}</td>'
        elif opt == 'inf_copyright':
            htm += f'<td {css} title="{t}">{html.span(place,"val")}</td>'
        elif opt == 'inf_place':
            htm += f'<td {css}>{html.span(place,"val")}</td>'
        elif opt == 'inf_province':
            htm += f'<td {css}>{html.span(province,"val")}</td>'
        elif opt == 'inf_country':
            htm += f'<td {css}>{html.span(country,"val")}</td>'
        elif opt in ['inf_period', 'inf_period-1']:
            htm += f'<td>{html.span(period1,"val")}</td>'
        elif opt == 'inf_period-2':
            htm += f'<td>{html.span(period2,"val")}</td>'

        # No values available
        else: 
            htm += f'<td title="{t}">{html.span(cfg.no_val,"val")}</td>' 

    # Close htm row
    htm += '</tr>' 

    return htm

def columns(station, options, np_period1, np_period2, day=cfg.e, cnt=-1):
    '''Process all the data cells types'''
    col_htm, col_txt, col_csv = cfg.e, cfg.e, cfg.e
    file_type = options[text.ask_file_type]

    for cell in options[text.ask_select_cells]: # Check all the available given options
        txt, htm, csv = '', '', '' # Init/reset data vars
        lst_cell_id = cell.split('_')  # Example: ave_tg. Make a lst of cell id type

        # At least two id's must be available
        # E.g: max_tx (=minimum)
        if len(lst_cell_id) < 2:
            continue

        # Get first id of cell
        # E.g: ave from ave_tg
        opt = lst_cell_id[0]  

        # # Check for data
        if np.size(np_period1) == 0: 
            t = f"No data station {station.wmo} {station.place} available for {cell}" 
            col_txt += cfg.no_val 
            col_htm += f'<td title="{t}">{html.span(cfg.no_val,"val")}</td>' 
            col_csv += cfg.no_val 
            # Skip calculating values, 
            # because there are no values
            continue 

        # If a second period is available and not empthy 
        # The second period must be the period for the calculations.
        # Update the period with the second period
        if options[text.ask_period_2] != cfg.e:
            if opt not in text.lst_info: # Not for info texts
                np_period1 = np_period2 # Update period for the calculations

        # Info texts
        if opt in text.lst_info: 
            txt, htm, csv = col_inf.body(options, np_period1, np_period2, 
                                         lst_cell_id, day, cnt, file_type) 

        # Fixed day values
        elif opt in text.lst_day: 
            txt, htm, csv = col_fixed_day.body(np_period1, lst_cell_id, file_type) 

        # Extremes (opt is maximum or minimum) 
        elif opt in text.lst_extremes: 
            txt, htm, csv = col_extreme.body(np_period1, lst_cell_id, file_type) 

        # Average
        elif opt in text.lst_ave: 
            txt, htm, csv = col_mean.body(np_period1, lst_cell_id, file_type) 

        # Sum
        elif opt in text.lst_sum:
            txt, htm, csv = col_sum.body(np_period1, lst_cell_id, file_type) 

        # Indexes
        elif opt in text.lst_ndx:
            txt, htm, csv = col_ndx.body(np_period1, lst_cell_id, file_type) 

        # Counters (conditional)
        elif opt in text.lst_count:
            txt, htm, csv = condit_cnt.body(np_period1, lst_cell_id, file_type)

        # Climate calculations
        elif opt in text.lst_clima:  
            txt, htm, csv = col_clima.body(np_period1, lst_cell_id, file_type) 

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

def row(station, options, period1, period2, day=cfg.e, cnt=-1):
    '''Put all the data columns in one body row'''
    # Init empthy vars
    body_htm, body_txt, body_csv = cfg.e, cfg.e, cfg.e

    # Get the column cells with data  
    htm, txt, csv = columns(station, options, period1, period2, day, cnt=cnt)      
    if htm: 
        body_htm += '<tr>'  # Open htm row
        body_htm += htm     # Add columns to row
        body_htm += '</tr>' # Close htm row
    if txt or csv:
        body_txt += cfg.e   # Open txt row
        body_txt += txt     # Add columns to row
        body_txt += cfg.ln  # Close txt row
    if csv:
        body_csv += cfg.e   # Open txt row
        body_csv += csv     # Add columns to row
        body_csv += cfg.ln  # Close txt row
    
    return body_htm, body_txt, body_csv
