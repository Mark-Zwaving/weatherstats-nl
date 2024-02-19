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
import sources.model.ymd as ymd
import sources.control.answer as answer
import sources.control.ask as ask
import sources.control.fio as fio
import sources.view.console as cnsl
import sources.view.text as text

##########################################################################################
# KNMI download dayvalues
def download_knmi_dayvalues_all(): 
    cnsl.log(text.head('START DOWNLOAD ALL DAYVALUES KNMI'), True)
    daydata.process_all()
    cnsl.log(text.foot('END DOWNLOAD ALL DAYVALUES KNMI'), True)
    ask.question(text.back_main, default=cfg.e, back=False, prev=False, exit=True, spacer=True)

def download_knmi_dayvalues_select():
    '''Function asks for one or more wmo numbers to download their data'''
    lst_ask = text.lst_ask_stations
    while True:
        cnsl.log( text.head('START DOWNLOAD DAYVALUES KNMI'), True)
        options = ask.lst( lst_ask, default=cfg.e, back=True, prev=False, exit=True, spacer=True )
        daydata.process_lst(options[text.ask_stations])

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
def table_stats(title, lst_ask, lst_cells=[]):
    '''Function makes calculations for all statistics'''
    while True:
        cnsl.log(text.head(f'START {title.capitalize()}'), True)
        
        # Ask list with questions
        options = ask.lst( lst_ask, title, back=True, prev=True, exit=True, spacer=True )
  
        if answer.is_back(options[text.ask_other_menu]): 
            break # Go back to menu

        # Cells td list. As parameter or asked for
        if lst_cells:
            options[text.ask_select_cells] = lst_cells

        st = time.time_ns() # Set the timer
        ok, path = stats_tables.calculate(options) # Calculate with the given options
        cnsl.log(text.process_time('Total processing time is ', st), cfg.verbose)

        if ok:
            if options[text.ask_file_type] in text.lst_output_files:
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
    table_stats(title, text.lst_ask_stats, cfg.lst_cells_winter_summer)

def table_stats_winter():
    title = 'winter statistics'
    table_stats(title, text.lst_ask_stats, cfg.lst_cells_winter)

def table_stats_summer(): 
    title = 'summer statistics'
    table_stats(title, text.lst_ask_stats, cfg.lst_cells_summer)

def table_stats_default_1(): 
    title = 'my default statistics 1'
    table_stats(title, text.lst_ask_stats, cfg.lst_cells_my_default_1)

def table_stats_extremes(): 
    title = 'my default extremes'
    table_stats(title, text.lst_ask_stats, cfg.lst_cells_my_extremes)

def table_stats_counts(): 
    title = 'my default counters'
    table_stats(title, text.lst_ask_stats, cfg.lst_cells_my_counts)

def table_stats_diy():
    title ='diy statistics'
    table_stats(title, text.lst_ask_stats_diy)
    
def table_stats_period_in_period():
    title = 'period statistics'
    table_stats(title, text.lst_ask_stats_p1_p2_diy)

def table_stats_compare():
    title = 'compare statistics'
    table_stats(title, text.lst_ask_stats_compare)

# Add your own default function
# See menu.py -> def select_menu_option( option ):
# See text.py -> lst_menu_statistics
def table_stats_id_1(): 
    title = 'statistics <subject>'
    table_stats(title, text.lst_ask_stats, cfg.lst_cells_id_1) 

##########################################################################################
# DAYVALUES
def make_dayvalues():
    '''Funtion gets day values from data knmi '''
    while True:
        cnsl.log(text.head('START MAKE DAY VALUES'), True)
        title = 'dayvalues' # Unused!
 
        # Ask list with questions
        options = ask.lst(
            text.lst_ask_make_dayval, title, default=cfg.e, 
            back=True, prev=True, exit=True, spacer=True
        )

        if answer.is_back(options[text.ask_other_menu]): break # Go back to menu

        options[text.ask_download] = False # Default is False, do not give a download option
        options[text.ask_select_cells] = cfg.lst_cells_dayvalues # Data cells to show

        st = time.time_ns()
        ok, path = dayvalues.calculate(options)
        cnsl.log(text.process_time('Total processing time is ', st), cfg.verbose)

        if ok:
            if options[text.ask_file_type] in text.lst_output_files:
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

    cnsl.log(text.foot('END MAKE DAY VALUES'), True)

