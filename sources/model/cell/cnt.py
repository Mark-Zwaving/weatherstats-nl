# -*- coding: utf-8 -*-
'''Library contains function for the calculation of the counter cells'''
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

'''
CELL ID
cnt_?ENTITY?_?SIGN?_?VALUE?
'''

def head(lst_cell, file_type): 
    '''Make the title header for a given file type option'''
    txt, htm, csv = '', '', ''
    entity, sign, value = lst_cell[1], lst_cell[2], lst_cell[3]

    # Head text
    txt = text.padding(f'{entity} {sign} {value}', 'center', text.pad_cnt)[:text.pad_cnt]

    # Head html
    if file_type in text.lst_output_htm: 
        ico = html.entity_to_icon(sign, size="fa-xs") # Update icon
        htm = f'<th title="{text.title(entity,sign,value)}">{entity}{ico}{value}</th>'
        
    # Head csv
    elif file_type in text.lst_output_csv_excel:
        csv = f'{entity}{sign}{value}{cfg.csv_sep}'

    return txt, htm, csv


def calc(days, lst_cell, file_type):
    '''Make or calculate the value for a given file type option'''
    # Init empthy vars. Start count at 0
    cnt, txt, htm, csv = 0, '', '', ''
    # title = lst_cell[0] 
    entity, sign, value = lst_cell[1], lst_cell[2], lst_cell[3]  # Get values

    # Get days based on a condition. For example: tx >= 25
    np_terms_2d, days_cnt_2d = days.conditional_2d( entity, sign, value )

    if np_terms_2d == cfg.np_empthy_2d: # No data available (better not)
        txt = text.padding(cfg.no_val, 'center', text.pad_cnt)[:text.pad_cnt]

        if file_type in text.lst_output_htm:
            htm = f'<td>{html.span(cfg.no_val, "val")}</td>'

        if file_type in text.lst_output_csv_excel:
            csv = f'{cfg.no_val}{cfg.csv_sep}'

    else:
        cnt = text.fix_ent( np.size(np_terms_2d, axis=0 ), 'cnt' ) # Count the days!
        txt = text.padding(cnt, 'center', text.pad_cnt)[:text.pad_cnt] # Always make a text output

        if file_type in text.lst_output_htm:
            value = html.span(cnt, 'val')
            table = html.table_count(days_cnt_2d, entity)
            htm = f'<td>{value}{table}</td>'

        if file_type in text.lst_output_csv_excel:
            csv = f'{cnt}{cfg.csv_sep}'

    return txt, htm, csv 