# -*- coding: utf-8 -*-
'''
Library contains a function for the calculation of the climate indeces
E.g: hellmann, heat-ndx, frostsum
'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.0.3'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import sources.model.dayvalues.select as select
import sources.model.statistic.indexes.heat as heat 
import sources.model.statistic.indexes.hellmann as hellmann
import sources.model.statistic.indexes.frostsum as frostsum
import sources.model.statistic.indexes.ijnsen as ijnsen 
import sources.view.text as text

def calculate(
        np_lst_days, 
        entity   # Type entity index -> frostsum, heat-ndx
    ):
    '''Calculates the mean value for a given entity'''
    ndx = cfg.no_val

    # Get the clima days
    np_days_clima = select.clima_days(np_lst_days)

    if entity in text.lst_heat_ndx:
        ndx, _ = heat.calculate_nl(np_days_clima)

    elif entity in text.lst_helmmann:
        ndx, _ = hellmann.calculate(np_days_clima)

    elif entity in text.lst_frost_sum:
        ndx, _, _, _, _, _, _ = frostsum.calculate_nl(np_days_clima)

    elif entity in text.lst_ijnsen:
        ndx, _ = ijnsen.calculate(np_days_clima)

    if ndx != cfg.no_val:
        ndx /= 30.0 # Just divide by 30 years
        ndx = round(ndx, 1)

    return ndx
