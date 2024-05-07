# -*- coding: utf-8 -*-
'''Database Queries'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__version__    =  '0.0.4'
__license__    =  'GNU General Public License version 2 - GPLv2'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

mk_db_weatherstats = '''
    CREATE DATABASE IF NOT EXISTS weatherstats ;
'''

rm_db_weatherstats = '''
    DROP DATABASE IF EXISTS weatherstats ;
'''

rm_db_weatherstats = '''
    DROP TABLE IF EXISTS dayvalues ;
'''

mk_table_dayvalues_sqlite = '''
    CREATE TABLE IF NOT EXISTS dayvalues (
        id        INTEGER NOT NULL UNIQUE,
        stn       INTEGER NOT NULL,
        yyyymmdd  INTEGER NOT NULL,
        ddvec     INTEGER,
        fhvec     REAL,
        fg        REAL,
        fhx       REAL,
        fhxh      INTEGER,
        fhn       REAL,
        fhnh      INTEGER,
        fxx       REAL,
        fxxh      INTEGER,
        tg        REAL,
        tn        REAL,
        tnh       INTEGER,
        tx        REAL,
        txh       INTEGER,
        t10n      REAL,
        t10nh     INTEGER,
        sq        INTEGER,
        sp        INTEGER,
        q         REAL,
        dr        INTEGER,
        rh        REAL,
        rhx       REAL,
        rhxh      INTEGER,
        pg        REAL,
        px        REAL,
        pxh       INTEGER,
        pn        REAL,
        pnh       INTEGER,
        vvn       INTEGER,
        vvnh      INTEGER,
        vvx       INTEGER,
        vvxh      INTEGER,
        ng        INTEGER,
        ug        REAL,
        ux        REAL,
        uxh       INTEGER,
        un        REAL,
        unh       INTEGER,
        ev24      REAL,
        PRIMARY KEY("id" AUTOINCREMENT)
    ) 
    ;
'''

insert_into_dayvalues = '''
    INSERT INTO dayvalues ( 
        stn, yyyymmdd, ddvec, fhvec, fg, fhx, 
        fhxh, fhn, fhnh, fxx, fxxh, tg, 
        tn, tnh, tx, txh, t10n, t10nh, 
        sq, sp, q, dr, rh, rhx, 
        rhxh, pg, px, pxh, pn, pnh, 
        vvn, vvnh, vvx, vvxh, ng, ug, 
        ux, uxh, un, unh, ev24 
    )
    VALUES( 
        {}, {}, {}, {}, {}, {}, 
        {}, {}, {}, {}, {}, {}, 
        {}, {}, {}, {}, {}, {}, 
        {}, {}, {}, {}, {}, {}, 
        {}, {}, {}, {}, {}, {}, 
        {}, {}, {}, {}, {}, {}, 
        {}, {}, {}, {}, {}
    )
    ;
'''

update_into_dayvalues = '''
    UPDATE dayvalues
    SET 
        ddvec={}, fhvec={}, fg={}, fhx={}, 
        fhxh={}, fhn={}, fhnh={}, fxx={}, fxxh={}, tg={}, 
        tn={}, tnh={}, tx={}, txh={}, t10n={}, t10nh={}, 
        sq={}, sp={}, q={}, dr={}, rh={}, rhx={}, 
        rhxh={}, pg={}, px={}, pxh={}, pn={}, pnh={}, 
        vvn={}, vvnh={}, vvx={}, vvxh={}, ng={}, ug={}, 
        ux={}, uxh={}, un={}, unh={}, ev24={} 

    WHERE stn={} and yyyymmdd={};
'''
