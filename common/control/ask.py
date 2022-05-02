# -*- coding: utf-8 -*-
'''Library for handling (easy) questions'''
import common.control.fio as fio
import common.view.txt as text
import common.view.console as cnsl
__author__     = 'Mark Zwaving'
__email__      = 'markzwaving@gmail.com'
__copyright__  = 'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    = 'MIT License'
__version__    = '0.1.2'
__maintainer__ = 'Mark Zwaving'
__status__     = 'Development'


marker = '\n  ?  '
def ln(t):  return '\n' if t else ''
def txt(t): return f'{t}{marker}'

def space(spacer, verbose): 
    cnsl.log('', spacer and verbose) 


def any_key(t='', spacer=False, verbose=True):
    '''Answer can be anything'''
    tt = txt(t)
    answ = text.sanitize( input(tt) )
    space(spacer, verbose)

    return answ


def answer(t='', spacer=False, verbose=True):
    '''An answer must be given'''
    while True:
        answ = any_key(t, spacer, verbose)
        if answ:
            return answ

        cnsl.log('Please type in something...', verbose)
        space(spacer, verbose)


def question(t='', spacer=False, verbose=True):
    '''Ask a question. Canonical with any key'''
    return any_key(t, spacer, verbose)


def integer(t='Give an integer', spacer=False, verbose=True):
    answ = any_key(t, spacer, verbose)

    try:
        answ = int(answ)
    except ValueError:
        return False
    else:
        return answ


def quit(t='Press "q" to quit...', spacer=False, verbose=True):
    answ = any_key(t, spacer, verbose)
    if answ:
        if answ.lower() in text.quit:
            return True

    return False


def exit(t='Press "q" to exit...', spacer=False, verbose=True):
    if quit(any_key(t, spacer, verbose)):
        exit(0)


def continu(t='Press a key to continue...', spacer=False, verbose=True):
    input(t); space(spacer, verbose)


def pause(t='Program paused. Press a key to continue...', spacer=False, verbose=True):
    continu(t, spacer, verbose)


def yess_or_no(t='Type in "y" for yess or "n" for no', spacer=False, verbose=True):
    answ = answer(t, spacer, verbose)
    if answ in text.yess:
        return answ
    elif answ in text.no:
        return answ
    else:
        cnsl.log(t, verbose)
        space(spacer, verbose)


def number(t='Give a number', spacer=False, verbose=True):
    while True:
        answ = answer(t, spacer, verbose)
        if answ.isdigit():
            return answ
        else:
            cnsl.log(f'Please type in a number', True)


def letter(t='Give a letter from a..Z', spacer=False, verbose=True):
    while True:
        answ = answer(t, spacer, verbose)
        if answ.isalpha():
            return answ
        else:
            cnsl.log(f'Please type in a letter', True)


def open_with_app(t='Do you want to open the file with an (default) application', path='', spacer=False, verbose=True):
    cnsl.log(f'{t}\nFile: {path}', verbose)
    if yess_or_no(spacer=spacer, verbose=verbose):
        fio.open_with_app(path, verbose)


def yess_or_continue(t='Press a key to continue or press "y" for yess', spacer=False, verbose=True):
    answ = any_key(t, spacer, verbose)
    return True if answ.lower() in text.yess else False


def continue_or_quit(t='Press a key to continue or press "q" to quit', spacer=False, verbose=True):
    answ = any_key(t, spacer, verbose)
    if answ:
        if answ.lower() in txt.quit:
            exit(0)

