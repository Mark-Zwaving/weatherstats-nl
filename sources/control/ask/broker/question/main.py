'''Library processes the main questions'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.2.5'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import sources.view.text as text
import sources.control.ask.answer as answer
import sources.control.ask.question as ask_question
import sources.control.fio as fio
import sources.model.utils as utils

def process(question, answ, dict_results, back, prev_act, exit, spacer):
    '''Function processes the basic questions for the options in the menu. 
       And puts the answers in the dict_results if the question is asked
    '''
    # If there is one
    fname = dict_results[text.ask_filename] 

    # Ask for stations lst
    if question == text.ask_lst_stations:
        dict_results[text.ask_lst_stations] = answ = ask_question.lst_places(
            'Select one or more weatherstations ?', 
            cfg.e, back, prev_act, exit, spacer )

    # Ask for entities lst
    elif question == text.ask_lst_entities:
        dict_results[text.ask_lst_entities] = answ = ask_question.lst_entities(
            'Select one or more weather entities ?', 
            cfg.e, back, prev_act, exit, spacer )
        
    # Ask for a start datetime
    elif question == text.ask_start_datetime: 
        dt_plus = utils.datetime_plus_minutes_rounded( minute=10 )
        dict_results[text.ask_start_datetime] = answ = ask_question.date_time( 
            'a start', dt_plus, back, prev_act, exit, spacer )

    # Ask for a end datetime
    elif question == text.ask_end_datetime: 
        dt_plus = utils.datetime_plus_minutes_rounded( minute=70 )
        dict_results[text.ask_end_datetime] = answ = ask_question.date_time( 
            'an end', dt_plus, back, prev_act, exit, spacer )

    # Ask for the statistics cell 
    elif question == text.ask_select_cells: 
        dict_results[text.ask_select_cells] = answ = ask_question.lst_diy_cells(
            'What will be the statistics cells ?', 
            '', back, prev_act, exit, spacer )

    # Ask for the statistics cells. 
    # All options including default lists are given 
    elif question == text.ask_select_all_cells: 
        # Use same end cells name: text.ask_select_cells
        dict_results[text.ask_select_cells] = answ = ask_question.lst_sel_all_type_cells(
            'What will be the statistics cells ?', 
            '', back, prev_act, exit, spacer )      

    # Ask for the first period
    elif question == text.ask_period_1: 
        dict_results[text.ask_period_1] = answ = ask_question.period_1(
            f'Give a period for the calculations of the statistics ?', 
           '', back, prev_act, exit, spacer ) 

    # Ask for the second period
    elif question == text.ask_period_2:
        dict_results[text.ask_period_2] = answ = ask_question.period_2(
            'Select a second period (day, month or period) ?', 
            '', back, prev_act, exit, spacer )

        # # Is there a second period in the DIY question lst. 
        # # If not add one Period 2 to the GLOBAL Question lst!
        # if 'inf_period-2' in dict_results[text.ask_diy_cells]: 
        #     # Add question to lst
        #     lst_questions.insert(num_question, text.ask_period_2)
        #     # Increase maximum questions with 1
        #     max_question = len(lst_questions)  

    # Ask for a type file
    elif question == text.ask_file_type: # Ask for a file types
        dict_results[text.ask_file_type] = answ = ask_question.file_type(
            'Select type output file ?', 
            cfg.default_output, back, prev_act, exit, spacer )

    # Ask for a filename
    elif question == text.ask_filename: 
        # Get a default name
        default = f'wstats-{dict_results[text.ask_title]}-{utils.now_for_file()}' 
        default = fio.sanitize_file_name(default)

        # Ask filename
        dict_results[text.ask_filename] = answ = ask_question.file_name(
            'Give a name for the output file ?', 
            default, back, prev_act, exit, spacer )

    # Save to a file?
    elif question == text.ask_save_txt_file: 
        dict_results[text.ask_save_txt_file] = answ = ask_question.y_or_n(
            'Do you want to save the result to a file ?', 
            'n', back, prev_act, exit, spacer )

    # Ask for the first period list NEW
    elif question == text.ask_lst_period_1: 
        dict_results[text.ask_lst_period_1] = answ = ask_question.lst_period_1(
            f'Give the period for the calculation of {fname} ?', 
            cfg.e, back, prev_act, exit, spacer ) 

    # Ask for a period to compare with an other period     
    elif question == text.ask_per_compare:
        dict_results[text.ask_per_compare] = answ = ask_question.period_compare(
            'Give the period to compare ?', 
            cfg.e, back, prev_act, exit, spacer )

    # Rewrite or only make new non-existing files
    elif question == text.ask_write_dayval: 
        dict_results[text.ask_write_dayval] = answ = ask_question.type_options(
            'Do you want to add only new files or rewrite it all ?', 
            ['add', 'rewrite'], 'add', back, prev_act, exit, spacer )

    # Select a list with dates
    elif question == text.ask_lst_see_days: 
        dict_results[text.ask_lst_see_days] = answ = ask_question.lst_yyyymmdd(
            'Give the days <yyyymmdd> you want to see ?', 
            cfg.e, back, prev_act, exit, spacer )

    # Ask for a Search for days Query
    elif question == text.ask_s4d_query:
        dict_results[text.ask_s4d_query] = answ = ask_question.s4d_query(
            'Type in a query to search for days ?', 
            cfg.e, back, prev_act, exit, spacer )
        
    # Arrange the go back to main menu option
    if answer.is_back(answ):
        dict_results[text.ask_other_menu] = text.lst_back[0]
        
    return answ, dict_results 
