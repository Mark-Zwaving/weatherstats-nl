'''Library contains functions for asking questions and to deal with the input
given by a user'''
import sources.model.graphs as graphs
import sources.view.text as text
import sources.control.ask as ask
import sources.model.weather as weather
import sources.model.dayvalues as dayvalues
import sources.model.stats_tables as stats_tables
import sources.model.daydata as daydata
import common.control.answer as answer
import common.view.console as cnsl
import common.control.fio as fio

__author__ = 'Mark Zwaving'
__email__ = 'markzwaving@gmail.com'
__copyright__ = 'Copyright (C) Mark Zwaving. All rights reserved.'
__license__ = 'GNU Lesser General Public License (LGPL)'
__version__ = '0.2.8'
__maintainer__ = 'Mark Zwaving'
__status__ = 'Development'

import time
import config as cfg
import sources.model.utils as utils

# TODO Heatwaves, coldwaves

##########################################################################################
# DOWNLOADS

# Menu choice 1
def process_knmi_dayvalues_all(): 
    cnsl.log(text.head('START DOWNLOAD ALL KNMI DAYVALUES'), True)
    daydata.process_all()
    cnsl.log(text.foot('END DOWNLOAD ALL KNMI DAYVALUES'), True)
    ask.back_to_main_menu()


# Menu choice 2
def process_knmi_dayvalues_select():
    '''Function asks for one or more wmo numbers to download their data'''
    while True:
        cnsl.log( text.head('START DOWNLOAD KNMI DAYVALUES'), True)
        options = ask.lst(['lst-places'], '', back=True, prev=False, exit=True, spacer=True)
        if options['quit']: 
            break

        daydata.process_lst(options['lst-places'])

        if answer.quit( utils.again('Do you want to download more stations ? Press a key.') ):
            break

    cnsl.log(text.foot('END DOWNLOAD KNMI DAYVALUES'), True)


##########################################################################################
# TABLE STATISTICS

# Base for table statistics
def table_stats(title, lst_questions, lst_cells=[]):
    '''Function makes calculations for all statistics'''
    while True:
        cnsl.log(text.head(f'START {title.upper()}'), True)
        
        # Ask list with questions
        options = ask.lst(lst_questions, title, back=True, prev=True, exit=True, spacer=True)
        if options['quit']:
            break

        # Cells td list. As parameter or asked for
        if lst_cells: 
            options['lst-sel-cells'] = lst_cells

        st = time.time_ns() # Set the timer
        ok, path = stats_tables.calculate(options) # Calculate with the given options
        cnsl.log(text.process_time('Total processing time is ', st), cfg.verbose)

        if answer.quit( utils.open_with_default_app(path, options) ):
            break

        if answer.quit( utils.again(f'Do you want to make another <{title}> table ?') ):
            break

    cnsl.log(text.foot(f'END {title.upper()}'), True)


# Winter and summer statistics
def table_stats_winter_summer():
    title = 'winter and summer statistics'
    lst_ask = ['lst-places', 'period', 'file-type', 'file-name']
    table_stats(title, lst_ask, cfg.lst_cells_winter_summer)


# Winter statistics
def table_stats_winter():
    title = 'winter statistics'
    lst_ask = ['lst-places', 'period', 'file-type', 'file-name']
    table_stats(title, lst_ask, cfg.lst_cells_winter)


# Summer statistics
def table_stats_summer(): 
    title = 'summer statistics'
    lst_ask = ['lst-places', 'period', 'file-type', 'file-name']
    table_stats(title, lst_ask, cfg.lst_cells_summer)


# Default statistics
def table_stats_default(): 
    title = 'my default statistics'
    lst_ask = ['lst-places', 'period', 'file-type', 'file-name']
    table_stats(title, lst_ask, cfg.lst_cells_default)


# Default extremes
def table_stats_extremes(): 
    title = 'my default extremes'
    lst_ask = ['lst-places', 'period', 'file-type', 'file-name']
    table_stats(title, lst_ask, cfg.lst_cells_my_extremes)


