'''Library processes the questions for the graph into a dictionary'''
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

def graph_defaults(question, answ, dict_results, back, prev_act, exit, spacer):
    '''Graph Questions only to be asked asked if 
       the graph default option is not selected'''
         
    # If no defaults are used, ask the specific questions
    if answer.is_no(dict_results[text.ask_graph_default]):

        # Ask for the graph width
        if question == text.ask_graph_width:
            dict_results[text.ask_graph_width] = answ = ask_question.integer(
                'Give the width (in pixels) for the graph ?', 
                cfg.plot_width, back, prev_act, exit, spacer )

        # Ask for the graph height
        elif question == text.ask_graph_height:
            dict_results[text.ask_graph_height] = answ = ask_question.integer(
                'Give the height (in pixels) for the graph ?', 
                cfg.plot_height, back, prev_act, exit, spacer )

        # Ask for the graph cummulation values option
        elif question == text.ask_graph_cummul_val:
            dict_results[text.ask_graph_cummul_val] = answ = ask_question.y_or_n(
                'Do you want cummulative values for the graph ?', 
                cfg.plot_cummul_val, back, prev_act, exit, spacer )

        # Ask for the graph type
        elif question == text.ask_graph_entity_type:
            dict_results[text.ask_graph_entity_type] = answ = ask_question.lst_options(
                'What type of image ?', 
                ['png', 'jpg', 'ps', 'pdf', 'svg'], 
                cfg.plot_image_type, back, prev_act, exit, spacer )

        # Ask for the graph dpi 
        elif question == text.ask_graph_dpi:
            dict_results[text.ask_graph_dpi] = answ = ask_question.integer(
                'Give the dpi ?', 
                cfg.plot_dpi, back, prev_act, exit, spacer )
            
        # Arrange the go back to main menu option
        if answer.is_back(answ):
            dict_results[text.ask_other_menu] = text.lst_back[0]

    return answ, dict_results

def climate_options_entity(entity, question, answ, dict_results, dict_results_entities,
                    back, prev_act, exit, spacer):
    
    # Ask for the climate options to be added to the graph
    if question == text.ask_graph_entity_climate_ave:
        dict_results_entities[text.ask_graph_entity_climate_ave] = answ = \
                ask_question.y_or_n(f'Calculate and plot the climate averages for {entity} ?',
                                    cfg.plot_climate_ave, back, prev_act, exit, spacer )

    # Questions only to be asked if the climate average is demanded
    elif answer.is_yes(dict_results_entities[text.ask_graph_entity_climate_ave]):

        # Ask for markers next to the climate values
        if question == text.ask_graph_entity_climate_ave_marker_txt:
            dict_results_entities[text.ask_graph_entity_climate_ave_marker_txt] = answ = \
                ask_question.y_or_n(f'Set values next to the markers for climate averages for {entity} ?', 
                                    cfg.plot_climate_marker_txt, back, prev_act, exit, spacer )

        # Ask Climate start year
        elif question == text.ask_graph_entity_climate_yyyy_start:
            sy, ey = cfg.climate_period.split('-')
            dict_results_entities[text.ask_graph_entity_climate_yyyy_start] = answ = \
                ask_question.integer('Give a start year for the calculation of climate averages <yyyy> '
                                     f'for {entity} ?', sy, back, prev_act, exit, spacer )

        # Ask Climate end year
        elif question == text.ask_graph_entity_climate_yyyy_end:
            sy, ey = cfg.climate_period.split('-')
            dict_results_entities[text.ask_graph_entity_climate_yyyy_end] = answ = \
                ask_question.integer('Give an end year for the calculation of climate average <yyyy> '
                                     f'for {entity} ?', ey, back, prev_act, exit, spacer )

    # Arrange the go back to main menu option
    if answer.is_back(answ):
        dict_results[text.ask_other_menu] = text.lst_back[0]

    return answ, dict_results, dict_results_entities

