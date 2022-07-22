# -*- coding: utf-8 -*-
'''Library contains classes and functions for calculating summerstatistics'''
import numpy as np
from pyparsing import col
import common.model.util as util
import common.model.ymd as ymd
import common.view.console as cnsl
import common.control.fio as fio
import sources.view.text as text
import sources.view.icon as icon
import sources.view.html as html
import sources.model.stats as stats
import sources.model.daydata as daydata
import sources.model.utils as utils
import config as cfg
__author__ = "Mark Zwaving"
__email__ = "markzwaving@gmail.com"
__copyright__ = "Copyright (C) Mark Zwaving. All rights reserved."
__license__ = "GNU Lesser General Public License (LGPL)"
__version__ = "0.1.0"
__maintainer__ = "Mark Zwaving"
__status__ = "Development"


# Options examples what can be shown
# lst_cells = [
#     # Info cells
#     'inf_copyright', 'inf_place', 'inf_province', 'inf_country', 'inf_period', 'inf_month', 'inf_num', 'inf_period-2'
#     # Normal statistics cells
#     'ave_tg',

#     # Extremes
#     'max_tx', 'max_tg', 'max_tn', 'max_t10n', 'min_tx', 'min_tg', 'min_tn', 'min_t10n',
#     'max_rh', 'max_sq', 'max_rhx',
#     'max_px', 'max_pn', 'min_px', 'min_pn',
#     'max_ux', 'max_ug', 'max_un', 'min_ux', 'min_ug', 'min_un',

#     'sum_sq', 'sum_rh',
#     'ndx_hellmann', 'ndx_ijnsen', 'ndx_frost-sum', 'ndx_heat-ndx',
#     'cnt_tx_ge_20', 'cnt_tx_ge_25', 'cnt_tx_ge_30', 'cnt_tx_ge_35', 'cnt_tx_ge_40', 'cnt_tg_ge_18', 'cnt_tg_ge_20', 'cnt_sq_ge_10', 'cnt_rh_ge_10',
#     'cnt_tx_lt_0', 'cnt_tg_lt_0', 'cnt_tn_lt_0', 'cnt_tn_lt_-5', 'cnt_tn_lt_-10', 'cnt_tn_lt_-15', 'cnt_tn_lt_-20',

#     # Search for days cells
#     'day_num', 'day_yyyymmdd',
#     'day_tx', 'day_tg', 'day_tn', 'day_t10n', 'day_sq', 'day_sp', 'day_rh', 'day_rhx',
#     'day_dr', 'day_pg', 'day_px', 'day_pn', 'day_ug', 'day_ux', 'day_un', 'day_ng', 'day_ddvec',
#     'day_fhvec', 'day_fg', 'day_fhx', 'day_fhn', 'day_fxx', 'day_vvx', 'day_vvn', 'day_q'
# ]