def see_dayvalues():
    '''Funtion for seeing a day value from data knmi '''
    while True:
        cnsl.log(text.head('START SEE A DAY'), True)
        title = 'see a day' # Unused!
        options = ask.lst(text.lst_ask_see_dayval, title, default=cfg.e, back=True, prev=True, exit=True, spacer=True)

        if answer.is_back(options[text.ask_other_menu]): 
            break # Go back to menu

        options[text.ask_download] = False # Default is False, do not give a download option
        options[text.ask_select_cells] = cfg.lst_cells_dayvalues # Data cells to show

        st = time.time_ns()
        ok, path = dayvalues.calculate(options)
        cnsl.log(text.process_time('Total processing time is ', st), cfg.verbose)

        if ok:
            if options[text.ask_file_type] in text.lst_output_files:
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
        options = ask.lst(
            text.lst_ask_search_4_day, title, default=cfg.e, back=True, prev=True, exit=True, spacer=True
        )

        if answer.is_back(text.ask_other_menu): break # Go back to menu

        st = time.time_ns() # Set the timer
        query_title =  options[text.ask_s4d_query].replace('\s+', ' ').strip()
        options[text.ask_title] = f'{title} ~ {query_title}' # Add query to the title
        options[text.ask_select_cells] = cfg.lst_cells_s4d_default # Set the table colls
        ok, path = stats_tables.calculate(options) # Calculate with the given options
        cnsl.log(text.process_time('Total processing time is ', st), cfg.verbose)

        if ok:
            if options[text.ask_file_type] in text.lst_output_files:
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
def weather_buienradar_forecast():
    '''Function downloads and print a global weather forecast from the website from the knmi'''
    cnsl.log(text.head('START FORECAST BUIENRADAR'), True)
    weather.process('buienradar-weather')
    cnsl.log(text.foot('END FORECAST BUIENRADAR'), True)
    ask.question(text.back_main, default=cfg.e, back=False, prev=False, exit=True, spacer=True)

# weather cities
def weather_buienradar_current():
    '''Function downloads and print a actual weather values to the screen'''
    cnsl.log(text.head('START WEATHERSTATIONS BUIENRADAR'), True)
    weather.process('buienradar-stations')
    cnsl.log(text.foot('END WEATHERSTATIONS BUIENRADAR'), True)
    ask.question(text.back_main, default=cfg.e, back=False, prev=False, exit=True, spacer=True)

##########################################################################################
# KNMI Weather
def weather_knmi_forecast():
    '''Function downloads and prints a global weather forecast from the website from the knmi'''
    cnsl.log(text.head('START FORECAST KNMI'), True)
    weather.process('knmi-weather')
    cnsl.log(text.foot('END FORECAST KNMI'), True)
    ask.question(text.back_main, default=cfg.e, back=False, prev=False, exit=True, spacer=True)

def weather_knmi_model():
    '''Function downloads and prints a global weather forecast from the website from the knmi'''
    cnsl.log(text.head('START KNMI FORECAST MODEL LONG TERM'), True)
    weather.process('knmi-model')
    cnsl.log(text.foot('END KNMI FORECAST MODEL LONG TERM'), True)
    ask.question(text.back_main, default=cfg.e, back=False, prev=False, exit=True, spacer=True)

def weather_knmi_guidance():
    '''Function downloads and prints a global weather forecast from the website from the knmi'''
    cnsl.log(text.head('START KNMI FORECAST GUIDANCE SHORT TERM'), True)
    weather.process('knmi-guidance')
    cnsl.log(text.foot('END KNMI FORECAST GUIDANCE SHORT TERM'), True)
    ask.question(text.back_main, default=cfg.e, back=False, prev=False, exit=True, spacer=True)

def weather_knmi_current():
    '''Function downloads and print a actual weather values to the screen'''
    cnsl.log(text.head('START WEATHERSTATIONS KNMI'), True)
    weather.process('knmi-stations')
    cnsl.log(text.foot('END WEATHERSTATIONS KNMI'), True)
    ask.question(text.back_main, default=cfg.e, back=False, prev=False, exit=True, spacer=True)