# Default extremes
def table_stats_counts(): 
    title = 'my default counters'
    lst_ask = ['lst-places', 'period', 'file-type', 'file-name']
    table_stats(title, lst_ask, cfg.lst_cells_my_extremes)


# Do it yourself
def table_stats_diy():
    title ='diy statistics'
    lst_ask = ['lst-places', 'period', 'lst-sel-cells', 'file-type', 'file-name']
    table_stats(title, lst_ask)
    

def table_stats_period_in_period():
    title = 'period statistics'
    lst_ask = ['lst-places', 'period',  'period-2', 'lst-sel-cells', 'file-type', 'file-name']
    table_stats(title, lst_ask)


def table_stats_compare():
    title = 'compare statistics'
    lst_ask = ['lst-places', 'period',  'period-cmp', 'lst-sel-cells', 'file-type', 'file-name']
    table_stats(title, lst_ask)


##########################################################################################
# DAYVALUES
def make_dayvalues():
    '''Funtion gets day values from data knmi '''
    while True:
        cnsl.log(text.head('START MAKE OR SEE DAY VALUES'), True)
        title = 'dayvalues' # Unused!
 
        # Ask list with questions
        lst_ask = ['lst-places', 'period', 'file-type', 'write']
        options = ask.lst(lst_ask, title, default='', back=True, prev=True, exit=True, spacer=True)
        if options['quit']:
            break
        
        options['download'] = False # Default is False, do not give a download option
        options['lst-sel-cells'] = cfg.lst_cells_dayvalues # Data cells to show

        st = time.time_ns()
        path = dayvalues.calculate(options)
        cnsl.log(text.process_time('Total processing time is ', st), cfg.verbose)

        if answer.quit( utils.open_with_default_app(path, options) ):
            break

        if answer.quit( utils.again('Do you want to select other period(s) or station(s) ?') ):
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
        lst_ask = ['lst-places', 'period', 's4d-query', 'file-type', 'file-name']
        options = ask.lst(lst_ask, title, default='', back=True, prev=True, exit=True, spacer=True)
        if options['quit']:
            break

        st = time.time_ns() # Set the timer
        query_title =  options['s4d-query'].replace('\s+', ' ').strip()
        options['title'] = f'{title} ~ {query_title}' # Add query to the title
        options['lst-sel-cells'] = cfg.lst_cells_s4d_default # Set the table colls
        ok, path = stats_tables.calculate(options) # Calculate with the given options
        cnsl.log(text.process_time('Total processing time is ', st), cfg.verbose)

        if answer.quit( utils.open_with_default_app(path, options) ):
            break
        
        if answer.quit( utils.again('Do you want to search for days again ?') ):
            break
        
    cnsl.log(text.foot('END SEARCH 4 DAYS'), True)


##########################################################################################
# BUIENRADAR 

# WEATHER FORECAST
def process_weather_buienradar_forecast():
    '''Function downloads and print a global weather forecast from the website from the knmi'''
    cnsl.log(text.head('START BUIENRADAR FORECAST'), True)
    weather.process('buienradar-weather')
    cnsl.log(text.foot('END BUIENRADAR FORECAST'), True)
    ask.back_to_main_menu(back=False, exit=True, spacer=True)

# CURRENT WEATHER CITIES 
def process_weather_buienradar_current():
    '''Function downloads and print a actual weather values to the screen'''
    cnsl.log(text.head('START BUIENRADAR WEATHERSTATIONS'), True)
    weather.process('buienradar-stations')
    cnsl.log(text.foot('END BUIENRADAR WEATHERSTATIONS'), True)
    ask.back_to_main_menu(back=False, exit=True, spacer=True)


##########################################################################################
# KNMI

