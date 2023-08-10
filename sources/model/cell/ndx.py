# -*- coding: utf-8 -*-
'''
Library contains function for the calculation of the index digits
Examples: heat, hellmann, frostsum

CELL ID
ndx_?ENTITY?

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

def head(lst_cell, file_type):
    txt, htm, csv = '', '', ''
    title  = lst_cell[0]  # ndx
    entity = lst_cell[1] # hellmann, frostsum, heat
    ico = ''

    if entity in text.lst_helmmann:
        txt = text.padding('HMANN', 'center', text.pad_hmann)[:text.pad_hmann]
        if file_type in text.lst_output_htm: 
            htm = f'<th title="{text.hellmann()}">{ico}hmann</th>'
        elif file_type in text.lst_output_csv_excel:
            csv = f'HMANN{cfg.csv_sep}'
            
    elif entity in text.lst_ijnsen:
        txt = text.padding('IJNS', 'center', text.pad_ijns)[:text.pad_ijns]
        if file_type in text.lst_output_htm: 
            htm = f'<th title="{text.ijnsen()}">{ico}ijnsen</th>'
        elif file_type in text.lst_output_csv_excel:
            csv = f'IJNS{cfg.csv_sep}'

    elif entity in text.lst_frost_sum:
        txt = text.padding('FSUM', 'center', text.pad_fsum)[:text.pad_fsum]
        if file_type in text.lst_output_htm: 
            htm = f'<th title="{text.frostsum()}">{ico}fsum</th>'
        elif file_type in text.lst_output_csv_excel:
            csv = f'FSUM{cfg.csv_sep}'

    elif entity in text.lst_heat_ndx:
        txt = text.padding('HEAT', 'center', text.pad_heat_ndx)[:text.pad_heat_ndx]
        if file_type in text.lst_output_htm: 
            htm = f'<th title="{text.heat_ndx()}">{ico}heat</th>'
        elif file_type in text.lst_output_csv_excel:
            csv = f'HEAT{cfg.csv_sep}'

    return txt, htm, csv


def calc(days, lst_cell, file_type):
    '''Calculate the cells for the specific index digit'''
    txt, htm, csv = '', '', '' # Three types
    entity = lst_cell[1]

    # Heat Index
    if entity in text.lst_heat_ndx:
        heat_ndx_raw, days_heat_2d = days.heat_ndx()
        heat_ndx_val = text.fix_ent(heat_ndx_raw, entity)

        txt = text.padding(heat_ndx_val, 'center', text.pad_heat_ndx)[:text.pad_heat_ndx]
        if file_type in text.lst_output_htm:
            value = html.span(heat_ndx_val, 'val')
            table = html.table_heat_ndx(days_heat_2d)
            htm = f'<td>{value}{table}</td>'
        elif file_type in text.lst_output_csv_excel:
            csv = f'{heat_ndx_val}{cfg.csv_sep}'

    # Hellmann
    elif entity in text.lst_helmmann:
        hellmann_raw, days_hmann_2d = days.hellmann()
        hellmann_val = text.fix_ent(hellmann_raw, entity)

        txt += text.padding(hellmann_val, 'center', text.pad_hmann)[:text.pad_hmann]
        if file_type in text.lst_output_htm:
            value = html.span(hellmann_val, 'val')
            table = html.table_hellmann(days_hmann_2d)
            htm = f'<td>{value}{table}</td>'
        elif file_type in text.lst_output_csv_excel:
            csv = f'{hellmann_val}{cfg.csv_sep}'

    # IJnsen
    elif entity in text.lst_ijnsen:
        ijnsen_raw, days_ijnsen_2d = days.ijnsen()
        ijnsen_val = text.fix_ent(ijnsen_raw, entity)

        txt = text.padding(ijnsen_val, 'center', text.pad_ijns)[:text.pad_ijns]
        if file_type in text.lst_output_htm:
            value = html.span(ijnsen_val, 'val')
            table = html.table_ijnsen(days_ijnsen_2d)
            htm = f'<td>{value}{table}</td>'
        elif file_type in text.lst_output_csv_excel:
            csv = f'{ijnsen_val}{cfg.csv_sep}'

    # Frost sum
    elif entity in text.lst_frost_sum:
        fsum_raw, days_fsum_2d = days.frost_sum()
        fsum_val = text.fix_ent(fsum_raw, entity)

        txt += text.padding(fsum_val, 'center', text.pad_fsum)[:text.pad_default]
        if file_type in text.lst_output_htm:
            value = html.span(fsum_val, 'val')
            table = html.table_frost_sum(days_fsum_2d)
            htm = f'<td>{value}{table}</td>'
        elif file_type in text.lst_output_csv_excel:
            csv = f'{fsum_val}{cfg.csv_sep}'

    return txt, htm, csv 
