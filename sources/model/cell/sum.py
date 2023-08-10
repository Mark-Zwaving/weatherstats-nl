# -*- coding: utf-8 -*-
'''
Library contains functions for the calculation of the sum cells

CELL ID
sum_?ENTITY?
'''

__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 3 - GPLv3'
__version__    =  '0.0.1'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg 
import numpy as np
import sources.view.text as text 
import sources.view.html as html 


def head(lst, file_type):
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


def calc(days, lst_cell, file_type):
    txt, htm, csv = '', '', ''
    entity = lst_cell[1]

    # Calculate sum
    sum_raw, days_sum_2d = days.sum(entity)
    sum_val = text.fix_ent(sum_raw, entity)

    txt = text.padding(sum_val, 'center', text.pad_sum)[:text.pad_sum]
    if file_type in text.lst_output_htm:
        value = html.span(sum_val, 'val')
        table = html.table_sum(days_sum_2d, entity)
        htm = f'<td>{value}{table}</td>'
    
    elif file_type in text.lst_output_csv_excel:
        csv = f'{sum_val}{cfg.csv_sep}'

    return txt, htm, csv