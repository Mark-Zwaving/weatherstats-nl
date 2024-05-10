# -*- coding: utf-8 -*-
'''
Library contains functions for the calculation of the info cell options

CELL ID
inf_?OPTION?

Examples: inf_province, inf_period1, inf_period2
'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.0.5'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import sources.view.text as text 
import sources.view.html as html
import sources.view.html as icon
import sources.model.ymd as ymd
import sources.model.dayvalues.data as data
import sources.model.stations as stations
import sources.model.convert as convert
import sources.model.utils as utils

def header( lst_cell, file_type ):
    txt, htm, csv = '', '', ''
    title = lst_cell[0] # inf, info
    entity = lst_cell[1]
    ico = html.entity_to_icon(entity, size='fa-sm', color=cfg.e, extra=cfg.e) # Icon

    if entity in text.lst_copyright:
        txt = text.padding(' ', 'center', text.pad_copyright)[:text.pad_copyright]
        if file_type in text.lst_output_htm: 
            htm = '<th title="copyright data_notification"></th>'
        elif file_type in text.lst_output_csv_excel:
            csv = f'copy{cfg.csv_sep}'

    elif entity in text.lst_geo_places:
        if entity == 'place':
            txt = text.padding('PLACE', 'left', text.pad_place)[:text.pad_place]
            if file_type in text.lst_output_htm: 
                htm = f'<th>{ico}place</th>'
            elif file_type in text.lst_output_csv_excel:
                csv = f'place{cfg.csv_sep}'

        elif entity == 'province':
            txt = text.padding('PROVINCE', 'left', text.pad_province)[:text.pad_province]
            if file_type in text.lst_output_htm: 
                htm = f'<th>{ico}province</th>'
            elif file_type in text.lst_output_csv_excel:
                csv = f'province{cfg.csv_sep}'

        elif entity == 'country':
            txt = text.padding('COUNTRY', 'left', text.pad_country)[:text.pad_country]
            if file_type in text.lst_output_htm: 
                htm = f'<th>{ico}country</th>'
            elif file_type in text.lst_output_csv_excel:
                csv = f'country{cfg.csv_sep}'

    elif entity in text.lst_period_1:
        txt = text.padding('PERIOD1', 'center', text.pad_period_1)[:text.pad_period_1]
        if file_type in text.lst_output_htm: 
            htm = f'<th>{ico}period</th>'
        elif file_type in text.lst_output_csv_excel:
            csv = f'period{cfg.csv_sep}'
            
    elif entity in text.lst_period_2:
        txt = text.padding('PERIOD2', 'center', text.pad_period_2)[:text.pad_period_2]
        if file_type in text.lst_output_htm: 
            htm = f'<th>{ico}period2</th>'    
        elif file_type in text.lst_output_csv_excel:
            csv = f'period2{cfg.csv_sep}'

    elif entity in text.lst_num:
        txt = text.padding('NUM', 'center', text.pad_num)[:text.pad_num]
        if file_type in text.lst_output_htm: 
            htm = f'<th>{ico}num</th>'
        elif file_type in text.lst_output_csv_excel:
            csv = f'num{cfg.csv_sep}'

    elif entity in text.lst_month:
        txt = text.padding('MONTH', 'center', text.pad_month)[:text.pad_month]
        if file_type in text.lst_output_htm: 
            htm = f'<th>{ico}month</th>'
        elif file_type in text.lst_output_csv_excel:
            csv = f'month{cfg.csv_sep}'

    elif entity in text.lst_day:
        txt = text.padding('DAY', 'center', text.pad_day)[:text.pad_day]
        if file_type in text.lst_output_htm: 
            htm = f'<th>{ico}day</th>'
        elif file_type in text.lst_output_csv_excel:
            csv = f'day{cfg.csv_sep}'

    return txt, htm, csv


def body(options, np_lst_days_1, np_lst_days_2, lst_cell, day, cnt, file_type):
    txt, htm, csv = '', '', ''
    title, entity  = lst_cell[0], lst_cell[1]
    col_ymd, col_stn = data.column('yyyymmdd'), data.column('stn')

    wmo = str(int(np_lst_days_1[0, col_stn]))
    station = stations.wmo_to_station(wmo) 
    symd = str(int(np_lst_days_1[ 0, col_ymd]))
    eymd = str(int(np_lst_days_1[-1, col_ymd]))

    if entity in text.lst_copyright:
        txt = text.padding('©', 'center', text.pad_copyright)[:text.pad_copyright]
        if file_type in text.lst_output_htm:
            htm = f'<td title="{station.data_notification.lower()}"><small class="text-muted">{icon.copy_light(size="fa-xs")}</small></td>'
        elif file_type in text.lst_output_csv_excel:
            csv = '©,'

    elif entity in text.lst_place:
        txt = text.padding(station.place, 'left', text.pad_place)[:text.pad_place]
        if file_type in text.lst_output_htm: 
            htm = f'<td class="font-italic text-left">{html.span(station.place, "val")}</td>'
        elif file_type in text.lst_output_csv_excel:
            csv = f'{station.place}{cfg.csv_sep}'

    elif entity in text.lst_province:
        txt = text.padding(station.province, 'left', text.pad_province)[:text.pad_province]
        if file_type in text.lst_output_htm: 
            htm = f'<td class="font-italic text-left">{html.span(station.province, "val")}</td>'
        elif file_type in text.lst_output_csv_excel:
            csv = f'{station.province}{cfg.csv_sep}'

    elif entity in text.lst_country:
        txt = text.padding(station.country, 'left', text.pad_country)[:text.pad_country]
        if file_type in text.lst_output_htm: 
            htm = f'<td class="font-italic text-left">{html.span(station.country, "val")}</td>'
        elif file_type in text.lst_output_csv_excel:
            csv = f'{station.country}{cfg.csv_sep}'

    # yyyymmdd - yyyymmdd
    elif entity in text.lst_period_1:
        if symd == cfg.date_false:
            period_ymd  = cfg.no_val
            period_txt  = cfg.no_val
        else:
            period_ymd = f'{symd}-{eymd}'
            period_txt = f'{ymd.yyyymmdd_to_text(symd)} - {ymd.yyyymmdd_to_text(eymd)}'

        txt = text.padding(period_ymd, 'center', text.pad_period_1)[:text.pad_period_1]

        if file_type in text.lst_output_htm:
            htm = f'<td title="{period_txt}">{html.span(period_ymd, "val")}</td>'
        elif file_type in text.lst_output_csv_excel:
            csv = f'{period_ymd}{cfg.csv_sep}'

    # yyyymmdd or mmdd or yyyymmdd-yyyymmdd
    elif entity in text.lst_period_2:
        # Make new period
        symd = str(int(np_lst_days_2[ 0, col_ymd]))
        eymd = str(int(np_lst_days_2[-1, col_ymd]))
        period2 = f'{symd}-{eymd}' # Later
        period2 = options[text.ask_period_2]
        txt = text.padding(period2, 'center', text.pad_period_2)[:text.pad_period_2]
        if file_type in text.lst_output_htm:
            htm = f'<td>{html.span(period2, "val")}</td>'
        elif file_type in text.lst_output_csv_excel:
            csv = f'{period2}{cfg.csv_sep}'

    # Counter for rows
    elif entity in text.lst_num:
        txt = text.padding(cnt, 'center', text.pad_num)[:text.pad_num]
        cnt = utils.l0(cnt, 3)
        if file_type in text.lst_output_htm:
            htm = f'<td title="num of day">{html.span(cnt, "val")}</td>'
        elif file_type in text.lst_output_csv_excel:
            csv = f'{cnt}{cfg.csv_sep}'

    # Day
    elif entity in text.lst_day:
        yymmdd = convert.fl_to_s(day[data.column('yyyymmdd')])
        
        txt = text.padding(ymd, 'center', text.pad_day)[:text.pad_day]
        if file_type in text.lst_output_htm:
            htm = f'<td title="{ymd.yyyymmdd_to_text(yymmdd)}">{html.span(int(yymmdd), "val")}</td>'
        elif file_type in text.lst_output_csv_excel:
            csv = f'{yymmdd}{cfg.csv_sep}'

    # A day in a month
    elif entity in text.lst_yyyymmdd:
        txt = text.padding(entity, 'center', text.pad_day)[:text.pad_day]
        if file_type in text.lst_output_htm:
            htm = f'<td title="">{html.span(entity, "val")}</td>'
        elif file_type in text.lst_output_csv_excel:
            csv = f'{entity}{cfg.csv_sep}'

    # Month num/name TODO
    elif entity in text.lst_month:
        txt = text.padding(entity, 'center', text.pad_month)[:text.pad_month]
        if file_type in text.lst_output_htm:
            htm = f'<td>{html.span(entity, "val")}</td>'
        elif file_type in text.lst_output_csv_excel:
            csv = f'{entity}{cfg.csv_sep}'

    return txt, htm, csv 
