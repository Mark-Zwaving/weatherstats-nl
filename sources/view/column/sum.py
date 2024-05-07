# -*- coding: utf-8 -*-
'''
Library contains functions for the calculation of the sum cells

CELL ID
sum_?ENTITY?
'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.0.3'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg 
import sources.view.text as text 
import sources.view.html as html 
import sources.view.popup as popup
import sources.model.dayvalues.np_days as np_days
import sources.model.statistic.sum as sum

def header(lst, file_type):
    txt, htm, csv = '', '', ''
    # title  = lst[0]  # sum
    entity = lst[1]
    ico = 'Σ'  # Sigma

    # Text head title
    txt = text.padding(f'{ico}{entity}', 'center', text.pad_sum)[:text.pad_sum]

    # HTML head title
    if file_type in text.lst_output_htm: 
        htm = f'<th title="{html.attr_title(entity)}">{ico}{entity}</th>'

    # CSV head title
    elif file_type in text.lst_output_csv_excel:
        csv = f'{ico}{entity}{cfg.csv_sep}'

    return txt, htm, csv 

def body(np_lst_days, lst_cell, file_type):
    txt, htm, csv = '', '', ''
    entity = lst_cell[1]

    # Get only valid values, remove NAN values from np lst
    ok, np_lst_valid = np_days.rm_nan(np_lst_days, entity)

    # Calculate sum
    sum_raw, _ = sum.calculate(np_lst_valid, entity)
    sum_val = text.fix_for_entity(sum_raw, entity)

    txt = text.padding(sum_val, 'center', text.pad_sum)[:text.pad_sum]
    if file_type in text.lst_output_htm:
        value = html.span(sum_val, 'val')
        pop_up = popup.table_sum(np_lst_valid, entity)
        htm = f'<td>{value} {pop_up}</td>'
    
    elif file_type in text.lst_output_csv_excel:
        csv = f'{sum_val}{cfg.csv_sep}'

    return txt, htm, csv