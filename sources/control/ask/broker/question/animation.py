'''Library processes the questions for the animation into a dictionary'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.0.9'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import sources.view.text as text
import sources.control.ask.answer as answer
import sources.control.ask.question as ask_question
import sources.model.ymd as ymd

def process(question, answ, dict_results, back, prev_act, exit, spacer):
    '''Function processes questions for the animation option in the menu. 
       The answers will be updated in the dict_results, if the question is asked
    ''' 

    # Ask to download a image url
    if question == text.ask_download_url: 
        dict_results[text.ask_download_url] = answ = ask_question.image_download_url(
            'Give an (image) url to download ?', 
            cfg.e, back, prev_act, exit, spacer )

    # Ask download interval time (integer)
    elif question == text.ask_download_interval: 
        default = 10
        dict_results[text.ask_download_interval] = answ = ask_question.integer(
            'Give the interval download time (minutes) ?', 
            default, back, prev_act, exit, spacer ) 

    # Ask for an animation time
    elif question == text.ask_animation_time: 
        dict_results[text.ask_animation_time] = answ = ask_question.floatt( 
            'Give the animation interval time ?', 
            cfg.animation_time, back, prev_act, exit, spacer ) 

    # Ask for a name for the animation file
    elif question == text.ask_animation_name: 
        gif_ext = f'.{cfg.animation_ext}' # Animation extension

        dict_results[text.ask_animation_name] = answ = ask_question.ask(
            'Give a name for the animation file or press enter for default ?', 
            f'animation-{ymd.yyyymmdd_now()}-{ymd.hhmmss_now()}{gif_ext}', # Default
            back, prev_act, exit, spacer )

        # Check for an extension. If it has not ,add it
        if not dict_results[text.ask_animation_name].lower().endswith(gif_ext):
            dict_results[text.ask_animation_name] += gif_ext 

    # UNUSED Ask for an verbose option
    # elif question == text.ask_verbose: 
    #     dict_results[text.ask_verbose] = answ = ask_question.y_or_n(
    #         f'Do you want to use the verbose option ?{cfg.ln}'
    #         f'With verbose enabled the programm cannot do something else.{cfg.ln}'
    #         'Although wsstats can be started in another console.', 
    #         'y', back, prev_act, exit, spacer )

    # Ask to remove the downloaded files
    elif question == text.ask_rm_downloads: 
        dict_results[text.ask_rm_downloads] = answ = ask_question.y_or_n(
            'Do you want to remove the downloaded images ?', 
            'n', back, prev_act, exit, spacer )

    # Ask to compress a gif file animation
    elif question == text.ask_gif_compress: 
        dict_results[text.ask_gif_compress] = answ = ask_question.y_or_n(
            f'Do you want compress the animation file ?{cfg.ln}'
            'Software gifsicle needs to be installed on your OS...',
                'n', back, prev_act, exit, spacer )

    # Ask for one or more weatherstations
    elif question == text.ask_gif_compress: 
        dict_results[text.ask_gif_compress] = answ = ask_question.lst_places(
            'Select one (or more) weather station(s) ?', 
            cfg.e, back, prev_act, exit, spacer )

    # Arrange the go back to main menu option
    if answer.is_back(answ):
        dict_results[text.ask_other_menu] = text.lst_back[0]

    return answ, dict_results