def process_weather_knmi_forecast():
    '''Function downloads and prints a global weather forecast from the website from the knmi'''
    cnsl.log(text.head('START KNMI FORECAST'), True)
    weather.process_knmi(cfg.knmi_forecast_global_url, 'knmi-weather-forecast')
    cnsl.log(text.foot('END KNMI FORECAST'), True)
    ask.back_to_main_menu(back=False, exit=True, spacer=True)

def process_weather_knmi_model():
    '''Function downloads and prints a global weather forecast from the website from the knmi'''
    cnsl.log(text.head('START KNMI FORECAST MODEL'), True)
    weather.process_knmi(cfg.knmi_forecast_model_url, 'knmi-weather-model')
    cnsl.log(text.foot('END KNMI FORECAST MODEL'), True)
    ask.back_to_main_menu(back=False, exit=True, spacer=True)

def process_weather_knmi_guidance():
    '''Function downloads and prints a global weather forecast from the website from the knmi'''
    cnsl.log(text.head('START KNMI FORECAST GUIDANCE'), True)
    weather.process_knmi(cfg.knmi_forecast_guidance_url, 'knmi-weather-guidance')
    cnsl.log(text.foot('END KNMI FORECAST GUIDANCE'), True)
    ask.back_to_main_menu(back=False, exit=True, spacer=True)

def process_weather_knmi_current():
    '''Function downloads and print a actual weather values to the screen'''
    cnsl.log(text.head('START KNMI WEATHERSTATIONS'), True)
    weather.process('knmi-stations')
    cnsl.log(text.foot('END KNMI WEATHERSTATIONS'), True)
    ask.back_to_main_menu()


##########################################################################################
# GRAPHS

def graph_period():
    '''Funtion makes images for a period from the data of the knmi'''
    while True:
        cnsl.log(text.head('START MAKE GRAPH'), True)

        # Ask list with questions
        title = 'graph statistics'
        lst_ask = [
            'lst-places', 'period', 'lst-entities', 'file-name', 'graph-type',
            'graph-title', 'graph-y-label', 'graph-default','graph-width',
            'graph-height', 'graph-cummul-val','graph-dpi', 'graph-lst-entities-types'
        ]
        options = ask.lst(lst_ask, title, default='', back=True, prev=True, exit=True, spacer=True)
        if options['quit']: break

        st = time.time_ns()
        path = graphs.calculate(options)
        cnsl.log( text.process_time('Total processing time is ',st), cfg.verbose )

        if answer.quit( utils.open_with_default_app(path, options) ):
            break

        if answer.quit( utils.again('Do you want to make more graphs ?') ):
            break

    cnsl.log(text.foot('END MAKE GRAPH'), True)

# def graph_period_quick_default():
#     while True:
#         cnsl.log(text.head('START MAKE DEFAULT GRAPH'), True)

#         title = 'graph statistics'
#         lst_ask = ['lst-places', 'period']
#         options = ask.lst(lst_ask, title, default='', back=True, prev=True, exit=True, spacer=True)
#         if options['quit']:
#             break

#         st = time.time_ns()
#         path = graphs.calculate(options)
#         cnsl.log( text.process_time('Total processing time is ',st), cfg.verbose )

#         if answer.quit( utils.open_with_default_app(path, options) ):
#             break

#         if answer.quit( utils.again('Do you want to make more graphs ?') ):
#             break

#     cnsl.log(text.foot('END MAKE GRAPH'), True)



# def graph_period_quick_default():
#     while True:
#         cnsl.log(text.head('START MAKE DEFAULT GRAPH'), True)

#         st = time.time_ns()
#         path = graphs.calculate(options)
#         cnsl.log( text.process_time('Total processing time is ',st), cfg.verbose )

#         if answer.quit( utils.open_with_default_app(path, options) ):
#             break

#         if answer.quit( utils.again('Do you want to make more graphs ?') ):
#             break

#     cnsl.log(text.foot('END MAKE GRAPH'), True)


##########################################################################################
# MAIN MENU 

