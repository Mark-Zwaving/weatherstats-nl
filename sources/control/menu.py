'''Library contains functions for asking questions and to deal with the input
given by a user'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.3.7'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import time, os
import config as cfg, defaults
import sources.view.graphs as graphs
import sources.model.forecast.broker as weather
import sources.model.animation as animation
import sources.model.utils as utils
import sources.model.database as database
import sources.model.ymd as ymd
import sources.model.images as images
import sources.control.fio as fio
import sources.control.ask.answer as answer
import sources.control.ask.broker.questions as broker_questions
import sources.control.dayvalues.download as dayvalues_download
import sources.control.ask.question as ask_question
import sources.view.console as cnsl
import sources.view.text as text
import sources.view.dayvalues as dayvalues
import sources.view.select_days as select_days
import sources.view.table.broker as tbl_broker

##########################################################################################
# KNMI download dayvalues OK
def download_knmi_dayvalues_all(): 
    '''Functions process data (download and unzip) from all 
       the weatherstations listed in the stations.lst'''
    cnsl.log(text.head('START DOWNLOAD ALL DAYVALUES KNMI'), True)
    dayvalues_download.process_all()
    cnsl.log(text.foot('END DOWNLOAD ALL DAYVALUES KNMI'), True)

    # Press enter to go back
    ask_question.ask(text.enter_back_main, default=cfg.e, 
                 back=False, prev=False, exit=True, spacer=True)

def download_knmi_dayvalues_select(): 
    '''Function asks for one or more wmo numbers to process 
       (download and unzip) the data'''
    # Menu title
    title = 'Download one or more stations'

    while True:
        cnsl.log( text.head('START DOWNLOAD DAYVALUES KNMI'), True)

        # Ask to download specific files
        options = broker_questions.process(text.lst_ask_download_knmi, title, default=cfg.e,
                                           back=True, prev=False, exit=True, spacer=True)

        # If the options list has the go back to main menu option filled in
        if options[text.ask_other_menu]:  
            break # Go back to mainmenu

        # Download the stations in the list
        dayvalues_download.process_lst(options[text.ask_lst_stations])

        # More downloads?
        if answer.is_yes( ask_question.y_or_n( 
                'Do you want to download more stations?', default='n', 
                back=False, prev=False, exit=True, spacer=True
            ) ):
            continue 

        break

    cnsl.log(text.foot('END DOWNLOAD DAYVALUES KNMI'), True)

##########################################################################################
# TABLE STATISTICS OK
# Base fn for table statistics
def table_stats(
        title,         # Title to show in the menu
        lst_cells=[],  # What are the statisitcs cells to calculate for
        lst_questions = text.lst_ask_stats  # Lst with all the questions
    ):
    '''Function makes calculations for all statistics'''
    
    while True:
        cnsl.log(text.head(f'START {title.capitalize()}'), True)

        # Ask list with questions
        options = broker_questions.process(lst_questions, title, default=cfg.e, 
                                           back=True, prev=True, exit=True, spacer=True)

        # If the options list has the go back to main menu option fiiled in
        if options[text.ask_other_menu]:  
            break # Go back to mainmenu

        # Cells td list. As parameter or asked for
        if lst_cells:
            options[text.ask_select_cells] = lst_cells

        # Calculate the statistics
        st = time.time_ns() # Start the timer
        ok, path = tbl_broker.process(options) # Calculate with the given options
        et = time.time_ns() # End the timer
        t = utils.process_time_delta_ns('Total process time is ', et - st)
        cnsl.log(t, cfg.verbose)

        if ok:
            typ = options[text.ask_file_type]
            if typ in text.lst_output_files:
                if answer.is_yes( ask_question.y_or_n(
                        f'Do you want to open the <{typ}> file ?', default='y', 
                        back=False, prev=False, exit=True, spacer=True
                    ) ):
                    utils.exec_with_app(path, verbose=False)

        # Ask to make another table
        if answer.is_yes( ask_question.y_or_n(
                f'Do you want to make another <{title}> table ?', 
                default='n', back=False, prev=False, exit=True, spacer=True
            ) ):
            continue 
        break # Stop table stats

    cnsl.log(text.foot(f'END {title.capitalize()}'), True)

def table_stats_diy():
    title = 'DIY statistics'
    lst_questions = text.lst_ask_stats_diy
    table_stats(title, lst_cells=[], lst_questions=lst_questions )
    
def table_stats_period_in_period():
    '''Two periods: period a period in a period'''
    title = 'Two periods statistics' 
    lst_questions = text.lst_ask_stats_p1_p2_diy # List with another period
    table_stats(title, lst_cells=[], lst_questions=lst_questions)

def table_stats_period_compare():
    title = 'compare statistics'
    lst_questions = text.lst_ask_stats_compare
    table_stats(title, lst_cells=[], lst_questions=lst_questions)

##########################################################################################
# DAYVALUES OK
def make_days_dayvalues():
    '''Funtion makes files with day values from data knmi '''
    title = 'dayvalues' # Unused!

    while True:
        cnsl.log(text.head('START MAKE DAY VALUES'), True)
 
        # Ask list with questions
        options = broker_questions.process(text.lst_ask_make_dayval, title, default=cfg.e, 
                                           back=True, prev=True, exit=True, spacer=True) 

        # If the options list has the go back to main menu option filled in
        if options[text.ask_other_menu]:  
            break # Go back to mainmenu

        options[text.ask_select_cells] = defaults.lst_dayvalues # Data cells to show

        st = time.time_ns() # Start the timer
        ok, path = dayvalues.process(options)
        et = time.time_ns() # End the timer
        t = utils.process_time_delta_ns('Total process time is ', et - st)
        cnsl.log(t + cfg.ln, cfg.verbose)

        if ok:
            if options[text.ask_file_type] in text.lst_output_htm:
                if answer.is_yes( ask_question.y_or_n(
                    f'Do you want to open the main index html file ?', default='y', 
                    back=False, prev=False, exit=True, spacer=True
                ) ):
                    utils.exec_with_app(path, verbose=False)
            # TODO other file types

        if answer.is_yes( ask_question.y_or_n(
                'Do you want to make more dayvalues ?', 
                default='n', back=False, prev=False, exit=True, spacer=True
            ) ):
            continue 
        break 

    cnsl.log(text.foot('END MAKE DAY VALUES'), True)

def see_days_dayvalues():
    '''Funtion for seeing a day value from data knmi '''
    while True:
        cnsl.log(text.head('START SEE DAYS'), True)
        title = 'see a day' # Unused!
        options = broker_questions.process(text.lst_ask_see_dayval, title, default=cfg.e,
                                           back=True, prev=True, exit=True, spacer=True )

        # If the options list has the go back to main menu option filled in
        if options[text.ask_other_menu]:  
            break # Go back to mainmenu

        options[text.ask_download] = False # Default is False, do not give a download option
        options[text.ask_file_type] = text.lst_output_cnsl[0] # 

        st = time.time_ns() # Start the timer
        ok, path, txt = select_days.process(options)
        et = time.time_ns() # End the timer
        t = utils.process_time_delta_ns('Total process time is ', et - st)
        cnsl.log(t + cfg.ln, cfg.verbose)

        if ok:
            if answer.is_yes( ask_question.y_or_n(
                    'Do you want to save the results in a file ?', 'n', 
                    back=False, prev=False, exit=True, spacer=True
                ) ):
                select_days.save_txt_file()

        if answer.is_yes( ask_question.y_or_n(
                'Do you want to see more days ?', default='n', 
                back=False, prev=False, exit=True, spacer=True 
            ) ):
            continue 
        else:
            break 

    cnsl.log(text.foot('END SEE DAYVALUES'), True)

##########################################################################################
# SEARCH FOR DAYS
def search_for_days_dayvalues():
    '''Function searches files for days with specific values. ie > 30 degrees'''
    while True:
        cnsl.log(text.head('START SEARCH 4 DAYS'), True)

        # Ask list with questions
        title = 'search 4 days'
        options = broker_questions.process(text.lst_ask_search_4_day, title, default=cfg.e, 
                                           back=True, prev=True, exit=True, spacer=True
        )

        # If the options list has the go back to main menu option fiiled in
        if options[text.ask_other_menu]: 
            break # Go back to mainmenu

        st = time.time_ns() # Start the timer
        query_title =  options[text.ask_s4d_query].replace('\s+', ' ').strip()
        options[text.ask_title] = f'{title} ~ {query_title}' # Add query to the title
        options[text.ask_select_cells] = defaults.lst_search4day # Set the table colls
        ok, path = tbl_broker.process(options) # Calculate with the given options
        et = time.time_ns() # End the timer
        t = utils.process_time_delta_ns('Total process time is ', et - st)
        cnsl.log(t, cfg.verbose)

        if ok:
            typ = options[text.ask_file_type]
            if typ in text.lst_output_htm:
                if answer.is_yes( ask_question.y_or_n(
                    f'Do you want to open the <{typ}> file ?', default='y', 
                    back=False, prev=False, exit=True, spacer=True
                ) ):
                    utils.exec_with_app(path, verbose=False)

        if answer.is_yes( ask_question.y_or_n(
            'Do you want to do a search for days again ?', 
            default='n', back=False, prev=False, exit=True, spacer=True
            ) ):
            continue 
        
        break 

    cnsl.log(text.foot('END SEARCH 4 DAYS'), True)

##########################################################################################
# BUIENRADAR 
# Forecast
def weather_buienradar_forecast():
    '''Function downloads and print a global weather forecast from the website from the knmi'''
    cnsl.log(text.head('START FORECAST BUIENRADAR'), True)
    weather.process('buienradar-forecast')
    cnsl.log(text.foot('END FORECAST BUIENRADAR'), True)
    ask_question.ask(text.enter_back_main, default=cfg.e, 
                     back=False, prev=False, exit=True, spacer=True)

# Weather cities
def weather_buienradar_stations():
    '''Function downloads and print a actual weather values to the screen'''
    cnsl.log(text.head('START WEATHERSTATIONS BUIENRADAR'), True)
    weather.process('buienradar-stations')
    cnsl.log(text.foot('END WEATHERSTATIONS BUIENRADAR'), True)
    ask_question.ask(text.enter_back_main, default=cfg.e, 
                     back=False, prev=False, exit=True, spacer=True)

##########################################################################################
# KNMI Weather
# Forecast
def weather_knmi_forecast():
    '''Function downloads and prints a global weather forecast from the website from the knmi'''
    cnsl.log(text.head('START FORECAST KNMI'), True)
    weather.process('knmi-forecast')
    cnsl.log(text.foot('END FORECAST KNMI'), True)
    ask_question.ask(text.enter_back_main, default=cfg.e, 
                     back=False, prev=False, exit=True, spacer=True)

# Weather cities
def weather_knmi_stations():
    '''Function downloads and prints a global weather forecast from the website from the knmi'''
    cnsl.log(text.head('START WEATHERSTATIONS KNMI'), True)
    weather.process('knmi-stations')
    cnsl.log(text.foot('END WEATHERSTATIONS KNMI'), True)
    ask_question.ask(text.enter_back_main, default=cfg.e, 
                     back=False, prev=False, exit=True, spacer=True)

# def weather_knmi_model():
#     '''Function downloads and prints a global weather forecast from the website from the knmi'''
#     cnsl.log(text.head('START KNMI FORECAST MODEL LONG TERM'), True)
#     weather.process('knmi-model')
#     cnsl.log(text.foot('END KNMI FORECAST MODEL LONG TERM'), True)
#     questions.ask(text.enter_back_main(), default=cfg.e, back=False, prev=False, exit=True, spacer=True)

# def weather_knmi_guidance():
#     '''Function downloads and prints a global weather forecast from the website from the knmi'''
#     cnsl.log(text.head('START KNMI FORECAST GUIDANCE SHORT TERM'), True)
#     weather.process('knmi-guidance')
#     cnsl.log(text.foot('END KNMI FORECAST GUIDANCE SHORT TERM'), True)
#     questions.ask(text.enter_back_main(), default=cfg.e, back=False, prev=False, exit=True, spacer=True)

# def weather_knmi_current():
#     '''Function downloads and print a actual weather values to the screen'''
#     cnsl.log(text.head('START WEATHERSTATIONS KNMI'), True)
#     weather.process('knmi-stations')
#     cnsl.log(text.foot('END WEATHERSTATIONS KNMI'), True)
#     questions.ask(text.enter_back_main(), default=cfg.e, back=False, prev=False, exit=True, spacer=True)

##########################################################################################
# GRAPHS
def graph_period():
    '''Funtion makes images for a period from the data of the knmi'''
    while True:
        cnsl.log(text.head('START MAKE GRAPH'), True)

        # Ask list with questions
        title = 'graph statistics'
        options = broker_questions.process(text.lst_ask_graph, title, default=cfg.e, 
                                           back=True, prev=True, exit=True, spacer=True)

        # If the options list has the go back to main menu option filled in
        if options[text.ask_other_menu]:  
            break # Go back to mainmenu

        st = time.time_ns() # Start the timer
        ok, path = graphs.calculate(options)
        et = time.time_ns() # End the timer
        t = utils.process_time_delta_ns('Total process time is ', et - st)
        cnsl.log(t, cfg.verbose)

        if ok and answer.is_yes( ask_question.y_or_n(
                f'Do you want to open the graph ?', default='y', 
                back=False, prev=False, exit=True, spacer=True
            ) ):
            utils.exec_with_app(path, verbose=False)
        else:
            cnsl.log('Graph made failed', True )

        if answer.is_yes( ask_question.y_or_n(
                'Do you want to make more graphs ?', default='y', 
                back=False, prev=False, exit=True, spacer=True
            ) ):
            continue 
        
        break 

    cnsl.log(text.foot('END MAKE GRAPH'), True)

# def graph_period_quick_default():
#     while True:
#         cnsl.log(txt.head('START MAKE DEFAULT GRAPH'), True)

#         title = 'graph statistics'
#         lst_ask = ['lst-stations', 'period']
#         options = broker_questions.process(lst_ask, title, default=cfg.e, back=True, prev=True, exit=True, spacer=True)

#         st = time.time_ns()
#         path = graphs.calculate(options)
#         cnsl.log( utils.process_time_ns('Total process time is ',st), cfg.verbose )

#         if answer.is_quit( questions.open_with_default_app(path, options) ):
#             break

#         if answer.is_quit( ask.again('Do you want to make more graphs ?') ):
#             break

#     cnsl.log(txt.foot('END MAKE GRAPH'), True)



# def graph_period_quick_default():
#     while True:
#         cnsl.log(txt.head('START MAKE DEFAULT GRAPH'), True)

#         st = time.time_ns()
#         path = graphs.calculate(options)
#         cnsl.log( utils.process_time_ns('Total process time is ',st), cfg.verbose )

#         if answer.is_quit( questions.open_with_default_app(path, options) ):
#             break

#         if answer.is_quit( ask.again('Do you want to make more graphs ?') ):
#             break

#     cnsl.log(txt.foot('END MAKE GRAPH'), True)

##########################################################################################
# ANIMATIONS
def interval_download_files():
    '''Function downloads images'''
    title = 'download (weather) images'

    while True:
        cnsl.log(text.head('START DOWNLOAD IMAGES'), True)

        options = broker_questions.process(text.lst_ask_download_files, title, 
                                           back=True, prev=True, exit=True, spacer=True)

        # If the options list has the go back to main menu option filled in
        if options[text.ask_other_menu]:  
            break # Go back to mainmenu

        # Get the start download date and time 
        yymd, hms = options[text.ask_start_datetime].split(' ') 

        # Start the timer
        st = time.time_ns() 

        # Pause untill download must start
        utils.pause(
            # <optional> Date to start. Format <yyyymmdd> or <yyyy-mm-dd>
            end_date = yymd, 
            # Time with format <HH:MM:SS> or <HHMMSS> to pause untill to
            end_time = hms,  # If omitted current date will be used.
            # <optional> Output text second substring
            output  = 'Programm will start downloading images at',   
            # Show more
            verbose = True ) 
        
        # Dowload the images
        lst_images = fio.download_interval(
                url            =  options[text.ask_download_url],      # Url for the files on the web
                start_datetime =  options[text.ask_start_datetime],    # Start time <yyyy-mm-dd HH:MM:SS>
                end_datetime   =  options[text.ask_end_datetime],      # End datetime <yyyy-mm-dd HH:MM:SS>
                interval       =  options[text.ask_download_interval], # Interval time for downloading Images (minutes)
                check          =  True,                                # No double downloads check
                verbose        =  True )          # With output to scree

        # End the timer
        et = time.time_ns() 

        t = utils.process_time_delta_ns('Total process time is ', et - st)
        cnsl.log(t + cfg.ln, cfg.verbose)
        
        # Show downloaded images to screen
        cnsl.log(f'[{ymd.now()}] Downloaded images are', True)
        for num, path in enumerate(lst_images, start=1): 
            cnsl.log(f'{num}: {path}', True )
        cnsl.log(' ', True)

        # Ask for again
        if answer.is_yes( ask_question.y_or_n(
            f'Do you want to download more files?', default='n', 
            back=False, prev=False, exit=True, spacer=True
           ) ):
            continue 
        
        break # Stop download images

    cnsl.log( text.foot('END DOWNLOAD IMAGES'), True )

def download_animation():
    '''Function downloads images and makes from the downloaded images an animation'''
    title = 'download (weather images) and make an animation'

    while True:
        cnsl.log(text.head('START DOWNLOAD IMAGES AND MAKE AN ANIMATION'), True)

        # pprint.pp(text.lst_ask_download_files + text.lst_ask_animation)

        # Ask list with question
        ask_lst = text.lst_ask_download_files + text.lst_ask_animation
        options = broker_questions.process(ask_lst, title, default=cfg.e, 
                                          back=True, prev=True, exit=True, spacer=True)

        # If the options list has the go back to main menu option filled in
        if options[text.ask_other_menu]:  
            break # Go back to main menu

        # Get the start download date and time 
        yymd, hms = options[text.ask_start_datetime].split(' ') 

        # Start the global timer
        st = time.time_ns() 

        # Pause untill download must start
        utils.pause(
            # <optional> Date to start. Format <yyyymmdd> or <yyyy-mm-dd>
            end_date = yymd, 
            # Time with format <HH:MM:SS> or <HHMMSS> to pause untill to
            end_time = hms,  # If omitted current date will be used.
            # <optional> Output text second substring
            output  = 'Programm will start downloading images at',   
            # Show more
            verbose = True ) 
        
        # Dowload the images
        lst_images = fio.download_interval(
                # Url for the files on the web
                url            =  options[text.ask_download_url],
                # Start time <yyyy-mm-dd HH:MM:SS>
                start_datetime =  options[text.ask_start_datetime],
                # End datetime <yyyy-mm-dd HH:MM:SS>
                end_datetime   =  options[text.ask_end_datetime],
                 # Interval time for downloading Images (minutes)
                interval       =  options[text.ask_download_interval],
                # No double downloads check
                check          =  True,
                # With output to screen   
                verbose        =  True )
    
        # Make add animation path to file name
        y, m, d, H, M, S = ymd.y_m_d_h_m_s_now() # Get current date and time
        animation_map = os.path.join(cfg.dir_animation, f'{y}/{m}/{d}')
        path = os.path.join(animation_map, options[text.ask_animation_name])

        # Create the animation
        ok, path = animation.create(
            # File path/name for the animation image
            path,  
            # List with all the images for the animation        
            lst_images,
            # Interval time for the image
            options[text.ask_animation_time], 
            # Show output on screen
            True )

        # Compress the gif if asked for
        if answer.is_yes(options[text.ask_gif_compress]):
            images.compress_gif( path, verbose=True )

        # End the timer
        et = time.time_ns()
        t = utils.process_time_delta_ns('Total process time is ', et - st)
        cnsl.log(t + cfg.ln, cfg.verbose)

        if ok and answer.is_yes( ask_question.y_or_n(
                f'Do you want to open the animation file ?', default='y', 
                back=False, prev=False, exit=True, spacer=True
            ) ):
            utils.exec_with_app(path, verbose=False)

        if answer.is_yes( ask_question.y_or_n(
                f'Do you want to make another animation ?', default='n', 
                back=False, prev=False, exit=True, spacer=True 
            ) ):
            continue 

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
def database_create_renew():
    '''Function downloads images ad makes an animation'''
    title = 'Fill database'
    lst_ask = text.lst_ask_db_fill 

    while True:
        cnsl.log(text.head('START FILL DATABASE'), True)

        # Ask list with questions
        options = broker_questions.process(lst_ask, title, default=cfg.e,
                                           back=True, prev=False, exit=True, spacer=True )

        # If the options list has the go back to main menu option filled in
        if options[text.ask_other_menu]:  
            break # Go back to mainmenu

        st = time.time_ns() # Start the timer
        ok = database.calculate(options)
        et = time.time_ns() # End the timer
        t = utils.process_time_delta_ns('Total process time is ', et - st)
        cnsl.log(t, cfg.verbose)

    cnsl.log(text.foot('END FILL DATABASE'), True)

    # Ask to go back to the main menu
    ask_question.ask(text.enter_back_main(), default=cfg.e,
                     back=False, prev=False, exit=True, spacer=True)

def database_query():
    title = 'SQLite query'
    lst_ask = text.lst_ask_sqlite_query
    while True:
        cnsl.log(text.head('START EXECUTE QUERY'), True)

        # Ask list with questions
        options = broker_questions.process(lst_ask, title, default=cfg.e,
                                           back=True, prev=False, exit=True, spacer=True )

        # If the options list has the go back to main menu option filled in
        if options[text.ask_other_menu]:  
            break # Go back to mainmenu

        st = time.time_ns() # Start the timer
        ok, rows = database.select(options)
        et = time.time_ns() # End the timer
        t = utils.process_time_delta_ns('Total process time is ', et - st)
        cnsl.log(t, cfg.verbose)

        if ok:
            for row in rows:
                cnsl.log(row, True)
        
        if answer.is_yes( ask_question.y_or_n(
                f'Do you want te execute an other query?', 
                default='y', back=False, prev=False, exit=True, spacer=True
            ) ):
            continue 
        
        break # Stop execute queries

    cnsl.log(text.foot('END EXECUTE QUERY'), True)

def todo():
    pass