def lst_graph_entities_options(entity, question, answ, dict_results,
                               back, prev_act, exit, spacer):
    '''Make a lst with the options for the entities'''

    # Climate period
    clima_period_yyyy = f'{cfg.climate_start_year}-{cfg.climate_end_year}'

    # Reset result ent options dictionary
    dict_results_entities = {
        text.ask_graph_entity_name:                   entity, 
        text.ask_graph_entity_type:                   cfg.plot_graph_type, 
        text.ask_graph_entity_line_width :            cfg.plot_line_width, 
        text.ask_graph_entity_marker_size:            cfg.plot_marker_size, 
        text.ask_graph_entity_marker_text:            cfg.plot_marker_txt, 
        text.ask_graph_entity_min_max:                cfg.plot_min_max_ave_period, 
        text.ask_graph_entity_climate_ave:            cfg.plot_climate_ave, 
        text.ask_graph_entity_climate_ave_marker_txt: cfg.plot_climate_marker_txt, 
        text.ask_graph_entity_climate_yyyy_start:     cfg.climate_start_year, 
        text.ask_graph_entity_climate_yyyy_end:       cfg.climate_end_year, 
        text.ask_graph_entity_climate_period:         clima_period_yyyy 
    }

    # Questions for the graph options of the entity
    num_opt, max_opt = 1, len(text.lst_ask_graph_entities)

    # Loop through entity options
    while num_opt <= max_opt:

        question_loc = text.lst_ask_graph_entities[num_opt-1]

        # TODO PREVIOUS NOT WORKING
        # Ask for the type graph for the entity
        if question_loc == text.ask_graph_entity_type: 
            dict_results_entities[text.ask_graph_entity_type] = answ = \
                    ask_question.lst_options(
                        f'Which type graph do you want to use for {entity} ?', 
                        ['line', 'bar'], 
                        cfg.plot_graph_type, back, prev_act, exit, spacer )

        # Ask for the markers next to the entity
        elif question_loc == text.ask_graph_entity_marker_text: 
            dict_results_entities[text.ask_graph_entity_marker_text] = answ = \
                    ask_question.y_or_n(
                        f'Set values next to the markers for {entity} ?', 
                        cfg.plot_marker_txt, back, prev_act, exit, spacer )

        # Ask for the calculation of the min, max and average
        elif question_loc == text.ask_graph_entity_min_max: 
            dict_results_entities[text.ask_graph_entity_min_max] = answ = \
                    ask_question.y_or_n(
                        f'Calculate min, max and average value for {entity} ?', 
                        cfg.plot_min_max_ave_period, back, prev_act, exit, spacer )

        # Ask for the climate options
        answ, dict_results, dict_results_entities = \
                    climate_options_entity(entity, question_loc, answ,
                                           dict_results, dict_results_entities,
                                           back, prev_act, exit, spacer)

        # When previous question is called
        if answer.is_prev(answ):
            # Cannot go back to previous at the 1st question
            if num_opt <= 1: 
                # Stop the loop of entities
                break
            else:
                num_opt -= 1
                continue

        # Arrange the go back to main menu option
        elif answer.is_back(answ):
            dict_results[text.ask_other_menu] = text.lst_back[0]
            break

        else:
            # Make climate period
            graph_climate_periode  = f'{dict_results_entities[text.ask_graph_entity_climate_yyyy_start]}-'
            graph_climate_periode += f'{dict_results_entities[text.ask_graph_entity_climate_yyyy_end]}'
            dict_results_entities[text.ask_graph_entity_climate_period] = graph_climate_periode

            # Next question
            num_opt += 1

    return answ, dict_results, dict_results_entities

def lst_graph_entities(question, answ, dict_results, back, prev_act, exit, spacer):
    '''Handle the lst graph entitis one by one. '''

    if question == text.ask_lst_graph_entities_options: 
        # Init variabeles for loops
        lst_graph_entities = dict_results[text.ask_lst_graph_entities]
        num_ent, max_ent = 1, len(lst_graph_entities)

        # Result lst
        lst_ent_results = [] 
        
        # Loop through all the entities
        while num_ent <= max_ent:
            # Entity
            entity = lst_graph_entities[num_ent-1]

            answ, dict_results, dict_results_entities = \
                lst_graph_entities_options(
                    entity, question, answ, dict_results, 
                    back, prev_act, exit, spacer)

            # Answer is go back
            if answer.is_back(answ):
                # Get out of here
                dict_results[text.ask_other_menu] = text.lst_back[0]
                break

            # When previous question is called
            elif answer.is_prev(answ):
                # Cannot go back to previous at the 1st question
                if num_ent <= 1:
                    # Stop the loop entities options
                    break  
                else:
                    # Go back to previous qustion
                    num_ent -= 1
                    continue 

            else:
                # Add results dictionary to lists
                lst_ent_results.append( dict_results_entities )

                # Nex question
                num_ent  += 1

        # Add lst with entity options to global dictionary
        dict_results[text.ask_lst_graph_entities_options] = lst_ent_results

    return answ, dict_results

def process(question, answ, dict_results, back, prev_act, exit, spacer):
    '''Function processes questions for the graphs options in the menu. 
       And puts the answers in the dict_results if the question is asked
    '''

    # Ask for a graph title
    if question == text.ask_graph_title:
        dict_results[text.ask_graph_title] = answ = ask_question.ask(
            'Give a title for the graph ?', 
            'My Graph Title', back, prev_act, exit, spacer )

    # Ask for a graph y-as lable
    elif question == text.ask_graph_ylabel:
        dict_results[text.ask_graph_ylabel] = answ = ask_question.ask(
            'Give a y-as label for the graph ?', 
            'weatherdata', back, prev_act, exit, spacer )

    # Ask for the defaults or not
    elif question == text.ask_graph_default:
        dict_results[text.ask_graph_default] = answ = ask_question.y_or_n(
            'Do you want to use default values ? See defaults.py TODO', 
            cfg.plot_default, back, prev_act, exit, spacer )

    # Ask for the graph entities to show in the graph
    elif question == text.ask_lst_graph_entities:
        dict_results[text.ask_lst_graph_entities] = answ = ask_question.lst_entities(
            'Select the weather entity(s) for the graph ?', 
            '', back, prev_act, exit, spacer )

    # Ask for the defaults, if chosen 
    answ, dict_results = graph_defaults(question, answ, dict_results, 
                                        back, prev_act, exit, spacer)

    # Ask for graph lst entities options
    answ, dict_results = lst_graph_entities(question, answ, dict_results, 
                                            back, prev_act, exit, spacer)

    # Arrange the go back to main menu option
    if answer.is_back(answ):
        dict_results[text.ask_other_menu] = text.lst_back[0]

    # When previous question is called
    elif answer.is_prev(answ):
        # Cannot go back to previous at the 1st question
        pass

    return answ, dict_results
