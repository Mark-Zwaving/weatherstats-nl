# -*- coding: utf-8 -*-
'''Functions for seaching days with charateristics'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.1.5'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import sources.model.stations as stations
import sources.model.dayvalues.data as data
import sources.model.utils as utils
import sources.model.check as chk
import sources.model.ymd as ymd
import sources.model.dayvalues.s4d_query as s4d_query
import sources.view.html as vhtml
import sources.view.icon as icon
import sources.view.text as text
import sources.control.fio as fio
import sources.view.console as cnsl


def calculate(np_lst_days, options):
    '''Prints all the days found on screen et cetera'''

    # All days for the query given
    ok, np_lst_res = s4d_query.calculate(np_lst_days, options[text.ask_s4d_query]) 



    # Make path if it is a html or txt file
    dir = fio.mk_path(cfg.dir_search4days, type)
    path_to_file = fio.mk_path(dir, f'{fname}.{type}')
    fio.mk_dir(dir)

    if type =='html':
        title = f'Days {query}'

        # Proces data in html table
        colspan = 30
        html  = f'''
        <table id="stats">
            <thead>
                <tr>
                    <th colspan="{colspan}">
                        {icon.weather_all()}
                        {title}
                        {icon.wave_square()}
                        {period}
                        {icon.cal_period()}
                    </th>
                </tr>
                <tr>
                    <th title="copyright data_notification"> </th>
                    <th> place {icon.home(size='fa-sm')}</th>
                    <th> state {icon.flag(size='fa-sm')}</th>
                    <th> periode {icon.cal_period(size='fa-sm')}</th>
                    <th> day {icon.cal_day(size='fa-sm')}</th>
                    <th {text.ent_to_txt("tx")}> TX{icon.temp_full(size='fa-sm')}</th>
                    <th {text.ent_to_txt("tg")}> TG{icon.temp_half(size='fa-sm')}</th>
                    <th {text.ent_to_txt("tn")}>  TN{icon.temp_empty(size='fa-sm')}</th>
                    <th {text.ent_to_txt("t10n")}> T10N{icon.temp_empty(size='fa-sm')}</th>
                    <th {text.ent_to_txt("sq")}> SQ{icon.sun(size='fa-sm')}</th>
                    <th {text.ent_to_txt("sp")}> SP{icon.sun(size='fa-sm')}</th>
                    <th {text.ent_to_txt("rh")}> RH{icon.shower_heavy(size='fa-sm')}</th>
                    <th {text.ent_to_txt("rhx")}> RHX{icon.shower_heavy(size='fa-sm')} </th>
                    <th {text.ent_to_txt("dr")}> DR{icon.shower_heavy(size='fa-sm')}</th>
                    <th {text.ent_to_txt("pg")}> PG{icon.compress_alt(size='fa-sm')}</th>
                    <th {text.ent_to_txt("px")}> PX{icon.compress_alt(size='fa-sm')}</th>
                    <th {text.ent_to_txt("pn")}> PN{icon.compress_alt(size='fa-sm')}</th>
                    <th {text.ent_to_txt("ug")}> UG{icon.drop_tint(size='fa-sm')}</th>
                    <th {text.ent_to_txt("ux")}> UX{icon.drop_tint(size='fa-sm')}</th>
                    <th {text.ent_to_txt("un")}> UN{icon.drop_tint(size='fa-sm')}</th>
                    <th {text.ent_to_txt("ng")}> NG{icon.cloud(size='fa-sm')}</th>
                    <th {text.ent_to_txt("ddvec")}> DDVEC{icon.arrow_loc(size='fa-sm')}</th>
                    <th {text.ent_to_txt("fhvec")}> FHVEC{icon.wind(size='fa-sm')}</th>
                    <th {text.ent_to_txt("fg")}> FG{icon.wind(size='fa-sm')}</th>
                    <th {text.ent_to_txt("fhx")}> FHX{icon.wind(size='fa-sm')}</th>
                    <th {text.ent_to_txt("fhn")}> FHN{icon.wind(size='fa-sm')}</th>
                    <th {text.ent_to_txt("fxx")}> FXX{icon.wind(size='fa-sm')}</th>
                    <th {text.ent_to_txt("vvx")}> VVX{icon.eye(size='fa-sm')}</th>
                    <th {text.ent_to_txt("vvn")}> VVN{icon.eye(size='fa-sm')}</th>
                    <th {text.ent_to_txt("q")}> Q{icon.radiation(size='fa-sm')}</th>
                </tr>
            </thead>
            <tbody>
        '''

        if len(data) > 0:
            for day in data:
                stn, yymmdd, ddvec, fhvec, fg, fhx, fhxh, fhn, fhnh, fxx, \
                fxxh, tg, \
                tn, tnh, tx, txh, t10n, t10nh, sq, sp, q, dr, rh, rhx, \
                rhxh, pg, px, pxh, pn, pnh, vvn, vvnh, vvx, vvxh, ng, ug, \
                ux, uxh, un, unh, ev24 = data.ents( day )

                place = stations.wmo_to_place(stn)
                state = stations.wmo_to_province(stn)
                station = stations.wmo_to_station(stn)
                date = f'{day[data.YYYYMMDD]:.0f}'

                lfg, fg_ms, fg_bft = fg.split(' '), cfg.e, cfg.e
                if len(lfg) == 2: fg_ms, fg_bft = lfg[0], lfg[1]
                else: fg_ms = fg

                lfhvec, fhvec_ms, fhvec_bft = fhvec.split(' '), cfg.e, cfg.e
                if len(lfhvec) == 2: fhvec_ms, fhvec_bft = lfg[0], lfg[1]
                else: fhvec_ms = fhvec

                lddvec, ddvec_deg, ddvec_txt = ddvec.split(' '), cfg.e, cfg.e
                if len(lddvec) == 2: ddvec_deg, ddvec_txt = lddvec[0], lddvec[1]
                else: ddvec_deg = ddvec

                html += f'''
                <tr>
                    <td title="{station.data_notification.lower()}">
                            {icon.copy_light(size='fa-xs')}
                    </td>
                    <td> <span class="val">{place}</span> </td>
                    <td> <span class="val">{state}</span> </td>
                    <td> <span class="val">{period}</span> </td>
                    <td title="{ymd.ymd_to_text(date)}"> <span class="val">{date}</span> </td>
                    <td> <span class="val">{tx}</span> <br> <small>{txh}</small> </td>
                    <td> <span class="val">{tg}</span> </td>
                    <td> <span class="val">{tn}</span> <br> <small>{tnh}</small> </td>
                    <td> <span class="val">{t10n}</span> <br> <small>{t10nh}</small> </td>
                    <td> <span class="val">{sq}</span> </td>
                    <td> <span class="val">{sp}</span> </td>
                    <td> <span class="val">{rh}</span> </td>
                    <td> <span class="val">{rhx}</span> <br> <small>{rhxh}</small> </td>
                    <td> <span class="val">{dr}</span> </td>
                    <td> <span class="val">{pg}</span> </td>
                    <td> <span class="val">{px}</span> <br> <small>{pxh}</small> </td>
                    <td> <span class="val">{pn}</span> <br> <small>{pnh}</small> </td>
                    <td> <span class="val">{ug}</span> </td>
                    <td> <span class="val">{ux}</span> <br> <small>{uxh}</small> </td>
                    <td> <span class="val">{un}</span> <br> <small>{unh}</small> </td>
                    <td> <span class="val">{ng}</span> </td>
                    <td> <span class="val">{ddvec_deg}</span> <br> <small>{ddvec_txt}</small> </td>
                    <td> <span class="val">{fhvec_ms}</span> <br> <small>{fhvec_bft}</small> </td>
                    <td> <span class="val">{fg_ms}</span> <br> <small>{fg_bft}</small> </td>
                    <td> <span class="val">{fhx}</span> <br> <small>{fhxh}</small> </td>
                    <td> <span class="val">{fhn}</span> <br> <small>{fhnh}</small> </td>
                    <td> <span class="val">{fxx}</span> <br> <small>{fxxh}</small> </td>
                    <td> <span class="val">{vvx}</span> <br> <small>{vvxh}</small> </td>
                    <td> <span class="val">{vvn}</span> <br> <small>{vvnh}</small> </td>
                    <td> <span class="val">{q}</span> </td>
                </tr>
                '''
        else:
            html += f'''
                <tr>
                    <td colspan="{colspan}"> {text.t("No days found")} </td>
                </tr>
                '''

        html += f'''
            </tbody>
            <tfoot>
                <tr>
                    <td colspan="{colspan}">{utils.now_created_notification()}</td>
                </tr>
            </tfoot>
        </table>
        '''

        cnsl.log('\nWrite/print results... ', True)

        # Write to html, screen, console
        page       =  vhtml.Template()
        page.title =  title
        page.main  =  html
        page.strip =  True
        page.path_to_root = cfg.path_to_html_root
        page.path_to_thirdparty = cfg.path_to_thirdparty
        page.path_to_file = path_to_file
        # Styling
        page.css_files = [ f'{cfg.path_to_html_root}css/default.css',
                           f'{cfg.path_to_html_root}css/table-statistics.css',
                           f'{cfg.path_to_html_root}css/search4days.css' ]
        # Scripts
        page.script_files = [ f'{cfg.path_to_html_root}js/search4days.js',
                              f'{cfg.path_to_html_root}js/sort-col.js',
                              f'{cfg.path_to_html_root}js/default.js' ]
        page.save()

    elif type == 'text':
        # TODO:
        pass
    elif type == 'cmd':
        # TODO
        pass

    return path_to_file




# def query_simple( data, query ):
#     ent, op, val = query.split(' ')
#     days = stats.terms_days(data, ent, op, val)

#     return days

# def query_parser( query ):
#     l, queries = query.lower().split(' '), []
#     mem, key, max = 0, 0, len(l)
#     while key < max:
#         el = l[key]
#         if el in ['and', 'or']:
#             q = cfg.e # Create part query
#             for i in range(mem,key):
#                 q += f' {l[i]} '
#             queries.append( utils.clean(q) ) # Append query part
#             queries.append( el ) # Append 'or', 'and'
#             mem = key + 1 # Always start at the next key
#         key += 1

#     q = cfg.e # Create last part query
#     for i in range(mem,key):
#         q += f' {l[i]} '
#     queries.append( utils.clean(q) )

#     return queries

# def np_and( np1, np2 ):
#     if np1.size == 0 and np2.size == 0:
#         return np.array([])
#     elif np1.size == 0 and np2.size > 0:
#         return np.array([])
#     elif np2.size == 0 and np1.size > 0:
#         return np.array([])
#     else:
#         col_ymd, col_stn, l = data.YYYYMMDD, data.STN, []
#         # Get only the (same) days in both lists for a station
#         for n1 in list(np1):
#             for n2 in list(np2):
#                 if n1[col_ymd] == n2[col_ymd] and \
#                    n1[col_stn] == n2[col_stn]:
#                     # Check first if element already in list
#                     found = False
#                     for el in l:
#                         if set(el) == set(n1):
#                             found = True
#                     if not found:
#                         l.append(n1)

#         return np.array(l)

# def np_or( np1, np2 ):
#     if np1.size == 0 and np2.size == 0:
#         return np.array([])
#     elif np1.size == 0 and np2.size > 0:
#         return np2
#     elif np2.size == 0 and np1.size > 0:
#         return np1
#     else:
#         col_ymd, col_stn, l = data.YYYYMMDD, data.STN, []
#         npl = np.concatenate( (np1, np2) ) # Sum together
#         # Add only unique days for station to the list
#         # for el in np:
#         #
#         # for n1 in list(np1):
#         #     for n2 in list(np2):
#         #         if n1[ymd] == n2[ymd] and n1[stn] == n2[stn]:
#         #             pass
#         #         else:
#         #             l.append(n1)

#         return npl

# def query_advanced( data, query ):
#     # Make a query list
#     queries = query_parser( query )
#     # Make one list with the days based on the queries
#     # The other list with the (and, or) operators
#     days, oper = [], []
#     for el in queries:
#         if el not in ['and', 'or']:
#             days.append(query_simple(data, el))
#         else:
#             oper.append(el)

#     # Proces all the days with the and,or operators and add to sel
#     ndx, key, max, sel = 0, 1, len(days), np.array([])
#     while key < max:
#         op, d1, d2 = oper[ndx], days[key-1], days[key] # Get the days from the query
#         # Make new days and put in same list as a replacement
#         if op == 'and':
#             np_a = np_and( d1, d2 )
#             if np_a.size != 0:
#                 sel = np_a if sel.size == 0 else np.concatenate( (sel, np_a) )
#         elif op == 'or':
#             # Or is +/- the same as a normal plus
#             np_o = np_or( d1, d2 )
#             if np_o.size != 0:
#                 sel = np_o if sel.size == 0 else np.concatenate( (sel, np_o) )

#         days[key] = sel
#         ndx += 1 # Next operator
#         key += 1 # Next days in list

#     # All selected (unique)  days
#     return sel