def calculate(options, type='normal'):
    '''Function calculates all statistics'''
    cnsl.log(f'[{ymd.now()}] {options["title"].upper()}', True)

    body_htm, body_txt, options, cnt = body(options)
    options['colspan'] = len(options['lst-sel-cells'])
    head_htm, head_txt, script = head(options, cnt)
    foot_htm, foot_txt = foot(options)
    htm = head_htm + body_htm + foot_htm + script
    txt = f'{head_txt}\n{body_txt}\n{foot_txt}'

    # Output to screen or file(s)
    ok, path = output(htm, txt, options)

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
    head_htm, head_txt, script = '', '', ''
    # Sorting script vars
    col_num    = 0     # Start column num is 0 increment at start
    descending = '+'   # Identifier sort direction: large to small
    ascending  = '-'   # Identifier sort direction: small to high
    sort_num   = 'num' # Identifier sort num-based
    sort_txt   = 'txt' # Identifier sort txt-based
    row_num    = 2     # Row tr num for click to sort

    if options['file-type'] in text.typ_htm:
        head_htm += f'''
        <table class="rounded shadow border" id="stats"><thead><tr>
            <th colspan="{options['colspan']}">
                {icon.weather_all()} {options['title']} {icon.wave_square()} 
                {options['period']} {icon.cal_period()}                 
            </th></tr><tr>'''

    if options['file-type'] in text.typ_txt:
        head_txt += '#' * 80 + '\n'

    # Add a script with a Javascript object for sorting with columns
    script = '' 
    for option in options['lst-sel-cells']:
        # Sort options. 
        # Defaults: sort is True, numeric and descending. Add 1 to col_num
        sort, sort_type, sort_dir, col_num = True, sort_num, descending, col_num + 1
        lst = option.split('_') # Make lst
        typ, entity = lst[0], lst[1]
        ico = text.entity_to_icon(entity, size='fa-sm', color='', extra='') # Icon

        # Info texts
        if typ == 'inf':
            if entity in text.lst_copyright:
                if options['file-type'] in text.typ_htm: head_htm += '<th title="copyright data_notification"></th>'
                if options['file-type'] in text.typ_txt: head_txt += 'COPY'
                sort = False # No sort

            elif entity == 'place':
                if options['file-type'] in text.typ_htm: head_htm += f'<th>{ico}place</th>'
                if options['file-type'] in text.typ_txt: head_txt += f'PLACE'
                sort_type = sort_txt # Text sort

            elif entity == 'province':
                if options['file-type'] in text.typ_htm: head_htm += f'<th>{ico}province</th>'
                if options['file-type'] in text.typ_txt: head_txt += f'PROVINCE'
                sort_type = sort_txt # Text sort

            elif entity == 'country':
                if options['file-type'] in text.typ_htm: head_htm += f'<th>{ico}country</th>'
                if options['file-type'] in text.typ_txt: head_txt += f'COUNTRY'
                sort_type = sort_txt # Text sort

            elif entity in text.lst_period_1:
                if options['file-type'] in text.typ_htm: head_htm += f'<th>{ico}period</th>'
                if options['file-type'] in text.typ_txt: head_txt += f'PERIOD'

            elif entity in text.lst_period_2:
                if options['file-type'] in text.typ_htm: head_htm += f'<th>{ico}period2</th>'
                if options['file-type'] in text.typ_txt: head_txt += f'PERIOD2'

            elif entity in text.lst_num:
                if options['file-type'] in text.typ_htm: head_htm += f'<th>{ico}num</th>'
                if options['file-type'] in text.typ_txt: head_txt += f'NUM'

            elif entity in text.lst_month:
                if options['file-type'] in text.typ_htm: head_htm += f'<th>{ico}month</th>'
                if options['file-type'] in text.typ_txt: head_txt += f'MONTH'

            elif entity in text.lst_day:
                if options['file-type'] in text.typ_htm: head_htm += f'<th>{ico}day</th>'
                if options['file-type'] in text.typ_txt: head_txt += f'DAY'
                
        # Fixed day values
        elif typ == 'day':
            if options['file-type'] in text.typ_htm: head_htm += f'<th title="{html.attr_title(entity)}">{ico}{entity}</th>'
            if options['file-type'] in text.typ_txt: head_txt += f'{entity}'

        # Max extreme
        if typ in text.lst_max:
            ico2 = text.entity_to_icon(typ, size='fa-sm', color='', extra='') # Icon2
            if options['file-type'] in text.typ_htm: head_htm += f'<th title="{html.attr_title(entity)}">{ico}{entity}{ico2}</th>'
            if options['file-type'] in text.typ_txt: head_txt += f'{entity} {entity}'

        # Min extreme
        elif typ in text.lst_min:
            ico2 = text.entity_to_icon(typ, size='fa-sm', color='', extra='') # Icon2
            if options['file-type'] in text.typ_htm: head_htm += f'<th title="{html.attr_title(entity)}">{ico}{entity}{ico2}</th>'
            if options['file-type'] in text.typ_txt: head_txt += f'{entity} {entity}'

        # Average
        elif typ in text.lst_ave:
            if options['file-type'] in text.typ_htm: head_htm += f'<th title="{html.attr_title(entity)}">{html.title_mean(entity)}</th>'
            if options['file-type'] in text.typ_txt: head_txt += f'{typ} {entity}'

        # Sum
        elif typ in text.lst_sum:
            if options['file-type'] in text.typ_htm: head_htm += f'<th title="{html.attr_title(entity)}">Σ{entity}</th>'
            if options['file-type'] in text.typ_txt: head_txt += f'Σ{entity}'

        # Indexes
        elif typ == 'ndx':
            if entity in text.lst_helmmann:
                if options['file-type'] in text.typ_htm: head_htm += f'<th title="{text.hellmann()}">{ico}hmann</th>'
                if options['file-type'] in text.typ_txt: head_txt += 'HMANN'

            elif entity in text.lst_ijnsen:
                if options['file-type'] in text.typ_htm: head_htm += f'<th title="{text.ijnsen()}">{ico}ijnsen</th>'
                if options['file-type'] in text.typ_txt: head_txt += 'IJNS'

            elif entity in text.lst_frost_sum:
                if options['file-type'] in text.typ_htm: head_htm += f'<th title="{text.frostsum()}">{ico}fsum</th>'
                if options['file-type'] in text.typ_txt: head_txt += 'FSUM'

            elif entity in text.lst_heat_ndx:
                if options['file-type'] in text.typ_htm: head_htm += f'<th title="{text.heat_ndx()}">{ico}heat</th>'
                if options['file-type'] in text.typ_txt: head_txt += 'HEAT'

        # Counters
        elif typ in text.lst_count:
            sign, val = lst[2], lst[3]
            ico = text.entity_to_icon(sign, size="fa-xs") # Update icon
            if options['file-type'] in text.typ_htm: head_htm += f'<th title="{text.title(entity,sign,val)}">{entity}{ico}{val}</th>'
            if options['file-type'] in text.typ_txt:  head_txt += f'{entity}{sign}{val}'

        # Add Sort Script
        if sort:
            col_id = f'{entity}_col_{col_num}'.replace('-','').upper()
            script += js_script_fn( col_id, sort_type, sort_dir, row_num, col_num )

    # Close
    if options['file-type'] in text.typ_htm: head_htm += '</tr></thead><tbody>'
    if options['file-type'] in text.typ_txt: head_txt += '\n'

    # Make JS script
    js  = ' <script> ' 
    js += 'let col_titles = { ' 
    js += script.strip()[:-1] # Remove comma
    js += ' }; </script> '     # Close JS object and script tag

    return head_htm, head_txt, js