# Menu list
lst_menu = [

    [ 'DOWNLOAD', [ 
        [ 'Download all dayvalues knmi stations', process_knmi_dayvalues_all ],
        [ 'Download dayvalues selected knmi stations', process_knmi_dayvalues_select]
    ] ],

    [ 'STATISTICS TABLES', [  
        [ 'DIY cells statistics', table_stats_diy ],
        [ 'Winter statistics', table_stats_winter ],
        [ 'Summer statistics', table_stats_summer ],
        [ 'Winter & summer statistics', table_stats_winter_summer ],
        [ 'My default statistics (see config.py)', table_stats_default ],
        [ 'My default extremes (see config.py)', table_stats_extremes ],
        [ 'My default counts (see config.py)', table_stats_counts ],
        [ 'Day, month & period statistics in a period', table_stats_period_in_period ],
        [ 'Compare (day, month, year and season)', table_stats_compare ],
    ] ],

    [ 'DAYS', [ 
        [ 'Make or see dayvalues', make_dayvalues ],
        [ 'Search 4 days', search_for_days ]
    ] ],

    [ 'GRAPHS', [ 
        [ 'DIY period', graph_period ]
    ] ],

    [ 'WEATHER (dutch)', [ 
        [ 'Forecast buienradar', process_weather_buienradar_forecast ],
        [ 'Stations NL buienradar', process_weather_buienradar_current ],
        [ 'Forecast knmi', process_weather_knmi_forecast ],
        [ 'Forecast model knmi', process_weather_knmi_model ],
        [ 'Forecast guidance knmi', process_weather_knmi_guidance ],
        [ 'Stations NL knmi', process_weather_knmi_current ]
    ] ]

    # [ 'QUICK IO <TODO>',
    #     [ [ 'Quick statistics', cquick_stats_io ],
    #       [ 'Quick graphs', cquick_graphs_io ],
    #     ]
    # ],

]


def check_menu_options():
    '''If no internet, skip download part'''
    ok_web, ok_data, loc_menu = False, False, lst_menu
    # Check internet
    if fio.has_internet(verbose=False):
        ok_web = True
    else:
        loc_menu = loc_menu[2:] # Update menu. Skip download options menu

    if fio.is_dir_empthy(cfg.dir_dayvalues_txt, verbose=False):
        loc_menu = loc_menu[:-3] # Update menu. Skip data handling options menu
    else:
        ok_data = True

    return ok_web, ok_data, loc_menu


def main_menu():
    space = '    '
    while True:  # Main menu
        ok_web, ok_data, loc_menu = check_menu_options()
        num = 1
        t = text.head('MAIN MENU') + '\n'

        tmenu = ''
        for el in loc_menu:
            title, options = el[0], el[1]
            tmenu += f'\n{space}{title}\n'
            for option in options:
                title, fn = option[0], option[1]
                tmenu += f'{space*2}{num}) {title}\n'
                num += 1
        t += f'{tmenu}\n' if tmenu else ''

        if ok_data == False and ok_web == False:
            t += text.menu_no_internet_no_data + '\n'
            t += text.foot("\tPress a key to reload the menu or press 'q' to quit...")

        else:
            if ok_web == False:
                t += '\tNo internet connection. Get an working internet connection for more menu options.\n'
            elif ok_data == False:
                t += '\tNo data found. Download the weather data (option 1 & 2) for more menu options.\n'

            t += f'\tChoose one of the following options: 1...{num-1}\n'
            t += "\tPress 'x' to quit program...\n\n"
            t += text.foot('Your choice ? ')

        answ = ask.question(t, back=False, exit=False, spacer=True)  # Make a choice

        if not answ:
            continue
        elif answer.quit(answ):
            break
        else:
            try:
                choice = int(answ)
            except ValueError:
                t = f'Option "{answ}" unknown...\n' # Input was not a number
            else:
                if choice in range( 1, num ):
                    fn_exec(choice, loc_menu)
                else:
                    t = f'Option "{answ}" out of reach\n'
            
            cnsl.log(t, True)

