# -*- coding: utf-8 -*-
'''Library contains functions for building html'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 3 - GPLv3'
__version__    =  '0.9.7'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import datetime, re
import numpy as np
import sources.control.fio as fio
import sources.model.utils as util
import sources.model.ymd as ymd
import sources.model.daydata as daydata
import sources.model.stats as stats
import sources.view.console as cnsl
import sources.view.text as text
import sources.view.icon as icon

class Template():
    ''' Class to make a html page based on the template - template.html'''
    charset     = 'UTF-8'
    author      = 'WeatherstatsNL'
    viewport    = 'width=device-width, initial-scale=1.0, shrink-to-fit=no'
    description = cfg.e
    icon        = cfg.e
    html        = cfg.e
    header      = cfg.e
    main        = cfg.e
    footer      = cfg.e
    title       = cfg.e
    js_files    = []
    js_code     = cfg.e
    css_files   = []
    css_code    = cfg.e
    strip       = cfg.html_strip
    verbose     = cfg.verbose
    template    = cfg.e
    path        = cfg.e

    def __init__(self, title='WeatherstatsNL - template',
                       header=cfg.e, main=cfg.e,  footer=cfg.e ):
        self.title  = title
        self.header = header
        self.main   = main
        self.footer = footer

        title = self.title.strip().replace(' ', cfg.e)
        dt = ymd.text(ymd.yyyymmdd_now())
        self.file_name = f'{title}-{dt}.html'
        self.template  = cfg.html_template_statistics
        self.path_to_root = cfg.e

    def set_path(self, path):
        self.path = path

    def add_css_file(self, path=cfg.e):
        self.css_files.append(f'<link rel="stylesheet" type="text/css" href="{path}">')

    def add_js_file(self, path=cfg.e):
        self.js_files.append(f'<script src="{path}"></script>')

    def add_description(self, description):
        self.description = f'<meta name="description" content="{description}">'

    def add_icon(self, icon_url):
        self.icon = f'<link rel="shortcut icon" href="{icon_url}">'

    def create(self):
        ok, self.html = fio.read( self.template, verbose=False )
        if ok:
            self.html = self.html.replace('{{%now%}}', str( datetime.datetime.now()))
            self.html = self.html.replace('{{%title%}}', self.title)
            self.html = self.html.replace('{{%icon%}}', self.icon)
            self.html = self.html.replace('{{%charset%}}', self.charset)
            self.html = self.html.replace('{{%author%}}', self.author)
            self.html = self.html.replace('{{%description%}}', self.description)
            self.html = self.html.replace('{{%viewport%}}', self.viewport)
            self.html = self.html.replace('{{%css_files%}}', util.lst_to_s(self.css_files,'\n'))
            self.html = self.html.replace('{{%css_code%}}', self.css_code)
            self.html = self.html.replace('{{%header%}}', self.header)
            self.html = self.html.replace('{{%main%}}', self.main)
            self.html = self.html.replace('{{%footer%}}', self.footer)
            self.html = self.html.replace('{{%js_files%}}', util.lst_to_s(self.js_files,'\n'))
            self.html = self.html.replace('{{%js_code%}}', self.js_code)
            self.html = self.html.replace('{{%path_to_root%}}', self.path_to_root)
        else:
            cnsl.log(f'Read {self.template} file failed!', cfg.error)

        return ok

    def save(self):
        ok = self.create()
        if ok:
            if self.strip:
                self.html = text.clean_html(self.html)

            ok = fio.write(self.path, self.html, verbose=False)
        return ok

    def delete(self):
        fio.delete(self.path, self.verbose)

    def reset(self):
        self.description = cfg.e
        self.icon = cfg.e
        self.html = cfg.e
        self.header = cfg.e
        self.main = cfg.e
        self.footer = cfg.e
        self.title = cfg.e
        self.js_files = []
        self.js_code = cfg.e
        self.css_files = []
        self.css_code = cfg.e
        self.strip = cfg.html_strip
        self.verbose = cfg.verbose
        self.template = cfg.e
        self.path = cfg.e

def max_popup_rows(total, max):
    return total if max == -1 else max

def footer_data_notification(station):
    t  = f'{station.data_notification}'.lower()
    t += f'<br>{text.now_created_notification()}'
    return t

# DAYVALUES
def dayvalue_div_entity(title=False, val=False, time=False ):
    val  =  val if  val != False else cfg.e
    time = time if time != False else cfg.e
    return f'''
        <div class="card col-12 col-xs-12 col-sm-12 col-md-6 col-lg-4 col-xl-3 mx-auto border-0 card-dayvalue">
            <div class="card-body text-center card-dayvalue-body">
                <h6 class="card-title text-capitalize card-dayvalue-body-title">{title}</h6>
                <div class="card-text card-dayvalue-body-data">{val}<br><small class="text-muted">{time}</small></div>
            </div>
        </div>
    '''.format( title, val, time )

def day_value_tx(tx, txh):
    if tx != cfg.no_val: 
        tx = f'{entity_to_icon("tx", "text-danger")} {tx}'
    htm = dayvalue_div_entity( text.ent_to_txt('TX'), tx, txh )
    return htm

def day_value_tg(tg): 
    if tg != cfg.no_val:
        tg = f'{entity_to_icon("tg", "text-success")} {tg}'
    htm = dayvalue_div_entity( text.ent_to_txt('TG'), tg, cfg.e)
    return htm

def day_value_tn(tn, tnh):
    if tn != cfg.no_val: 
        tn = f'{entity_to_icon("tn", "text-primary")} {tn}'
    htm = dayvalue_div_entity( text.ent_to_txt('TN'), tn, tnh )
    return htm

def day_value_t10n(t10n, t10nh):    
    if t10n != cfg.no_val:
        t10n = f'{entity_to_icon("t10n", "text-warning")} {t10n}'
    htm = dayvalue_div_entity( text.ent_to_txt('T10N'), t10n, t10nh)
    return htm

def day_value_ddvec(ddvec): 
    if ddvec != cfg.no_val: 
        ddvec = f'{entity_to_icon("ddvec", "text-info")} {ddvec}'
    htm = dayvalue_div_entity( text.ent_to_txt('DDVEC'), ddvec, cfg.e)
    return htm

def day_value_fhvec(fhvec):
    if fhvec != cfg.no_val: 
        fhvec = f'{entity_to_icon("fhvec", "text-success")} {fhvec}'
    htm = dayvalue_div_entity( text.ent_to_txt('FHVEC'), fhvec, cfg.e)
    return htm

def day_value_fg(fg):
    if fg != cfg.no_val:
        fg = f'{entity_to_icon("fg", "text-success")} {fg}'
    htm = dayvalue_div_entity( text.ent_to_txt('FG'), fg, cfg.e)
    return htm

def day_value_fhx(fhx, fhxh):
    if fhx != cfg.no_val:
        fhx = f'{entity_to_icon("fhx", "text-success")} {fhx}'
    htm = dayvalue_div_entity( text.ent_to_txt('FHX'), fhx, fhxh)
    return htm

def day_value_fxx(fxx, fxxh):
    if fxx !=  cfg.no_val:
        fxx = f'{entity_to_icon("fxx", "text-success")} {fxx}'
    htm = dayvalue_div_entity( text.ent_to_txt('FXX'), fxx, fxxh)
    return htm

def day_value_fhn(fhn, fhnh):
    if fhn != cfg.no_val:
        fhn = f'{entity_to_icon("fhn", "text-success")} {fhn}'
    htm = dayvalue_div_entity( text.ent_to_txt('FHN'), fhn, fhnh)
    return htm

def day_value_sq(sq):
    if sq != cfg.no_val:
        sq = f'{entity_to_icon("sq", "text-warning")} {sq}'
    htm = dayvalue_div_entity( text.ent_to_txt('SQ'), sq, cfg.e)
    return htm

def day_value_sp(sp):
    if sp != cfg.no_val:
        sp = f'{entity_to_icon("sp", "text-warning")} {sp}'
    htm = dayvalue_div_entity( text.ent_to_txt('SP'), sp, cfg.e)
    return htm

def day_value_rh(rh):
    if rh != cfg.no_val: 
        rh = f'{entity_to_icon("rh", "text-primary")} {rh}'
    htm = dayvalue_div_entity( text.ent_to_txt('RH'), rh, cfg.e)
    return htm

def day_value_rhx(rhx, rhxh):
    if rhx != cfg.no_val: 
        rhx = f'{entity_to_icon("rhx", "text-primary")} {rhx}'
    htm = dayvalue_div_entity( text.ent_to_txt('RHX'), rhx, rhxh)
    return htm

def day_value_dr(dr):
    if dr != cfg.no_val: 
        dr = f'{entity_to_icon("dr", "text-primary")} {dr}'
    htm = dayvalue_div_entity( text.ent_to_txt('DR'), dr, cfg.e)
    return htm

def day_value_px(px, pxh):
    if px != cfg.no_val:
        px = f'{entity_to_icon("px", "text-warning")} {px}'
    htm = dayvalue_div_entity( text.ent_to_txt('PX'), px, pxh)
    return htm 

def day_value_pg(pg):
    if pg != cfg.no_val: 
        pg = f'{entity_to_icon("pg", "text-warning")} {pg}'
    htm = dayvalue_div_entity( text.ent_to_txt('PG'), pg, cfg.e)
    return htm 

def day_value_pn(pn, pnh):
    if pn != cfg.no_val: 
        pn = f'{entity_to_icon("pn", "text-warning")} {pn}'
    htm =  dayvalue_div_entity( text.ent_to_txt('PN'), pn, pnh)
    return htm 

def day_value_ux(ux, uxh):
    if ux != cfg.no_val: 
        ux = f'{entity_to_icon("ux", "text-primary")} {ux}'
    htm = dayvalue_div_entity( text.ent_to_txt('UX'), ux, uxh)
    return htm

def day_value_ug(ug):
    if ug != cfg.no_val: 
        ug = f'{entity_to_icon("ug", "text-primary")} {ug}'
    htm = dayvalue_div_entity( text.ent_to_txt('UG'), ug, cfg.e)
    return htm 

def day_value_un(un, unh):
    if un != cfg.no_val: 
        un = f'{entity_to_icon("un", "text-primary")} {un}'
    htm = dayvalue_div_entity( text.ent_to_txt('UN'), un, unh)
    return htm 

def day_value_vvx(vvx, vvxh):
    if vvx != cfg.no_val:
        vvx = f'{entity_to_icon("vvx", "text-info")} {vvx}'
    htm = dayvalue_div_entity( text.ent_to_txt('VVX'), vvx, vvxh)
    return htm

def day_value_vvn(vvn, vvnh):
    if vvn != cfg.no_val:
        vvn = f'{entity_to_icon("vvn", "text-info")} {vvn}'
    htm = dayvalue_div_entity( text.ent_to_txt('VVN'), vvn, vvnh )
    return htm

def day_value_ng(ng):
    if ng != cfg.no_val: 
        ng = f'{entity_to_icon("ng", "text-secondary")} {ng}'
    htm = dayvalue_div_entity( text.ent_to_txt('NG'), ng, cfg.e)
    return htm 

def day_value_q(q):
    if q != cfg.no_val:
        q = f'{entity_to_icon("q", "text-danger")} {q}'
    htm = dayvalue_div_entity( text.ent_to_txt('Q'), q, cfg.e)
    return htm

def day_value_ev24(ev24):
    if ev24 != cfg.no_val: 
        ev24 = f'{entity_to_icon("ev24", "text-warning")} {ev24}'
    htm = dayvalue_div_entity( text.ent_to_txt('EV24'), ev24, cfg.e)
    return htm 

def day_values_all(day):
    stn, yymmdd, ddvec, fhvec, fg, fhx, fhxh, fhn, fhnh, fxx, fxxh, tg, tn,\
    tnh, tx, txh, t10n, t10nh, sq, sp, q, dr, rh, rhx, rhxh, pg, px, pxh,\
    pn, pnh, vvn, vvnh, vvx, vvxh, ng, ug, ux, uxh, un, unh, ev24 = daydata.entities(day)

    htm  = day_value_tx(tx, txh)
    htm += day_value_tg(tg)
    htm += day_value_tn(tn, tnh)
    htm += day_value_t10n(t10n, t10nh)
    htm += day_value_ddvec(ddvec)
    htm += day_value_fhvec(fhvec)
    htm += day_value_fg(fg)
    htm += day_value_fhx(fhx, fhxh)
    htm += day_value_fhn(fhn, fhnh)
    htm += day_value_fxx(fxx, fxxh)
    htm += day_value_sq(sq)
    htm += day_value_sp(sp)
    htm += day_value_rh(rh)
    htm += day_value_rhx(rhx, rhxh)
    htm += day_value_dr(dr)
    htm += day_value_px(px, pxh)
    htm += day_value_pg(pg)
    htm += day_value_pn(pn, pnh)
    htm += day_value_ux(ux, uxh)
    htm += day_value_ug(ug)
    htm += day_value_un(un, unh)
    htm += day_value_vvx(vvx, vvxh)
    htm += day_value_vvn(vvn, vvnh)
    htm += day_value_ng(ng)
    htm += day_value_q(q)
    htm += day_value_ev24(ev24)

    return htm

def th(t, clas=cfg.e):
    cl = f' class="{clas}"' if clas else cfg.e
    return f'<th{cl}>{t}</th>'

def span(t, clas=cfg.e):
    cl = f' class="{clas}"' if clas else cfg.e
    return f'<span{cl}>{t}</span>'

def tr_th(lth, clas=cfg.e):
    cl = f' class="{clas}"' if clas else cfg.e
    t = f'<tr{cl}>'
    for th in lth:
        t += f'<th>{th}</th>'
    t += '</tr>'
    return t

def tr_td(ltd, clas=cfg.e):
    cl = f' class="{clas}"' if clas else cfg.e
    t = f'<tr{cl}>'
    for td in ltd:
        t += '<td>{td}</td>'
    t += '</tr>'
    return t

def title_mean(entity):
    return f'<span class="overline">{entity_to_icon("ave")} {entity}</span>'

def attr_title(entity, value=cfg.e):
    return f'{text.ent_to_txt(entity)} { text.fix_ent(value) if value else cfg.e }'.strip()

def extreme_values( day, entity ):
    span = f'<span class="val">{cfg.no_val}</span>' 
    try:
        val_raw = day[daydata.etk(entity)]
        ymd_raw = day[daydata.etk('yyyymmdd')]
    except Exception as e:
        # cnsl.log(f'Exception {e} !', cfg.error)
        pass
    else:
        span1 = f'<span class="val">{ text.fix_ent(val_raw, entity) }</span>' 
        span2 = f'<span class="dat">{ text.fix_ent(ymd_raw, "yyyymmdd") }</span>' 
        span = f'{span1}{span2}'

    return span

def table( lst_head, lst_body, reverse=False ):
    htm = cfg.e
    if lst_body:
        htm = f'''
        <table class="popup">
        <thead>{ tr_th(lst_head) }</thead>
        <tbody>'''

        # Reverse list optional
        if reverse: lst_body = lst_body[::-1]
        for el in lst_body[: cfg.html_popup_table_max_rows]: 
            htm += el
    
        htm += '</tbody></table>'

    return htm

def table_days(days, entity, reverse=False):

    html = cfg.e
    if cfg.html_popup_table_show:
        if days.np_period_2d_has_days():
            time_too, t_td, lst_head = False, cfg.e, ['pos', 'date', entity]
            t_entity = daydata.entity_to_t_entity(entity)
            if t_entity:
                lst_head.append(t_entity)
                time_too = True 

            pos, lst_body = 1, []
            for day in days.np_period_2d:
                if np.size(day, axis=0) == 0:
                    continue

                try:
                    yymmdd, act = day[daydata.etk('yyyymmdd')], day[daydata.etk(entity)]
                    if time_too: # Add time td
                        t_td = f'<td>{ text.fix_ent(day[daydata.etk(t_entity)], t_entity) }</td>'
                except Exception as e:
                    cnsl.log(f'Exception {e} !', cfg.verbose)
                else:
                    lst_body.append(f'''
                        <tr>
                            <td>{ pos }</td>
                            <td title="{ymd.text(yymmdd)}">{text.fix_ent(yymmdd, 'date')}</td>
                            <td>{ text.fix_ent( act, entity ) }</td>
                            {t_td}
                        </tr>
                    ''')

                pos += 1

            # create html table
            html = table( lst_head, lst_body, reverse )

    return html

def table_average(days, entity, reverse=False):

    html = cfg.e
    if cfg.html_popup_table_show:
        if days.np_period_2d_has_days():
            # Make lst header titles and time too if there
            time_too, t_td, lst_head = False, cfg.e, ['cnt', 'date', entity, 'ave']
            t_entity = daydata.entity_to_t_entity(entity)
            if t_entity:
                lst_head = ['cnt', 'date', entity, t_entity, 'ave']
                time_too = True 

            cnt, pos, lst_body, station = 1, 1, [], days.station
            for day in days.np_period_2d:
                if np.size(day, axis=0) == 0:
                    continue
                # Calculate values
                try:
                    yymmdd = day[daydata.etk('yyyymmdd')]
                    act = day[daydata.etk(entity)]
                    ave, _ = stats.Days( station, days.np_period_2d[:cnt] ).average(entity)
                    if time_too: # Add time td
                        t_td = f'<td>{ text.fix_ent(day[daydata.etk(t_entity)], t_entity) }</td>'
                except Exception as e:
                    cnsl.log(f'Exception {e} !', cfg.verbose)
                else:
                    lst_body.append(f'''
                        <tr>
                            <td>{ cnt }</td>
                            <td title="{ymd.text(yymmdd)}">{text.fix_ent(yymmdd, 'date')}</td>
                            <td>{ text.fix_ent( act, entity ) }</td>
                            {t_td}
                            <td>{ text.fix_ent( ave, entity ) }</td>
                        </tr>
                    ''')

                cnt += 1
                pos += 1

            # create html table
            html = table( lst_head, lst_body, reverse )

    return html

def table_count(days, entity):
    html = cfg.e
    if cfg.html_popup_table_show:
        if days.np_period_2d_has_days():
            # Make lst header titles and time too if there
            time_too, t_td, lst_head = False, cfg.e, ['cnt', 'date', entity]
            t_entity = daydata.entity_to_t_entity(entity)
            if t_entity:
                lst_head.append(t_entity)
                time_too = True 
    
            cnt, lst, station = 1, [], days.station
            for day in days.np_period_2d:
                if np.size(day, axis=0) == 0:
                    continue
                # Calculate values
                try:
                    yymmdd = day[daydata.etk('yyyymmdd')]
                    act = day[daydata.etk(entity)]
                    cnt_days = stats.Days( station, days.np_period_2d[:cnt] ).count_np_period_2d()
                    if time_too: # Add time td
                       t_td = f'<td>{ text.fix_ent(day[daydata.etk(t_entity)], t_entity) }</td>'
                except Exception as e:
                    cnsl.log(f'Exception {e} !', cfg.verbose)
                else:
                    lst.append(f'''
                    <tr>
                        <td>{cnt_days}</td>
                        <td title="{ ymd.text( yymmdd ) }">{ text.fix_ent(yymmdd, 'date') }</td>
                        <td>{ text.fix_ent( act, entity ) }</td>
                        {t_td}
                    </tr>
                    ''')

                cnt += 1

            # Create html table
            html = table(lst_head, lst, reverse=True)

    return html

def table_sum(days, entity):
    html = cfg.e
    if cfg.html_popup_table_show:
        if days.np_period_2d_has_days():
            # Make lst header titles and time too if there
            time_too, t_td, lst_head = False, cfg.e, ['cnt','date',entity,'sum']
            t_entity = daydata.entity_to_t_entity(entity)
            if t_entity:
                time_too = True 
                lst_head = ['cnt','date',entity,t_entity,'sum']

            cnt, lst, station, format = 1, [], days.station, days.station.format
            for day in days.np_period_2d:
                if np.size(day, axis=0) == 0:
                    continue
                # Calculate values
                try:
                    yymmdd = day[daydata.etk('yyyymmdd')]
                    act = day[daydata.etk(entity, format)]
                    sum_tot, _ = stats.Days( station, days.np_period_2d[:cnt] ).sum(entity)
                    if time_too: # Add time td
                        t_td = f'<td>{ text.fix_ent(day[daydata.etk(t_entity)], t_entity) }</td>'
                except Exception as e:
                    cnsl.log(f'Exception {e} !', cfg.verbose)
                else:
                    lst.append(f'''
                    <tr>
                        <td>{ cnt }</td>
                        <td title="{ ymd.text( yymmdd ) }">{ text.fix_ent(yymmdd, 'date') }</td>
                        <td>{ text.fix_ent(act, entity) }</td>
                        {t_td}
                        <td>{ text.fix_ent(sum_tot, entity) }</td>
                    </tr>
                    ''')

                cnt += 1

            # create html table
            html = table(lst_head, lst, reverse = True)

    return html

def table_frost_sum(days):
    html = cfg.e
    if cfg.html_popup_table_show:
        if days.np_period_2d_has_days():
            cnt, lst, station, format = 1, [], days.station, days.station.format
            for day in days.np_period_2d:
                if np.size(day, axis=0) == 0:
                    continue
                # Calculate values 
                try:
                    yymmdd = day[daydata.etk('yyyymmdd')]
                    tx, txh = day[daydata.etk('tx', format)], day[daydata.etk('txh', format)]
                    tn, tnh = day[daydata.etk('tn', format)], day[daydata.etk('tnh', format)]
                    fsum_act = 0.0
                    if tx < 0.0: fsum_act += abs(tx)
                    if tn < 0.0: fsum_act += abs(tn)
                    fsum_tot, _ = stats.Days( station, days.np_period_2d[:cnt] ).frost_sum()
                except Exception as e:
                    cnsl.log(f'Exception {e} !', cfg.verbose)
                else:
                    lst.append(f'''
                    <tr>
                        <td>{ cnt }</td>
                        <td title="{ ymd.text( yymmdd ) }">{ text.fix_ent(yymmdd, 'date') }</td>
                        <td>{ text.fix_ent( tx, 'tx') }</td> 
                        <td>{ text.fix_ent( txh, 'txh') }</td>
                        <td>{ text.fix_ent( tn, 'tn') }</td> 
                        <td>{ text.fix_ent( tnh, 'tnh') }</td>
                        <td>{ text.fix_ent( fsum_act, 'frost-sum') }</td>
                        <td>{ text.fix_ent( fsum_tot, 'frost-sum') }</td>
                    </tr>
                    ''')

                cnt += 1

            # create html table
            html = table(['cnt','date','tx','txh','tn','tnh','fsum','total'], lst, reverse=True)

    return html

def table_ijnsen(days):
    html = cfg.e
    if cfg.html_popup_table_show:
        if days.np_period_2d_has_days():
            cnt, lst, station, format = 1, [], days.station, days.station.format
            for day in days.np_period_2d:
                if np.size(day, axis=0) == 0:
                    continue
                # Calculate values 
                try:
                    yymmdd = day[daydata.etk('yyyymmdd')]
                    tx_raw, txh = day[daydata.etk('tx', format)], day[daydata.etk('txh', format)]
                    tn_raw, tnh = day[daydata.etk('tn', format)], day[daydata.etk('tnh', format)]
                    ijnsen_tot, Days = stats.Days( station, days.np_period_2d[:cnt] ).ijnsen() # Ijnsen total

                    # Calculate ijnsen for this day
                    ijnsen_act = 0.0 # WEIRD ERROR ?
                    tx, tn = daydata.process_value(tx_raw, 'tx'), daydata.process_value(tn_raw, 'tn')
                    if tn <   0.0: ijnsen_act +=  1.0 * 1.0 / 363.0
                    if tn < -10.0: ijnsen_act += 10.0 * 1.0 /   9.0
                    if tx <   0.0: ijnsen_act +=  2.0 * 1.0 /   3.0
                except Exception as e:
                    cnsl.log(f'Exception {e} !', cfg.verbose)
                else:
                    lst.append(f'''
                    <tr>
                        <td>{ cnt }</td>
                        <td title="{ ymd.text( yymmdd ) }">{ text.fix_ent(yymmdd, 'date') }</td>
                        <td>{ text.fix_ent( tx_raw, 'tx') }</td> 
                        <td>{ text.fix_ent( txh, 'txh') }</td>
                        <td>{ text.fix_ent( tn_raw, 'tn') }</td> 
                        <td>{ text.fix_ent( tnh, 'tnh') }</td>
                        <td>{ round(ijnsen_act, 5) } ?</td>
                        <td>{ text.fix_ent( ijnsen_tot, 'ijnsen') } ?</td>
                    </tr>
                    ''')

                cnt += 1

            # create html table
            html = table(['cnt','date','tx','txh','tn','tnh','ijnsen','total'], lst, reverse=True)

    return html

def table_hellmann(days):
    html = cfg.e
    if cfg.html_popup_table_show:
        if days.np_period_2d_has_days():
            cnt, lst, station = 1, [], days.station
            for day in days.np_period_2d:
                if np.size(day, axis=0) == 0:
                    continue
                # Calculate values
                try:
                    yymmdd = day[daydata.etk('yyyymmdd')]
                    hmann_act = abs(day[daydata.etk('tg')])
                    hmann_sum, _ = stats.Days( station, days.np_period_2d[:cnt] ).hellmann()
                except Exception as e:
                    cnsl.log(f'Exception {e} !', cfg.verbose)
                else:
                    lst.append(f'''
                    <tr>
                        <td>{ cnt }</td>
                        <td title="{ ymd.text( yymmdd ) }">{ text.fix_ent(yymmdd, 'date') }</td>
                        <td>{ text.fix_ent(hmann_act, 'hellmann') }</td>
                        <td>{ text.fix_ent(hmann_sum, 'hellmann') }</td>
                    </tr>
                    ''')

                cnt += 1

            # create html table
            html = table(['cnt','date','hmann','total'], lst, reverse=True)

    return html

def table_heat_ndx(days):
    html = cfg.e
    if cfg.html_popup_table_show:
        if days.np_period_2d_has_days():
            cnt, lst, station = 1, [], days.station
            for day in days.np_period_2d:
                if np.size(day, axis=0) == 0:
                    continue
                # Calculate values
                try:
                    yymmdd = day[daydata.key('yyyymmdd')]
                    tg = day[daydata.etk('tg')]
                    heat_act = tg - 180.0 
                    heat_sum, _ = stats.Days(station, days.np_period_2d[:cnt]).heat_ndx()
                except Exception as e:
                    cnsl.log(f'Exception {e} !', cfg.verbose)
                else:
                    lst.append(f'''
                    <tr>
                        <td>{ cnt }</td>
                        <td title="{ ymd.text( yymmdd ) }">{ text.fix_ent(yymmdd, 'date') }</td>
                        <td>{ text.fix_ent(tg, 'tg') }</td>
                        <td>{ text.fix_ent(heat_act, 'heat-ndx') }</td>
                        <td>{ text.fix_ent(heat_sum, 'heat-ndx') }</td>
                    </tr>
                    ''')

                cnt += 1

            # create html table
            html = table(['cnt', 'date', 'tg', 'heat', 'total'], lst, reverse=True)

    return html

def entity_to_icon(entity, color=cfg.e, size=cfg.e, extra=cfg.e):
    e = entity.lower()
    if   e == 'tx':    return icon.temp_full(color, extra, size)
    elif e == 'tg':    return icon.temp_half(color, extra, size)
    elif e == 'tn':    return icon.temp_empty(color, extra, size)
    elif e == 't10n':  return icon.temp_empty(color, extra, size)
    elif e == 'ddvec': return icon.wind_dir(color, extra, size)
    elif e == 'fg':    return icon.wind(color, extra, size)
    elif e == 'rh':    return icon.shower_heavy(color, extra, size)
    elif e == 'sq':    return icon.sun(color, extra, size)
    elif e == 'pg':    return icon.compress_alt(color, extra, size)
    elif e == 'ug':    return icon.drop_tint(color, extra, size)
    elif e == 'fxx':   return icon.wind(color, extra, size)
    elif e == 'fhvec': return icon.wind(color, extra, size)
    elif e == 'fhx':   return icon.wind(color, extra, size)
    elif e == 'fhn':   return icon.wind(color, extra, size)
    elif e == 'sp':    return icon.sun(color, extra, size)
    elif e == 'q':     return icon.radiation(color, extra, size)
    elif e == 'dr':    return icon.shower_heavy(color, extra, size)
    elif e == 'rhx':   return icon.shower_heavy(color, extra, size)
    elif e == 'px':    return icon.compress_alt(color, extra, size)
    elif e == 'pn':    return icon.compress_alt(color, extra, size)
    elif e == 'vvn':   return icon.eye(color, extra, size)
    elif e == 'vvx':   return icon.eye(color, extra, size)
    elif e == 'ng':    return icon.cloud(color, extra, size)
    elif e == 'ux':    return icon.drop_tint(color, extra, size)
    elif e == 'un':    return icon.drop_tint(color, extra, size)
    elif e == 'ev24':  return icon.sweat(color, extra, size)
    elif e in text.lst_day: return icon.day(color, extra, size)
    elif e in text.lst_max: return icon.arrow_up(color, extra, size)
    elif e in text.lst_min: return icon.arrow_down(color, extra, size)
    elif e in text.lst_home: return icon.home(color, extra, size)
    elif e in text.lst_states: return icon.flag(color, extra, size)
    elif e in text.lst_states: return icon.flag(color, extra, size)
    elif e in text.lst_period_1: return icon.cal_period(color, extra, size)
    elif e in text.lst_period_2: return icon.cal_day(color, extra, size)
    elif e in text.lst_heat_ndx: return icon.fire(color, extra, size)
    elif e in text.lst_cold_ndx: return icon.icicles(color, extra, size)
    elif e in ['pg', 'pn', 'px']: return icon.compress_alt(color, extra, size)
    elif e in ['ux', 'un', 'ug']: return icon.drop_tint(color, extra, size)
    elif e in text.lst_wind: return icon.wind(color, extra, size)
    elif e in text.lst_rain: return icon.shower_heavy(color, extra, size)
    elif e in text.lst_wind_direction: return icon.wind_dir(color, extra, size)
    elif e in text.lst_copyright: return icon.copy(color, extra, size)
    elif e in text.lst_view: return icon.eye(color, extra, size)
    elif e in ['q']: return icon.radiation(color, extra, size)
    elif e in ['ng']: return icon.cloud(color, extra, size)
    elif e in text.lst_evaporation: return icon.sweat(color, extra, size)
    elif e in ['sq','sp']: return icon.sun(color, extra, size)
    elif e in text.lst_sum: return 'Σ'
    elif e in text.lst_ave: return cfg.e
    elif e in text.lst_gt: return icon.gt(color, extra, size)
    elif e in text.lst_ge: return icon.ge(color, extra, size)
    elif e in text.lst_lt: return icon.lt(color, extra, size)
    elif e in text.lst_le: return icon.le(color, extra, size)
    elif e in text.lst_eq: return '=='
    elif e in text.lst_ne: return '!=' 
    elif e in text.lst_num: return icon.sort_down(color, extra, size)
    elif e in text.lst_clima: return icon.ellipsis(color, extra, size)
    else: return icon.umbrella(color, extra, size)
