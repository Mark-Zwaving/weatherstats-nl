# -*- coding: utf-8 -*-
'''
Library contains functions for the calculation of the max and min extremes cells

CELL ID
sum_?ENTITY?
'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.0.4'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg 
import sources.model.dayvalues.data as data 
import sources.model.dayvalues.np_days as np_days 
import sources.model.statistic.maximum as maximum
import sources.model.statistic.minimum as minimum
import sources.view.text as text 
import sources.view.html as html 
import sources.view.table.popup as popup

def header( lst, file_type):
    txt, htm, csv = '', '', ''
    title  = lst[0] # min or max
    entity = lst[1] # TX, RH

    # Make head txt
    txt = text.padding(f'{title} {entity}', 'center', text.pad_extreme)[:text.pad_extreme] 

    # Make head htm
    if file_type in text.lst_output_htm:
        ico1 = html.entity_to_icon(entity, size='fa-sm', color=cfg.e, extra=cfg.e) # Icon1
        ico2 = html.entity_to_icon(title,  size='fa-sm', color=cfg.e, extra=cfg.e) # Icon2
        htm = f'<th title="{html.attr_title(entity)}">{ico1}{entity}{ico2}</th>'

    # Make head csv 
    elif file_type in text.lst_output_csv_excel:
        csv = f'{title} {entity}{cfg.csv_sep}'

    return txt, htm, csv 


def body(np_lst_days, lst_cell, file_type):
    txt, htm, csv = '', '', ''
    extreme = lst_cell[0] # Min or max
    entity = lst_cell[1] # 
    value = cfg.no_val 
    type_sort = 'H-L'
    pop_up = '' 

     # Get only valid values, remove NAN values from np lst
    ok, np_lst_valid = np_days.rm_nan(np_lst_days, entity)

    if ok:
        # Max extreme
        if extreme in text.lst_max:
            type_sort = 'H-L'
            # Get maximum extreme
            raw, np_day, _ = maximum.calculate(np_lst_valid, entity) 
        
        # Min extreme
        elif extreme in text.lst_min:
            type_sort = 'L-H'
            # Get maximum extreme
            raw, np_day, _ = minimum.calculate(np_lst_valid, entity) 

        # print(np_day)
        # print(np_day[0,:])

        if np_day.size != 0:
            col_ymd = data.column("yyyymmdd")
            xtr_val = text.fix_for_entity(raw, entity)
            xtr_ymd = str(int(np_day[0,col_ymd]))
            value   = f'{xtr_val} {xtr_ymd}'

    # Output
    # Always make a text output
    txt = text.padding(value, 'center', text.pad_extreme)[:text.pad_extreme]

    if file_type in text.lst_output_csv_excel:
        csv = f'{value}{cfg.csv_sep}'

    elif file_type in text.lst_output_htm:
        if ok:
            value = html.extreme_values(np_day, entity) # Update value
            pop_up = popup.table_extremes(np_lst_valid, entity, type_sort)

        htm = f'<td>{value}{pop_up}</td>'

    return txt, htm, csv 
