'''Library processes the questions for the animation into a dictionary'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.0.8'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import sources.view.text as text
import sources.control.ask.answer as answer
import sources.control.ask.question as ask_question

def process(question, answ, dict_results, back, prev_act, exit, spacer): 
   '''Function processes questions for the databases options in the menu. 
      And puts the answers in the dict_results if the question is asked
   '''    
   # Ask for a sqlite query
   if question == text.ask_sqlite_query:
      dict_results[text.ask_sqlite_query] = answ = ask_question.ask(
            'Enter a (sqlite) query ?', 
            cfg.e, back, prev_act, exit, spacer )

   # Arrange the go back to main menu option
   if answer.is_back(answ):
      dict_results[text.ask_other_menu] = text.lst_back[0]

   return answ, dict_results