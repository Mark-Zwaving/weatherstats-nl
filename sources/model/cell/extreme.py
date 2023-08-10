# -*- coding: utf-8 -*-
'''
Library contains functions for the calculation of the max and min extremes cells

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
import sources.model.daydata as daydata 
import sources.model.convert as convert 
import sources.view.text as text 
import sources.view.html as html 


def head( lst, file_type):
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


def calc(days, lst_cell, file_type):
    txt, htm, csv = '', '', ''
    title  = lst_cell[0] # Min or max
    entity = lst_cell[1] # 
    value = cfg.no_val  

    # Max extreme
    if title in text.lst_max:
        raw, day, days_extr_2d = days.max(entity) # Get maximum extreme
    
    # Min extreme
    elif title in text.lst_min:
        raw, day, days_extr_2d = days.min(entity) # Get maximum extreme

    if day != cfg.np_empthy_2d:
        value = f'{text.fix_ent(raw, entity)} {convert.fl_to_s(day[daydata.etk("yyyymmdd")])}'

    # Specific output
    txt = text.padding(value, 'center', text.pad_min)[:text.pad_min]

    if file_type in text.lst_output_htm:
        value = html.extreme_values(day, entity) # Update value
        table = html.table_days(days_extr_2d, entity)
        htm = f'<td>{value}{table}</td>'

    elif file_type in text.lst_output_csv_excel:
        csv = f'{value}{cfg.csv_sep}'

    return txt, htm, csv 
