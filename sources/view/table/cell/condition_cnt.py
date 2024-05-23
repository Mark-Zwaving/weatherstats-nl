# -*- coding: utf-8 -*-
'''Library contains function for the calculation of the counter cells'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.0.5'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg 
import numpy as np
import sources.view.text as text 
import sources.view.html as html 
import sources.view.table.popup as popup
import sources.model.statistic.conditional as conditional
'''
CELL ID
cnt_?ENTITY?_?SIGN?_?VALUE?
'''
def header(lst_cell, file_type): 
    '''Make the title header for a given file type option'''
    txt, htm, csv = '', '', ''
    cnt, entity, operand, value = lst_cell
    title = f'Σ{entity}{operand}{value}'

    # Head text
    txt = text.padding(title, 'center', text.pad_cnt)[:text.pad_cnt]

    # Head html
    if file_type in text.lst_output_htm: 
        htm = f'<th title="{text.title(entity,operand,value)}">{title}</th>'
        
    # Head csv
    elif file_type in text.lst_output_csv_excel:
        csv = f'{title}{cfg.csv_sep}'

    return txt, htm, csv


def body(np_lst_days, lst_cell, file_type):
    '''Make or calculate the value for a given file type option'''
    # Init empthy vars. Start count at 0
    cnt_val, txt, htm, csv = cfg.no_val, '', '', ''

    # Get values
    cnt, entity, sign, value = lst_cell

    # Get days based on a condition. For example: tx >= 25
    ok, np_lst_condit, _ = conditional.calculate(np_lst_days, entity, sign, value )

    if ok: 
        # Count all the days 
        cnt_val = len(np_lst_condit)

    # Text output
    txt = text.padding(cnt_val, 'center', text.pad_cnt)[:text.pad_cnt] 

    # HTML output
    if file_type in text.lst_output_htm:
        value  = html.span(cnt_val, 'val')
        pop_up = popup.table_count(np_lst_condit, entity)
        htm = f'<td>{value}{pop_up}</td>'

    # CSV output
    if file_type in text.lst_output_csv_excel:
        csv = f'{cnt_val}{cfg.csv_sep}'

    return txt, htm, csv 