def cells(options, days1, days2='', day='', cnt=-1):
    '''Process all the data cells types'''
    cell_htm, cell_txt = '', ''
    station = days1.station
    days = days2 if days2 else days1

    for option in options['lst-sel-cells']:  # Check all the available given options
        lst = option.split('_')  # Make lst
        typ, entity = lst[0], lst[1]  # Always two available

        # Info texts
        if typ == 'inf':
            if entity in text.lst_copyright:
                if options['file-type'] in text.typ_htm:
                    cell_htm += f'<td title="{station.data_notification.lower()}"><small class="text-muted">{icon.copy_light(size="fa-xs")}</small></td>'
                if options['file-type'] in text.typ_txt:
                    cell_txt += station.format

            elif entity == 'place':
                if options['file-type'] in text.typ_htm:
                    cell_htm += f'<td class="font-italic text-left"><span class="val">{station.place}</span></td>'
                if options['file-type'] in text.typ_txt:
                    cell_txt += station.place

            elif entity == 'province':
                if options['file-type'] in text.typ_htm:
                    cell_htm += f'<td class="font-italic text-left"><span class="val">{station.province}</span></td>'
                if options['file-type'] in text.typ_txt:
                    cell_txt += station.province

            elif entity == 'country':
                if options['file-type'] in text.typ_htm:
                    cell_htm += f'<td class="font-italic text-left"><span class="val">{station.country}</span></td>'
                if options['file-type'] in text.typ_txt:
                    cell_txt += station.country

            # yyyymmdd - yyyymmdd
            elif entity in text.lst_period_1:
                if options['file-type'] in text.typ_htm:
                    period_ymd = f'{int(days1.ymd_start)}-{int(days1.ymd_end)}'
                    period_txt = f'{ymd.text(days1.ymd_start)} - {ymd.text(days1.ymd_end)}'
                    cell_htm += f'<td title="{period_txt}"><span class="val">{period_ymd}</span></td>'
                if options['file-type'] in text.typ_txt:
                    cell_txt += days.period

            # yyyymmdd or mmdd or yyyymmdd-yyyymmdd
            elif entity in text.lst_period_2:
                per2 = days2.period.replace('*', '')
                if options['file-type'] in text.typ_htm:
                    cell_htm += f'<td><span class="val">{per2}</span></td>'
                if options['file-type'] in text.typ_txt:
                    cell_txt += per2

            # Counter for rows
            elif entity in text.lst_num:
                cnt = util.l0(cnt, 3)
                if options['file-type'] in text.typ_htm:
                    cell_htm += f'<td title="num of day">{cnt}</td>'
                if options['file-type'] in text.typ_txt:
                    cell_txt += cnt  # TODO
            # Day
            elif entity in text.lst_day:
                ymd1 = day[daydata.etk('yyyymmdd')]
                if options['file-type'] in text.typ_htm:
                    cell_htm += f'<td title="{ymd.text(ymd1)}">{int(ymd1)}</td>'
                if options['file-type'] in text.typ_txt:
                    cell_txt += ymd

            # A day in a month
            elif entity in text.lst_yyyymmdd:
                if options['file-type'] in text.typ_htm:
                    cell_htm += f'<td title="">{entity}</td>'
                if options['file-type'] in text.typ_txt:
                    cell_txt += entity  # TODO

            # Month num/name TODO
            elif entity in text.lst_month:
                if options['file-type'] in text.typ_htm:
                    head_htm += f'<td>month</tdh>'
                if options['file-type'] in text.typ_txt:
                    head_txt += f'{entity}'

        # if not days1.np_period_2d_has_days():
        #     cell_txt += cfg.txt_no_data
        #     cell_htm += f'<td>{cfg.txt_no_data}</t>'
        #     continue

        # Fixed day values
        elif typ in text.lst_day:
            val = text.fix_entity(day[daydata.etk(entity)], entity)
            if options['file-type'] in text.typ_htm:
                cell_htm += f'<td>{val}</td>'
            if options['file-type'] in text.typ_txt:
                cell_txt += val  # TODO

        # Max extreme
        elif typ in text.lst_max:
            max_raw, max_day, days_max_2d = days.max(entity)
            if options['file-type'] in text.typ_htm:
                htm_val = html.extreme_values(max_day, entity)
                table = html.table_days(days_max_2d, entity)
                cell_htm += f'<td>{htm_val}{table}</td>'
            if options['file-type'] in text.typ_txt:
                cell_txt += text.fix_entity(max_raw, entity)

        # Min extreme
        elif typ in text.lst_min:
            min_raw, min_day, days_min_2d = days.min(entity)
            if options['file-type'] in text.typ_htm:
                htm_val = html.extreme_values(min_day, entity)
                table = html.table_days(days_min_2d, entity)
                cell_htm += f'<td>{htm_val}{table}</td>'
            if options['file-type'] in text.typ_txt:
                cell_txt += text.fix_entity(min_raw, entity)

        # Average
        elif typ in text.lst_ave:
            ave_raw, days_ave_2d = days.average(entity)
            ave_val = text.fix_entity(ave_raw, entity)
            if options['file-type'] in text.typ_htm:
                value = html.span(ave_val, 'val')
                table = html.table_average(days_ave_2d, entity, reverse=True)
                cell_htm += f'<td>{value}{table}</td>'
            if options['file-type'] in text.typ_txt:
                cell_txt += ave_val

        # Sum
        elif typ in text.lst_sum:
            sum_raw, days_sum_2d = days.sum(entity)
            sum_val = text.fix_entity(sum_raw, entity)
            if options['file-type'] in text.typ_htm:
                value = html.span(sum_val, 'val')
                table = html.table_sum(days_sum_2d, entity)
                cell_htm += f'<td>{value}{table}</td>'
            if options['file-type'] in text.typ_txt:
                cell_txt += sum_val

        # Indexes
        elif typ == 'ndx':
            if entity in text.lst_heat_ndx:
                heat_ndx_raw, days_heat_2d = days.heat_ndx()
                heat_ndx_val = text.fix_entity(heat_ndx_raw, entity)
                if options['file-type'] in text.typ_htm:
                    value = html.span(heat_ndx_val, 'val')
                    table = html.table_heat_ndx(days_heat_2d)
                    cell_htm += f'<td>{value}{table}</td>'
                if options['file-type'] in text.typ_txt:
                    cell_txt += heat_ndx_val

            elif entity in text.lst_helmmann:
                hellmann_raw, days_hmann_2d = days.hellmann()
                hellmann_val = text.fix_entity(hellmann_raw, entity)
                if options['file-type'] in text.typ_htm:
                    value = html.span(hellmann_val, 'val')
                    table = html.table_hellmann(days_hmann_2d)
                    cell_htm += f'<td>{value}{table}</td>'
                if options['file-type'] in text.typ_txt:
                    cell_txt += hellmann_val

            elif entity in text.lst_ijnsen:
                ijnsen_raw, days_ijnsen_2d = days.ijnsen()
                ijnsen_val = text.fix_entity(ijnsen_raw, entity)
                if options['file-type'] in text.typ_htm:
                    value = html.span(ijnsen_val, 'val')
                    table = html.table_ijnsen(days_ijnsen_2d)
                    cell_htm += f'<td>{value}{table}</td>'
                if options['file-type'] in text.typ_txt:
                    cell_txt += ijnsen_val

            elif entity in text.lst_frost_sum:
                fsum_raw, days_fsum_2d = days.frost_sum()
                fsum_val = text.fix_entity(fsum_raw, entity)
                if options['file-type'] in text.typ_htm:
                    value = html.span(fsum_val, 'val')
                    table = html.table_frost_sum(days_fsum_2d)
                    cell_htm += f'<td>{value}{table}</td>'
                if options['file-type'] in text.typ_txt:
                    cell_txt += fsum_val

        # Counters
        elif typ in text.lst_count:
            sign, val = lst[2], lst[3]

            np_terms_2d, days_cnt_2d = days.conditional_2d(entity, sign, val)  # Get days
            cnt = 0
            if np_terms_2d != cfg.np_no_data: # This hack must not
                cnt = text.fix_entity(np.size(np_terms_2d, axis=0), typ) 
            else:
                cell_txt += cfg.txt_no_data
                cell_htm += f'<td>{cfg.txt_no_data}</td>'
                continue


            if options['file-type'] in text.typ_htm:
                value = html.span(cnt, 'val')
                table = html.table_count(days_cnt_2d, entity)
                cell_htm += f'<td>{value}{table}</td>'
            if options['file-type'] in text.typ_txt:
                cell_txt += cnt

        else:
            cell_txt += cfg.txt_no_data
            cell_htm += f'<td>{cfg.txt_no_data}</td>'

    return cell_htm, cell_txt

