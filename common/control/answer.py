'''Library helper fn for answers (checks)'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.0.1"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import common.view.txt as txt

# Makes versatile answers possible (list or string)
def answer_lst_to_str(answ):
    if type(answ) == list:
        answ = str(answ[0]) if len(answ) > 0 else ''

    return answ

# Check answer functions. Answ can be list or str
def quit(answ): 
    s = str(answ)
    return True if s.lower() in txt.lst_quit else False

def yes(answ):
    s = str(answ)
    return True if s.lower() in txt.lst_yess else False

def no(answ):
    s = str(answ)
    return True if s.lower() in txt.lst_no else False

def empty(answ): 
    s = str(answ)
    return True if not s else False

def prev(answ):
    s = str(answ)
    return True if s.lower() in txt.lst_prev else False
