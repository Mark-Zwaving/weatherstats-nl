# -*- coding: utf-8 -*-
'''Library contains classes and functions for calculating statistics'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 3 - GPLv3'
__version__    =  '0.1.1'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

from importlib.resources import path
from pkgutil import read_code
import numpy as np
import pandas as pd
import sources.view.text as text
import sources.view.icon as icon
import sources.view.html as html
import sources.view.console as cnsl
import sources.model.stats as stats
import sources.model.daydata as daydata
import sources.model.utils as utils
import sources.model.validate as valid
import sources.model.ymd as ymd
import sources.model.convert as convert
import sources.control.fio as fio
import config as cfg

def calculate(options, type='normal'):
    '''Function calculates all statistics'''
    cnsl.log(f'[{ymd.now()}] {options["title"].upper()}', True)

    body_htm, body_txt, body_csv, options, cnt = body(options)
    options['colspan'] = len(options['lst-sel-cells'])

    head_htm, head_txt, head_csv, script = head(options, cnt)
    foot_htm, foot_txt, foot_csv = foot(options)

    htm = f'{head_htm}{body_htm}{foot_htm}{script}' # HTML data
    txt = f'{head_txt}\n{body_txt}{foot_txt}' # Text data

    # Remove separator at the end if there
    if len( head_csv) > 0: 
        if head_csv[-1] == cfg.csv_sep: 
            head_csv = head_csv[:-1]
    if len(body_csv) > 0: 
        if body_csv[-1] == cfg.csv_sep: 
            body_csv = body_csv[:-1]
    if len(foot_csv) > 0: 
        if foot_csv[-1] == cfg.csv_sep: 
            foot_csv = foot_csv[:-1]

    csv = f'{head_csv}\n{body_csv}\n{foot_csv}' # Csv data

    # Output to screen or file(s) 
    ok, path = output(htm, txt, csv, options)

    return ok, path

def js_script_fn( option, sort_type, sort_dir, row_num, col_num ):
    '''Function makes an JavaScript object to handle a function call for sorting the table column'''
    # Option    : type coll TX, province, ... 
    # Sort_type : 'num' or 'txt' (numeric of alfa)
    # Sort_dir  : '+' (descending: large to small), '-' (ascending: small to high)
    # Row_num   : 2 (num of row in table)
    # Col_num   : 1..end (colum num in table)

    # Sort object 
    return f'\n{option}' + ': { ' + f''' 
        name: '{option}',
        doc: document.querySelector('table#stats>thead>tr:nth-child({row_num})>th:nth-child({col_num})'),
        type: '{sort_type}', dir: '{sort_dir}', row: {row_num}, col: {col_num-1}
    ''' + ' },'

def head(options, cnt=0):
    '''Makes the header'''
    head_htm, head_txt, head_csv, ftyp = '', '', '', options['file-type']
    # Sorting script vars
    col_num    = 0     # Start column num is 0 increment at start
    descending = '+'   # Identifier sort direction: large to small
    ascending  = '-'   # Identifier sort direction: small to high
    sort_num   = 'num' # Identifier sort num-based
    sort_txt   = 'txt' # Identifier sort txt-based
    row_num    = 2     # Row tr num for click to sort
    # Add a script with a Javascript object for sorting with columns
    script     = '' 

    if ftyp in text.lst_output_htm:
        head_htm += f'''
        <table class="rounded shadow border" id="stats"><thead><tr>
            <th colspan="{options['colspan']}">
                {icon.weather_all()} {options['title']} {icon.wave_square()} {options['period']} {icon.cal_period()}                 
            </th></tr><tr>'''

    if ftyp in text.lst_output_txt_cnsl:
        pass # head_txt += '#' * 80 + '\n'

    for option in options['lst-sel-cells']:
        # Sort options. 
        # Defaults: sort is True, numeric and descending. Add 1 to col_num
        sort_type, sort_dir, col_num = sort_num, descending, col_num + 1
        lst = option.split('_') # Make lst
        typ, entity = lst[0], lst[1]
        ico = html.entity_to_icon(entity, size='fa-sm', color='', extra='') # Icon

        # Info texts
        if typ in text.lst_info:
            if entity in text.lst_copyright:
                head_txt += text.padding(' ', 'center', text.pad_copyright)[:text.pad_copyright]
                if ftyp in text.lst_output_htm: 
                    head_htm += '<th title="copyright data_notification"></th>'
                elif ftyp in text.lst_output_csv_excel:
                    head_csv += f'copy{cfg.csv_sep}'

            elif entity in text.lst_geo_places:
                if entity == 'place':
                    head_txt += text.padding('PLACE', 'left', text.pad_place)[:text.pad_place]
                    if ftyp in text.lst_output_htm: 
                        head_htm += f'<th>{ico}place</th>'
                    elif ftyp in text.lst_output_csv_excel:
                        head_csv += f'place{cfg.csv_sep}'

                elif entity == 'province':
                    head_txt += text.padding('PROVINCE', 'left', text.pad_province)[:text.pad_province]
                    if ftyp in text.lst_output_htm: 
                        head_htm += f'<th>{ico}province</th>'
                    elif ftyp in text.lst_output_csv_excel:
                        head_csv += f'province{cfg.csv_sep}'

                elif entity == 'country':
                    head_txt += text.padding('COUNTRY', 'left', text.pad_country)[:text.pad_country]
                    if ftyp in text.lst_output_htm: 
                        head_htm += f'<th>{ico}country</th>'
                    elif ftyp in text.lst_output_csv_excel:
                        head_csv += f'country{cfg.csv_sep}'

                sort_type = sort_txt # Text sort

            elif entity in text.lst_period_1:
                head_txt += text.padding('PERIOD1', 'center', text.pad_period_1)[:text.pad_period_1]
                if ftyp in text.lst_output_htm: 
                    head_htm += f'<th>{ico}period</th>'
                elif ftyp in text.lst_output_csv_excel:
                    head_csv += f'period{cfg.csv_sep}'
                    
            elif entity in text.lst_period_2:
                head_txt += text.padding('PERIOD2', 'center', text.pad_period_2)[:text.pad_period_2]
                if ftyp in text.lst_output_htm: 
                    head_htm += f'<th>{ico}period2</th>'    
                elif ftyp in text.lst_output_csv_excel:
                    head_csv += f'period2{cfg.csv_sep}'

            elif entity in text.lst_num:
                head_txt += text.padding('NUM', 'center', text.pad_num)[:text.pad_num]
                if ftyp in text.lst_output_htm: 
                    head_htm += f'<th>{ico}num</th>'
                elif ftyp in text.lst_output_csv_excel:
                    head_csv += f'num{cfg.csv_sep}'

            elif entity in text.lst_month:
                head_txt += text.padding('MONTH', 'center', text.pad_month)[:text.pad_month]
                if ftyp in text.lst_output_htm: 
                    head_htm += f'<th>{ico}month</th>'
                elif ftyp in text.lst_output_csv_excel:
                    head_csv += f'month{cfg.csv_sep}'

            elif entity in text.lst_day:
                head_txt += text.padding('DAY', 'center', text.pad_day)[:text.pad_day]
                if ftyp in text.lst_output_htm: 
                    head_htm += f'<th>{ico}day</th>'
                elif ftyp in text.lst_output_csv_excel:
                    head_csv += f'day{cfg.csv_sep}'

        # Fixed day values
        elif typ in text.lst_day:
            head_txt += text.padding(entity, 'center', text.pad_day)[:text.pad_day]
            if ftyp in text.lst_output_htm: 
                head_htm += f'<th title="{html.attr_title(entity)}">{ico}{entity}</th>'
            elif ftyp in text.lst_output_csv_excel:
                head_csv += f'{entity}{cfg.csv_sep}'

        # Max extreme
        if typ in text.lst_max:
            head_txt += text.padding(f'max {entity}', 'center', text.pad_max)[:text.pad_max]
            if ftyp in text.lst_output_htm:
                ico2 = html.entity_to_icon(typ, size='fa-sm', color='', extra='') # Icon2
                head_htm += f'<th title="{html.attr_title(entity)}">{ico}{entity}{ico2}</th>'
            elif ftyp in text.lst_output_csv_excel:
                head_csv += f'max {entity}{cfg.csv_sep}'

        # Min extreme
        elif typ in text.lst_min:
            head_txt += text.padding(f'min {entity}', 'center', text.pad_min)[:text.pad_min]
            if ftyp in text.lst_output_htm: 
                ico2 = html.entity_to_icon(typ, size='fa-sm', color='', extra='') # Icon2
                head_htm += f'<th title="{html.attr_title(entity)}">{ico}{entity}{ico2}</th>'
            elif ftyp in text.lst_output_csv_excel:
                head_csv += f'min {entity}{cfg.csv_sep}'

        # Average
        elif typ in text.lst_ave:
            head_txt += text.padding(f'ave {entity}', 'center', text.pad_ave)[:text.pad_ave]
            if ftyp in text.lst_output_htm:
                ico2 = html.entity_to_icon(entity, size='fa-sm', color='', extra='')
                head_htm += f'<th title="{html.attr_title(entity)}">{html.title_mean(f"{ico2}{entity}")}</th>'
            elif ftyp in text.lst_output_csv_excel:
                head_csv += f'ave {entity}{cfg.csv_sep}'

        # Sum
        elif typ in text.lst_sum:
            head_txt += text.padding(f'Σ{entity}', 'center', text.pad_sum)[:text.pad_sum]
            if ftyp in text.lst_output_htm: 
                head_htm += f'<th title="{html.attr_title(entity)}">Σ{entity}</th>'
            elif ftyp in text.lst_output_csv_excel:
                head_csv += f'Σ{entity}{cfg.csv_sep}'

        # Indexes
        elif typ in text.lst_ndx:
            if entity in text.lst_helmmann:
                head_txt += text.padding('HMANN', 'center', text.pad_hmann)[:text.pad_hmann]
                if ftyp in text.lst_output_htm: 
                    head_htm += f'<th title="{text.hellmann()}">{ico}hmann</th>'
                elif ftyp in text.lst_output_csv_excel:
                    head_csv += f'HMANN{cfg.csv_sep}'
                    
            elif entity in text.lst_ijnsen:
                head_txt += text.padding('IJNS', 'center', text.pad_ijns)[:text.pad_ijns]
                if ftyp in text.lst_output_htm: 
                    head_htm += f'<th title="{text.ijnsen()}">{ico}ijnsen</th>'
                elif ftyp in text.lst_output_csv_excel:
                    head_csv += f'IJNS{cfg.csv_sep}'

            elif entity in text.lst_frost_sum:
                head_txt += text.padding('FSUM', 'center', text.pad_fsum)[:text.pad_fsum]
                if ftyp in text.lst_output_htm: 
                    head_htm += f'<th title="{text.frostsum()}">{ico}fsum</th>'
                elif ftyp in text.lst_output_csv_excel:
                    head_csv += f'FSUM{cfg.csv_sep}'

            elif entity in text.lst_heat_ndx:
                head_txt += text.padding('HEAT', 'center', text.pad_heat_ndx)[:text.pad_heat_ndx]
                if ftyp in text.lst_output_htm: 
                    head_htm += f'<th title="{text.heat_ndx()}">{ico}heat</th>'
                elif ftyp in text.lst_output_csv_excel:
                    head_csv += f'HEAT{cfg.csv_sep}'

        # Counters
        elif typ in text.lst_count:
            sign, val = lst[2], lst[3]
            head_txt += text.padding(f'{entity} {sign} {val}', 'center', text.pad_cnt)[:text.pad_cnt]
            if ftyp in text.lst_output_htm: 
                ico = html.entity_to_icon(sign, size="fa-xs") # Update icon
                head_htm += f'<th title="{text.title(entity,sign,val)}">{entity}{ico}{val}</th>'
            elif ftyp in text.lst_output_csv_excel:
                head_csv += f'{entity}{sign}{val}{cfg.csv_sep}'

        # Climate
        elif typ in text.lst_clima:
            option = entity
            entity = lst[2]

            # print(typ, option, entity)
            # input()
            ico_clima = icon.ellipsis(size='fa-sm', color='', extra='')
            
            htm, title = f'{ico_clima}{entity}', f'{text.ent_to_txt(entity)}'
            if option in text.lst_ave: 
                title = f'climate mean {title}' 
            elif option in text.lst_sum: 
                title = f'climate sum {title}'
        
            head_txt += text.padding(f'CLI {option} {entity}', 'center', text.pad_clima)[:text.pad_clima]
            if ftyp in text.lst_output_htm: 
                head_htm += f'<th title="{title}">{htm}</th>'
            elif ftyp in text.lst_output_csv_excel:
                head_csv += f'CLI {option} {entity}{cfg.csv_sep}'

        # Add Sort Script
        if ftyp in text.lst_output_htm:
            col_id = text.strip_all_whitespace(f'{entity}_col_{col_num}'.replace('-','_')).upper()
            script += js_script_fn( col_id, sort_type, sort_dir, row_num, col_num )

    # Close
    if ftyp in text.lst_output_htm: 
        head_htm += '</tr></thead><tbody>'

    # Make JS script
    js  = ' <script> ' 
    js += 'let col_titles = { ' 
    js += script.strip()[:-1]  # Remove comma
    js += ' }; </script> '     # Close JS object and script tag

    return head_htm, head_txt.upper(), head_csv, js

def cells(options, days1, days2='', day='', cnt=-1):
    '''Process all the data cells types'''
    cell_htm, cell_txt, cell_csv, ftyp = '', '', '', options['file-type']
    station = days1.station
    days = days2 if days2 else days1

    for option in options['lst-sel-cells']:  # Check all the available given options
        lst = option.split('_')  # Make lst
        typ, entity = lst[0], lst[1]  # Always two available

        # Info texts
        if typ in text.lst_info:
            if entity in text.lst_copyright:
                cell_txt += text.padding('©', 'center', text.pad_copyright)[:text.pad_copyright]
                if ftyp in text.lst_output_htm:
                    cell_htm += f'<td title="{station.data_notification.lower()}"><small class="text-muted">{icon.copy_light(size="fa-xs")}</small></td>'
                elif ftyp in text.lst_output_csv_excel:
                    cell_csv += '©,'

            elif entity in text.lst_geo_places:
                if entity == 'place':
                    cell_txt += text.padding(station.place, 'left', text.pad_place)[:text.pad_place]
                    if ftyp in text.lst_output_htm: 
                        cell_htm += f'<td class="font-italic text-left">{html.span(station.place, "val")}</td>'
                    elif ftyp in text.lst_output_csv_excel:
                        cell_csv += f'{station.place}{cfg.csv_sep}'

                elif entity == 'province':
                    cell_txt += text.padding(station.province, 'left', text.pad_province)[:text.pad_province]
                    if ftyp in text.lst_output_htm: 
                        cell_htm += f'<td class="font-italic text-left">{html.span(station.province, "val")}</td>'
                    elif ftyp in text.lst_output_csv_excel:
                        cell_csv += f'{station.province}{cfg.csv_sep}'

                elif entity == 'country':
                    cell_txt += text.padding(station.country, 'left', text.pad_country)[:text.pad_country]
                    if ftyp in text.lst_output_htm: 
                        cell_htm += f'<td class="font-italic text-left">{html.span(station.country, "val")}</td>'
                    elif ftyp in text.lst_output_csv_excel:
                        cell_csv += f'{station.country}{cfg.csv_sep}'

            # yyyymmdd - yyyymmdd
            elif entity in text.lst_period_1:
                period_ymd = f'{int(days1.ymd_start)}-{int(days1.ymd_end)}'
                cell_txt += text.padding(period_ymd, 'center', text.pad_period_1)[:text.pad_period_1]
                if ftyp in text.lst_output_htm:
                    period_txt = f'{ymd.text(days1.ymd_start)} - {ymd.text(days1.ymd_end)}'
                    cell_htm += f'<td title="{period_txt}">{html.span(period_ymd, "val")}</td>'
                elif ftyp in text.lst_output_csv_excel:
                    cell_csv += f'{period_ymd}{cfg.csv_sep}'

            # yyyymmdd or mmdd or yyyymmdd-yyyymmdd
            elif entity in text.lst_period_2:
                per2 = days2.period.replace('*', '')
                
                cell_txt += text.padding(per2, 'center', text.pad_period_2)[:text.pad_period_2]
                if ftyp in text.lst_output_htm:
                    cell_htm += f'<td>{html.span(per2, "val")}</td>'
                elif ftyp in text.lst_output_csv_excel:
                    cell_csv += f'{per2}{cfg.csv_sep}'

            # Counter for rows
            elif entity in text.lst_num:
                cell_txt += text.padding(cnt, 'center', text.pad_num)[:text.pad_num]
                cnt = utils.l0(cnt, 3)
                if ftyp in text.lst_output_htm:
                    cell_htm += f'<td title="num of day">{html.span(cnt, "val")}</td>'
                elif ftyp in text.lst_output_csv_excel:
                    cell_csv += f'{cnt}{cfg.csv_sep}'

            # Day
            elif entity in text.lst_day:
                yymmdd = convert.fl_to_s(day[daydata.etk('yyyymmdd')])
                
                cell_txt += text.padding(ymd, 'center', text.pad_day)[:text.pad_day]
                if ftyp in text.lst_output_htm:
                    cell_htm += f'<td title="{ymd.text(yymmdd)}">{html.span(int(yymmdd), "val")}</td>'
                elif ftyp in text.lst_output_csv_excel:
                    cell_csv += f'{yymmdd}{cfg.csv_sep}'

            # A day in a month
            elif entity in text.lst_yyyymmdd:
                cell_txt += text.padding(entity, 'center', text.pad_day)[:text.pad_day]
                if ftyp in text.lst_output_htm:
                    cell_htm += f'<td title="">{html.span(entity, "val")}</td>'
                elif ftyp in text.lst_output_csv_excel:
                    cell_csv += f'{entity}{cfg.csv_sep}'

            # Month num/name TODO
            elif entity in text.lst_month:
                cell_txt += text.padding(entity, 'center', text.pad_month)[:text.pad_month]
                if ftyp in text.lst_output_htm:
                    cell_htm += f'<td>{html.span(entity, "val")}</td>'
                elif ftyp in text.lst_output_csv_excel:
                    cell_csv += f'{entity}{cfg.csv_sep}'

        # if not days1.np_period_2d_has_days():
        #     cell_txt += cfg.txt_no_data
        #     cell_htm += f'<td>{cfg.txt_no_data}</t>'
        #     continue

        # Fixed day values
        elif typ in text.lst_day:
            val = text.fix_ent(day[daydata.etk(entity)], entity)
            cell_txt += text.padding(val, 'center', text.pad_day)[:text.pad_day]
            if ftyp in text.lst_output_htm:
                cell_htm += f'<td>{html.span(val, "val")}</td>'
            elif ftyp in text.lst_output_csv_excel:
                cell_csv += f'{val}{cfg.csv_sep}'

        # Max extreme
        elif typ in text.lst_max:
            max_txt = cfg.empthy  
            max_raw, max_day, days_max_2d = days.max(entity)
            if max_day != cfg.np_no_data:
                max_txt = f'{text.fix_ent(max_raw, entity)} {convert.fl_to_s(max_day[daydata.etk("yyyymmdd")])}'

            cell_txt += text.padding(max_txt, 'center', text.pad_max)[:text.pad_max]

            if ftyp in text.lst_output_htm:
                value = html.extreme_values(max_day, entity)
                table = html.table_days(days_max_2d, entity)
                cell_htm += f'<td>{value}{table}</td>'
            elif ftyp in text.lst_output_csv_excel:
                 cell_csv += f'{max_txt}{cfg.csv_sep}'

        # Min extreme
        elif typ in text.lst_min:
            min_txt = cfg.empthy
            min_raw, min_day, days_min_2d = days.min(entity)
            if min_raw != cfg.np_no_data:
                min_txt  = f'{text.fix_ent(min_raw, entity)} '
                min_txt += f'{convert.fl_to_s(min_day[daydata.etk("yyyymmdd")])}'
            
            cell_txt += text.padding(min_txt, 'center', text.pad_min)[:text.pad_min]
 
            if ftyp in text.lst_output_htm:
                value = html.extreme_values(min_day, entity)
                table = html.table_days(days_min_2d, entity)
                cell_htm += f'<td>{value}{table}</td>'
            elif ftyp in text.lst_output_csv_excel:
                cell_csv += f'{min_txt}{cfg.csv_sep}'

        # Average
        elif typ in text.lst_ave:
            ave_raw, days_ave_2d = days.average(entity)
            ave_val = text.fix_ent(ave_raw, entity)

            cell_txt += text.padding(ave_val, 'center', text.pad_ave)[:text.pad_ave]
            if ftyp in text.lst_output_htm:
                value = html.span(ave_val, 'val')
                table = html.table_average(days_ave_2d, entity, reverse=True)
                cell_htm += f'<td>{value}{table}</td>'
            elif ftyp in text.lst_output_csv_excel:
                cell_csv += f'{ave_val}{cfg.csv_sep}'

        # Sum
        elif typ in text.lst_sum:
            sum_raw, days_sum_2d = days.sum(entity)
            sum_val = text.fix_ent(sum_raw, entity)

            cell_txt += text.padding(sum_val, 'center', text.pad_sum)[:text.pad_sum]
            if ftyp in text.lst_output_htm:
                value = html.span(sum_val, 'val')
                table = html.table_sum(days_sum_2d, entity)
                cell_htm += f'<td>{value}{table}</td>'
            elif ftyp in text.lst_output_csv_excel:
                cell_csv += f'{sum_val}{cfg.csv_sep}'

        # Indexes
        elif typ in text.lst_ndx:
            if entity in text.lst_heat_ndx:
                heat_ndx_raw, days_heat_2d = days.heat_ndx()
                heat_ndx_val = text.fix_ent(heat_ndx_raw, entity)

                cell_txt += text.padding(heat_ndx_val, 'center', text.pad_heat_ndx)[:text.pad_heat_ndx]
                if ftyp in text.lst_output_htm:
                    value = html.span(heat_ndx_val, 'val')
                    table = html.table_heat_ndx(days_heat_2d)
                    cell_htm += f'<td>{value}{table}</td>'
                elif ftyp in text.lst_output_csv_excel:
                    cell_csv += f'{heat_ndx_val}{cfg.csv_sep}'

            elif entity in text.lst_helmmann:
                hellmann_raw, days_hmann_2d = days.hellmann()
                hellmann_val = text.fix_ent(hellmann_raw, entity)

                cell_txt += text.padding(hellmann_val, 'center', text.pad_hmann)[:text.pad_hmann]
                if ftyp in text.lst_output_htm:
                    value = html.span(hellmann_val, 'val')
                    table = html.table_hellmann(days_hmann_2d)
                    cell_htm += f'<td>{value}{table}</td>'
                elif ftyp in text.lst_output_csv_excel:
                    cell_csv += f'{hellmann_val}{cfg.csv_sep}'

            elif entity in text.lst_ijnsen:
                ijnsen_raw, days_ijnsen_2d = days.ijnsen()
                ijnsen_val = text.fix_ent(ijnsen_raw, entity)

                cell_txt += text.padding(ijnsen_val, 'center', text.pad_ijns)[:text.pad_ijns]
                if ftyp in text.lst_output_htm:
                    value = html.span(ijnsen_val, 'val')
                    table = html.table_ijnsen(days_ijnsen_2d)
                    cell_htm += f'<td>{value}{table}</td>'
                elif ftyp in text.lst_output_csv_excel:
                    cell_csv += f'{ijnsen_val}{cfg.csv_sep}'

            elif entity in text.lst_frost_sum:
                fsum_raw, days_fsum_2d = days.frost_sum()
                fsum_val = text.fix_ent(fsum_raw, entity)

                cell_txt += text.padding(fsum_val, 'center', text.pad_fsum)[:text.pad_default]
                if ftyp in text.lst_output_htm:
                    value = html.span(fsum_val, 'val')
                    table = html.table_frost_sum(days_fsum_2d)
                    cell_htm += f'<td>{value}{table}</td>'
                elif ftyp in text.lst_output_csv_excel:
                    cell_csv += f'{fsum_val}{cfg.csv_sep}'

        # Counters
        elif typ in text.lst_count:
            sign, val = lst[2], lst[3]
            np_terms_2d, days_cnt_2d = days.conditional_2d(entity, sign, val)  # Get days
            cnt = 0
            if np_terms_2d != cfg.np_no_data: # This hack must not
                cnt = text.fix_ent(np.size(np_terms_2d, axis=0), typ) 
            else:
                cell_txt += text.padding(cfg.txt_no_data, 'center', text.pad_cnt)[:text.pad_cnt]
                cell_htm += f'<td>{html.span(cfg.txt_no_data, "val")}</td>'
                continue

            cell_txt += text.padding(cnt, 'center', text.pad_cnt)[:text.pad_cnt]
            if ftyp in text.lst_output_htm:
                value = html.span(cnt, 'val')
                table = html.table_count(days_cnt_2d, entity)
                cell_htm += f'<td>{value}{table}</td>'
            elif ftyp in text.lst_output_csv_excel:
                cell_csv += f'{cnt}{cfg.csv_sep}'

        # Climate calculations
        # TODO / beta
        # calculate month clima values 
        # for the period for every climate year and month
        elif typ in text.lst_clima:
            option = entity
            entity = lst[2]

            # print(typ, option, entity)
            # input()

            # Make clima days object
            raw, _ = days.climate( entity, option ) # Calculate average
            val = text.fix_ent( raw, entity )

            cell_txt += text.padding(val, 'center', text.pad_clima)[:text.pad_clima]
            if ftyp in text.lst_output_htm:
                cell_htm += f'<td>{html.span(val, "val")}</td>'
            elif ftyp in text.lst_output_csv_excel:
                cell_csv += f'{val}{cfg.csv_sep}'

        else:
            cell_txt += text.padding(cfg.txt_no_data, 'center', text.pad_default)[:text.pad_default]
            cell_htm += f'<td>{html.span(cfg.txt_no_data, "val")}</td>' 
            cell_csv += f'{cfg.txt_no_data}{cfg.csv_sep}'

    return cell_htm, cell_txt, cell_csv

def tr_cells(options, days1, days2='', day='', cnt=-1):
    body_htm, body_txt, body_csv = '', '', ''
    htm, txt, csv = cells(options, days1, days2, day, cnt=cnt)     # Get the cells with data        
    if htm: 
        body_htm += '<tr>'  # Open htm row
        body_htm += htm     # Add to body
        body_htm += '</tr>' # Close htm row
    if txt or csv:
        body_txt += ''      # Open txt row
        body_txt += txt     # Add to body
        body_txt += '\n'    # Close txt row
    if csv:
        body_csv += ''      # Open txt row
        body_csv += csv     # Add to body
        body_csv += '\n'    # Close txt row
    
    return body_htm, body_txt, body_csv

def info_line(txt, options, station):
    t  = f'[{ymd.now()}] {txt} <{options["title"]}> '
    t += f'for {station.wmo} {station.place} '
    t += f'in period <{options["period"]}> '
    t += f'with sub-period <{options["period-2"]}>' if options['period-2'] else ''
    cnsl.log(t, True)

def subject_map( title, map ):
    # TODO
    pass

def body(options):
    '''Makes the body'''
    body_htm, body_txt, body_csv, cnt = '', '', '', 0

    # Walkthrough stations and calculate statistics and add to table
    for station in options['lst-stations']:
        info_line('Start', options, station)

        ok, np_data_2d = daydata.read(station, verbose=False)  # Read data stations
        if not ok: 
            continue 

        # Get days from a station for the given period
        days1, days2 = stats.Days( station, np_data_2d, options['period'] ), ''
    
        # Compare periods
        if options['period-cmp']: # More periods to calculate
            typ, val = options['period-cmp'][0], options['period-cmp'][1]
            lst_yyyy = [ str(yymmdd)[:4] for yymmdd in range( int(days1.ymd_start), int(days1.ymd_end), 10000 ) ]
            
            # Add period-2 to list cell to show in table, if not there yet
            if utils.key_from_lst(options['lst-sel-cells'], 'inf_period-2') == -1:
                lst = options['lst-sel-cells']
                key = utils.key_from_lst( options['lst-sel-cells'], 'inf_period' ) # Get key value
                key = 0 if key == -1 else key + 1 # input(key)
                lst_2 = lst[:key] # Add period-2 to lst to show in table
                lst_2.append('inf_period-2')
                options['lst-sel-cells'] = lst_2 + lst[key:] 
                # Now remove period 1 from lst
                if 'inf_period' in options['lst-sel-cells']:
                    options['lst-sel-cells'].remove('inf_period')

            for yyyy in lst_yyyy[::-1]: # Reverse lst
                if   typ in text.lst_year:  options['period-2'] = f'{yyyy}****'
                elif typ in text.lst_month: options['period-2'] = f'{yyyy}{val}**'
                elif typ in text.lst_day:   options['period-2'] = f'{yyyy}{val}'
                elif typ in text.lst_season:
                    if   val == 'winter': options['period-2'] = f'{int(yyyy)-1}1201-{yyyy}{"0229" if valid.is_leap(yyyy) else "0228"}'
                    elif val == 'spring': options['period-2'] = f'{yyyy}0301-{yyyy}0531'
                    elif val == 'summer': options['period-2'] = f'{yyyy}0601-{yyyy}0831'
                    elif val == 'autumn': options['period-2'] = f'{yyyy}0901-{yyyy}1130'
                elif typ in text.lst_period_1:
                    mmdd1, mmdd2 = val.split('-')
                    if int(mmdd1) <= int(mmdd2): options['period-2'] = f'{yyyy}{mmdd1}-{yyyy}{mmdd2}'
                    else: options['period-2'] = f'{int(yyyy)-1}{mmdd1}-{yyyy}{mmdd2}'

                info_line('Calculate', options, station)
                days2 = stats.Days(station, days1.np_period_2d, options['period-2'])
                if not days2.np_period_2d_has_days(): 
                    continue # Skip whole day/row

                cnt += 1  # Count the days
                htm, txt, csv = tr_cells( options, days1, days2, day='', cnt=cnt ) # Get the cells with data
                body_htm, body_txt, body_csv = body_htm + htm, body_txt + txt, body_csv + csv # Add to body

            info_line('End', options, station)
            continue

        # Search for days table
        if options['s4d-query']:  # Update days
            days = days2 if days2 else days1
            np_2d_search, _ = days.query(options['s4d-query'])
            if not days.np_period_2d_has_days():
                continue  # Skip whole day/row
            else:
                for day in np_2d_search:
                    cnt += 1  # Count the days
                    htm, txt, csv = tr_cells(options, days1, days2, day=day, cnt=cnt) # Get the cells with data
                    body_htm, body_txt, body_csv = body_htm + htm, body_txt + txt, body_csv + csv # Add to body
            info_line('End', options, station)
            continue

        # Period in period
        if options['period-2']:  # Get days2 for calculation of statistics
            days2 = stats.Days(station, days1.np_period_2d, options['period-2'])
            
            # Add period-2 to list cell to show in table, if not there yet
            if utils.key_from_lst(options['lst-sel-cells'], 'inf_period-2') == -1:
                lst = options['lst-sel-cells']
                key = utils.key_from_lst( options['lst-sel-cells'], 'inf_period' ) # Get key value
                key = 0 if key == -1 else key + 1 # input(key)
                lst_2 = lst[:key] # Add period-2 to lst to show in table
                lst_2.append('inf_period-2')
                options['lst-sel-cells'] = lst_2 + lst[key:] 

        # Statistics table
        cnt += 1  # Count the days
        htm, txt, csv = tr_cells(options, days1, days2, day='', cnt=cnt) # Get the tr cells with data
        body_htm, body_txt, body_csv = body_htm + htm, body_txt + txt, body_csv + csv # Add to body
        info_line('End', options, station)

    return body_htm, body_txt, body_csv, options, cnt

def foot(options):
    '''Makes the footer'''
    foot_htm, foot_txt, foot_csv, ftyp = '', '', '', options['file-type']

    if ftyp in text.lst_output_htm:
        foot_htm += f'''
        </tbody><tfoot>
        <tr><td class="text-muted" colspan="{options['colspan']}">
            {text.now_created_notification()}
            {cfg.knmi_dayvalues_notification.lower()}
        </td></tr>
        </tfoot></table>'''

    if ftyp in text.lst_output_txt_cnsl:
        foot_txt += cfg.knmi_dayvalues_notification

    return foot_htm, foot_txt, foot_csv

def output(htm, txt, csv, options):
    '''Make output to screen or file(s)'''
    ok, path, ftyp = True, '', options['file-type'] 
    # input(ftyp)

    if ftyp in text.lst_output_cnsl or cfg.console:  # For console
        cnsl.log(f'\n{txt}\n', True)  # Add 1 spacer/enter around console output

    if ftyp in text.lst_output_files:
        fname = options['file-name'] + text.file_extension(ftyp)  # File name
        data, map = '.', cfg.dir_data # Data and dir
        if   ftyp in text.lst_output_txt:   data, map = txt, cfg.dir_stats_txt
        elif ftyp in text.lst_output_htm:   data, map = htm, cfg.dir_stats_htm
        elif ftyp in text.lst_output_csv:   data, map = csv, cfg.dir_stats_csv
        elif ftyp in text.lst_output_excel: data, map = csv, cfg.dir_stats_excel

        path, map, _ = utils.mk_path_with_dates(map, fname) # Update dir with date maps
        fio.mk_dir( map, verbose=False ) # Make dir if not there yet 

        if ftyp in text.lst_output_htm: # Create html file
            page = html.Template()
            page.template = cfg.html_template_statistics
            page.verbose = False
            page.path  = path
            page.title = options['title']
            page.add_description(f'{options["title"]} {", ".join(options["lst-sel-cells"])}')
            page.main = data
            ok = page.save()  # Save page
            if not ok: 
                cnsl.log( f'Save {ftyp} file failed!', cfg.error )

        elif ftyp in text.lst_output_txt + text.lst_output_csv: # text, csv
            ok = fio.save( path, data, verbose=True )  # Schrijf naar bestand

        elif ftyp in text.lst_output_excel: # Convert csv to excel 
            csv_data = pd.read_table(data, sep=cfg.csv_sep ) # Read the csv data with panda
            csv_data.to_excel(path, index = None, header=True) # Write excel file

    return ok, path
