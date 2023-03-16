'''Library contains functions for asking questions and to deal with the input
given by a user'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 3 - GPLv3'
__version__    =  '0.3.4'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import time
import config as cfg, stations
import sources.model.graphs as graphs
import sources.model.weather as weather
import sources.model.dayvalues as dayvalues
import sources.model.stats_tables as stats_tables
import sources.model.animation as animation
import sources.model.daydata as daydata
import sources.model.utils as utils
import sources.control.answer as answer
import sources.control.ask as ask
import sources.control.fio as fio
import sources.view.console as cnsl
import sources.view.text as text

##########################################################################################
# KNMI download dayvalues
def process_knmi_dayvalues_all(): 
    cnsl.log(text.head('START DOWNLOAD ALL DAYVALUES KNMI'), True)
    daydata.process_all()
    cnsl.log(text.foot('END DOWNLOAD ALL DAYVALUES KNMI'), True)
    ask.question(text.back_main, default='', back=False, prev=False, exit=True, spacer=True)

def process_knmi_dayvalues_select():
    '''Function asks for one or more wmo numbers to download their data'''
    while True:
        cnsl.log( text.head('START DOWNLOAD DAYVALUES KNMI'), True)
        options = ask.lst(['lst-stations'], '', back=True, prev=False, exit=True, spacer=True)

        daydata.process_lst(options['lst-stations'])

        if ask.is_yes(
            'Do you want to download more stations?', 
            default='y', back=False, prev=False, exit=True, spacer=True
        ):
            continue 
        else:
            break

    cnsl.log(text.foot('END DOWNLOAD DAYVALUES KNMI'), True)

##########################################################################################
# TABLE STATISTICS
# Base fn for table statistics
def table_stats(title, lst_questions, lst_cells=[]):
    '''Function makes calculations for all statistics'''
    while True:
        cnsl.log(text.head(f'START {title.capitalize()}'), True)
        
        # Ask list with questions
        options = ask.lst(lst_questions, title, back=True, prev=True, exit=True, spacer=True)
  
        if answer.is_back(options['other']): break # Go back to menu

        # Cells td list. As parameter or asked for
        options['lst-sel-cells'] = lst_cells

        st = time.time_ns() # Set the timer
        ok, path = stats_tables.calculate(options) # Calculate with the given options
        cnsl.log(text.process_time('Total processing time is ', st), cfg.verbose)

        if ok:
            if options['file-type'] in text.lst_output_files:
                if answer.is_back(
                    ask.open_with_app(path, options, back=False, prev=False, exit=True, spacer=True)
                ):
                    break

        if ask.is_yes(
            f'Do you want to make another <{title}> table ?', 
            default='y', back=False, prev=False, exit=True, spacer=True
        ):
            continue 
        else:
            break # Stop animation

    cnsl.log(text.foot(f'END {title.capitalize()}'), True)

def table_stats_winter_summer():
    title = 'winter and summer statistics'
    lst_ask = ['lst-stations', 'period', 'file-type', 'file-name']
    table_stats(title, lst_ask, cfg.lst_cells_winter_summer)

def table_stats_winter():
    title = 'winter statistics'
    lst_ask = ['lst-stations', 'period', 'file-type', 'file-name']
    table_stats(title, lst_ask, cfg.lst_cells_winter)

def table_stats_summer(): 
    title = 'summer statistics'
    lst_ask = ['lst-stations', 'period', 'file-type', 'file-name']
    table_stats(title, lst_ask, cfg.lst_cells_summer)

def table_stats_default_1(): 
    title = 'my default statistics 1'
    lst_ask = ['lst-stations', 'period', 'file-type', 'file-name']
    table_stats(title, lst_ask, cfg.lst_cells_my_default_1)

def table_stats_default_2(): 
    title = 'my default statistics 2'
    lst_ask = ['lst-stations', 'period', 'file-type', 'file-name']
    table_stats(title, lst_ask, cfg.lst_cells_my_default_2)

def table_stats_extremes(): 
    title = 'my default extremes'
    lst_ask = ['lst-stations', 'period', 'file-type', 'file-name']
    table_stats(title, lst_ask, cfg.lst_cells_my_extremes)

def table_stats_counts(): 
    title = 'my default counters'
    lst_ask = ['lst-stations', 'period', 'file-type', 'file-name']
    table_stats(title, lst_ask, cfg.lst_cells_my_counts)

def table_stats_diy():
    title ='diy statistics'
    lst_ask = ['lst-stations', 'period', 'lst-sel-cells', 'file-type', 'file-name']
    table_stats(title, lst_ask)
    
def table_stats_period_in_period():
    title = 'period statistics'
    lst_ask = ['lst-stations', 'period',  'period-2', 'lst-sel-cells', 'file-type', 'file-name']
    table_stats(title, lst_ask)

def table_stats_compare():
    title = 'compare statistics'
    lst_ask = ['lst-stations', 'period',  'period-cmp', 'lst-sel-cells', 'file-type', 'file-name']
    table_stats(title, lst_ask)

##########################################################################################
# DAYVALUES
def make_dayvalues():
    '''Funtion gets day values from data knmi '''
    while True:
        cnsl.log(text.head('START MAKE OR SEE DAY VALUES'), True)
        title = 'dayvalues' # Unused!
 
        # Ask list with questions
        lst_ask = ['lst-stations', 'period', 'file-type', 'write']
        options = ask.lst(lst_ask, title, default='', back=True, prev=True, exit=True, spacer=True)

        if answer.is_back(options['other']): break # Go back to menu

        options['download'] = False # Default is False, do not give a download option
        options['lst-sel-cells'] = cfg.lst_cells_dayvalues # Data cells to show

        st = time.time_ns()
        ok, path = dayvalues.calculate(options)
        cnsl.log(text.process_time('Total processing time is ', st), cfg.verbose)

        if ok:
            if options['file-type'] in text.lst_output_files:
                if answer.is_back(
                    ask.open_with_app( 
                        path, options, back=False, prev=False, exit=True, spacer=True
                    )
                ):
                    break

        if ask.is_yes(
            'Do you want to select other period(s) or station(s) ?', 
            default='y', back=False, prev=False, exit=True, spacer=True
        ):
            continue 
        else:
            break 

    cnsl.log(text.foot('END MAKE OR SEE DAY VALUES'), True)

##########################################################################################
# SEARCH FOR DAYS
def search_for_days():
    '''Function searches files for days with specific values. ie > 30 degrees'''
    while True:
        cnsl.log(text.head('START SEARCH 4 DAYS'), True)

        # Ask list with questions
        title = 'search 4 days'
        lst_ask = ['lst-stations', 'period', 's4d-query', 'file-type', 'file-name']
        options = ask.lst(lst_ask, title, default='', back=True, prev=True, exit=True, spacer=True)

        if answer.is_back(options['other']): break # Go back to menu

        st = time.time_ns() # Set the timer
        query_title =  options['s4d-query'].replace('\s+', ' ').strip()
        options['title'] = f'{title} ~ {query_title}' # Add query to the title
        options['lst-sel-cells'] = cfg.lst_cells_s4d_default # Set the table colls
        ok, path = stats_tables.calculate(options) # Calculate with the given options
        cnsl.log(text.process_time('Total processing time is ', st), cfg.verbose)

        if ok:
            if options['file-type'] in text.lst_output_files:
                if answer.is_back(
                    ask.open_with_app(path, options, back=False, prev=False, exit=True, spacer=True)
                ):
                    break

        if ask.is_yes(
            'Do you want to do a search for days again ?', 
            default='y', back=False, prev=False, exit=True, spacer=True
        ):
            continue 
        else:
            break 

    cnsl.log(text.foot('END SEARCH 4 DAYS'), True)

##########################################################################################
# BUIENRADAR 
# Forecast
def process_weather_buienradar_forecast():
    '''Function downloads and print a global weather forecast from the website from the knmi'''
    cnsl.log(text.head('START FORECAST BUIENRADAR'), True)
    weather.process('buienradar-weather')
    cnsl.log(text.foot('END FORECAST BUIENRADAR'), True)
    ask.question(text.back_main, default='', back=False, prev=False, exit=True, spacer=True)

# weather cities
def process_weather_buienradar_current():
    '''Function downloads and print a actual weather values to the screen'''
    cnsl.log(text.head('START WEATHERSTATIONS BUIENRADAR'), True)
    weather.process('buienradar-stations')
    cnsl.log(text.foot('END WEATHERSTATIONS BUIENRADAR'), True)
    ask.question(text.back_main, default='', back=False, prev=False, exit=True, spacer=True)

##########################################################################################
# KNMI Weather
def process_weather_knmi_forecast():
    '''Function downloads and prints a global weather forecast from the website from the knmi'''
    cnsl.log(text.head('START FORECAST KNMI'), True)
    weather.process('knmi-weather')
    cnsl.log(text.foot('END FORECAST KNMI'), True)
    ask.question(text.back_main, default='', back=False, prev=False, exit=True, spacer=True)

def process_weather_knmi_model():
    '''Function downloads and prints a global weather forecast from the website from the knmi'''
    cnsl.log(text.head('START KNMI FORECAST MODEL LONG TERM'), True)
    weather.process('knmi-model')
    cnsl.log(text.foot('END KNMI FORECAST MODEL LONG TERM'), True)
    ask.question(text.back_main, default='', back=False, prev=False, exit=True, spacer=True)

def process_weather_knmi_guidance():
    '''Function downloads and prints a global weather forecast from the website from the knmi'''
    cnsl.log(text.head('START KNMI FORECAST GUIDANCE SHORT TERM'), True)
    weather.process('knmi-guidance')
    cnsl.log(text.foot('END KNMI FORECAST GUIDANCE SHORT TERM'), True)
    ask.question(text.back_main, default='', back=False, prev=False, exit=True, spacer=True)

def process_weather_knmi_current():
    '''Function downloads and print a actual weather values to the screen'''
    cnsl.log(text.head('START WEATHERSTATIONS KNMI'), True)
    weather.process('knmi-stations')
    cnsl.log(text.foot('END WEATHERSTATIONS KNMI'), True)
    ask.question(text.back_main, default='', back=False, prev=False, exit=True, spacer=True)

##########################################################################################
# GRAPHS
def graph_period():
    '''Funtion makes images for a period from the data of the knmi'''
    while True:
        cnsl.log(text.head('START MAKE GRAPH'), True)

        # Ask list with questions
        title = 'graph statistics'
        lst_ask = [
            'lst-stations', 'period', 'lst-entities', 'file-name', 'graph-type',
            'graph-title', 'graph-y-label', 'graph-default','graph-width',
            'graph-height', 'graph-cummul-val','graph-dpi', 'graph-lst-entities-types'
        ]
        options = ask.lst(lst_ask, title, default='', back=True, prev=True, exit=True, spacer=True)

        if answer.is_back(options['other']): break # Go back to menu

        st = time.time_ns()
        ok, path = graphs.calculate(options)
        cnsl.log( text.process_time('Total processing time is ',st), cfg.verbose )

        if ok:
            if options['file-type'] in text.lst_output_files:
                if answer.is_back(
                    ask.open_with_app(
                        path, options, 
                        back=False, prev=False, exit=True, spacer=True
                    )
                ):
                    break

        if ask.is_yes(
            'Do you want to make more graphs ?', 
            default='y', back=False, prev=False, exit=True, spacer=True
        ):
            continue 
        else:
            break 

    cnsl.log(text.foot('END MAKE GRAPH'), True)

# def graph_period_quick_default():
#     while True:
#         cnsl.log(txt.head('START MAKE DEFAULT GRAPH'), True)

#         title = 'graph statistics'
#         lst_ask = ['lst-stations', 'period']
#         options = ask.lst(lst_ask, title, default='', back=True, prev=True, exit=True, spacer=True)

#         st = time.time_ns()
#         path = graphs.calculate(options)
#         cnsl.log( txt.process_time('Total processing time is ',st), cfg.verbose )

#         if answer.is_quit( utils.open_with_default_app(path, options) ):
#             break

#         if answer.is_quit( ask.again('Do you want to make more graphs ?') ):
#             break

#     cnsl.log(txt.foot('END MAKE GRAPH'), True)



# def graph_period_quick_default():
#     while True:
#         cnsl.log(txt.head('START MAKE DEFAULT GRAPH'), True)

#         st = time.time_ns()
#         path = graphs.calculate(options)
#         cnsl.log( txt.process_time('Total processing time is ',st), cfg.verbose )

#         if answer.is_quit( utils.open_with_default_app(path, options) ):
#             break

#         if answer.is_quit( ask.again('Do you want to make more graphs ?') ):
#             break

#     cnsl.log(txt.foot('END MAKE GRAPH'), True)

##########################################################################################
# ANIMATIONS
def process_download_animation():
    '''Function downloads images ad makes an animation'''
    title = 'download and make an animation'
    lst_ask = [
        'image-download-url', 'start-datetime', 'end-datetime', 'interval-download', 
        'animation-name', 'animation-time', 'remove-downloads', 'gif-compress', 'verbose'
    ]
    while True:
        cnsl.log(text.head('START DOWNLOAD IMAGES AND MAKE AN ANIMATION'), True)
        # Ask list with questions
        options = ask.lst(lst_ask, title, back=True, prev=True, exit=True, spacer=True)

        if answer.is_back(options['other']): break # Go back to menu

        options['file-type'] = cfg.animation_ext

        st = time.time_ns() # Set the timer
        ok, path = animation.download_images_and_make_animations(
            options['image-download-url'],# Url for the files on the web
            options['animation-name'],    # Name of animation file   
            options['start-datetime'],    # Start time <yyyy-mm-dd HH:MM:SS>
            options['end-datetime'],      # End datetime <yyyy-mm-dd HH:MM:SS>
            options['interval-download'], # Interval time for downloading Images (minutes)
            True,                         # No double downloads check
            options['animation-time'],    # Animation interval time for gif animation
            options['remove-downloads'],  # Remove the downloaded images
            options['gif-compress'],      # Compress the size of the animation
            options['verbose']            # With output to screen
        )
        cnsl.log(text.process_time('Total processing time is ', st), cfg.verbose)

        if ok:
            if options['file-type'] in text.lst_output_gif:
                if answer.is_back(
                    ask.open_with_app(
                        path, options, 
                        back=False, prev=False, exit=True, spacer=True
                    )
                ):
                    break

        if ask.is_yes(
            f'Do you want to make another animation file?', 
            default='y', back=False, prev=False, exit=True, spacer=True
        ):
            continue 
        else:
            break # Stop animation

    cnsl.log(text.foot('END DOWNLOAD IMAGES AND MAKE AN ANIMATION'), True)

#TODO
def process_download_images():
    pass

#TODO       
def proces_images_from_dir():
    pass

##########################################################################################
# MAIN MENU 
def select_menu_option( option ):
    # Downloads
    if   option == 'process_knmi_dayvalues_all':     process_knmi_dayvalues_all()
    elif option == 'process_knmi_dayvalues_select':  process_knmi_dayvalues_select()
    # Statistics
    elif option == 'table_stats_diy':              table_stats_diy()
    elif option == 'table_stats_winter':           table_stats_winter()
    elif option == 'table_stats_summer':           table_stats_summer()
    elif option == 'table_stats_winter_summer':    table_stats_winter_summer()
    elif option == 'table_stats_extremes':         table_stats_extremes()
    elif option == 'table_stats_counts':           table_stats_counts()
    elif option == 'table_stats_default_1':        table_stats_default_1()
    elif option == 'table_stats_default_2':        table_stats_default_2()
    elif option == 'table_stats_period_in_period': table_stats_period_in_period()
    elif option == 'table_stats_compare':          table_stats_compare()
    # Days
    elif option == 'make_dayvalues':  make_dayvalues()
    elif option == 'search_for_days': search_for_days()
    # Graphs
    elif option == 'graph_period': graph_period()
    # Weather
    elif option == 'process_weather_buienradar_forecast': process_weather_buienradar_forecast()
    elif option == 'process_weather_buienradar_current':  process_weather_buienradar_current()
    elif option == 'process_weather_knmi_forecast':       process_weather_knmi_forecast()
    elif option == 'process_weather_knmi_model':          process_weather_knmi_model()
    elif option == 'process_weather_knmi_guidance':       process_weather_knmi_guidance()
    elif option == 'process_weather_knmi_current':        process_weather_knmi_current()
    # Animations
    elif option == 'process_download_animation':          process_download_animation()

def fn_exec( choice, menu ):
    n = 1
    for title in menu:
        for option in title[1]:
            if n == choice:
                select_menu_option( option[1] )
            n += 1

def check_menu_options():
    '''If no internet, skip download part'''
    web, data, lst_menu = False, False, []

    # Check internet
    if fio.check_for_internet_connection():
        web = True

    # Check for data in map
    if not fio.is_dir_empthy(cfg.dir_dayvalues_txt, verbose=cfg.verbose):
        data = True
        
    if data: # Add data menu options to menu 
        lst_menu.append(text.lst_menu_statistics)
        lst_menu.append(text.lst_menu_days)
        lst_menu.append(text.lst_menu_graphs)

    if web: # Add downloadable options
        lst_menu.insert(0, text.lst_menu_download) # Add at first position
        lst_menu.append(text.lst_menu_weather) # Add at the end
        lst_menu.append(text.lst_menu_animation)

    return web, data, lst_menu

def main():
    if len(stations.lst) == 0:
        cnsl.log(text.menu_no_weather_stations, True )
        exit(0)

    space = '    '  
    while True:  # Main menu
        web, data, lst_menu = check_menu_options()
        num, main = 1, ''
        for el in lst_menu:
            title, options = el[0], el[1]
            main += f'\n{space}{title}\n'
            for option in options:
                title = option[0]
                main += f'{space*2}{num}) {title}\n'
                num += 1

        t = text.head('MAIN MENU - Welcome to WeatherStatsNL') + '\n'
        t += main  + '\n'

        if not data and not web:
            t += text.menu_no_internet_no_data + '\n'
            t += text.foot(f"{space}Press a key to reload the menu or press 'q' to quit...")

        else:
            if not web:
                t += f'{space}No internet connection.\n'
                t += f'{space}Get an working internet connection for more menu options.\n'
            elif not data:
                t += f'{space}No data found.\n'
                t += f'{space}Download the weather data (option 1 & 2) for more menu options.\n'

            t += f'{space}Choose one of the following options: 1...{num-1}\n'
            t += f"{space}Press 'x' to quit program...\n\n"
            t += text.foot('Your choice ? ')

        answ = ask.question(t, spacer=True)  # Make a choice

        if not answ:
            continue
        elif answer.is_quit(answ):
            break
        else:
            try:
                choice = int(answ)
            except ValueError:
                t = f'Option "{answ}" unknown...\n' # Input was not a number
            else:
                if choice in range( 1, num ):
                    fn_exec(choice, lst_menu)
                    continue
                else:
                    t = f'Option "{answ}" out of reach\n'
            
            cnsl.log(t, True)