def tr_cells(options, days1, days2='', day='', cnt=-1):
    body_htm, body_txt = '', '' 
    htm, txt = cells(options, days1, days2, day, cnt=cnt)     # Get the cells with data        
    if htm: 
        body_htm += '<tr>'  # Open htm row
        body_htm += htm     # Add to body
        body_htm += '</tr>' # Close htm row
    if txt:
        body_txt += ''      # Open txt row
        body_txt += txt     # Add to body
        body_txt += '\n'    # Close txt row
 
    return body_htm, body_txt 

def info_line(txt, options, station):
    t  = f'[{ymd.now()}] {txt} <{options["title"]}> '
    t += f'for {station.wmo} {station.place} '
    t += f'in period <{options["period"]}> '
    t += f'with sub-period <{options["period-2"]}>' if options['period-2'] else ''
    cnsl.log(t, True)

def body(options):
    '''Makes the body'''
    body_htm, body_txt, cnt = '', '', 0

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
            lst_yyyy = [ str(y)[:4] for y in range( int(days1.ymd_start), int(days1.ymd_end) + 1, 10000 ) ]
            
            # Add period-2 to list cell to show in table, if not there yet
            if util.key_from_lst(options['lst-sel-cells'], 'inf_period-2') == -1:
                lst = options['lst-sel-cells']
                key = util.key_from_lst( options['lst-sel-cells'], 'inf_period' ) # Get key value
                key = 0 if key == -1 else key + 1 # input(key)
                lst_2 = lst[:key] # Add period-2 to lst to show in table
                lst_2.append('inf_period-2')
                options['lst-sel-cells'] = lst_2 + lst[key:] 
                # Now remove period 1 from lst
                if 'inf_period' in options['lst-sel-cells']:
                    options['lst-sel-cells'].remove('inf_period')

            for yyyy in lst_yyyy[::-1]: # Reverse lst
                if   typ in text.lst_year:  
                    options['period-2'] = f'{yyyy}**'
                elif typ in text.lst_month: 
                    options['period-2'] = f'{yyyy}{val}**'
                elif typ in text.lst_day:   
                    options['period-2'] = f'{yyyy}{val}'
                elif typ in text.lst_season:
                    if val == 'winter':
                        sp, ep = '1201', '0229' if util.is_leap(yyyy) else '0228'
                        options['period-2'] = f'{int(yyyy)-1}{sp}-{yyyy}{ep}'
                    elif val == 'spring': 
                        options['period-2'] = f'{yyyy}0301-{yyyy}0531'
                    elif val == 'summer': 
                        options['period-2'] = f'{yyyy}0601-{yyyy}0831'
                    elif val == 'autumn': 
                        options['period-2'] = f'{yyyy}0901-{yyyy}1130'
                elif typ in text.lst_period_1:
                    mmdd1, mmdd2 = val.split('-')
                    if int(mmdd1) <= int(mmdd2):
                        options['period-2'] = f'{yyyy}{mmdd1}-{yyyy}{mmdd2}'
                    else:
                        options['period-2'] = f'{int(yyyy)-1}{mmdd1}-{yyyy}{mmdd2}'

                days2 = stats.Days(station, days1.np_period_2d, options['period-2'])
                if not days2.np_period_2d_has_days(): continue  # Skip whole day/row

                info_line('Calculate statistics to compare', options, station)

                cnt += 1  # Count the days
                htm, txt = tr_cells(options, days1, days2, day='', cnt=cnt) # Get the cells with data
                body_htm, body_txt = body_htm + htm, body_txt + txt # Add to body

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
                    htm, txt = tr_cells(options, days1, days2, day=day, cnt=cnt) # Get the cells with data
                    body_htm, body_txt = body_htm + htm, body_txt + txt # Add to body
            info_line('End', options, station)
            continue

        # Period in period
        if options['period-2']:  # Get days2 for calculation of statistics
            days2 = stats.Days(station, days1.np_period_2d, options['period-2'])
            
            # Add period-2 to list cell to show in table, if not there yet
            if util.key_from_lst(options['lst-sel-cells'], 'inf_period-2') == -1:
                lst = options['lst-sel-cells']
                key = util.key_from_lst(options['lst-sel-cells'], 'inf_period') # Get key value
                key = 0 if key == -1 else key + 1 # input(key)
                lst_2 = lst[:key] # Add period-2 to lst to show in table
                lst_2.append('inf_period-2')
                options['lst-sel-cells'] = lst_2 + lst[key:] 

        # Statistics table
        cnt += 1  # Count the days
        htm, txt = tr_cells(options, days1, days2, day='', cnt=cnt) # Get the tr cells with data
        body_htm, body_txt = body_htm + htm, body_txt + txt # Add to body
        info_line('End', options, station)

    return body_htm, body_txt, options, cnt


