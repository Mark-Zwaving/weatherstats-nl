'''Library contains function for the calculation of the fix day cells'''
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
import sources.model.dayvalues.data as data 

def header(lst_cell, file_type):
    txt, htm, csv = '', '', ''
    entity = lst_cell[1]  

    txt = text.padding(entity, 'center', text.pad_day)[:text.pad_day]
    ico = html.entity_to_icon(entity, size='fa-sm', color=cfg.e, extra=cfg.e) # Icon
    if file_type in text.lst_output_htm: 
        htm = f'<th title="{html.attr_title(entity)}">{ico}{entity}</th>'
    elif file_type in text.lst_output_csv_excel:
        csv = f'{entity}{cfg.csv_sep}'

    return txt, htm, csv

def body(np_lst_days, lst_cell, file_type):
    txt, htm, csv = '', '', ''
    entity = lst_cell[1] 

    val = text.fix_for_entity(np_lst_days[data.column(entity)], entity) 
    txt += text.padding(val, 'center', text.pad_day)[:text.pad_day] 
    if file_type in text.lst_output_htm: 
        htm += f'<td>{html.span(val, "val")}</td>' 
    elif file_type in text.lst_output_csv_excel: 
        csv += f'{val}{cfg.csv_sep}' 

    return txt, htm, csv
