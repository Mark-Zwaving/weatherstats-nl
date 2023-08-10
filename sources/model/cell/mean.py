# -*- coding: utf-8 -*-
'''
Library contains functions for the calculation of the sum cells

CELL ID
ave_?ENTITY?
'''

__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 3 - GPLv3'
__version__    =  '0.0.1'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg 
import sources.view.text as text 
import sources.view.html as html 

def head(lst, file_type):
    txt, htm, csv = '', '', ''
    title, entity = lst[0], lst[1] # Cell option id. Example lst: [ave, tx]

    txt = text.padding(f'{title} {entity}', 'center', text.pad_ave)[:text.pad_ave]
    if file_type in text.lst_output_htm:
        ico1 = html.entity_to_icon(entity, size='fa-sm', color=cfg.e, extra=cfg.e)
        htm = f'<th title="{html.attr_title(entity)}">{html.title_mean(f"{ico1}{entity}")}</th>'
    elif file_type in text.lst_output_csv_excel:
        csv = f'{title} {entity}{cfg.csv_sep}'

    return txt, htm, csv 

def calc(days, lst_cell, file_type):
    txt, htm, csv = '', '', ''
    entity = lst_cell[1]

    # Calculate means
    ave_raw, days_ave_2d = days.average(entity)
    ave_val = text.fix_ent(ave_raw, entity)

    txt = text.padding(ave_val, 'center', text.pad_ave)[:text.pad_ave]
    if file_type in text.lst_output_htm:
        value = html.span(ave_val, 'val')
        table = html.table_average(days_ave_2d, entity, reverse=True)
        htm = f'<td>{value}{table}</td>'
    elif file_type in text.lst_output_csv_excel:
        csv = f'{ave_val}{cfg.csv_sep}'

    return txt, htm, csv
