# -*- coding: utf-8 -*-
'''Library contains functions for building html popup table'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.0.5'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg 
import numpy as np
import sources.model.ymd as ymd
import sources.model.dayvalues.data as data
import sources.model.statistic.mean as mean
import sources.model.statistic.indexes.heat as heat 
import sources.model.statistic.indexes.hellmann as hellmann
import sources.model.statistic.indexes.ijnsen as ijnsen 
import sources.model.statistic.indexes.frostsum as frostsum 
import sources.model.statistic.sum as static_sum
import sources.model.statistic.sort_days as sort_days
import sources.model.statistic.cnt_days as cnt_days
import sources.view.html as html
import sources.view.console as cnsl
import sources.view.text as text

def table( lst_head, lst_body, reverse=False ):
    htm = cfg.e
    if lst_body:
        htm = f'''
        <table class="popup">
        <thead>{ html.tr_th(lst_head) }</thead>
        <tbody>'''

        # Reverse list optional
        if reverse: lst_body = lst_body[::-1]
        for el in lst_body[: cfg.html_popup_table_max_rows]: 
            htm += el
    
        htm += '</tbody></table>'

    return htm

def table_days(np_lst_days, entity, reverse=False):
    html = cfg.e

    if cfg.html_popup_table_show:

        if len(np_lst_days) > 0: # There are days
            t_td, lst_head = cfg.e, ['pos', 'date', entity]
            col_ymd, col_ent = data.column('yyyymmdd'), data.column(entity)

            t_entity = data.entity_to_t_entity(entity)
            if data.is_time_entity(t_entity): # Add time if available
                col_t_ent = data.column(t_entity)
                lst_head.append(t_entity)

            pos, lst_body = 1, []
            for np_day in np_lst_days:
                if np.size(np_day, axis=0) == 0:
                    continue

                try:
                    raw_ymd = np_day[col_ymd]
                    raw_ent = np_day[col_ent]
 
                    if data.is_time_entity(t_entity): # Add time if available
                        raw_t_ent = np_day[col_t_ent]

                except Exception as e:
                    err  = f'Error in tbl_popup table_days()\n{np_lst_days}\n'
                    err += f'Entity {entity}\n{e}'
                    cnsl.log(err, cfg.error)

                else:
                    ymd_txt = ymd.yyyymmdd_to_text(raw_ymd)
                    ymd_val = text.fix_for_entity(raw_ymd, 'date')
                    val_ent = text.fix_for_entity(raw_ent, entity)

                    if data.is_time_entity(t_entity): # Add time if available
                        val_t_ent = text.fix_for_entity(raw_t_ent, t_entity)
                        t_td = f'<td>{val_t_ent}</td>'

                    lst_body.append(f'''
                        <tr>
                            <td>{pos}</td>
                            <td title="{ymd_txt}">{ymd_val}</td>
                            <td>{val_ent}</td>
                            {t_td}
                        </tr>
                    ''')

                pos += 1

            # create html table
            html = table( lst_head, lst_body, reverse )

    return html

def table_extremes(np_lst_days, entity, sort='H-L'):
    # Sort table 
    np_lst_sort = sort_days.calculate(np_lst_days, entity, sort)

    # Make HTML table
    html = table_days(np_lst_sort, entity, reverse=False)

    return html

def table_average(np_lst_days, entity, reverse=False):

    html = cfg.e
    if cfg.html_popup_table_show:
        if len(np_lst_days[:]) > 0:

            # Make lst header titles and time too if there
            t_td, lst_head = cfg.e, ['cnt', 'date', entity, 'ave']
            col_ymd, col_ent = data.column('yyyymmdd'), data.column(entity)

            t_entity = data.entity_to_t_entity(entity)
            if t_entity: # Add time td, if available for entity
                lst_head = ['cnt', 'date', entity, t_entity, 'ave']
                col_t_ent = data.column(t_entity)

            cnt, lst_body = 1, []
            for np_day in np_lst_days:
                if np.size(np_day, axis=0) == 0:
                    continue

                # Calculate values
                try:
                    raw_ymd = np_day[col_ymd]
                    raw_ent = np_day[col_ent]
                    raw_ave, _ = mean.calculate(np_lst_days[:cnt,:], entity)

                    if t_entity: # Add time td, if available
                        raw_t_val = np_lst_days[col_t_ent]

                except Exception as e:
                    err  = f'Error in tbl_popup table_average()\n{np_lst_days}\n'
                    err += f'entity {entity}\n{e}'
                    cnsl.log(err, cfg.error)

                else:
                    txt_ymd = ymd.yyyymmdd_to_text(raw_ymd) 
                    val_ymd = text.fix_for_entity(raw_ymd, 'date') 
                    val_ent = text.fix_for_entity(raw_ent, entity )
                    val_ave = text.fix_for_entity(raw_ave, entity )

                    if t_entity: # Add time td, if available
                        val_t_ent = text.fix_for_entity(raw_t_val, t_entity)
                        t_td = f'<td>{val_t_ent}</td>' 

                    lst_body.append(f'''
                        <tr>
                            <td>{cnt}</td>
                            <td title="{txt_ymd}">{val_ymd}</td>
                            <td>{val_ent}</td>
                            {t_td}
                            <td>{val_ave}</td>
                        </tr>
                    ''')

                cnt += 1

            # Create html table
            html = table( lst_head, lst_body, reverse )

    return html

def table_count(np_lst_days, entity):
    html = cfg.e

    if cfg.html_popup_table_show:
        if len(np_lst_days[:]) > 0:
            # Make lst header titles and time too if there
            t_td, lst_head = cfg.e, ['cnt', 'date', entity]
            col_ymd, col_ent = data.column('yyyymmdd'), data.column(entity)
            
            t_entity = data.entity_to_t_entity(entity)
            if t_entity:
                col_t_ent = data.column(t_entity)
                lst_head.append(t_entity) 
    
            cnt, lst = 1, []
            for np_day in np_lst_days:
                if np.size(np_day, axis=0) == 0:
                    continue

                # Calculate values
                try:
                    raw_ymd = np_day[col_ymd]
                    raw_ent = np_day[col_ent]
                    count = cnt_days.calculate(np_lst_days[:cnt])

                    if t_entity: # Add time td, if available
                       raw_t_ent = np_day[col_t_ent]

                except Exception as e:
                    err  = f'Error in tbl_popup table_count()\n{np_day}\n'
                    err += f'Entity {entity}\n{e}'
                    cnsl.log(err, cfg.error)

                else:
                    txt_ymd = ymd.yyyymmdd_to_text(raw_ymd)
                    val_ymd = text.fix_for_entity(raw_ymd, 'date') 
                    val_ent = text.fix_for_entity(raw_ent, entity)

                    if t_entity: # Add time td, if available
                        val_t_ent = text.fix_for_entity(raw_t_ent, t_entity) 
                        t_td = f'<td>{val_t_ent}</td>'

                    lst.append(f'''
                    <tr>
                        <td>{count}</td>
                        <td title="{txt_ymd}">{val_ymd}</td>
                        <td>{val_ent}</td>
                        {t_td}
                    </tr>
                    ''')

                cnt += 1

            # Create html table
            html = table(lst_head, lst, reverse=True)

    return html

def table_sum(np_lst_days, entity):
    html = cfg.e

    if cfg.html_popup_table_show:
        if len(np_lst_days[:]) > 0:
            # Make lst header titles and time too if there
            t_td, lst_head = cfg.e, ['cnt','date','sum',entity]
            col_ymd, col_ent = data.column('yyyymmdd'), data.column(entity) 

            t_entity = data.entity_to_t_entity(entity)
            if t_entity:
                col_t_ent = data.column(t_entity)
                lst_head.append(t_entity)

            cnt, lst = 1, []
            for np_day in np_lst_days:
                if np.size(np_day, axis=0) == 0:
                    continue

                # Calculate values
                try:
                    raw_ymd = np_day[col_ymd]
                    raw_ent = np_day[col_ent]
                    raw_sum, _ = static_sum.calculate(np_lst_days[:cnt,:], entity)
                    
                    if t_entity: # Add time td
                        raw_t_ent = np_day[col_t_ent]

                except Exception as e:
                    err  = f'Error in tbl_popup table_sum()\n{np_day}\n'
                    err += f'Entity {entity}\n{e}'
                    cnsl.log(err, cfg.error)

                else:
                    txt_ymd = ymd.yyyymmdd_to_text(raw_ymd)
                    val_ymd = text.fix_for_entity(raw_ymd, 'date')
                    val_ent = text.fix_for_entity(raw_ent, entity)
                    val_sum = text.fix_for_entity(raw_sum, entity)

                    if t_entity: # Add time td
                        val_t_ent = text.fix_for_entity(raw_t_ent, t_entity)
                        t_td = f'<td>{val_t_ent}</td>'

                    lst.append(f'''
                    <tr>
                        <td>{ cnt }</td>
                        <td title="{txt_ymd}">{val_ymd}</td>
                        <td>{val_sum}</td>
                        <td>{val_ent}</td>
                        {t_td}
                    </tr>
                    ''')
                cnt += 1

            # create html table
            html = table(lst_head, lst, reverse = True)

    return html

def table_frost_sum(np_lst_days):
    html = cfg.e

    if cfg.html_popup_table_show:
        if len(np_lst_days[:]) > 0:
            cnt, lst = 1, []
            col_ymd = data.column('yyyymmdd')
            col_tx, col_tn,= data.column('tx'), data.column('tn')
            col_txh, col_tnh = data.column('txh'), data.column('tnh')

            for np_day in np_lst_days:
                if np.size(np_day, axis=0) == 0:
                    continue

                # Calculate values 
                try:
                    raw_ymd = np_day[col_ymd]
                    raw_tx, raw_txh = np_day[col_tx], np_day[col_txh]
                    raw_tn, raw_tnh = np_day[col_tn], np_day[col_tnh]
                    raw_frostsum_act, _, _, _, _ ,_ = frostsum.calculate_nl(np.array([np_day]))
                    raw_frostsum_tot, _, _, _, _ ,_ = frostsum.calculate_nl(np_lst_days[:cnt,:])

                except Exception as e:
                    err  = f'Error in tbl_popup table_frost)sum()\n{np_lst_days}\n{0}'
                    cnsl.log(err, cfg.error)

                else:
                    txt_ymd = ymd.yyyymmdd_to_text(raw_ymd)
                    val_ymd = text.fix_for_entity(raw_ymd, 'date')
                    val_tx  = text.fix_for_entity(raw_tx, 'tx')
                    val_txh = text.fix_for_entity(raw_txh, 'txh')
                    val_tn  = text.fix_for_entity(raw_tn, 'tn')
                    val_tnh = text.fix_for_entity(raw_tnh, 'tnh')
                    val_frostsum_act = text.fix_for_entity(raw_frostsum_act, 'frost-sum') 
                    val_frostsum_tot = text.fix_for_entity(raw_frostsum_tot, 'frost-sum')

                    lst.append(f'''
                    <tr>
                        <td>{cnt}</td>
                        <td title="{txt_ymd}">{val_ymd}</td>
                        <td>{val_tx}</td> 
                        <td>{val_txh}</td>
                        <td>{val_tn}</td> 
                        <td>{val_tnh}</td>
                        <td>{val_frostsum_act}</td>
                        <td>{val_frostsum_tot}</td>
                    </tr>
                    ''')

                cnt += 1

            # create html table
            html = table(['cnt','date','tx','txh','tn','tnh','fsum','total'], lst, reverse=True)

    return html

def table_ijnsen(np_lst_days):
    html = cfg.e

    if cfg.html_popup_table_show:
        if len(np_lst_days[:]) > 0:
            cnt, lst = 1, []
            col_ymd = data.column('yyyymmdd')
            col_tx,  col_tn  = data.column('tx'),  data.column('tn')
            col_txh, col_tnh = data.column('txh'), data.column('tnh')

            for np_day in np_lst_days:
                if np.size(np_day, axis=0) == 0:
                    continue

                # Calculate values 
                try:
                    raw_ymd = np_day[col_ymd] 
                    raw_tx, raw_txh = np_day[col_tx], np_day[col_txh] 
                    raw_tn, raw_tnh = np_day[col_tn], np_day[col_tnh] 
                    raw_ijnsen_act, _, _, _, _ = ijnsen.calculate(np.array([np_day])) 
                    raw_ijnsen_sum, _, _, _, _ = ijnsen.calculate(np_lst_days[:cnt,:]) 

                except Exception as e:
                    err  = f'Error in tbl_popup table_ijnsen()\n{np_lst_days}\n{e}'
                    cnsl.log(err, cfg.error)

                else:
                    txt_ymd = ymd.yyyymmdd_to_text(raw_ymd)
                    val_ymd = text.fix_for_entity(raw_ymd, 'date')
                    val_tx  = text.fix_for_entity(raw_tx, 'tx')
                    val_txh = text.fix_for_entity(raw_txh, 'txh')
                    val_tn  = text.fix_for_entity(raw_tn, 'tn')
                    val_tnh = text.fix_for_entity(raw_tnh, 'tnh')
                    val_ijnsen_act = text.fix_for_entity(raw_ijnsen_act, 'ijnsen')
                    val_ijnsen_sum = text.fix_for_entity(raw_ijnsen_sum, 'ijnsen')

                    lst.append(f'''
                    <tr>
                        <td>{cnt}</td>
                        <td title="{txt_ymd}">{val_ymd}</td>
                        <td>{val_tx}</td> 
                        <td>{val_txh}</td>
                        <td>{val_tn}</td> 
                        <td>{val_tnh}</td>
                        <td>{val_ijnsen_act}</td>
                        <td>{val_ijnsen_sum}</td>
                    </tr>
                    ''')

                cnt += 1

            # create html table
            html = table(['cnt','date','tx','txh','tn','tnh','ijnsen','total'], lst, reverse=True)

    return html

def table_hellmann(np_lst_days):
    html = cfg.e

    if cfg.html_popup_table_show:
        if len(np_lst_days[:]) > 0:
            cnt, lst,= 1, []

            for np_day in np_lst_days:
                if np.size(np_day, axis=0) == 0:
                    continue

                # Calculate values
                try:
                    raw_ymd = np_day[data.column('yyyymmdd')]
                    raw_hman_act, _ = hellmann.calculate(np.array([np_day]))
                    raw_hman_sum, _ = hellmann.calculate(np_lst_days[:cnt,:])

                except Exception as e:
                    err  = f'Error in tbl_popup table_hellmann()\n{np_lst_days}\n{e}'
                    cnsl.log(err, cfg.error)

                else:
                    txt_ymd = ymd.yyyymmdd_to_text(raw_ymd)
                    val_ymd = text.fix_for_entity(raw_ymd, 'date')
                    val_hman_act = text.fix_for_entity(raw_hman_act, 'hellmann')
                    val_hman_sum = text.fix_for_entity(raw_hman_sum, 'hellmann')

                    lst.append(f'''
                    <tr>
                        <td>{cnt}</td>
                        <td title="{txt_ymd}">{val_ymd}</td>
                        <td>{val_hman_act}</td>
                        <td>{val_hman_sum}</td>
                    </tr>
                    ''')

                cnt += 1

            # create html table
            html = table(['cnt','date','hmann','total'], lst, reverse=True)

    return html

def table_heat_ndx(np_lst_days):
    html = cfg.e

    if cfg.html_popup_table_show:
        if len(np_lst_days[:]):
            cnt, lst= 1, []

            for np_day in np_lst_days:
                if np.size(np_day, axis=0) == 0:
                    continue

                # Calculate values
                try:
                    raw_ymd = str(int(np_day[data.column('yyyymmdd')]))
                    raw_tg  = np_day[data.column('tg')]
                    raw_heat_act = raw_tg - 180.0
                    raw_heat_sum, _ = heat.calculate_nl(np_lst_days[:cnt,:])

                except Exception as e:
                    err  = f'Error in tbl_popup table_heat_ndx()\n{np_lst_days}\n{e}'
                    cnsl.log(err, cfg.error)

                else:
                    txt_ymd = ymd.yyyymmdd_to_text(raw_ymd)
                    val_ymd = text.fix_for_entity(raw_ymd, 'date')
                    val_tg  = text.fix_for_entity(raw_tg, 'tg')
                    val_heat_act = text.fix_for_entity(raw_heat_act, 'heat-ndx')
                    val_heat_sum = text.fix_for_entity(raw_heat_sum, 'heat-ndx') 

                    lst.append(f'''
                    <tr>
                        <td>{cnt}</td>
                        <td title="{txt_ymd}">{val_ymd}</td>
                        <td>{val_tg}</td>
                        <td>{val_heat_act}</td>
                        <td>{val_heat_sum}</td>
                    </tr>
                    ''')

                cnt += 1

            # create html table
            html = table(['cnt', 'date', 'tg', 'heat', 'sum'], lst, reverse=True)

    return html