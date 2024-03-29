'''Library helper fn for answers (checks)'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 3 - GPLv3'
__version__    =  '0.0.4'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import sources.view.text as text

# Makes versatile answers possible (list or string)
def lst_to_str(answ):
    if type(answ) == list:
        answ = str(answ[0]) if len(answ) > 0 else cfg.e

    return answ

def is_quit(answ):
    if type(answ) == list:
        if answ == text.lst_quit:
            answ = text.lst_quit[0]
        else:
            answ = lst_to_str(answ)
    else:
        answ = str(answ)

    return text.clear(answ).lower() in text.lst_quit

def is_yes(answ):
    if type(answ) == list:
        if answ == text.lst_yess:
            answ = text.lst_yess[0]
        else:
            answ = lst_to_str(answ)
    else:
        answ = str(answ)

    return text.clear(answ).lower() in text.lst_yess

def is_no(answ):
    if type(answ) == list:
        if answ == text.lst_no:
            answ = text.lst_no[0]
        else:
            answ = lst_to_str(answ)
    else:
        answ = str(answ)

    return text.clear(answ).lower() in text.lst_no

def is_empty(answ):
    if type(answ) == list:
        if answ == []:
            answ = cfg.e
        else:
            answ = lst_to_str(answ)
    else:
        answ = str(answ)

    return False if answ.strip() else True

def is_prev(answ):
    if type(answ) == list:
        if answ == text.lst_prev:
            answ = text.lst_prev[0]
        else:
            answ = lst_to_str(answ)
    else:
        answ = str(answ)

    return text.clear(answ).lower() in text.lst_prev

def is_back(answ):
    if type(answ) == list:
        if answ == text.lst_back:
            answ = text.lst_back[0]
        else:
            answ = lst_to_str(answ)

    return text.clear(answ).lower() in text.lst_back