# -*- coding: utf-8 -*-
'''Select days from data'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__version__    =  '0.0.6'
__license__    =  'GNU Lesser General Public License (LGPL)'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import calendar, numpy as np, datetime
import sources.model.utils as utils
import sources.model.daydata as daydata
import common.model.convert as convert
import common.model.util as util

# # Init wildcards
x1, x2, x3, x4 = '*', '*'*2, '*'*3, '*'*4
x5, x6, x7, x8 = '*'*5, '*'*6, '*'*7, '*'*8

lst_xx = [x1, x2, x3, x4, x5, x6, x7, x8]

dd = ['0','1','2','3','4','5','6','7','8','9']

def is_(s):
    return False if str(s).strip() else True

def is_xx(s):
    for el in s:
        if el != x1:
            return False
    return True

def is_x_or_(s):
    return is_xx(s) or is_(s)

def is_dd(s):
    if s:
        for el in s:
            if el not in dd:
                return False
        return True
    return False

def days_in_month(y,m):
    d  = calendar.monthrange( int(y), int(m) )[1]
    return str(d)

def check_mm(m):
    '''No months numbers out of range'''
    im = int(m)
    if   im <  1: im =  1
    elif im > 12: im = 12

    mm = util.l0(im, 2)
    return mm

def check_dd(d):
    '''No days numbers must be out of range'''
    id = int(d)
    if   id <  1: id =  1
    elif id > 31: id = 31 # Possible max

    dd = util.l0(id, 2)
    return dd

def check_yy(y):
    iy = int(y)
    y_now = datetime.datetime.now().strftime('%Y')

    # Check ranges
    iy = cfg.data_min_year if iy < cfg.data_min_year else iy
    yy = y_now if iy > int(y_now) else str(iy)

    return yy

def check_mmdd(m, d):
    # !!!!
    im = int(check_mm(m))
    id = int(check_dd(d))

    if im in [1,3,5,7,8,10,12]:
        pass
    elif im in [4,6,9,11]:
        if id > 30:
            id = 30
    elif im == 2:
        if id > 29:
            id = 29

    mm = util.l0(im, 2)
    dd = util.l0(id, 2)
    return mm, dd

def check_yymmdd(y, m, d):
    y = check_yy(y)
    m, d = check_mmdd(m, d)

    # Max possible days in month -> correct for leap year too
    dmax = days_in_month(y,m)
    if int(d) > int(dmax):
        d = dmax

    return y, m, d

# Check for weird dates. TODO make better with x stars
def check_ymd(ymd):
    y, m, d, r = '', '', '', ''
    ymd = ymd.replace(' ', '').strip()

    if ymd == x1: 
        ymd = x8

    if len(ymd) >= 10:
        # yyyy*mmdd*
        if ymd[4] == x1 and ymd[9] == x1:
            y, m, d, r = ymd[:4], ymd[5:7], ymd[7:9], ymd[9:]

    # yyyymmdd*
    elif len(ymd) >= 9:
        y, m, d, r = ymd[:4], ymd[4:6], ymd[6:8], ymd[8:]

    # yyyymmdd
    elif len(ymd) >= 8:
        y, m, d, r = ymd[:4], ymd[4:6], ymd[6:8], ymd[8:]

    # yyyymm
    elif len(ymd) >= 6:
        y, m, r = ymd[:4], ymd[4:6], ymd[6:]

    # yyyy
    elif len(ymd) >= 4:
        y, r = ymd[:4], ymd[4:]

    # mm
    elif len(ymd) >= 2:
        ymd = ymd 

    # all
    elif len(ymd) == 1:
        ymd = ymd
    

    # Check individual
    if is_dd(y):  y = check_yy(y)
    if is_dd(d):  d = check_dd(d)
    if is_dd(m):  m = check_mm(m)
    # Check more for weird dates
    if   is_dd(y) and is_dd(m) and is_dd(d): y, m, d = check_yymmdd(y, m, d)
    elif is_dd(m) and is_dd(d): m, d = check_mmdd(m, d)

    ym, md, ymd = f'{y}{m}', f'{m}{d}', f'{y}{m}{d}'

    return y, m, d, ym, md, ymd, r

def now_ymd():
    # Current date
    now = datetime.datetime.now() # Date now
    y, m, d = now.strftime('%Y'), now.strftime('%m'), now.strftime('%d')
    ym, md = f'{y}{m}', f'{m}{d}'
    ymd = f'{y}{md}'

    return y, m, d, ym, md, ymd

def max_date( ymd ):
    '''Function selects max date from a given period.
       Possible with widcards *
       ie. yyyy****, yyyymm**
       '''
    # Current date
    y_now, m_now, d_now, ym_now, md_now, ymd_now = now_ymd()

    # OPTION '*', '****', '******' or '********'
    # ONLY *
    if ymd in lst_xx: return ymd_now

    # Split ymd in y, m and d, ym, md, ymd. And check for sanity
    y, m, d, ym, md, ymd, r = check_ymd(ymd)

    if y == x4: y = y_now
    if is_xx(m) or is_(m): m = m_now

    if is_dd(d):
        if m == m_now:
            if int(d) > int(d_now):
                d = d_now
    elif is_xx(d) or is_(d):
        d = days_in_month(y, m)

    # Recheck
    y, m, d, ym, md, ymd, r = check_ymd(f'{y}{m}{d}')

    # Make date yyyymmdd
    p = ymd_now # Fallback period is latest possbible date

    if is_dd(y):
        # OPTION YYYYMMDD
        if is_dd(md):
            p = ymd

        # OPTION YYYY**** | YYYY
        elif md in [x4, '']:
            if y == y_now:
                p = ymd_now
            else:
                p = f'{y}{md_now}'

        # OPTION YYYYMM** | YYYMM
        elif is_dd(m) and d in [x2,'']:
            if ym == ym_now:
                p = ymd_now

            elif m == m_now:
                p = f'{y}{md_now}'

            else:
                d = days_in_month(y,m)
                p = f'{y}{m}{d}'

    return p

def sel_days(np_data, sp, ep):
    '''Return a data np array based on a start and a end date'''
    ymd = np_data[:, daydata.etk('yyyymmdd')]
    fs, fe = float(sp), float(ep)
    sel = np.where( (ymd >= fs) & (ymd <= fe) )
    return np_data[sel]

def np_merge(result, new):
    result = new if result.size == 0 else np.concatenate( (result, new), axis=0)
    return result

def days_period(np_data_2d=np.array([[]]), period='*', check_only=False):
    '''Function returns a np array with data based on a period.
       Function can be used to check_only periods too.'''
    ok, lst_periods, result = False, [], np.array([])  # Lst with all the dates
    if not check_only:
        if np_data_2d.size == 0:
            return np_data_2d, lst_periods # This must not

    # Get the dates array from data
    if not check_only: 
        dymd  = np_data_2d[:, daydata.etk('yyyymmdd')] 
        dymds = convert.fl_to_s(dymd[0]) 
        dymde = convert.fl_to_s(dymd[-1]) 

        # Init varstack
        dys, dms, dds, dyms, dmds, dymds, drs = check_ymd(dymds)
        dye, dme, dde, dyme, dmde, dymde, dre = check_ymd(dymde)

    # Current date
    y_now, m_now, d_now, ym_now, md_now, ymd_now = now_ymd() 

    # Process period
    if period.find('-') != -1: # Yes '-' in period is given
        # Split in start and end-date
        ymdss, ymdee = period.split('-')
        ys, ms, ds, yms, mds, ymds, rs = check_ymd(ymdss)
        ye, me, de, yme, mde, ymde, re = check_ymd(ymdee)

        # print(ymdss, ys, ms, ds, yms, mds, ymds, rs)
        # print(ymdee, ye, me, de, yme, mde, ymde, re)
        # # input()

        # OPTION YYYYMMDD-YYYYMMDD
        # Get keys for the given periode
        if ymdss.isdigit() and ymdee.isdigit() and \
           len(ymdss) == 8 and len(ymdee) == 8:
            # print('OPTION YYYYMMDD-YYYYMMDD')
            if check_only: 
                ok = True
            else:
                sp, ep = ymds, ymde
                lst_periods.append( [sp, ep] )
                result = sel_days(np_data_2d, sp, ep)

        # OPTION: YYYY****-****
        # From a full year till data end
        elif ys.isdigit() and is_x_or_(ys) and \
             len(ymdss) == 8 and is_xx(ymdee):
            # print('OPTION YYYY****-****')
            if check_only: 
                ok = True
            else:
                for y in utils.l_years(ys, ye):
                    sp, ep = f'{y}0101', max_date(ymde)
                    lst_periods.append( [sp, ep] )
                    result = np_merge(result, sel_days(np_data_2d, sp, ep))

        # OPTION: YYYY****-YYYY**** | YYYY**-YYYY** | YYYY-YYYY
        # From full year to year
        elif ys.isdigit() and ye.isdigit() and is_x_or_(mds) and \
             len(ymdss) <= 8 and len(ymdee) <= 8 and \
             ( is_xx(mde) or is_(mde) ):
            # print('OPTION YYYY****-YYYY**** | YYYY**-YYYY** | YYYY-YYYY')
            if check_only: 
                ok = True
            else:
                sp, ep = f'{ys}0101',  max_date(ymde)
                lst_periods.append( [sp, ep] )
                result = sel_days(np_data_2d, sp, ep)

        # OPTION: YYYYMMDD-YYYYMM** | YYYYMMDD-YYYYMM**
        # A start day untill possible month end end
        elif ymdss.isdigit() and yme.isdigit() and is_x_or_(de) and \
             len(ymdss) == 8 and len(ymdee) in [6,8]:
            # print('OPTION YYYYMMDD-YYYYMM** | YYYYMMDD-YYYYMM**')
            if check_only: 
                ok = True
            else:
                sp, ep = ymds, max_date(ymde)
                lst_periods.append( [sp, ep] )
                result = sel_days(np_data_2d, sp, ep)

        # Other options more later maybe
        #

        # OPTION YYYY*MMDD*-YYYY*MMDD*
        # A certain period in a year. From startyear to endyear
        elif ys.isdigit() and ye.isdigit() and \
             len(ymdss) == 10 and len(ymdee) == 10 and \
             ymdss[4] == x1 and ymdee[4] == x1 and \
             ymdss[9] == x1 and ymdee[9] == x1:
            # print('OPTION YYYY*MMDD*-YYYY*MMDD*')
            if check_only: 
                ok = True
            else:
                iys, iye = int(ys), int(ye)
                imds, imde = int(mds), int(mde)
                diff = 1 if imds > imde else 0 # Date will go over a year

                while (iys+diff) <= iye:
                    sp, ep = f'{iys}{mds}', f'{iys+diff}{mde}'
                    lst_periods.append( [sp, ep] )
                    result = np_merge(result, sel_days(np_data_2d, sp, ep))
                    iys += 1

        # ADVANCED OPTIONS for more different periods in a given period
        # OPTION YYYY-YYYYMMDD* | YYYY****-YYYYMMDD*
        # A certain day in a year. From startyear to endyear.
        elif ys.isdigit() and is_x_or_(mds) and ymde.isdigit() and \
             len(ymdss) in [4,8] and len(ymdee) == 9 and \
             re == x1:
            # print('OPTION YYYY-YYYYMMDD* | YYYY****-YYYYMMDD*')
            if check_only: 
                ok = True
            else:
                for y in utils.l_years(ys, ye):
                    p = f'{y}{me}{de}'
                    lst_periods.append( [p] )
                    result = np_merge(result, sel_days( np_data_2d, p, p ) )

        # OPTION YYYY****-YYYYMM** | YYYY-YYYYMM** | YYYY-YYYYMM
        # A full 1 month in an year. From startyear to endyear
        elif ys.isdigit() and is_x_or_(mds) and \
             len(ymdss) in [4,8] and len(ymdee) in [6,8] and \
             yme.isdigit() and is_x_or_(de):
            # print('OPTION YYYY****-YYYYMM** | YYYY-YYYYMM** | YYYY-YYYYMM')
            if check_only: 
                ok = True
            else:
                for y in utils.l_years(ys, ye):
                    d = days_in_month(y, me)
                    sp, ep = f'{y}{me}01', f'{y}{me}{d}'
                    lst_periods.append( [sp, ep] )
                    result = np_merge(result, sel_days(np_data_2d, sp, ep))

    else:
        # No '-' in period
        y, m, d, ym, md, ymd, r = check_ymd(period)

        # OPTION ******** or *
        # All the data # All time
        if ymd in [x8,x1] and len(ymd) in [1,8]:
            if check_only: 
                ok = True
            else:
                sp, ep = np_data_2d[0, daydata.etk('yyyymmdd')], np_data_2d[-1, daydata.etk('yyyymmdd')]
                lst_periods.append( [sp, ep] )
                result = np_data_2d # All data

        # OPTION YYYYMMDD
        # Get only one day in a year
        elif ymd.isdigit() and len(ymd) == 8:
            if check_only: 
                ok = True
            else:
                lst_periods.append( [ymd] )
                result = sel_days(np_data_2d, ymd, ymd)

        # OPTION ****
        # The current whole year
        elif ymd == x4 and len(ymd) == 4:
            if check_only: 
                ok = True
            else:
                sp, ep = f'{y_now}0101', ymd_now
                lst_periods.append( [sp, ep] )
                result = sel_days(np_data_2d, sp, ep)

        # OPTION **
        # The current month
        elif ymd == x2 and len(ymd) == 2:
            if check_only: 
                ok = True
            else:
                d = days_in_month(y_now, m_now)
                sp, ep = f'{y_now}{m_now}01', f'{ymd_now}'
                lst_periods.append( [sp, ep] )
                result = sel_days(np_data_2d, sp, ep)

        # OPTION YYYY**** | YYYY
        # The whole year
        elif y.isdigit() and is_x_or_(md):
            if check_only: 
                ok = True
            else:
                sp, ep = f'{y}0101', ymd_now if y == y_now else f'{y}1231'
                lst_periods.append( [sp, ep] )
                result = sel_days(np_data_2d, sp, ep)

        # OPTION YYYYMM** | YYYYMM
        # The whole month in a year
        elif ym.isdigit() and is_x_or_(d):
            if check_only: 
                ok = True
            else:
                # Is it the actual month in the actual year? Then actual day
                sp, ep = f'{ym}01', max_date(ymd)
                lst_periods.append( [sp, ep] )
                result = sel_days(np_data_2d, sp, ep)

        # ADVANCED OPTIONS for more different periods in a given period
        # OPTION ****MM** | ****MM
        # Get selected month in all the years
        elif y == x4 and m.isdigit() and is_x_or_(d):
            if check_only: 
                ok = True
            else:
                for y in utils.l_years(dys, dye):
                    d  = days_in_month(y, m)
                    sp = f'{y}{m}01'
                    if int(sp) > int(ymd_now):
                        break
                    else:
                        if y == y_now:
                            if m == m_now:
                                d = d_now
                        ep = f'{y}{m}{d}'
                    lst_periods.append( [sp, ep] )
                    result = np_merge(result, sel_days(np_data_2d, sp, ep))

        # OPTION ****MMDD
        # Get the day for every available year
        elif y == x4 and md.isdigit():
            if check_only: 
                ok = True
            else:
                for y in utils.l_years(dys, dye):
                    p = f'{y}{md}'
                    if int(p) > int(ymd_now):
                        break
                    lst_periods.append( [p, p] )
                    result = np_merge(result, sel_days(np_data_2d, p, p))

    if check_only: 
        return ok
    else:
        return result, lst_periods


def day_only( data, period, mmdd ):
    '''Function selects a day over multiple years'''
    dp = days_period( data, period )
    ymd = dp[:, daydata.YYYYMMDD]
    ymds, ymde = ymd[0], ymd[-1]
    ys, ye = convert.fl_to_s(ymds)[:4], convert.fl_to_s(ymde)[:4]
    result = np.array([])
    for y in utils.l_years(ys, ye):
        p = f'{y}{mmdd}'
        days = days_period(data, p)
        result = np_merge(result, days)

    return result

def month_only( data, period, mm ):
    '''Function selects a month over multiple years'''
    dp = days_period( data, period )
    ymd = dp[:, daydata.YYYYMMDD]
    ymds, ymde = ymd[0], ymd[-1]
    ys, ye = convert.fl_to_s(ymds)[:4], convert.fl_to_s(ymde)[:4]
    result = np.array([])
    for y in utils.l_years(ys, ye):
        p = f'{y}{mm}**' # Get the whole month
        days = days_period(data, p)
        result = np_merge(result, days)

    return result
