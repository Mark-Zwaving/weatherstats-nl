# -*- coding: utf-8 -*-
'''
Library contains functions for the calculation of the climate cells

CELL ID
clima_?AVE|MEAN|SUM?_?ENTITY?
'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.0.8'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import sources.view.text as text 
import sources.view.html as html
import sources.model.statistic.clima.mean as mean
import sources.model.statistic.clima.sum as sum
import sources.model.statistic.clima.indexes as indexes
import sources.model.statistic.clima.condition_cnt as clima_condit_cnt

def header(lst_cell, file_type):
    # Init variables
    txt, htm, csv, title = '', '', '', '' 
    clima, typ, entity, operand, value = '', '', '', '', ''

    if len(lst_cell) == 5:
        clima, typ, entity, operand, value = lst_cell
    elif len(lst_cell) == 4:
        clima, typ, entity, operand = lst_cell
    elif len(lst_cell) == 3:
        clima, typ, entity = lst_cell
    elif len(lst_cell) == 2: # ? 
        clima, typ = lst_cell

    if typ in text.lst_count:
        title = f'~Σ{entity}{operand}{value}'
    elif typ in text.lst_sum:
        title = f'~Σ{entity}'
    elif typ in text.lst_ndx:
        title = f'~{entity}'
    else:
        title = f'~{typ} {entity}' 

    # Text title 
    txt = text.padding(title, 'center', text.pad_clima)[:text.pad_clima] # Maximum length

    # HTML title
    if file_type in text.lst_output_htm:
        htm = f'<th title="{text.ent_to_txt(entity)}">{title}</th>'

    # CSV title
    elif file_type in text.lst_output_csv_excel:
        csv = f'{title}{cfg.csv_sep}'

    return txt, htm, csv 

def body(np_lst_days, lst_cell, file_type):
    txt, htm, csv, raw_val = '', '', '', cfg.no_val 
    # clima is at pos 1 and typ is always at position 3
    typ = lst_cell[1] 
    ent_val = 'X'

    # Select what todo 
     # E.g: clima_sum_rh
    if typ in text.lst_sum: # Calculate clima sum
        clima, typ, entity = lst_cell
        raw_val = sum.calculate(np_lst_days, entity)
        ent_val = text.fix_for_entity(raw_val, entity)

    # E.g: clima_ave_tg
    elif typ in text.lst_ave: # Calculate clima mean
        clima, typ, entity = lst_cell
        raw_val = mean.calculate(np_lst_days, entity)
        ent_val = text.fix_for_entity(raw_val, entity)

    # E.g: clima_cnt_tx_>=_25  
    elif typ in text.lst_count: # Calculate condtional counters
        clima, typ, entity, operand, value = lst_cell

        # Calculater counter
        raw_val = clima_condit_cnt.calculate(np_lst_days, entity, operand, value)
        raw_val = round(raw_val, 1) # Round it to 1 decimal
        ent_val = text.fix_for_entity(raw_val, 'cnt')

    # TODO
    # E.g: clima_ndx_hellmann
    elif typ in text.lst_ndx:
        clima, typ, entity = lst_cell
        raw_val = indexes.calculate(np_lst_days, entity)
        ent_val = text.fix_for_entity(raw_val, entity)


    # Fix value entity for output 
    # But only for non counters 
    # if typ not in text.lst_count:
    #     clima, typ, entity = lst_cell 
    # else: 
    #     ent_val = raw_val

    # Data txt
    txt += text.padding(ent_val, 'center', text.pad_clima)[:text.pad_clima]

    # Data html
    if file_type in text.lst_output_htm:
        htm = f'<td>{html.span(ent_val, "val")}</td>'

    # Data csv
    elif file_type in text.lst_output_csv_excel:
        csv = f'{ent_val}{cfg.csv_sep}'

    return txt, htm, csv 
