# -*- coding: utf-8 -*-
'''Library contains functions for creating, updating and querying on a database'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.0.2'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import sources.control.fio as fio
import sources.model.dayvalues.data as data
import sources.view.text as text
import sources.view.console as cnsl
import sources.model.ymd as ymd
import sqlite3
import mysql.connector
import math, time

def nan(val):
    return 'null' if math.isnan(val) else val

def fill_template( s, search, value ):
    while s.find(search) != -1: 
        s = s.replace(search, value)
    return s

def proces_template( str, stn, yyyymmdd, ddvec, fhvec, fg, fhx, fhxh, fhn, fhnh, fxx, fxxh, 
                     tg, tn, tnh, tx, txh, t10n, t10nh, sq, sp, q, dr, rh, rhx, rhxh, pg, px,
                     pxh, pn, pnh, vvn, vvnh, vvx, vvxh, ng, ug, ux, uxh, un, unh, ev24 ):
    str = fill_template( str, '{{stn}}', nan(stn) )
    str = fill_template( str, '{{yyyymmdd}}', nan(yyyymmdd) )
    str = fill_template( str, '{{ddvec}}', nan(ddvec) )
    str = fill_template( str, '{{fhvec}}', nan(fhvec) )
    str = fill_template( str, '{{fg}}', nan(fg) )
    str = fill_template( str, '{{fhx}}', nan(fhx) )
    str = fill_template( str, '{{fhxh}}', nan(fhxh) )
    str = fill_template( str, '{{fhn}}', nan(fhn) )
    str = fill_template( str, '{{fhnh}}', nan(fhnh) )
    str = fill_template( str, '{{fxx}}', nan(fxx) )
    str = fill_template( str, '{{fxxh}}', nan(fxxh) )
    str = fill_template( str, '{{tg}}', nan(tg) )
    str = fill_template( str, '{{tn}}', nan(tn) )
    str = fill_template( str, '{{tnh}}', nan(tnh) )
    str = fill_template( str, '{{tx}}', nan(tx) )
    str = fill_template( str, '{{txh}}', nan(txh) )
    str = fill_template( str, '{{t10n}}', nan(t10n) )
    str = fill_template( str, '{{t10nh}}', nan(t10nh) )
    str = fill_template( str, '{{sq}}', nan(sq) )
    str = fill_template( str, '{{sp}}', nan(sp) )
    str = fill_template( str, '{{q}}', nan(q) )
    str = fill_template( str, '{{dr}}', nan(dr) )
    str = fill_template( str, '{{rh}}', nan(rh) )
    str = fill_template( str, '{{rhx}}', nan(rhx) )
    str = fill_template( str, '{{rhxh}}', nan(rhxh) )
    str = fill_template( str, '{{pg}}', nan(pg) )
    str = fill_template( str, '{{px}}', nan(px) )
    str = fill_template( str, '{{pxh}}', nan(pxh) )
    str = fill_template( str, '{{pn}}', nan(pn) )
    str = fill_template( str, '{{pnh}}', nan(pnh) )
    str = fill_template( str, '{{vvn}}', nan(vvn) )
    str = fill_template( str, '{{vvnh}}', nan(vvnh) )
    str = fill_template( str, '{{vvx}}', nan(vvx) )
    str = fill_template( str, '{{vvxh}}', nan(vvxh) )
    str = fill_template( str, '{{ng}}', nan(ng) )
    str = fill_template( str, '{{ug}}', nan(ug) )
    str = fill_template( str, '{{ux}}', nan(ux) )
    str = fill_template( str, '{{uxh}}', nan(uxh) )
    str = fill_template( str, '{{un}}', nan(un) )
    str = fill_template( str, '{{unh}}', nan(unh) )
    str = fill_template( str, '{{ev24}}', nan(ev24) )

    return str


def open_sqlite():
    connect_db, cursor, ok = False, False, False
    # input(cfg.db_dayvalues)

    if fio.check(cfg.db_dayvalues, verbose=cfg.verbose):
        try:
            connect_db = sqlite3.connect(cfg.db_dayvalues)
            cursor = connect_db.cursor()
        except Exception as e:
            cnsl.log(f'[{ymd.now()}] Error in open_sqlite()\n{e}', cfg.error)
        else:
            ok = True

    return ok, connect_db, cursor

def open_server(host, username, passwd):
    connect_db = mysql.connector.connect(
        host=host,
        user=username,
        password=passwd
    )
    cursor = connect_db.cursor()

    return connect_db, cursor

def close(db):
    db.close()

def query( q ):
    pass

def insert_all(station, verbose=cfg.verbose):
    ok, conn, cursor = open_sqlite()
    if ok:
        ok, np_lst = data.read(station, verbose=verbose)
        if ok:
            str_template = fio.read(path)
            for day in np_lst:
                # input(day)
                stn, yyyymmdd,                    \
                ddvec, fhvec, fg, fhx,            \
                fhxh, fhn, fhnh, fxx, fxxh, tg,   \
                tn, tnh, tx, txh, t10n, t10nh,    \
                sq, sp, q, dr, rh, rhx,           \
                rhxh, pg, px, pxh, pn, pnh,       \
                vvn, vvnh, vvx, vvxh, ng, ug,     \
                ux, uxh, un, unh, ev24 = data.normalize(day, format='knmi')

                query = proces_template( str, stn, yyyymmdd, ddvec, fhvec, fg, fhx, fhxh, fhn, fhnh, fxx, fxxh, 
                     tg, tn, tnh, tx, txh, t10n, t10nh, sq, sp, q, dr, rh, rhx, rhxh, pg, px,
                     pxh, pn, pnh, vvn, vvnh, vvx, vvxh, ng, ug, ux, uxh, un, unh, ev24 )
                query = text.remove_dumb_whitespace(query)
                cnsl.log_r(f'[{ymd.now()}] {query}')
                cursor.execute(query)
                conn.commit() 
                time.sleep(0.01)

            cnsl.log(f'[{ymd.now()}] Execute {query}') # Just double

    cursor.close()
    conn.close()

def select(options):
    ok, conn, cursor = open_sqlite()
    rows = []
    if ok:
        query = options[text.ask_sqlite_query]
        q = text.remove_dumb_whitespace(query)
        cursor.execute(q)

        rows = cursor.fetchall()

    return ok, rows

def write( station, st_yyyymmdd, ed_yyyymmdd ):
    # Read
    # Update values

    pass


def calculate( options ):
    lst_stations = options[text.ask_stations] 
    for station in lst_stations: 
        insert_all(station, verbose=cfg.verbose)
