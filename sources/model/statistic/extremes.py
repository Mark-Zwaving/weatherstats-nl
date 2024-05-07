# -*- coding: utf-8 -*-
'''
Library contains function for the calculation of the extremes values for an given entity
'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.0.3'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import sources.model.statistic.minimum as minimum
import sources.model.statistic.maximum as maximum

def calculate(np_lst_days, entity):
    '''Calculates the maximum en minimum value for a given entity'''

    mini, np_day_min = minimum.calculate(np_lst_days, entity) # Calculate minimum
    maxi, np_day_max = maximum.calculate(np_lst_days, entity) # Calculate maximum

    return mini, np_day_min, maxi, np_day_max
