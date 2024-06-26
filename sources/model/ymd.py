# -*- coding: utf-8 -*-
'''Functions date time base handling'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.1.0'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import numpy as np
import datetime, time
import sources.view.console as cnsl

# Short Quick fn
yyyy = lambda: datetime.datetime.now().strftime('%Y')
mm   = lambda: datetime.datetime.now().strftime('%m')
dd   = lambda: datetime.datetime.now().strftime('%\d')
HH   = lambda: datetime.datetime.now().strftime('%H')
MM   = lambda: datetime.datetime.now().strftime('%M')
SS   = lambda: datetime.datetime.now().strftime('%S')

# Quick txt lists
lst_m    = ['1','2','3','4','5','6','7','8','9','10','11','12']
lst_mm   = ['01','02','03','04','05','06','07','08','09','10','11','12']
lst_mmm  = ['jan','feb','mar','apr','mai','jun','jul','aug','sep','okt','nov','dec']
lst_mmmm = ['january','february','march','april','mai','june','july',
            'august','september','oktober','november','december']
lst_months_all = lst_m + lst_mm + lst_mmm + lst_mmmm

dd01, dd02, dd03, dd04, dd05, dd06 = 31, 29, 31, 30, 31, 30
dd07, dd08, dd09, dd10, dd11, dd12 = 31, 31, 30, 31, 30, 31
lst_dd = [dd01, dd02, dd03, dd04, dd05, dd06, dd07, dd08, dd09, dd10, dd11, dd12]

# Maximum days in month
jan = [str(i+1).zfill(2) for i in range(dd01)]
feb = [str(i+1).zfill(2) for i in range(dd02)]
mar = [str(i+1).zfill(2) for i in range(dd03)]
apr = [str(i+1).zfill(2) for i in range(dd04)]
mai = [str(i+1).zfill(2) for i in range(dd05)]
jun = [str(i+1).zfill(2) for i in range(dd06)]
jul = [str(i+1).zfill(2) for i in range(dd07)]
aug = [str(i+1).zfill(2) for i in range(dd08)]
sep = [str(i+1).zfill(2) for i in range(dd09)]
okt = [str(i+1).zfill(2) for i in range(dd10)]
nov = [str(i+1).zfill(2) for i in range(dd11)]
dec = [str(i+1).zfill(2) for i in range(dd12)]

lst_mmdd01 = [f'01{dd}' for dd in jan]
lst_mmdd02 = [f'02{dd}' for dd in feb]
lst_mmdd03 = [f'03{dd}' for dd in mar]
lst_mmdd04 = [f'04{dd}' for dd in apr]
lst_mmdd05 = [f'05{dd}' for dd in mai]
lst_mmdd06 = [f'06{dd}' for dd in jun]
lst_mmdd07 = [f'07{dd}' for dd in jul]
lst_mmdd08 = [f'08{dd}' for dd in aug]
lst_mmdd09 = [f'09{dd}' for dd in sep]
lst_mmdd10 = [f'10{dd}' for dd in okt]
lst_mmdd11 = [f'11{dd}' for dd in nov]
lst_mmdd12 = [f'12{dd}' for dd in dec]

lst_mmdd  = lst_mmdd01 + lst_mmdd02 + lst_mmdd03 + lst_mmdd04 + lst_mmdd05 + lst_mmdd06
lst_mmdd += lst_mmdd07 + lst_mmdd08 + lst_mmdd09 + lst_mmdd10 + lst_mmdd11 + lst_mmdd12

def symd(yyyymmdd):
    '''Date always to string'''
    # if   type(yyyymmdd) is str: return yyyymmdd
    if type(yyyymmdd) is str: 
        ymd = yyyymmdd.strip()
    elif type(yyyymmdd) is int: 
        ymd = str(yyyymmdd)
    elif type(yyyymmdd) is float: 
        ymd = str(int(yyyymmdd))
    elif isinstance(yyyymmdd, np.floating): 
        ymd = str(int(yyyymmdd)) # np.around(yyyymmdd).astype('str')

    return ymd
 
def is_yyyymmdd(
        yyyymmdd, # Date
        verbose = cfg.verbose
    ):
    '''Function validates a date. 
       Allowed date formats are
       1. yyyymmdd 
       2. yyyy-mm-dd
       3. yyyy mm dd
    '''
    ok, symd = False, symd(yyyymmdd)

    if symd.find('-'): # Given format is <yyyymmdd>
        symd = symd.replace('-', '') 
    elif symd.find(' '): # Given format is <yyyy mm dd>
        symd = symd.replace('-', '') 

    # Validate the date
    if len(symd) != 8:
        t = f'[{now()}] Date has wrong length. Correct length must be 8'
        cnsl.log(t, cfg.error)

    elif not symd.isdigit():
        t = f'[{now()}] Date must only contain digits'
        cnsl.log(t, cfg.error)

    else:
        try:
            y, m, d = split_yyyymmdd(symd)
            d = datetime.datetime( int(y), int(m), int(d) )

        except Exception as e:
            t = f'[{now()}] Error in check is_yyyymmdd().\nDate {yyyymmdd}\n{e}'
            cnsl.log(t, cfg.error)
            
        else:
            t = f'[{now()}] Validate date success'
            cnsl.log(t, verbose)
            ok = True

    cnsl.log(f'[{now()}] End validate date {yyyymmdd}', verbose)

    return ok

def yyyymmdd_to_text(yyyymmdd):
    yymmdd = symd(yyyymmdd)
    try:
        txt_ymd = datetime.datetime.strptime(yymmdd, '%Y%m%d').strftime('%A, %d %B %Y')
    except Exception as e:
        err = f'Error in ymd yyymmdd_to_text()\nDate {yymmdd}\n{e}'
        cnsl.log(err, cfg.error)
    else:
        return txt_ymd

    return yymmdd

def month_num_to_text( m, lang='en' ):
    lst, key = [], 0
    if lang == 'en': key = 0
    if lang == 'nl': key = 1

    if    m in ['01','1', 1]: lst = ['january','januari']
    elif  m in ['02','2', 2]: lst = ['february','februari']
    elif  m in ['03','3', 3]: lst = ['march','maart']
    elif  m in ['04','4', 4]: lst = ['april','april']
    elif  m in ['05','5', 5]: lst = ['mai','mei']
    elif  m in ['06','6', 6]: lst = ['june','juni']
    elif  m in ['07','7', 7]: lst = ['july','juli']
    elif  m in ['08','8', 8]: lst = ['august','augustus']
    elif  m in ['09','9', 9]: lst = ['september','september']
    elif  m in ['10', 10]:    lst = ['oktober','october']
    elif  m in ['11', 11]:    lst = ['november','november']
    elif  m in ['12', 12]:    lst = ['december','december']

    return  lst[key]

def text_datetime_now():
    return datetime.datetime.now().strftime('%A, %d %B %Y %H:%M:%S')

# ?????
def is_leap(yyyy):
    y = int(yyyy)
    if y % 4 == 0:
        if y % 100 == 0:
            if y % 400 == 0:
                return True
        else:
            return True
    
    return False

def valid_yyyymmdd( yyyymmdd ):
    ok = True 
    yyyymmdd = symd(yyyymmdd)
    try:
        yyyy, mm, dd = yyyymmdd[:4], yyyymmdd[4:6], yyyymmdd[6:8]
        d = datetime.datetime( int(yyyy), int(mm), int(dd) )
    except Exception as e:
        err = f'Error in ymd valid_yyyymmdd() \nDate {yyyymmdd} \n{e}'
        cnsl.log(err, cfg.error)
        ok = False

    return ok

def valid_mmdd( mmdd ):
    '''Check mmdd for possibility'''
    ok, mm, dd  = False, mmdd[:2], mmdd[2:]

    if   mm == '01' and dd in jan: ok = True
    elif mm == '02' and dd in feb: ok = True
    elif mm == '03' and dd in mar: ok = True
    elif mm == '04' and dd in apr: ok = True
    elif mm == '05' and dd in mai: ok = True
    elif mm == '06' and dd in jun: ok = True
    elif mm == '07' and dd in jul: ok = True
    elif mm == '08' and dd in aug: ok = True
    elif mm == '09' and dd in sep: ok = True
    elif mm == '10' and dd in okt: ok = True
    elif mm == '11' and dd in nov: ok = True
    elif mm == '12' and dd in dec: ok = True

    return ok

def valid_dd( d ):
    if d in jan: 
        return True
    return False

def valid_mm( m ):
    months = [str(i+1).zfill(2) for i in range(12)] # Month num with leading zero
    return True if m in months else False

def days_in_month( m ):
    if   m in ['01','1', 1]: return jan[-1]
    elif m in ['02','2', 2]: return feb[-1]
    elif m in ['03','3', 3]: return mar[-1]
    elif m in ['04','4', 4]: return apr[-1]
    elif m in ['05','5', 5]: return mai[-1]
    elif m in ['06','6', 6]: return jun[-1]
    elif m in ['07','7', 7]: return jul[-1]
    elif m in ['08','8', 8]: return aug[-1]
    elif m in ['09','9', 9]: return sep[-1]
    elif m in ['10', 10]: return okt[-1]
    elif m in ['11', 11]: return nov[-1]
    elif m in ['12', 12]: return dec[-1]

def month_num_to_mmmm( n ):
    return lst_mmmm[int(n)-1]

def month_to_mm( mm ):
    m = str(mm).lower()
    if m in [  1,  '1', '01', 'january',   'jan']:  return '01'
    if m in [  2,  '2', '02', 'februari',  'feb']:  return '02'
    if m in [  3,  '3', '03', 'march',     'mar']:  return '03'
    if m in [  4,  '4', '04', 'april',     'apr']:  return '04'
    if m in [  5,  '5', '05', 'mai',       'may']:  return '05'
    if m in [  6,  '6', '06', 'june',      'jun']:  return '06'
    if m in [  7,  '7', '07', 'july',      'jul']:  return '07'
    if m in [  8,  '8', '08', 'august',    'aug']:  return '08'
    if m in [  9,  '9', '09', 'september', 'sep']:  return '09'
    if m in [ 10, '10',       'oktober',   'okt']:  return '10'
    if m in [ 11, '11',       'november',  'nov']:  return '11'
    if m in [ 12, '12',       'december',  'dec']:  return '12'
    return -1 # Not found

def month_name_to_num ( name ):
    ndx = 0
    for mmm, mmmm in zip(lst_mmm, lst_mmmm):
        if name in [mmm,mmmm]:
            return ndx
        ndx += 1
    else:
        return -1 # Name not found

def m_to_mmmm ( m ):
    return lst_mmmm[int(m)-1] if str(m) in lst_m else -1

def m_to_mmm ( m ):
    return lst_mmm[ int(m)-1] if str(m) in lst_m else -1

def mm_to_mmmm( mm ): 
    return lst_mmmm[int(mm)-1] if mm in lst_mm else -1

def mm_to_mmm( mm ): 
    return lst_mmm[ int(mm)-1] if mm in lst_mm else -1

def mmm_to_m( mmm ): 
    return str(month_name_to_num(mmm))

def mmm_to_mm( mmm ): 
    return f'{month_name_to_num(mmm):0>2}'

def shms(hhmmss):
    '''Time always to string'''
    if type(hhmmss) is int: return str(hhmmss)
    elif type(hhmmss) is float: return str(int(round(hhmmss)))

    return hhmmss

def now():
    '''Function returns a date time string'''
    y, m, d, H, M, S = y_m_d_h_m_s_now()
    return f'{y}-{m}-{d} {H}:{M}:{S}'

def hhmmss_now():
    '''Function gets current time in hours, minutes and seconds format <hhmmss>'''
    return datetime.datetime.now().strftime('%H%M%S')

def yyyymmdd_now():
    '''Function gets current year, month and day in string format <yyyymmdd>.'''
    return datetime.datetime.now().strftime('%Y%m%d')

def time_now():
    '''Function gets current time in hours, minutes and seconds format <hhmmss>'''
    return datetime.datetime.now().strftime('%H:%M:%S')

def yyyy_mm_dd_now():
    '''Function gets current year, month and day in string format yyyy, mm, dd .'''
    return split_yyyymmdd( yyyymmdd_now() )

def hh_mm_ss_now():
    '''Function returns the current time in hours, minutes and seconds format hh, mm, ss
       with leading seconds'''
    return split_hhmmss( hhmmss_now() )

def y_m_d_h_m_s_now():
    '''Function returns current yyyy year, month mm, day dd, hour hh,
       minutes mi, seconds ss, with leading zeros'''
    y, m, d = yyyy_mm_dd_now()
    H, M, S = hh_mm_ss_now()
    return y, m, d, H, M, S

def yyyy_mm_dd_HH_MM_SS_now():
    return y_m_d_h_m_s_now()

def ymdhms_now():
    return f'{yyyymmdd_now()}{hhmmss_now()}'

def split_yyyymmdd(
        yyyymmdd # Format yyyymmdd
    ):
    '''Function will slice the string the three parts yyyy, mm and dd'''
    ymd = symd(yyyymmdd)
    return ymd[:4], ymd[4:6], ymd[6:8]

def split_yyyy_mm_dd(
        yyyy_mm_dd # Format yyyy-mm-dd
    ):
    '''Function will split the string the three parts yyyy, mm and dd'''
    return yyyy_mm_dd.split('-')

def split_hhmmss(
        hhmmss # Format hhmmss
    ):
    '''Function will slice the string in three parts hh, mm and dd'''
    hms = shms(hhmmss)
    return hms[:2], hms[2:4], hms[4:6]

def split_hh_mm_ss(
        hh_mm_ss # Format hh:mm:ss
    ):
    '''Function will split the timestring by : in three parts hh, mm and dd'''
    return hh_mm_ss.split(':')

def split_yyyymmdd_hhmmss(
        yyyymmdd,
        hhmmss
    ):
    hh, mm, ss = split_hhmmss(hhmmss) # Format hhmmss
    y, m, d = split_yyyymmdd(symd(yyyymmdd))
    return y, m, d, hh, mm, ss

def split_yyyymmdd_hh_mm_ss(
        yyyymmdd,
        hh_mm_ss
    ):
    hh, mm, ss = split_hh_mm_ss(hh_mm_ss) # Format hhmmss
    y, m, d = split_yyyymmdd(symd(yyyymmdd))
    return y, m, d, hh, mm, ss

def hh_mm_ss_plus_second(
        hh_mm_ss = cfg.e, # Time string format hh:mm:ss
        second = 1     # Seconds to add
    ):
    '''Function adds seconds to time string, format hh:mm:ss'''
    # if time hh_mm_ss not given get current time
    hh, mm, ss = hh_mm_ss.split(':') if hh_mm_ss else hh_mm_ss_now()
    y, m, d = yyyy_mm_dd_now()
    dt = datetime.datetime(int(y),int(m),int(d),int(hh),int(mm),int(ss))+datetime.timedelta(seconds=second)
    return dt.strftime('%H:%M:%S')

def hh_mm_ss_minus_second(
        hh_mm_ss = cfg.e, # Time string format hh:mm:ss
        second = 1     # Seconds to substract
    ):
    '''Function substract seconds of time string, format hh:mm:ss'''
    return hh_mm_ss_plus_second( hh_mm_ss, -second) # Just make seconds negative

def hh_mm_ss_plus_minute(
        hh_mm_ss = cfg.e, # Time string format hh:mm:ss
        minute = 1 # Minutes to add
    ):
    '''Function adds minutes to time string, format hh:mm:ss'''
    return hh_mm_ss_plus_second(hh_mm_ss, minute * cfg.sec_minute)

def hh_mm_ss_minus_minute(
        hh_mm_ss = cfg.e, # Time string format hh:mm:ss
        minute = 1 # Minutes to substract
    ):
    '''Function substract minutes of time string, format hh:mm:ss'''
    return hh_mm_ss_plus_minute( hh_mm_ss, -minute)

def hh_mm_ss_plus_hour(
        hh_mm_ss = cfg.e, # Time string format hh:mm:ss
        hour = 1 # Hours to add
    ):
    '''Function adds hours to time string, format hh:mm:ss'''
    return hh_mm_ss_plus_second(hh_mm_ss, hour * cfg.sec_hour)

def hh_mm_ss_minus_hour(
        hh_mm_ss = cfg.e, # Time string format hh:mm:ss
        hour = 1  # Hours to substract
    ):
    '''Function substracts hours of time string, format hh:mm:ss'''
    return hh_mm_ss_plus_hour(hh_mm_ss, -hour)

def yyyymmdd_plus_second(
        yyyymmdd = cfg.e,  # Date to add the seconds to
        second  = 0    # Seconds to add/substract seconds to date
    ):
    '''Functions adds or substracts one or more seconds to a given date'''
    yyyymmdd = symd(yyyymmdd) if yyyymmdd else yyyymmdd_now() # If empty get current date
    y, m, d = split_yyyymmdd( yyyymmdd ) # Split date
    dt_new = datetime.datetime(int(y),int(m),int(d)) + datetime.timedelta(seconds=second)
    return dt_new.strftime('%Y%m%d') # Return new yyyymmmdd string

def yyyymmdd_minus_sec(
        yyyymmdd = cfg.e,  # Date to add the seconds to
        second  = 0    # Seconds to substract seconds to date
    ):
    return yyyymmdd_plus_second(symd(yyyymmdd), -second)

def yyyymmdd_plus_hour(
        yyyymmdd = cfg.e,  # String date format is <yyyymmdd>
        hour = 1       # Integer/float add hours to a current day,
    ):
    '''Add or substract one or more days from date format <yyyymmdd>.
       If date is not given is uses current date.'''
    return yyyymmdd_plus_second(symd(yyyymmdd), hour * cfg.sec_hour)  # Add the hours seconds to date

def yyyymmdd_minus_hour(
        yyyymmdd = cfg.e,  # String date format is <yyyymmdd>
        hour = 1       # Integer/float substract hours from current day,
    ):
    return yyyymmdd_plus_hour(symd(yyyymmdd), -hour)

def yyyymmdd_plus_day(
        yyyymmdd = cfg.e, # String date format is <yyyymmdd>
        day = 1        # Integer/float add if positive and substract if negative days from current day,
    ):
    '''Add or substract one or more days from date format <yyyymmdd>.
       If date is not given is uses current date.'''
    return yyyymmdd_plus_second(symd(yyyymmdd), day * cfg.sec_day)  # Add the day seconds to date

def yyyymmdd_minus_day(
        yyyymmdd = cfg.e, # String date format is <yyyymmdd>
        day = 1        # Integer/float add if positive and substract if negative days from current day,
    ):
    return yyyymmdd_plus_day(yyyymmdd, -day)

def yyyymmdd_plus_week(
        yyyymmdd = cfg.e, # String date format is <yyyymmdd>
        week = 1       # Integer/float add if positive and substract if negative days from current day,
    ):
    '''Add or substract one or more days from date format <yyyymmdd>.
       If date is not given is uses current date.'''
    return yyyymmdd_plus_second(symd(yyyymmdd), week * cfg.sec_week)  # Add the week seconds to date

def yyyymmdd_next_month(yyyymmdd):
    '''Get date of next month in format <yyyymmdd>'''
    yyyy, mm , dd = split_yyyymmdd(yyyymmdd)
    if mm == '12': 
        yyyy, mm = str(int(yyyy) + 1), '01'
    else: 
        mm = str(int(mm) + 1)

    return f'{yyyy}{mm}{dd}'

def yyyymmdd_last_month(yyyymmdd):
    '''Get date of next month in format <yyyymmdd>'''
    yyyy, mm , dd = split_yyyymmdd(yyyymmdd)
    if mm == '01': 
        yyyy, mm = str(int(yyyy) + 1), '12'
    else: 
        mm = str(int(mm) - 1)

    return f'{yyyy}{mm}{dd}'

def yyyymmdd_next_day( yyyymmdd ):
    '''Get date of next day in format <yyyymmdd>'''
    return yyyymmdd_plus_day(yyyymmdd, 1)

def yyyymmdd_previous_day( yyyymmdd ):
    '''Get date of next day in format <yyyymmdd>'''
    return yyyymmdd_minus_day(yyyymmdd, 1)

def yyyymmdd_next_week( yyyymmdd ):
    '''Get date of next week in format <yyyymmdd>'''
    return yyyymmdd_plus_week(yyyymmdd, 1)

def yyyymmdd_previous_week( yyyymmdd ):
    '''Get date of previous week in format <yyyymmdd>'''
    return yyyymmdd_plus_week(yyyymmdd, -1)

def yyyymmdd_range_lst(ymds, ymde, verbose=cfg.verbose): # Probably slow fn
    '''Function makes a ordered list of dates with format yyyymmdd'''
    ok = False
    cnsl.log(f'[{now()}] date list', verbose)
    cnsl.log(f'From {symd(ymds)} to {symd(ymde)}', verbose)
    res, iymds, iymde = [], int(ymds), int(ymde) # Make int to compare
    reverse = True if iymds > iymde else False # Check reverse order
    if reverse: imem = iymds; iymds = iymde; iymde = imem # Swap start, end if reverse
    while iymds <= iymde: # Make a list with ordered dates
        cnsl.log_r(f'{iymds} - {iymde}', verbose)
        res.append(iymds)
        iymds = int( yyyymmdd_plus_day(iymds) ) # Get next day
    if reverse: res.reverse() # Reverse list, if True
    cnsl.log(f'End make a range date list', verbose)
    return res

def epoch_act():
    '''Function returns current epoch seconds (integer)'''
    return int(time.time())

def dt_to_epoch(
        yyyymmdd, # String date format <yyyymmdd>
        hh_mm_ss  # String time format <HH:MM:SS>
    ):
    '''Function converts a date time string with the format 'yyyymmdd-HH:MM'
       to epoch seconds'''
    y, m, d, hh, mm, ss = split_yyyymmdd_hh_mm_ss(yyyymmdd, hh_mm_ss )
    dt = datetime.datetime.fromisoformat(f'{y}-{m}-{d} {hh}:{mm}:{ss}.000')
    return int( dt.timestamp() ) # Return integer epoch seconds

def epoch_to_yyyymmdd(
        epoch = 0 # Epoch seconds
    ):
    '''Function translate epoch seconds to ymd with format: yyyymmdd'''
    return datetime.datetime.fromtimestamp(epoch).strftime('%Y%m%d')

def is_time_shift(
        epoch_1, # First time (seconds)
        epoch_2, # Second time (seconds)
        diff=cfg.sec_minute # Difference in time to check for (seconds)
    ):
    '''Function check if there is a timeshift of default one minute'''
    return True if abs(epoch_1 - epoch_2) >= diff else False
