'''Library processes the questions in a given lst'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.2.4'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import sources.control.fio as fio
import sources.control.ask.answer as answer
import sources.control.ask.question as question
import sources.model.utils as utils
import sources.model.ymd as ymd
import sources.view.text as text

# Init the empthy dictionary with all the possible answers/results
# This dictionary has to be filled with the given answers
dict_results = {
    text.ask_title:                   '', 
    text.ask_lst_stations:            [],
    text.ask_lst_period_1:            [],  # NEW
    text.ask_period_1:                '', 
    text.ask_period_2:                '', 
    text.ask_per_compare:             '',

    # TODO ASK for years and put in year in head of table
    text.ask_clima_period:            cfg.climate_period, 
    text.ask_select_cells:            [],
    text.ask_s4d_query:               '', 
    text.ask_write_dayval:            '', 
    text.ask_lst_see_days:            [],
    text.ask_save_txt_file:           '',
    text.ask_file_type:               '',
    text.ask_filename:                '',
    text.ask_lst_entities:            [],

    # Graphs
    text.ask_graph_title:             '',
    text.ask_graph_ylabel:            '', 
    text.ask_graph_default:           cfg.plot_default,
    text.ask_graph_width:             cfg.plot_width,
    text.ask_graph_height:            cfg.plot_height ,
    text.ask_graph_cummul_val:        cfg.plot_cummul_val ,
    text.ask_graph_extension:         cfg.plot_image_type,
    text.ask_graph_dpi:               cfg.plot_dpi , 
    text.ask_graph_entities:          [],
    text.ask_graph_entities_options:  [],

    # Animation and download images 
    text.ask_download_url:            '',
    text.ask_start_datetime:          '',
    text.ask_end_datetime:            '',
    text.ask_download_interval:       '',
    text.ask_animation_name:          '',
    text.ask_animation_time:          '',
    text.ask_rm_downloads:            '',
    text.ask_gif_compress:            '',
    text.ask_verbose:                 '',

    # Database
    text.ask_sqlite_query:            '', 

    # Go back to menu or backward one question
    text.ask_other_menu:              ''
}

def process(lst_questions, fname, default=cfg.e, 
            back=False, prev=False, exit=False, spacer=False):
    '''Process all the questions given in the lst with the questions'''
    # The list questions has the available question to be ask
    # Put the file name in the dictionary of questions
    dict_results[text.ask_filename] = fname

    # Init default answer
    answ = ''

    # Init questions var
    num_question, max_question = 1, len(lst_questions)

    # Walkthrough all the questions
    while num_question <= max_question:

        # For the first question there cannot be a previous option 
        prev_act = False if num_question == 1 else True 

        # Get correct question from list
        question_act = lst_questions[num_question-1]

        # input(cfg.ln + question_act + cfg.ln)

        # Reset answer and default
        answ, default = '', '' 

        # Ask to download a image url
        if question_act == text.ask_download_url: 
            dict_results[text.ask_download_url] = answ = question.image_download_url(
                'Give an (image) url to download ?', 
                cfg.e, back, prev_act, exit, spacer )
    
        # Ask for stations
        elif question_act == text.ask_lst_stations:
            dict_results[text.ask_lst_stations] = answ = question.lst_places(
                'Select one or more weatherstations ?', 
                cfg.e, back, prev_act, exit, spacer )

        # Ask for entities
        elif question_act == text.ask_lst_entities:
            dict_results[text.ask_lst_entities] = answ = question.lst_entities(
                'Select one or more weather entities ?', 
                cfg.e, back, prev_act, exit, spacer )

        # Ask for a sqlite query
        elif question_act == text.ask_sqlite_query:
            dict_results[text.ask_sqlite_query] = answ = question.ask(
                'Enter a (sqlite) query ?', 
                cfg.e, back, prev_act, exit, spacer )
            
        # Ask for a start datetime
        elif question_act == text.ask_start_datetime: 
            dt_plus = utils.datetime_plus_minutes_rounded( minute=10 )
            dict_results[text.ask_start_datetime] = answ = question.date_time( 
                'a start', dt_plus, back, prev_act, exit, spacer )

        # Ask for a end datetime
        elif question_act == text.ask_end_datetime: 
            dt_plus = utils.datetime_plus_minutes_rounded( minute=70 )
            dict_results[text.ask_end_datetime] = answ = question.date_time( 
                'an end', dt_plus, back, prev_act, exit, spacer )

        # Ask download interval time (integer)
        elif question_act == text.ask_download_interval: 
            default = 10
            dict_results[text.ask_download_interval] = answ = question.integer(
                'Give the interval download time (minutes) ?', 
                default, back, prev_act, exit, spacer ) 

        # Ask for an animation time
        elif question_act == text.ask_animation_time: 
            dict_results[text.ask_animation_time] = answ = question.floatt( 
                    'Give the animation interval time ?', 
                    cfg.animation_time, back, prev_act, exit, spacer ) 

        # Ask for a name for the animation file
        elif question_act == text.ask_animation_name: 
            gif_ext = f'.{cfg.animation_ext}' # Animation extension

            dict_results[text.ask_animation_name] = answ = question.ask(
                'Give a name for the animation file or press enter for default ?', 
                f'animation-{ymd.yyyymmdd_now()}-{ymd.hhmmss_now()}{gif_ext}', # Default
                back, prev_act, exit, spacer )

            # Check for an extension. If it has not ,add it
            if not dict_results[text.ask_animation_name].lower().endswith(gif_ext):
                dict_results[text.ask_animation_name] += gif_ext 

        # UNUSED Ask for an verbose option
        elif question_act == text.ask_verbose: 
            dict_results[text.ask_verbose] = answ = question.y_or_n(
                'Do you want to use the verbose option ?\n'
                'With verbose enabled the programm cannot do something else.\n'
                'Although wsstats can be started in another console.', 
                'y', back, prev_act, exit, spacer )

        # Ask to remove the downloaded files
        elif question_act == text.ask_rm_downloads: 
            dict_results[text.ask_rm_downloads] = answ = question.y_or_n(
                'Do you want to remove the downloaded images ?', 
                'n', back, prev_act, exit, spacer )

        # Ask to compress a gif file animation
        elif question_act == text.ask_gif_compress: 
            dict_results[text.ask_gif_compress] = answ = question.y_or_n(
                'Do you want compress the animation file ?\n'
                'Software gifsicle needs to be installed on your OS...',
                 'n', back, prev_act, exit, spacer )

        # Ask for one or more weatherstations
        elif question_act == text.ask_gif_compress: 
            dict_results[text.ask_gif_compress] = answ = question.lst_places(
                'Select one (or more) weather station(s) ?', 
                cfg.e, back, prev_act, exit, spacer )

        # Ask for the first period
        elif question_act == text.ask_period_1: 
            dict_results[text.ask_period_1] = answ = question.period_1(
                f'Give the period for the calculation of {fname} ?', 
                default, back, prev_act, exit, spacer ) 

        # Ask for the first period list NEW
        elif question_act == text.ask_lst_period_1: 
            dict_results[text.ask_lst_period_1] = answ = question.lst_period_1(
                f'Give the period for the calculation of {fname} ?', 
                default, back, prev_act, exit, spacer ) 

        # Ask for the second period
        elif question_act == text.ask_period_2:
            dict_results[text.ask_period_2] = answ = question.period_2(
                'Select a second day, month or period ?', 
                default, back, prev_act, exit, spacer )

        # Ask for a period to compare with an other period     
        elif question_act == text.ask_per_compare:
            dict_results[text.ask_per_compare] = answ = question.period_compare(
                'Give the period to compare ?', 
                default, back, prev_act, exit, spacer )

        # Ask for DIY cells
        elif question_act == text.ask_diy_cells:
            dict_results[text.ask_diy_cells] = answ = question.period_compare(
                cfg.e, default, back, prev_act, exit, spacer )

            # Is there a second period in the DIY question lst. 
            # If not add one Period 2 to the GLOBAL Question lst!
            if 'inf_period-2' in dict_results[text.ask_diy_cells]: 
                # Add question to lst
                lst_questions.insert(num_question, text.ask_period_2)
                # Increase maximum questions with 1
                max_question = len(lst_questions)  
        
        # Ask for the statistics cell 
        elif question_act == text.ask_select_cells: 
            dict_results[text.ask_select_cells] = answ = question.lst_diy_cells(
                'What will be the statistics cells ?', 
                default, back, prev_act, exit, spacer )

        # Rewrite or only make new non-existing files
        elif question_act == text.ask_write_dayval: 
            dict_results[text.ask_write_dayval] = answ = question.type_options(
                'Do you want to add only new files or rewrite it all ?', 
                ['add', 'rewrite'], 'add', back, prev_act, exit, spacer )

        # Select a list with dates
        elif question_act == text.ask_lst_see_days: 
            dict_results[text.ask_lst_see_days] = answ = question.lst_yyyymmdd(
                'Give the days <yyyymmdd> you want to see ?', 
                default, back, prev_act, exit, spacer )

        # Save to a file?
        elif question_act == text.ask_save_txt_file: 
            dict_results[text.ask_save_txt_file] = answ = question.save_text_file(
                'Do you want to save the result to a file ?', 
                default, back, prev_act, exit, spacer )

        # Ask for a Search for days Query
        elif question_act == text.ask_s4d_query:
            dict_results[text.ask_s4d_query] = answ = question.s4d_query(
                'Type in a query to search for days ?', 
                default, back, prev_act, exit, spacer )

        # Ask for a type file
        elif question_act == text.ask_file_type: # Ask for a file types
            dict_results[text.ask_file_type] = answ = question.file_type(
                'Select type output file ?', 
                cfg.default_output, back, prev_act, exit, spacer )

        # Ask for a filename
        elif question_act == text.ask_filename: 
            # Add query to title if there
            default = f'my-output-filename-{utils.now_for_file()}' 
            default = fio.sanitize_file_name(default)

            # Ask filename
            dict_results[text.ask_filename] = answ = question.file_name(
                'Give a name for the output file ? <optional>', 
                default, back, prev_act, exit, spacer )

        # Ask for a graph title
        elif question_act == text.ask_graph_title:
            dict_results[text.ask_graph_title] = answ = question.ask(
                'Give a title for the graph ?', 
                'My Graph Title', back, prev_act, exit, spacer )

        # Ask for a graph y-as lable
        elif question_act == text.ask_graph_ylabel:
            dict_results[text.ask_graph_ylabel] = answ = question.ask(
                'Give a y-as label for the graph ?', 
                'weatherdata', back, prev_act, exit, spacer )

        # Ask for the entities to show in the grpah
        elif question_act == text.ask_graph_entities:
            dict_results[text.ask_graph_dpi] = answ = question.lst_entities(
                'Select the weather entity(s) for the graph ?', 
                default, back, prev_act, exit, spacer )

        # Ask for the defaults or not
        elif question_act == text.ask_graph_default:
            dict_results[text.ask_graph_default] = answ = question.y_or_n(
                'Do you want to use default values ? See file -> config.py', 
                cfg.plot_default, back, prev_act, exit, spacer )

        # Graph Questions only to be asked asked if 
        # the graph default option is not selected
        if answer.is_no(dict_results[text.ask_graph_default]):

            # Ask for the graph width
            if question_act == text.ask_graph_width:
                
                dict_results[text.ask_graph_width] = answ = question.integer(
                    'Give the width (in pixels) for the graph ?', 
                    cfg.plot_width, back, prev_act, exit, spacer )

            # Ask for the graph height
            elif question_act == text.ask_graph_height:
                dict_results[text.ask_graph_height] = answ = question.integer(
                    'Give the height (in pixels) for the graph ?', 
                    cfg.plot_height, back, prev_act, exit, spacer )

            # Ask for the graph cummulation values option
            elif question_act == text.ask_graph_cummul_val:
                dict_results[text.ask_graph_cummul_val] = answ = question.y_or_n(
                    'Do you want cummulative values for the graph ?', 
                    cfg.plot_cummul_val, back, prev_act, exit, spacer )

            # Ask for the graph type
            elif question_act == text.ask_graph_entity_type:
                dict_results[text.ask_graph_entity_type] = answ = question.type_options(
                    'What type of image ?', ['png', 'jpg', 'ps', 'pdf', 'svg'], 
                    cfg.plot_image_type, back, prev_act, exit, spacer )

            elif question_act == text.ask_graph_dpi:
                dict_results[text.ask_graph_dpi] = answ = question.integer(
                    'Give the dpi ?', 
                    cfg.plot_dpi, back, prev_act, exit, spacer )

        # Handle the graph entitis one by one
        elif question_act == text.ask_graph_entities_options: 

            # Result lst
            lst_ent_results = [] 

            # Init variabeles for loops
            lst_entities = dict_results[text.ask_graph_entities]
            num_ent, max_ent = 1, len(lst_entities)

            # Loop through all the entities
            while num_ent <= max_ent:
                # Entity
                graph_ent = lst_entities[num_ent-1]

                # Reset result ent options dictionary
                dict_results_graph = {
                    text.ask_graph_entity:                        graph_ent , 
                    text.ask_graph_entity_type:                   cfg.plot_graph_type,
                    text.ask_graph_entity_line_width :            cfg.plot_line_width, 
                    text.ask_graph_entity_marker_size:            cfg.plot_marker_size, 
                    text.ask_graph_entity_marker_text:            cfg.plot_marker_txt,
                    text.ask_graph_entity_min_max:                cfg.plot_min_max_ave_period, 
                    text.ask_graph_entity_climate_ave:            cfg.plot_climate_ave, 
                    text.ask_graph_entity_climate_ave_marker_txt: cfg.plot_climate_marker_txt,
                    text.ask_graph_entity_climate_yyyy_start:     cfg.climate_start_year, 
                    text.ask_graph_entity_climate_yyyy_end:       cfg.climate_end_year,
                    text.ask_graph_entity_climate_period:         f'{cfg.climate_start_year}-{cfg.climate_end_year}'
                }

                # Questions for the correct handling of the specific entity
                num_ent_opt, max_ent_opt = 1, len( text.lst_ask_graph_entities )

                # Loop through entity options
                while num_ent_opt <= max_ent_opt:
                    # Get the question
                    question_act = text.lst_ask_graph_entities[num_ent_opt-1]

                    # Ask for the type graph for the entity
                    if question_act == text.ask_graph_entity_type: 
                        dict_results_graph[text.ask_graph_entity_type] = answ = question.type_options(
                            f'Which type graph do you want to use for {graph_ent} ?', 
                            ['line', 'bar'], 
                            cfg.plot_graph_type, back, prev_act, exit, spacer )

                    # Ask for the markers next to the entity
                    elif question_act == text.ask_graph_entity_marker_text: 
                        dict_results_graph[text.ask_graph_entity_marker_text] = answ = question.y_or_n(
                            f'Values next to the markers for {graph_ent} ?', 
                            cfg.plot_marker_txt, back, prev_act, exit, spacer )

                    # Ask for the calculation of the min, max and average
                    elif question_act == text.ask_graph_entity_min_max: 
                        dict_results_graph[text.ask_graph_entity_min_max] = answ = question.y_or_n(
                            f'Calculate min, max and average value for {graph_ent} ?', 
                            cfg.plot_min_max_ave_period, back, prev_act, exit, spacer )

                    # Ask for the climate options to be added to the graph
                    elif question_act == text.ask_graph_entity_climate_ave:
                        dict_results_graph[text.ask_graph_entity_climate_ave] = answ = question.y_or_n(
                            'Calculate and plot the climate averages for '
                            f'{graph_ent} ?', 
                            cfg.plot_climate_ave, back, prev_act, exit, spacer )

                    # Questions only to be asked if the climate average is demanded
                    elif answer.is_yes(dict_results[text.ask_graph_entity_climate_ave]):

                        # Ask for markers next to the climate values
                        if question_act == text.ask_graph_entity_climate_ave_marker_txt:
                            dict_results_graph[text.ask_graph_entity_marker_text] = answ = question.y_or_n(
                                f'Values next to the markers for climate averages for {graph_ent} ?', 
                                cfg.plot_climate_marker_txt, back, prev_act, exit, spacer )

                        # Ask Climate start year
                        elif question_act == text.ask_graph_entity_climate_yyyy_start:
                            sy, ey = cfg.climate_period.split('-')
                            dict_results_graph[text.ask_graph_entity_climate_yyyy_start] = answ = question.integer(
                                'Give a start year for the calculation of climate averages <yyyy> '
                                f'for {graph_ent} ?', sy, back, prev_act, exit, spacer )

                        # Ask Climate end year
                        elif question_act == text.ask_graph_entity_climate_yyyy_end:
                            sy, ey = cfg.climate_period.split('-')
                            dict_results_graph[text.ask_graph_entity_climate_yyyy_end] = answ = question.integer(
                                'Give an end year for the calculation of climate average <yyyy> '
                                f'for {graph_ent} ?', ey, back, prev_act, exit, spacer )

                    # Answer is go back
                    if answer.is_back(answ):
                        # Get out of here
                        dict_results[text.ask_other_menu] = text.lst_back[0]

                        # Oke done.
                        return dict_results

                    # When previous question is called
                    elif answer.is_prev(answ):
                        # Cannot go back to previous at the 1st question
                        if num_ent_opt == 1: 
                            # Stop the loop entities options
                            break
                        else:
                            num_ent_opt -= 1

                # When previous question is called
                if answer.is_prev(answ):
                    # Cannot go back to previous at the 1st question
                    if num_ent == 1: 
                        # Stop the loop of entities
                        break
                    else:
                        num_ent -= 1
                else:
                    # Make climate period
                    graph_climate_periode  = f'{dict_results[text.ask_graph_entity_climate_yyyy_start]}-'
                    graph_climate_periode += f'{dict_results[text.ask_graph_entity_climate_yyyy_end]}'
                    dict_results_graph[text.ask_graph_entity_climate_period] = graph_climate_periode

                    # Add results dictionary to lists
                    lst_ent_results.append( dict_results_graph )

            # Add lst with entity options to global dictionary
            dict_results[text.ask_graph_entities_options] = lst_ent_results

        # When previous question is called
        if answer.is_prev(answ):
            # Cannot go back to previous at the 1st question
            if num_question != 1: 
                # Goto previous question
                num_question -= 1 
        else:
            num_question += 1 

        # Answer is go back
        if answer.is_back(answ):
            # Get out of here
            dict_results[text.ask_other_menu] = text.lst_back[0]

            # Oke done.
            break

    # Oke done.
    return dict_results
