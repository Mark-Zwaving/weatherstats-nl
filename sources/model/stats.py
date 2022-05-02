# -*- coding: utf-8 -*-
'''Main statistics object for calculating and saving statistics'''
from cmath import nan
import common.view.console as cnsl
import sources.view.text as text
import sources.model.daydata as daydata
__author__ = "Mark Zwaving"
__email__ = "markzwaving@gmail.com"
__copyright__ = "Copyright (C) Mark Zwaving. All rights reserved."
__license__ = "GNU Lesser General Public License (LGPL)"
__version__ = "0.0.3"
__maintainer__ = "Mark Zwaving"
__status__ = "Development"

import config as cfg
import numpy as np
import sources.model.daydata as daydata
import sources.model.utils as utils

class Days:
    '''Class saves and stores statistics of a station in a given period'''
    np_data_2d   = cfg.np_no_data
    np_period_2d = cfg.np_no_data # This is the array with the period
    np_good_2d   = cfg.np_no_data # This the operatonal np array
    np_good_1d   = cfg.np_no_data # Good 1d entity array
    np_good_keys = cfg.np_no_data # Good keys array
    period    = '*'
    ymd_start = -1.0
    ymd_end   = -1.0

    def __init__(
            self,
            station,     # Station with type data
            np_data,     # Data from a webstation
            period = '*' # Set period from start <optional>
        ):
        self.station = station  # Weather station will be unchanged
        self.np_data_2d = np_data  # All the available data
        self.np_period_2d = np_data  # All the available data
        self.set_period( period ) # Set new data period


    def set_station(self, station):
        self.station = station


    def set_period(self, period):
        if not self.np_data_2d_has_days():
            return

        # Set period
        self.period = period

        # Set data for period
        self.np_period_2d = daydata.sel_period( self.np_data_2d, period )

        if self.np_period_2d_has_days():
            # Start and end dates format -> yyyymmdd
            if self.np_period_2d.size != 0:
                self.np_ymd = self.np_period_2d[:, daydata.etk('yyyymmdd')]
                self.ymd_start = f'{self.np_ymd[0]:.0f}' # Make txt and round 0
                self.ymd_end = f'{self.np_ymd[-1]:.0f}' # Make txt and round 0


    def process_days_1d_2d(self, entity):
        '''Removes nan values based on entity values from np days period 2d . 
           Returns a new 2D np days array'''
        # Reset init 
        key = daydata.etk(entity) # Get key entiy
        np_period_1d = self.np_period_2d[:, key] # Get the entity 1d np array
        row_keys = np.where( ( ~np.isnan( np_period_1d ) ) ) # Get keys with good data
        self.np_good_2d = self.np_period_2d[ row_keys ] # Good days
        self.np_good_1d = self.np_good_2d[:,key] # Good values entities 

        return self.np_good_1d, self.np_good_2d


    # Fn: quick checks
    def count_np_data_2d(self):   return np.size(self.np_data_2d, axis=0)
    def count_np_period_2d(self): return np.size(self.np_period_2d, axis=0)
    def count_np_good_2d(self):   return np.size(self.np_good_2d, axis=0)
    def count_np_good_1d(self):   return np.size(self.np_good_1d, axis=0)

    def npl_has_days(self, npl): return np.size(npl, axis=0) > 0
    def np_data_2d_has_days(self): return self.count_np_data_2d() > 0
    def np_period_2d_has_days(self): return self.count_np_period_2d() > 0
    def np_good_1d_has_days(self): return self.count_np_good_1d() > 0
    def np_good_2d_has_days(self): return self.count_np_good_2d() > 0
    def is_equal(self, np1, np2): return ( np1 == np2 ).all()


    def set_start_yyyymmdd(self, yyyymmdd):
        self.ymd_start = yyyymmdd  # Update start date
        self.period = f'{self.ymd_start}-{self.ymd_end}'  # Make new period
        self.set_period(self.period)  # Update array period


    def set_end_yyyymmdd(self, yyyymmdd):
        self.ymd_end = yyyymmdd
        self.period = f'{self.ymd_start}-{self.ymd_end}'
        self.set_period(self.period)


    def npl_yyyymmdd_from_val_2d(self, npl_2d, raw_val, entity):
        np_ymd_1d = npl_2d[:, daydata.etk('yyyymmdd')]
        np_val_1d = npl_2d[:, daydata.etk(entity)]
        ymd_raw = np_ymd_1d[np.where( np_val_1d == raw_val) ]

        return ymd_raw 


    def sort(
            self,
            entity,
            descend=True  # True -> high to low
         ):
        '''Sorts data based on a entity ie: tx, tg, tn)'''
        self.process_days_1d_2d(entity)  # Remove nan data of entity

        if self.np_good_1d_has_days(): # There are good days, lets sort
            np_sorted_2d = self.np_good_2d[self.np_good_2d[:,daydata.etk(entity)].argsort()]

            # Reverse the matrix (if asked)
            if descend: np_sorted_2d = np.flip(np_sorted_2d, axis=0)

        else: # No correct data found
            np_sorted_2d = cfg.np_no_data

        return np_sorted_2d, Days(self.station, np_sorted_2d)


    def npl_conditional_2d(
            self,
            npl_2d,   # numpy days 2d
            entity,   # TX, TG
            operator, # >, >=, lt, < et cetera
            value     # float
        ):
        '''Function returns keys of days and days np array based on conditionals like TX > 30 for example'''
        np_days_2d = cfg.np_no_data # Init data failure
        self.process_days_1d_2d( entity ) # Remove nan data of entity days 

        if self.npl_has_days( npl_2d ): # There are good days, lets check for days 
            fval = daydata.correct( value, entity ) # Make input value equal to (raw) data in matrix 
            op = operator.lower() # Lowercase operator 
            if op in text.lst_op: # Check if operator is allowed 
                # Get data keys where conditional is True 
                row_keys = 0
                if   op in text.lst_gt: row_keys = np.where( self.np_good_1d  > fval )
                elif op in text.lst_ge: row_keys = np.where( self.np_good_1d >= fval )
                elif op in text.lst_eq: row_keys = np.where( self.np_good_1d == fval )
                elif op in text.lst_lt: row_keys = np.where( self.np_good_1d  < fval )
                elif op in text.lst_le: row_keys = np.where( self.np_good_1d <= fval )
                elif op in text.lst_ne: row_keys = np.where( self.np_good_1d != fval )
                else: cnsl.log( f'Fatal error in operator {op} in terms for day', True )

                np_days_2d = self.np_good_2d[ row_keys ]

            else: # Wrong input
                cnsl.log( f'Fatal error, operator {op} is unknown', True )

        # Return keys, np entities and Days object
        return np_days_2d, Days( self.station, np_days_2d, self.period )


    def npl_conditional_1d(
            self,
            npl_2d,   # numpy days 2d
            entity,   # TX, TG
            operator, # >, >=, lt, < et cetera
            value     # float
        ):
        '''Function returns keys of days and days np array based on conditionals like TX > 30 for example'''
        np_days_2d, _ = self.npl_conditional_2d( npl_2d, entity, operator, value )
        return np_days_2d[:, daydata.etk(entity)]


    def conditional_2d(
            self,
            entity,   # TX, TG
            operator, # >, >=, lt, < et cetera
            value     # float
        ):
        np_days_2d, Days = self.npl_conditional_2d( self.np_period_2d, entity, operator, value )
        return np_days_2d, Days


    def average(
            self, 
            entity
        ):
        '''Calculates the average value for a given entity'''
        ave = cfg.np_no_data  # Init data failure
        self.process_days_1d_2d( entity ) # Remove nan data of entity

        if self.np_good_1d_has_days(): # There are good days
            ave = np.average( self.np_good_1d ) # Calculate average

        return ave, Days(self.station, self.np_good_2d)


    def max(self, entity):
        '''Gets maximum value for a given entity'''
        maxx, np_sorted_2d = cfg.np_no_data, cfg.np_no_data  # Init data failure
        self.process_days_1d_2d( entity ) # Remove nan data of entity
        max_day = ''

        if self.np_good_1d_has_days(): # There are good days
            np_sorted_2d, _ = self.sort( entity, descend=cfg.html_max ) # True -> high to low
            max_day = np_sorted_2d[0,:] # Get max day
            maxx = max_day[daydata.etk(entity)] # Get max value

        return maxx, max_day, Days(self.station, np_sorted_2d)

    def min(self, entity):
        '''Gets maximum value for a given entity'''
        minn, np_sorted_2d = cfg.np_no_data, cfg.np_no_data  # Init data failure
        self.process_days_1d_2d( entity ) # Remove nan data of entity
        min_day = ''

        if self.np_good_1d_has_days(): # There are good days
            np_sorted_2d, _ = self.sort( entity, descend=cfg.html_min ) # True -> high to low
            min_day = np_sorted_2d[0,:] # Get min day
            minn = min_day[daydata.etk(entity)] # Get min value

        return minn, min_day, Days(self.station, np_sorted_2d)

    def sum(self, entity):
        '''Calculates the sum value for a given entity'''
        summ = cfg.np_no_data  # Init data failure
        self.process_days_1d_2d( entity ) # Remove nan data of entity

        if self.np_good_1d_has_days(): # There are good days
            summ = np.sum(self.np_good_1d) # Get the sum

        return summ, Days(self.station, self.np_good_2d)


    def hellmann(self):
        '''Function calculation hellmann in given data'''
        hmann, np_hmann_2d, entity = cfg.np_no_data, cfg.np_no_data, 'tg'  # Init data failure
        self.process_days_1d_2d( entity ) # Remove nan data of entity

        if self.np_good_1d_has_days(): # There are good days
            np_hmann_2d, _ = self.conditional_2d( entity, '<', 0.0 )  # Get all days TG < 0
            np_hmann_1d = np_hmann_2d[:, daydata.etk(entity)]

            hmann = 0.0
            if self.npl_has_days(np_hmann_1d):
                hmann = abs( np.sum(np_hmann_1d) ) # Sum and make positive if tg < 0

        return hmann, Days(self.station, np_hmann_2d)


    def heat_ndx(self):
        '''Function calculates heat-ndx'''
        heat, np_heat_2d, entity = cfg.np_no_data, cfg.np_no_data, 'tg' # Init data failure
        self.process_days_1d_2d( entity ) # Remove nan data of entity

        if self.np_good_1d_has_days(): # There are good days
            np_heat_2d, _ = self.conditional_2d( entity, '>', 18.0 )  # Get all days TG > 18
            np_heat_1d = np_heat_2d[:, daydata.etk(entity)]

            heat = 0.0
            if self.npl_has_days(np_heat_1d):
                heat = np.sum(np_heat_1d - 180.0)  # Sum only above 18 degrees

        return heat, Days(self.station, np_heat_2d)


    def ijnsen(self):
        '''Calculates the cold number ijnsen.
        Count the days of:
        v = TN <  0
        y = TX <  0
        z = TN < -10 
        ijnsen = (v * v / 363.0)  +  (2.0 * y / 3.0)  +  (10.0 * z / 9.0) 
        ???? ERROR TODO
        '''
        ijnsen, np_ijnsen = cfg.np_no_data, cfg.np_no_data # Init data failure 
        np_tx_1d, np_tx_2d = self.process_days_1d_2d( 'tx' )  # Remove nan data of entity
        np_tn_1d, np_tn_2d = self.process_days_1d_2d( 'tn' )  # Remove nan data of entity

       # Get the days V: tn < 0.0
        if self.npl_has_days(np_tn_1d): # There are good days, calculate ijnsen partial
            ijnsen = 0.0 # Start at 0.0
            np_v_2d, _ = self.npl_conditional_2d(np_tn_2d, 'tn', '<', 0.0) # Get all days TN < 0
            if self.npl_has_days(np_v_2d):
                v = np.size(np_v_2d, axis=0)
                ijnsen += v * v / 363.0
                np_ijnsen = np_v_2d

        # Get the days Y: tx < 0
        if self.npl_has_days(np_tx_1d): # There are good days, calculate ijnsen partial
            np_y_2d, _ = self.npl_conditional_2d(np_tx_2d, 'tx', '<', 0.0) # Get all days TX < 0
            if self.npl_has_days(np_y_2d):
                y = np.size(np_y_2d, axis=0)
                ijnsen += 2.0 * y / 3.0

        # Get the days Z: tn < -10.0
        if self.npl_has_days(np_tn_1d): # There are good days, calculate ijnsen partial
            np_z_2d, _ = self.npl_conditional_2d(np_tn_2d, 'tn', '<', -10.0) # Get all days TN < 10.0
            if self.npl_has_days(np_z_2d):
                z = np.size(np_z_2d, axis=0)
                ijnsen += 10.0 * z / 9.0

        return ijnsen, Days(self.station, np_ijnsen)


    def frost_sum(self):
        '''Function calculates frost sum.
        Get all the days with a TX < 0 and TN < 0
        Calculate the sum of all these days and make it absolute (=positive)
        Sum the result tn and tx together 
        '''
        frost, np_frost = cfg.np_no_data, cfg.np_no_data   # Init data failure
        np_tx_1d, np_tx_2d = self.process_days_1d_2d('tx')  # Remove nan data of entity
        np_tn_1d, np_tn_2d = self.process_days_1d_2d('tn')  # Remove nan data of entity

        # Days: tn < 0
        if self.npl_has_days(np_tn_1d): # There are good days, calculate sum: tn < 0
            np_tn_2d, _ = self.npl_conditional_2d( np_tn_2d, 'tn', '<', 0.0 ) # Get all days Tn < 0
            np_tn_1d = np_tn_2d[:, daydata.etk('tn')]

            frost = 0.0
            if self.npl_has_days(np_tn_1d):
                frost += abs( np.sum(np_tn_1d) )

            np_frost = np_tn_2d

        # Days: tx < 0
        if self.npl_has_days(np_tx_1d): # There are good days, calculate sum: txx < 0
            np_tx_2d, _ = self.npl_conditional_2d(np_tx_2d, 'tx', '<', 0.0) # Get all days Tx < 0
            np_tx_1d = np_tx_2d[:, daydata.etk('tx')]

            if self.npl_has_days(np_tx_1d):
                frost += abs( np.sum(np_tx_1d) )

        return frost, Days( self.station, np_frost)


    def climate_average_periode_in_year(self, start_year, end_year, smmdd, emmdd, entity):
        '''Function calculates climate averages over a period in a year'''
        # YYYYMMDD-YYYY*MMDD*
        # Special period for a day during the years
        self.set_period(f'{start_year}*{smmdd}*-{end_year}*{emmdd}*')
        ave, Days = self.average(entity)  # Calculate averages

        return ave, Days


    def climate_average_for_a_day(self, start_year, end_year, mmdd, entity):
        '''Function calculate climate averages for a day for a station'''
        # yyyymmdd-yyyymmdd*
        # Special period for a day during the years
        self.set_period(f'{start_year}-{end_year}{mmdd}*')
        ave, Days = self.average(entity)

        return ave, Days


    def query(self, query):
        # Sanitize and split too lst
        query = query.replace('\s+', ' ').strip()  
        lst = query.split(' ')

        ok, err = utils.query_ok(query) # Check query

        if ok:
            i, max = 0, len(query.split(' '))
            # Get first conditional days
            ent,  i = lst[i], i + 1
            op,   i = lst[i], i + 1
            val,  i = lst[i], i + 1
            np_2d_1, _ = self.conditional_2d(ent, op, val) # Get days

            while i < max: # There is more
                and_or, i = lst[i], i + 1  # And | or

                # Get days next condition
                ent = lst[i]; i += 1
                op  = lst[i]; i += 1
                val = lst[i]; i += 1 # For next

                # Get conditional np array
                np_2d_2, _ = self.conditional_2d(ent, op, val) 

                # Make new days And | or
                if and_or in text.lst_or: # OR = is simple plus days
                    np_2d_1 = np.vstack( (np_2d_1, np_2d_2) ) # ok!

                elif and_or in text.lst_and: # And is merge only same days
                    key_ymd, key_stn = daydata.etk('yyyymmdd'), daydata.etk('stn')
                    # ymd_1, ymd_2 = np_2d_1[:, key_ymd], np_2d_2[:, key_ymd]
                    # stn_1, stn_2 = np_2d_1[:, key_stn], np_2d_2[:, key_stn]
                    # np_2d_1 = np_2d_1[ np.where( (ymd_1 == ymd_2) & (stn_1 == stn_2) ) ]
                    # ? 

                    lst_days_2d = []
                    # Check if on same day
                    for day_1 in np_2d_1:
                        for day_2 in np_2d_2:
                            if day_1[key_ymd] == day_2[key_ymd] and \
                               day_1[key_stn] == day_2[key_stn]: # Same days of same stations add to lst
                               lst_days_2d.append(day_1) 
                    np_2d_1 = np.array( lst_days_2d )

                np_2d_1 = np.unique( np_2d_1, axis=0 ) # No same days double

        if ok:
            np_2d_1 = np.unique(np_2d_1, axis=0)
            return np_2d_1, Days( self.station, np_2d_1)
        else:
            cnsl.log( err, cfg.error )
            return False, False