def foot(options):
    '''Makes the footer'''
    foot_htm, foot_txt = '', ''

    if options['file-type'] in text.typ_htm:
        foot_htm += f'''
        </tbody><tfoot>
        <tr><td class="text-muted" colspan="{options['colspan']}">
            {utils.now_created_notification()}
            {cfg.knmi_dayvalues_notification.lower()}
        </td></tr>
        </tfoot></table>'''

    if options['file-type'] in text.typ_txt:
        foot_txt += '\n{cfg.knmi_dayvalues_notification}'

    return foot_htm, foot_txt


def output(htm, txt, options):
    '''Make output to screen or file(s)'''
    ok = True

    if options['file-type'] in text.typ_htm:
        fname = f'{options["file-name"]}.{options["file-type"]}'
        path, dir, _ = utils.mk_path_with_dates(cfg.dir_stats_htm, fname)
        fio.mk_dir(dir, verbose=False)

        page = html.Template()
        page.template = fio.mk_path( cfg.dir_stats_templates, 'template.html' )
        page.verbose = False
        page.path  = path
        page.title = options['title']
        page.add_description(f'{options["title"]} {", ".join(options["lst-sel-cells"])}' )
        page.main = htm
        ok = page.save()
        if not ok:
            cnsl.log('Failed!', cfg.error)

    if options['file-type'] in text.typ_txt:
        cnsl.log(txt, True)

    if options['file-type'] in text.typ_txt:  # Save to htm/txt file
        path, dir, _ = utils.mk_path_with_dates(cfg.dir_stats_txt, f'{options["file-name"]}.{options["file-type"]}')
        fio.mk_dir(dir, verbose=False)

        ok = fio.save(path, txt, verbose=False)  # Schrijf naar bestand

    return ok, path