##########################################################################################
# GRAPHS
def graph_period():
    '''Funtion makes images for a period from the data of the knmi'''
    while True:
        cnsl.log(text.head('START MAKE GRAPH'), True)

        # Ask list with questions
        title = 'graph statistics'
        options = ask.lst(text.lst_ask_graph, title, default=cfg.e, back=True, prev=True, exit=True, spacer=True)
        options[text.ask_file_type] = options[text.ask_graph_extension] # For use in execute with default app

        if answer.is_back(text.ask_other_menu): break # Go back to menu

        st = time.time_ns()
        ok, path = graphs.calculate(options)
        cnsl.log( text.process_time( 'Total processing time is ', st ), cfg.verbose )

        if ok:
            cnsl.log( f'Graph made success\n{path}', True )
            if options[text.ask_file_type] in text.lst_output_files:
                if answer.is_back( 
                    ask.open_with_app( path, options, back=False, prev=False, exit=True, spacer=True)
                ): 
                    break
        else:
            cnsl.log('Graph made failed', True )
                    
        if ask.is_yes(
            'Do you want to make more graphs ?', default='y', back=False, prev=False, exit=True, spacer=True
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
#         options = ask.lst(lst_ask, title, default=cfg.e, back=True, prev=True, exit=True, spacer=True)

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
def download_images():
    '''Function downloads images'''
    title = 'download (weather images) and make an animation'
    lst_ask = text.lst_ask_download + [text.ask_verbose] # Ask list with questions

    while True:
        cnsl.log(text.head('START DOWNLOAD IMAGES'), True)

        options = ask.lst(lst_ask, title, back=True, prev=True, exit=True, spacer=True)

        if answer.is_back(options[text.ask_other_menu]): break # Go back to menu

        yymd, hms = options[text.ask_start_date].split(' ') # get date and time 

        # Wait/pause till download must start
        st = time.time_ns() # Set the timer
        utils.pause(
            end_date = yymd, # <optional> Date to start. Format <yyyymmdd> or <yyyy-mm-dd>
            end_time = hms,    # Time with format <HH:MM:SS> or <HHMMSS> to pause untill to
                  # If omitted current date will be used.
            output  = 'Programm will start downloading images at',   # <optional> Output text second substring
            verbose = options[text.ask_verbose]
        )
        # Dowload the images
        lst_images = animation.download_interval(
                url             =  options[text.ask_download_url],      # Url for the files on the web
                start_datetime  =  options[text.ask_start_date],        # Start time <yyyy-mm-dd HH:MM:SS>
                end_datetime    =  options[text.ask_end_date],          # End datetime <yyyy-mm-dd HH:MM:SS>
                interval        =  options[text.ask_download_interval], # Interval time for downloading Images (minutes)
                check           =  True,                                # No double downloads check
                verbose         =  options[text.ask_verbose]            # With output to screen
        )
        cnsl.log(text.process_time('Total processing time is ', st), cfg.verbose)
        
        # Show downloaded images to screen
        cnsl.log( text.head(f'[{ymd.now()}] Downloaded images are'), options[text.ask_verbose] )
        for n, img in enumerate(lst_images, start=1): print( f'{n}: {img}' )
        cnsl.log( f'{text.line_hashtag()}\n', options[text.ask_verbose] )

        if ask.is_yes(
            f'Do you want to download more images?', default='y', back=False, prev=False, exit=True, spacer=True
        ):
            continue 
        else:
            break # Stop download images

    cnsl.log(text.foot('END DOWNLOAD IMAGES'), True)


def download_animation():
    '''Function downloads images and makes from the downloaded images an animation'''
    title = 'download (weather images) and make an animation'
    lst_ask = text.lst_ask_download + text.lst_ask_animation + [text.ask_verbose] 

    while True:
        cnsl.log(text.head('START DOWNLOAD IMAGES AND MAKE AN ANIMATION'), True)
        # Ask list with questions
        options = ask.lst(lst_ask, title, back=True, prev=True, exit=True, spacer=True)

        if answer.is_back(options[text.ask_other_menu]): 
            break # Go back to menu

        options[text.ask_file_type] = cfg.animation_ext # Animation extension

        st = time.time_ns() # Set the timer
        ok, path = animation.download_images_and_make_animations(
            options[text.ask_download_url],      # Url for the files on the web
            options[text.ask_animation_name],    # Name of animation file   
            options[text.ask_start_date],        # Start time <yyyy-mm-dd HH:MM:SS>
            options[text.ask_end_date],          # End datetime <yyyy-mm-dd HH:MM:SS>
            options[text.ask_download_interval], # Interval time for downloading Images (minutes)
            True,                                # No double downloads check
            options[text.ask_animation_time],    # Animation interval time for gif animation
            options[text.ask_rm_downloads],      # Remove the downloaded images
            options[text.ask_gif_compress],      # Compress the size of the animation
            options[text.ask_verbose]            # With output to screen
        )
        cnsl.log(text.process_time('Total processing time is ', st), cfg.verbose)

        if ok:
            if options[text.ask_file_type] in text.lst_output_gif:
                if answer.is_back(
                    ask.open_with_app(
                        path, options, back=False, prev=False, exit=True, spacer=True
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
def animation_images_from_map():
    # Read images from a given map or maps
    # Sort images on date
    # Make animation
    pass


##########################################################################################
# DATABASES
def database_update():

    '''Function downloads images ad makes an animation'''
    title = 'Update database'
    lst_ask = [
        'image-download-url', 'start-datetime', 'end-datetime', 'interval-download', 
        'animation-name', 'animation-time', 'remove-downloads', 'gif-compress', 'verbose'
    ]
    while True:
        cnsl.log(text.head('START UPDATE DATABASE'), True)
        # Ask list with questions
        options = ask.lst(lst_ask, title, back=True, prev=True, exit=True, spacer=True)

        if answer.is_back(options['other']): break # Go back to menu

        options['file-type'] = cfg.animation_ext

        st = time.time_ns() # Set the timer
        ok, path = database.calculate(
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

    cnsl.log(text.foot('END UPDATE DATABASE'), True)

##########################################################################################
# MAIN MENU 
def select_menu_option( option ):
    '''Broker between text menu and python functions'''
    # Downloads
    if   option == text.menu_knmi_dayvalues_all:          download_knmi_dayvalues_all()
    elif option == text.menu_knmi_dayvalues_select:       download_knmi_dayvalues_select()
    # Statistics
    elif option == text.menu_table_stats_diy:             table_stats_diy()
    elif option == text.menu_table_stats_winter:          table_stats_winter()
    elif option == text.menu_table_stats_summer:          table_stats_summer()
    elif option == text.menu_table_stats_winter_summer:   table_stats_winter_summer()
    elif option == text.menu_table_stats_extremes:        table_stats_extremes()
    elif option == text.menu_table_stats_counts:          table_stats_counts()
    elif option == text.menu_table_stats_default_1:       table_stats_default_1()

    # Add your own stats table menu option
    # elif option == text.menu_table_stats_id_1:          table_stats_id_1()
    # See text.py -> lst_menu_statistics 

    elif option == text.menu_table_stats_per2_in_per1:    table_stats_period_in_period()
    elif option == text.menu_table_stats_compare:         table_stats_compare()
    # Days
    elif option == text.menu_make_dayvalues:              make_dayvalues()
    # TODO
    # elif option == text.menu_see_dayvalues:             see_dayvalues()
    elif option == text.menu_search_for_days:             search_for_days()

    # Graphs
    elif option == text.menu_graph_period:                graph_period()
    # Weather
    elif option == text.menu_buienradar_forecast:         weather_buienradar_forecast()
    elif option == text.menu_buienradar_act_values:       weather_buienradar_current()

    # Oke jammer! ftp pub opgeheven
    elif option == text.menu_knmi_forecast:               weather_knmi_forecast()
    elif option == text.menu_knmi_forecast_model:         weather_knmi_model()
    elif option == text.menu_knmi_forecast_guidance:      weather_knmi_guidance()
    elif option == text.menu_knmi_act_values:             weather_knmi_current()

    # Animations
    elif option == text.menu_anim_download_animation:     download_animation()
    elif option == text.menu_anim_download_images:        download_images()
    elif option == text.menu_anim_images_fom_map:         animation_images_from_map()

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
        num, main = 1, cfg.e
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
