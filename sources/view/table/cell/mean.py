# -*- coding: utf-8 -*-
'''
Library contains functions for the calculation of the sum cells

CELL ID
ave_?ENTITY?
'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.0.4'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg 
import sources.view.text as text 
import sources.view.html as html 
import sources.view.table.popup as popup
import sources.model.statistic.mean as mean

def header(lst, file_type):
    '''Function creates the head cell for mean''' 
    txt, htm, csv = '', '', ''
    title, entity = lst[0], lst[1] # Cell option id. Example lst: [ave, tx]

    txt = text.padding(f'{title} {entity}', 'center', text.pad_ave)[:text.pad_ave]

    if file_type in text.lst_output_htm:
        ico1 = html.entity_to_icon(entity, size='fa-sm', color=cfg.e, extra=cfg.e)
        htm = f'<th title="{html.attr_title(entity)}">{html.title_mean(f"{ico1}{entity}")}</th>'

    elif file_type in text.lst_output_csv_excel:
        csv = f'{title} {entity}{cfg.csv_sep}'

    return txt, htm, csv 

def body(np_lst_days, lst_cell, file_type):
    '''Function creates the body cell for mean''' 
    txt, htm, csv = '', '', '' 
    entity = lst_cell[1] 

    # Calculate mean
    ave_raw, np_lst_valid = mean.calculate(np_lst_days, entity)
    ave_val = text.fix_for_entity(ave_raw, entity)

    txt = text.padding(ave_val, 'center', text.pad_ave)[:text.pad_ave]

    if file_type in text.lst_output_htm:
        value = html.span(ave_val, 'val')
        pop_up = popup.table_average(np_lst_valid, entity, reverse=True)
        htm = f'<td>{value}{pop_up}</td>'

    elif file_type in text.lst_output_csv_excel:
        csv = f'{ave_val}{cfg.csv_sep}'

    return txt, htm, csv
