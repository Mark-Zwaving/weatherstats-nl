# -*- coding: utf-8 -*-
'''Functions for menu '''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.1.0"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import sources.model.utils as utils
import sources.view.console as console
import sources.view.txt as vtxt
import sources.control.ask as ask

def check_menu_options():
    '''If no internet, skip download part'''
    ok_web, ok_data = False, False

    # Make menu
    lst_menu = []

    # Check internet
    if utils.has_internet():
        ok_web = True 

    # Check data
    if utils.is_data_map_empthy():
        ok_data = True 

    if ok_web: 
        lst_menu += vtxt.lst_download # Add download menu options

    if ok_data:
        lst_menu += vtxt.lst_statistics  # Add data handling options menu 
        lst_menu += vtxt.lst_days    # Add days values
        lst_menu += vtxt.lst_graphs  # Add make graphs

    if ok_web: 
        lst_menu += vtxt.lst_weather # Add download menu options

    return ok_web, ok_data, lst_menu

def error_no_stations_found():
    console.header('No weatherstations found in configuration file !', True )
    console.log('Add one or more weatherstations in stations.py', True )
    console.footer('Press a key to quit...', True )
    input('...')

def fn_exec( choice, loc_menu ):
    n = 1
    for title in loc_menu:
        for option in title[1]:
            if n == choice:
                option[1]()
            n += 1

def main_menu():
    while True:  # Main menu
        ok_web, ok_data, loc_menu = check_menu_options()
        num = 1
        console.header('MAIN MENU', True )

        for el in loc_menu:
            title, options = el[0], el[1]
            console.log(f'\t{title}', True)
            for option in options:
                title, fn = option[0], option[1]
                console.log(f'\t\t{num}) {title}', True)
                num += 1
            # print('')

        if ok_data == False and ok_web == False:
            t  = '\tNo internet and no data! Not much can be done now.\n'
            t += '\tFirst.  Try to have a working internet connection.\n'
            t += '\tSecond. Press a key to reload the menu or restart the application.\n'
            t += '\tThird.  Download weatherdata from the download options in the menu.'
            console.log(t, True)
            console.footer("\tPress a key to reload menu or press 'q' to quit...", True )
            answ = ask.ask(' ? ')
            if vtxt.is_answ_quit(answ):
                break
            else:
                answ = False
        else:
            if ok_web == False:
                t = '\tNo internet connection. Get an working internet connection for more menu options.'
                console.log(t, True )
            elif ok_data == False:
                t = '\tNo data found. Download the weather data (option 1 & 2) for more menu options.'
                console.log(t, True )

            console.log(f'\tChoose one of the following options: 1...{num-1}', True )
            console.log(f"\tPress 'q' to quit...", True )
            console.footer('Your choice is ? ', True )
            answ = ask.ask(' ? ')  # Make a choice

        if not answ:
            continue
        elif vtxt.is_answ_quit(answ):
            break
        else:
            try:
                choice = int(answ)
            except ValueError:
                console.log(f'\nOption "{answ}" unknown...', True ) # Input was not a number
            else:
                if choice in range( 1, num ):
                    fn_exec(choice, loc_menu)
                else:
                    console.log(f'\nOption "{answ}" out of reach', True )
