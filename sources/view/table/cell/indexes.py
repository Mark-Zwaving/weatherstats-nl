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
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.0.6'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg 
import numpy as np
import sources.view.text as text 
import sources.view.html as html 
import sources.view.table.popup as popup
import sources.model.statistic.indexes.frostsum as frostsum
import sources.model.statistic.indexes.hellmann as hellmann
import sources.model.statistic.indexes.heat as heat
import sources.model.statistic.indexes.ijnsen as ijnsen

def header(lst_cell, file_type):
    txt, htm, csv = '', '', ''
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


def body(np_lst_days, lst_cell, file_type):
    '''Calculate the cells for the specific index digit'''
    txt, htm, csv = '', '', '' # Three types
    entity = lst_cell[1]

    # Heat Index (NL)
    if entity in text.lst_heat_ndx: 
        heat_raw, np_lst_heat_nl = heat.calculate_nl(np_lst_days) 
        heat_val = text.fix_for_entity(heat_raw, entity) 
        
        txt = text.padding(heat_val, 'center', text.pad_heat_ndx)[:text.pad_heat_ndx] 

        if file_type in text.lst_output_htm: 
            value = html.span(heat_val, 'val')
            pop_up = popup.table_heat_ndx(np_lst_heat_nl)
            htm = f'<td>{value}{pop_up}</td>'
        elif file_type in text.lst_output_csv_excel:
            csv = f'{heat_val}{cfg.csv_sep}'

    # Hellmann
    elif entity in text.lst_helmmann:
        hellmann_raw, np_lst_hellmann = hellmann.calculate(np_lst_days)
        hellmann_val = text.fix_for_entity(hellmann_raw, entity)

        txt += text.padding(hellmann_val, 'center', text.pad_hmann)[:text.pad_hmann]

        if file_type in text.lst_output_htm:
            value = html.span(hellmann_val, 'val')
            pop_up = popup.table_hellmann(np_lst_hellmann)
            htm = f'<td>{value}{pop_up}</td>'
        elif file_type in text.lst_output_csv_excel:
            csv = f'{hellmann_val}{cfg.csv_sep}'

    # IJnsen
    elif entity in text.lst_ijnsen:
        ijnsen_raw, np_lst_ijnsen, _, _, _ = ijnsen.calculate(np_lst_days)
        ijnsen_val = text.fix_for_entity(ijnsen_raw, entity)

        txt = text.padding(ijnsen_val, 'center', text.pad_ijns)[:text.pad_ijns]

        if file_type in text.lst_output_htm:
            value = html.span(ijnsen_val, 'val')
            pop_up = popup.table_ijnsen(np_lst_ijnsen)
            htm = f'<td>{value}{pop_up}</td>'
        elif file_type in text.lst_output_csv_excel:
            csv = f'{ijnsen_val}{cfg.csv_sep}'

    # Frost sum
    elif entity in text.lst_frost_sum:
        fsum_raw, np_lst_frostsum, _, _, _, _ = frostsum.calculate_nl(np_lst_days)
        fsum_val = text.fix_for_entity(fsum_raw, entity)

        txt += text.padding(fsum_val, 'center', text.pad_fsum)[:text.pad_default]
        
        if file_type in text.lst_output_htm:
            value = html.span(fsum_val, 'val')
            pop_up = popup.table_frost_sum(np_lst_frostsum)
            htm = f'<td>{value}{pop_up}</td>'
        elif file_type in text.lst_output_csv_excel:
            csv = f'{fsum_val}{cfg.csv_sep}'

    return txt, htm, csv 