def fn_exec( choice, loc_menu ):
    n = 1
    for title in loc_menu:
        for option in title[1]:
            if n == choice:
                option[1]()
            n += 1


def error_no_stations_found():
    cnsl.log(text.menu_no_weather_stations, True )
    input(' ')






##########################################################################################
##########################################################################################
##########################################################################################




# def quick_graphs_io():
#     '''Function makes a graph with a statistic for one or more stations'''
#     while True:
#         cnsl.log(text.head('START QUICK GRAPH'), True)

#         t = 'Give a correct quick command ?\n'
#         t += 'Format:  period -> station(s) (wmo or name) -> statistic(s)  -> width, heigth image \n'
#         t += 'Example: 202106 -> 310, Eelde, De Kooy, 380 -> TX+, TG~, TN-  -> 1280, 900'

#         query_io = ask.querio(t)
#         if answer.quit(query_io):
#             break

#         st = time.time_ns()
#         path = quickio.calculate(query_io)
#         t = f'Results are saved in {path}\nTotal processing time is '
#         cnsl.log(text.process_time(t, st), True)

#         # Always ask for going back
#         again = ask.again(
#             f'Do you want to calculate more statistics ?', True)
#         if answer.quit(again):
#             break

#         cnsl.log(text.foot('END QUICK GRAPH'), True)


# def quick_stats_io():
#     '''Function get statistics for one or more stations and return the statistics'''
#     while True:
#         cnsl.log(text.head('START QUICK STATISTICS'), True)

#         t = text.menu_info_quick_calculations
#         query_io = ask.querio(t)
#         if answer.quit(query_io):
#             break

#         st = time.time_ns()
#         path = quickio.calculate(query_io)
#         t = f'Results are saved in {path}\nTotal processing time is '
#         cnsl.log(text.process_time(t, st), True)

#         # Always ask for going back
#         again = ask.again(
#             f'Do you want to calculate more statistics ?', True)
#         if answer.quit(again):
#             break

#         cnsl.log(text.foot('END QUICK STATISTICS'), True)



# # Menu choice 7
# def table_heatwaves():
#     while True:
#         text.head('START CALCULATE HEATWAVES', True)
#         ok, period, places, type, name = ask.period_stations_type_name(True)
#
#         if not ok:
#             break
#         else:
#             text.head('CALCULATING HEATWAVES', True)
#
#             st = time.time_ns()
#             # path = hs.alg_heatwaves(l, sd, ed, type, name)
#             text.show_process_time(st)
#
#             if type != 'cmd':
#                 fopen = ask.open_with_app(
#                             f'\nOpen the file (type={type}) with your default application ?'
#                             )
#                 if fopen:
#                     fio.open_with_app(path)
#
#             # Always ask for going back
#             again = ask.again(
#                         f'Do you want to make another heatwaves table ?',
#                         True
#                     )
#             if answer.quit(again):
#                 break
#
#     text.foot(f'END CALCULATE HEATWAVES', True)
#
# # Menu choice 7
# def table_coldwaves():
#     while True:
#         text.head('START CALCULATE COLDWAVES', True)
#         ok, period, places, type, name = ask.period_stations_type_name(True)
#
#         if not ok:
#             break
#         else:
#             text.head('CALCULATING COLDWAVES', True)
#
#             st = time.time_ns()
#             # path = hs.alg_heatwaves(l, sd, ed, type, name)
#             text.show_process_time(st)
#
#             if type != 'cmd':
#                 fopen = ask.open_with_app(
#                             f'\nOpen the file (type={type}) with your default application ?'
#                             )
#                 if fopen:
#                     fio.open_with_app(path)
#
#             # Always ask for going back
#             again = ask.again(
#                         f'Do you want to make another coldwaves table ?'
#                         )
#             if answer.quit(again):
#                 break
#
#     text.foot(f'END CALCULATE COLDWAVES', True)