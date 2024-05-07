# -*- coding: utf-8 -*-
'''Library gives a np days list based on a query. E.g: tx > 25'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.1.6'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import numpy as np
import sources.model.dayvalues.data as data
import sources.model.check as chk
import sources.model.statistic.conditional as conditional
import sources.view.text as text 

def is_base_query(query):
    '''Functions check if a simple query (three part) is valid'''
    # Clean up query 
    query = text.clean(query)

    # Split query in parts
    lst_query = query.split(' ')

    # Count parts
    cnt_parts = len(lst_query)

    # Parts count must be 3
    if cnt_parts != 3:
        return False

    # Query format
    entity, operator, value = lst_query

    # First part must be an entity
    if not data.is_entity(entity):
        return False
    
    # Second part must be an operator
    if operator.lower() not in text.lst_op_relat:
        return False
    
    # Thrid part is a value must be integer or a float
    if not (chk.is_float(value) or chk.is_int(value)):
        return False
    
    return True

def is_long_query(query):
    '''Checks if its an long query'''
    # Clean up query 
    query = text.clean(query)

    # Split query in parts
    lst_query = query.split(' ')

    # Count parts
    cnt_parts = len(lst_query)

    # Parts count must be 3
    if cnt_parts < 7:
        return False
    
    return True

def is_query(query):
    '''Functions check if query is valid'''
    # Clean up query 
    query = text.clean(query)
    query = query.lower()

    if is_base_query(query):
        return True

    # Must have and | or
    elif is_long_query(query): 
        
        has_and, has_or = query.find('and'), query.find('or')

        if has_and != -1:
            q1, q2 = query.split('and')

            return is_query(q1) and is_query(q2)
            
        elif has_or == -1:
            q1, q2 = query.split('or')

            return is_query(q1) and is_query(q2)
    
    return False


def calculate(np_lst_days, query):
    ok = True
    np_lst_res = np.array([])
    # Sanitize query 
    query = text.clean(query)

    if not is_query(query):
        return False, np_lst_res
    
    # For the short query
    if is_base_query(query):
        # Split in 3 partt
        ent, op, val = query.split('or')
        
        # Get the days for the query
        ok, np_lst_res, _ = conditional.calculate(np_lst_days, ent, op, val)

        return ok, np_lst_res

    elif is_long_query(query):
        # Split in and | or 
        # Check base queries 
        # Select days based on query 

        # Check for which logical operator
        has_and, has_or = query.find('and'), query.find('or')

        # Check for an or
        if has_or != -1:
            # Split in or
            q1, q2 = query.split('or') 

            # Get the days for query 1
            ok1, np_lst_res1 = calculate(np_lst_days, q1)

            # Get the days for query 2
            ok2, np_lst_res2 = calculate(np_lst_days, q2)

            if ok1 and ok2:
                np_lst_res = np_lst_res1 or np_lst_res2
            elif ok1:
                np_lst_res = np_lst_res1
            elif ok2:
                np_lst_res = np_lst_res2
            else:
                # No days
                ok = False

            return ok, np_lst_res

        # Check for an and 
        elif has_and != -1:
            # Split in and
            q1, q2 = query.split('and') 

            # Get the days for query 1
            ok1, np_lst_res1 = calculate(np_lst_days, q1)

            # Get the days for query 2
            ok2, np_lst_res2 = calculate(np_lst_days, q2)

            if ok1 and ok2:
                np_lst_res = np_lst_res1 and np_lst_res2
            elif ok1:
                np_lst_res = np_lst_res1
            elif ok2:
                np_lst_res = np_lst_res2
            else:
                # No days
                ok = False

        return ok, np_lst_res
