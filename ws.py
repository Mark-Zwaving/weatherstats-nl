# -*- coding: utf-8 -*-
'''WeatherStatsNL calculates weather statistics for dutch cities with data from the knmi'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.1.9'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import sys
import config as cfg, stations, defaults

# Add dir (from this) app to system path, if not already there.
if cfg.dir_app not in sys.path: 
    sys.path.append(cfg.dir_app)

import sources.control.fio as fio 
import sources.control.ask.answer as answer
import sources.control.ask.question as question
import sources.view.menu as view_menu
import sources.control.menu as ctrl_menu
import sources.view.console as cnsl
import sources.view.text as text

from pprint import pprint

##########################################################################################
# START MAIN MENU 
def lst_menu():
    '''Make the menu lst with the options'''
    lst = []

    # Have internet ?
    internet = fio.check_for_internet_connection()

    # Have already data in the text dayvalues map ?
    data = not fio.is_dir_empthy(
        cfg.dir_dayvalues_txt, 
        verbose=False
    )

    # Add downloadable options with an internet connection
    if internet: 
        lst.append(view_menu.lst_downloads) # Add first

    # Add data menu options to menu 
    if data: 
        lst.append(view_menu.lst_divers_statistics)
        lst.append(view_menu.lst_default_statistics)
        lst.append(view_menu.lst_dayvalues)
        lst.append(view_menu.lst_graphs)
        # lst.append(view_menu.lst_databases) # TODO

    if internet:
        lst.append(view_menu.lst_current_weather) # Add at the end
        lst.append(view_menu.lst_animations)

    return lst, internet, data

def menu_broker(lst, choice):
    '''Broker between text menu's and the python functions'''
    # Number for menu
    number = 0 

    # Walkthrough menu list
    for lst_sub_menu in lst: 
        # Get the menu title
        main_menu_title = lst_sub_menu[0]

        # Walkthrough list with the submenu's 
        for lst_sub_opt in lst_sub_menu[1]: 
            # Menu number, increase very time
            number += 1 

            # Process the choice from user 
            if number == choice:
                # Special action for default statistics 
                if main_menu_title == defaults.title_statistics: 
                    # Get title and statistics lst 
                    sub_title, lst_stats = lst_sub_opt[0], lst_sub_opt[1]

                    # Execute statistics function with parameters 
                    ctrl_menu.table_stats(sub_title, lst_stats)

                else: # Normal execution of given fn 
                    fn = lst_sub_opt[1] # Get function

                    # Execute function from menu
                    fn()

def main():
    '''Print menu on screen'''
    if len(stations.lst) == 0:
        cnsl.log(text.menu_no_weather_stations, True )
        exit(0)

    # Show main menu
    while True:  
        # Check internet and data and get menu lst
        lst, internet, data  = lst_menu() 

        # Walkthrough menu options
        num, content = 1, cfg.e
        for el in lst:
            title, options = el[0], el[1]
            content += f'\n{cfg.spacer}{title}' + cfg.ln
            for option in options:
                title = option[0]
                content += f'{cfg.spacer*2}{num:>2}) {title}' + cfg.ln
                num += 1
        t  = text.head('BETA') + cfg.ln
        t += text.head('MAIN MENU - Welcome to WeatherStatsNL') + cfg.ln
        t += content  + cfg.ln

        if not data and not internet:
            t += text.menu_no_internet_no_data + cfg.ln
            t += text.foot(f"{cfg.spacer}Press a key to reload the menu or press 'q' to quit...")

        else:
            if not internet:
                t += f'{cfg.spacer}No internet connection.' + cfg.ln
                t += f'{cfg.spacer}Get an working internet connection for more menu options.' + cfg.ln
            elif not data:
                t += f'{cfg.spacer}No data found.\n'
                t += f'{cfg.spacer}Download the weather data (option 1 & 2) for more menu options.' + cfg.ln

            t += f'{cfg.spacer}Choose one of the following options: 1..{num-1}' + cfg.ln
            t += f"{cfg.spacer}Press 'x' to quit program..." + cfg.ln + cfg.ln
            t += text.foot('Your choice ? ')

        # Make a choice
        answ = question.ask(t, spacer=True)  

        if answer.is_quit(answ):
            break
        else: 
            # Check answer
            try:
                choice = int(answ)
            except Exception as e:
                pass # Input is not a number
            else:
                # Check availbale menu options 
                if choice in range( 1, num ):
                    # Menu choice is OK, goto menu broker 
                    menu_broker(lst, choice) 
                    continue
            
            # Input was not a number or out of range
            t  = f"Menu option '{answ}' is not available." + cfg.ln
            t += f'Enter a number from 1..{num-1}.' + cfg.ln
            t += text.press_enter_continue + cfg.ln
            # cnsl.log(t, True)
            input(t)

# Main programm
if __name__== '__main__':
    main()
