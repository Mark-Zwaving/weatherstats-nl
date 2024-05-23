# -*- coding: utf-8 -*-
'''Library contain functions to make the table row for the compare option'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.0.7'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import sources.view.text as text
import sources.view.table.body as body
import sources.view.console as cnsl
import sources.model.dayvalues.data as data
import sources.model.utils as utils
import sources.model.dayvalues.broker_period as dayval_broker
import sources.model.ymd as ymd
import numpy as np

def process(station, options, np_lst_period1, cnt):
    '''Function creates the rows for the compare table'''
    # Init variables
    id, period = options[text.ask_per_compare]
    col_ymd = data.column('yyyymmdd') # Column date  
    body_htm, body_txt, body_csv = '', '', ''

    # Get start and end date for period 1, make string 
    symd1 = str(int(np_lst_period1[ 0,col_ymd])) # Start date period 1
    eymd1 = str(int(np_lst_period1[-1,col_ymd])) # End date period 1
    
    # Extra 
    # Add period-2 to list cell to show in table, if not there yet
    if utils.key_from_lst(options[text.ask_select_cells], 'inf_period-2') == -1:
        lst = options[text.ask_select_cells]
        key = utils.key_from_lst( options[text.ask_select_cells], 'inf_period-1' ) # Get key value
        key = 0 if key == -1 else key + 1 # input(key)
        lst_2 = lst[:key] # Add period-2 to lst to show in table
        lst_2.append('inf_period-2')
        options[text.ask_select_cells] = lst_2 + lst[key:] 

        # Now remove period 1 from lst
        if 'inf_period-1' in options[text.ask_select_cells]:
            options[text.ask_select_cells].remove('inf_period-1')

    # Walkthrough the years
    lst_yyyy = [str(yymmdd)[:4] for yymmdd in range(int(symd1), int(eymd1), 10000)]

    # Reverse lst years and walkthrough the years
    # for the calculation data for a specific period
    for yyyy in lst_yyyy[::-1]: 
        print("id: ", id)
        print("period: " , period)
        # input()

        if id in text.lst_year:
            options[text.ask_period_2] = f'{yyyy}****'

        elif id in text.lst_month:
            options[text.ask_period_2] = f'{yyyy}{period}**'

        elif id in text.lst_day:
            options[text.ask_period_2] = f'{yyyy}{period}'
    
        elif id in text.lst_season:
    
            if period in text.lst_winter: 
                dec, feb = 1201, '0229' if ymd.is_leap(yyyy) else '0228' 
                options[text.ask_period_2] = f'{int(yyyy)-1}{dec}-{yyyy}{feb}'

            elif period in text.lst_spring: 
                march, mai = '0301', '0531'
                options[text.ask_period_2] = f'{yyyy}{march}-{yyyy}{mai}' 

            elif period in text.lst_summer: 
                jun, aug = '0601', '0831'
                options[text.ask_period_2] = f'{yyyy}{jun}-{yyyy}{aug}'

            elif period in text.lst_autumn: 
                sep, nov = '0901', '1130'
                options[text.ask_period_2] = f'{yyyy}{sep}-{yyyy}{nov}'
    
        elif id in text.lst_mmdd_compare:

            mmdd1, mmdd2 = period.split('-')

            if int(mmdd1) <= int(mmdd2): 
                options[text.ask_period_2] = f'{yyyy}{mmdd1}-{yyyy}{mmdd2}'
    
            else: 
                sy = str(int(yyyy)-1)
                options[text.ask_period_2] = f'{sy}{mmdd1}-{yyyy}{mmdd2}'

        # Get days period 2
        period2 = options[text.ask_period_2]
        ok, np_lst_period2 = dayval_broker.process(np_lst_period1, period2)

        # No data in period 2
        if np.size(np_lst_period2) == 0: 
            body_htm = body_htm + body.no_data_row_htm(station, options,  period2)
            body_txt = body_txt + cfg.no_val
            body_csv = body_csv + cfg.no_val

            # Skip row
            continue

        t = text.info_line('Calculate', options, station)
        cnsl.log(t, True)

        # Count the days
        cnt += 1  

        # Get the cells with data
        htm, txt, csv = body.row(station, options, np_lst_period1, np_lst_period2, 
                                 day=cfg.e, cnt=cnt) 
        body_htm = body_htm + htm
        body_txt = body_txt + txt
        body_csv = body_csv + csv

    return body_htm, body_txt, body_csv, cnt
