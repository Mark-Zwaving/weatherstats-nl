'''Library processes the questions in a given lst'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.2.5'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import sources.control.ask.answer as answer
import sources.control.ask.broker.question.animation as ask_animation
import sources.control.ask.broker.question.graph as ask_graph
import sources.control.ask.broker.question.main as ask_main
import sources.control.ask.broker.question.database as ask_database
import sources.view.text as text
import pprint

def process(lst_questions, title, default=cfg.e, 
            back=False, prev=False, exit=False, spacer=False):
    '''Process all the questions given in the lst with the questions'''
    # Init the empthy dictionary with all the possible answers/results
    # This dictionary has to be filled with the given answers
    dict_results = {
        text.ask_title:                   title, 
        text.ask_lst_stations:            [],
        text.ask_lst_period_1:            [],  # NEW
        text.ask_period_1:                '', 
        text.ask_period_2:                '', 
        text.ask_per_compare:             '',

        # TODO ASK for years and put in year in head of table
        text.ask_clima_period:            cfg.climate_period, 
        text.ask_select_cells:            [],
        text.ask_select_all_cells:        [],
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
        text.ask_lst_graph_entities_options:  [],
        text.ask_lst_graph_entities       :  [],

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

        # Go back to main menu
        text.ask_other_menu:              ''
    }

    # Init questions var
    num_question, max_question = 1, len(lst_questions)

    # Reset answer and default
    answ = ''

    # Walkthrough all the questions
    while num_question <= max_question:

        # For the first question there cannot be a previous option 
        prev_act = False if num_question == 1 else True 

        # Get correct question from list
        question = lst_questions[num_question-1]

        # Main questions
        answ, dict_results = ask_main.process(question, answ, dict_results,
                                              back, prev_act, exit, spacer)
        # Graph questions
        answ, dict_results = ask_graph.process(question, answ, dict_results, 
                                               back, prev_act, exit, spacer)
        # Animation questions
        answ, dict_results = ask_animation.process(question, answ, dict_results,
                                                   back, prev_act, exit, spacer)
        # Database questions
        answ, dict_results = ask_database.process(question, answ, dict_results,
                                                  back, prev_act, exit, spacer)

        # When previous question is called
        if answer.is_prev(answ):
            # Cannot go back to previous question at the 1st question
            if num_question == 1: 
                # It's the first question so go back to the main menu
                dict_results[text.ask_other_menu] = text.lst_back[0] 
                break # Out of loop
            else:
                # Goto previous question
                num_question -= 1 

        # Answer is go back
        elif answer.is_back(dict_results[text.ask_other_menu]):
            # Get out of here
            break
        
        else:
            # Next question
            num_question += 1 

    # Oke done.
    # Return all the given answers
    return dict_results
