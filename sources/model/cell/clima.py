# -*- coding: utf-8 -*-
'''
Library contains functions for the calculation of the climate cells

CELL ID
clima_?AVE|MEAN|SUM?_?ENTITY?
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
import sources.view.icon as icon 

def head(lst, file_type):
    txt, htm, csv = '', '', ''
    title  = lst[0] # climate, clima 
    option = lst[1] # AVE, MEAN, SUM
    entity = lst[2] # TX, SQ ...

    # Text title
    txt = text.padding(f'{title} {option} {entity}', 'center', text.pad_clima)[:text.pad_clima]

    # HTML title
    if file_type in text.lst_output_htm: 
        ico = icon.ellipsis(size='fa-sm', color=cfg.e, extra=cfg.e)
        htm = f'<th title="{text.ent_to_txt(entity)}">{ico}{entity}</th>'

    # CSV title
    elif file_type in text.lst_output_csv_excel:
        csv = f'CLI {option} {entity}{cfg.csv_sep}'

    return txt, htm, csv 


def calc(days, lst_cell, file_type):
    txt, htm, csv = '', '', '' 
    title  = lst_cell[0]
    option = lst_cell[1]
    entity = lst_cell[2]

    # Make clima days object
    raw, _ = days.climate( entity, option ) # Calculate average
    val = text.fix_ent( raw, entity )

    # Data txt
    txt += text.padding(val, 'center', text.pad_clima)[:text.pad_clima]

    # Data html
    if file_type in text.lst_output_htm:
        htm = f'<td>{html.span(val, "val")}</td>'

    # Data csv
    elif file_type in text.lst_output_csv_excel:
        csv = f'{val}{cfg.csv_sep}'

    return txt, htm, csv 
