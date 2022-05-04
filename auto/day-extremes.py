# -*- coding: utf-8 -*-
'''Library contains functions for calculating extremes for a day.'''
__author__ = 'Mark Zwaving'
__email__ = 'markzwaving@gmail.com'
__copyright__ = 'Copyright (C) Mark Zwaving. All rights reserved.'
__license__ = 'GNU Lesser General Public License (LGPL)'
__version__ = '0.0.1'
__maintainer__ = 'Mark Zwaving'
__status__ = 'Development'
# Calculate day extremes y

# To get access to all the code from weathersstats,
# add the root map from weatherstats to sys.path.
import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))

# Import weatherstats libraries
import config as cfg, stations  
import sources.model.stats_tables as stats_tables
import common.model.ymd as ymd 

# See all the files made
cfg.verbose = True 


################################################################################
# This options dictionary needs to be filled in for the calulating of the 
# extremes for a day

# Day to calculate the extremes for
mmdd = "0101" 
options = {
    # Title for table Januari 01 
    'title': f'dayextremes {mmdd}',
    # List with the stations to add in the table 
    'lst-stations': stations.lst,
    # Global period: * for all
    'period': '*',                    
    # This is the period string for the calculation of one day
    'period-2': f'****{mmdd}*',              
    # The table statistics cells - max_tx, min_tn - et cetera
    'lst-sel-cells': cfg.lst_cells_my_extremes, 
    # Output file type: html 
    'file-type': 'html',
    # Name for the file 
    'file-name': f'day-extremes-{mmdd}',
    # Leave empthy. Its not a compare table
    'period-cmp': '',   
    # Leave empthy. Its not search for day table
    's4d-query': '', 
}
# stats_tables.calculate(options)


################################################################################
# Example calculate extremes for a day
def extremes_for_a_day(mmdd):
    options = {
        'title': f'dayextremes {mmdd}',
        'lst-stations': stations.lst,
        'period': '*',                    
        'period-2': f'****{mmdd}*',              
        'lst-sel-cells': cfg.lst_cells_my_extremes, 
        'file-type': 'html',
        'file-name': f'day-extremes-{mmdd}',
        'period-cmp': '',   
        's4d-query': '', 
    }
    stats_tables.calculate(options)


################################################################################
# Example yesterday extremes
def yesterday_extremes():
    today = ymd.yyyymmdd_now() # Get today
    yesterday = ymd.yyyymmdd_minus_day(today, 1)
    mmdd = yesterday[4:]
    period_1 = '*'
    period_2 = f'****{mmdd}*'
    options = { 
        'title': f'dayextremes {mmdd}',
        'lst-stations': stations.lst, 
        'period': period_1,
        'period-2': period_2, 
        'period-cmp': '',
        'lst-sel-cells': cfg.lst_cells_my_extremes, 
        's4d-query': '', 
        'file-type': 'html',
        'file-name': f'day-extremes-{mmdd}'
    }
    stats_tables.calculate(options)


################################################################################
# Example for all days all time
def all_time_all_days():
    today = ymd.yyyymmdd_now()
    for _ in range(366):
        today = ymd.yyyymmdd_minus_day( today, 1 )
        mmdd = today[4:] # Get day
        extremes_for_a_day(mmdd) # Calulate the extremes


if __name__ == '__main__':
    pass
    # yesterday_extremes()
    all_time_all_days()
