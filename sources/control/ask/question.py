'''Library contains functions for questions'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.2.4'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import sys, config as cfg, defaults
import validators
import sources.control.ask.answer as answer
import sources.model.stations as stations
import sources.model.utils as utils
import sources.model.dayvalues.data as data
import sources.model.dayvalues.chk_period as chk_period
import sources.model.check as chk
import sources.view.search4days as s4d
import sources.view.console as cnsl
import sources.view.text as text

# Marker for adding a default question mark 
marker = '\n>>>  ?  '

def ask( 
        t='?',           # Question text
        default=cfg.e,   # Default text
        back=False,      # Add the go back option
        prev=False,      # Add the previous option
        exit=False,      # Add the exit option
        spacer=False     # Add a spacer line after the question
    ):
    '''Ask a question'''
    # Remove 1 ln if there
    if len(t) > 0 and t[-1] == cfg.ln:
        t = t[:-1] 
    # Add a default option
    if default != cfg.e: 
        t += cfg.ln + text.enter_default(default)
    # Add previous optoin
    if prev: 
        t += cfg.ln + text.enter_previous()
    # Add back option
    if back: 
        t += cfg.ln + text.enter_back_menu()
    # Add exit option
    if exit: 
        t += cfg.ln + text.enter_exit()

    # Ask a question on screen 
    answ = text.clean( input( f'{t}{marker}' ) )

    # Add a spacer line, if spacer is true
    cnsl.log(' ', spacer) 

    # User wants to quit
    if answer.is_quit(answ):
        cnsl.log('Goodbye!', True)
        sys.exit(0)
    # User wants the default answer
    elif answer.is_empty(answ) and default != cfg.e:
        return default

    return answ

def answ_to_lst(answ):
    lst = [] # Make a list with table cells
    if answ.find(',') != -1:
        lst = [e.strip() for e in answ.split(',')] # Clean input
    else:
        lst = [answ.strip()]

    return lst

def y_or_n(t=cfg.e, default=cfg.e, back=False, prev=False, exit=False, spacer=False):
    '''Question demands an answer yes or no'''
    while True:
        answ = ask( t + cfg.ln + text.enter_y_or_n(),
                   default, back, prev, exit, spacer )
        
        if ( back and answer.is_back(answ) ) or \
           ( prev and answer.is_prev(answ) ):
            return answ
        elif answ in text.lst_yes or \
             answ in text.lst_no:
            return answ
        else:
            cnsl.log("Type in a 'y' or 'n'...", True)

def integer(t='Give an integer ?', default=1, 
            back=False, prev=False, exit=True, spacer=False):
    '''Question demands an integer'''
    while True:
        answ = ask(t, default, back, prev, exit, spacer)

        if ( back and answer.is_back(answ) ) or \
           ( prev and answer.is_prev(answ) ):
            return answ
        elif chk.is_int(answ): # Check if it can be an int
            return int(answ)
        else:
            cnsl.log(f'{answ} is not an integer. Try again...{cfg.ln}', True)

def floatt(t='Give a float ?', default=1.0, 
          back=False, prev=False, exit=True, spacer=False):
    '''Question demands an integer'''
    while True:
        answ = ask(t, default, back, prev, exit, spacer)

        if ( back and answer.is_back(answ) ) or \
           ( prev and answer.is_prev(answ) ):
            return answ
        elif chk.is_float(answ): # Check if it can be an float
            return float(answ)
        else:
            cnsl.log(f'{answ} is not an float. Try again...{cfg.ln}', True)

def open_with_app(path, options, back=False, prev=False, exit=False, spacer=False):
    t = f'\nOpen the file <type={options["file-type"]}> with your default application ?'
    answ = y_or_n( t, default=cfg.e, back=back, prev=prev, exit=exit, spacer=spacer )

    if answer.is_yes(answ):
        utils.exec_with_app(path)
    
    return answ

def back_to_main_menu(default=cfg.e, back=False, prev=False, exit=False, spacer=False):
    ask(text.back_main, default, back, prev, exit, spacer)

def lst_places(t, default=cfg.e, back=False, prev=False, exit=False, spacer=False):
    lst_sel = []
    if len(stations.lst_stations_map()) > 0:
        while True:
            tt = cfg.e
            if cfg.info:
                tt += text.menu_info_stations.strip() + cfg.ln + cfg.ln

            tt += t + cfg.ln
            tt += '# To add one station, give a wmo-number or a city name' + cfg.ln
            tt += '# To add more stations, give a wmo-number or a city name separated by a comma' + cfg.ln
            tt += "# Press '*' to add all available weather stations" + cfg.ln
            tt += text.enter_next() if len(lst_sel) > 0 else cfg.e

            answ = ask(tt, default, back, prev, exit, spacer)

            ttt = cfg.e
            if answer.is_empty(answ) and \
               len(lst_sel) == 0:
                ttt += text.type_in + cfg.ln
            elif answer.is_empty(answ) and len(lst_sel) > 0:
                break # Done
            elif ( back and answer.is_back(answ) ) or \
                 ( prev and answer.is_prev(answ) ):
                return answ
            elif answ == '*':
                lst_sel = stations.lst_stations_map()
            else:
                lst = answ_to_lst(answ)

                # Check and add all added stations
                for wmo_or_place in lst:
                    if stations.wmo_or_place_in_map(wmo_or_place) :
                        station = stations.wmo_or_place_to_station(wmo_or_place)
                        if stations.station_in_list(station, lst_sel):
                            ttt += f'Station: {station.wmo} {station.place} already added...' + cfg.ln
                        else:
                            lst_sel.append(station) # Append station object to lst
                            ttt += f'Station: {station.wmo} {station.place} added...' + cfg.ln
                    else:
                        ttt += f'Station: {wmo_or_place} not found in list stations...' + cfg.ln

            if len(lst_sel) == len(stations.lst_stations_map()):
                ttt += 'All available weatherstations are  added...' + cfg.ln
                break
            elif len(lst_sel) > 0:
                ttt += 'All weatherstation(s) which are added are: ' + cfg.ln
                ttt += utils.lst_to_col([f'{station.wmo} {station.place}' for station in lst_sel], 'left', 4)
                ttt += cfg.ln

            cnsl.log(ttt, True)
    else:
        t = 'No weatherdata found in data map. Download weatherdata first...' + cfg.ln
        cnsl.log(t, cfg.error)

    return lst_sel


# OLD
def period_1( t=cfg.e, default=cfg.e, back=False, prev=False, exit=False, spacer=False):

    while True:
        tt = cfg.e
        if cfg.info:
            tt += text.menu_info_periods + '\n'
        tt += t

        answ = ask(tt, default, back, prev, exit, spacer)

        if answer.is_empty(answ):
            ttt = text.type_in + cfg.ln
        elif prev and answer.is_prev(answ):
            return answ 
        elif back and answer.is_back(answ):
            return answ
        else:
             # Check correctness period
            ok = chk_period.process(answ)
            if ok:
                return answ
            else:
                ttt = f'Period of format {answ} is unknown... Press a key... '

        cnsl.log(ttt, cfg.error)


def lst_period_1(t=cfg.e, default=cfg.e, 
                 back=False, prev=False, exit=False, spacer=False):
    lst_result = []

    while True:
        tt = cfg.e
        if cfg.info:
            tt += text.menu_info_periods.strip() + cfg.ln + cfg.ln

        tt += t + cfg.ln
        tt += '# To add more periods, separate the periods by a comma' + cfg.ln
        tt += text.enter_next() if len(lst_result) > 0 else cfg.e

        answ = ask(tt, default, back, prev, exit, spacer)

        # Reset output
        ttt = cfg.e
        if answer.is_empty(answ) and \
           len(lst_result) == 0:
            ttt += text.type_in + cfg.ln
        elif answer.is_empty(answ) and \
             len(lst_result) > 0:
            break
        elif ( prev and answer.is_prev(answ) ) or \
             ( back and answer.is_back(answ) ):
            return answ
        else:
            # Make list
            lst_new = answ.split(',') if answ.find(',') != -1 else [answ]
            lst_new = [el.strip() for el in lst_new] # Strip whitespace

            # Walkthough the new enitities, if there
            for period in lst_new:
                # Check correctness period
                ok = chk_period.process(period)
                if ok:
                    # Check if entity already in lst result
                    if utils.s_in_lst(lst_result, period):
                        ttt += f'Period {period} already added...' + cfg.ln
                    else:
                        # Add to lst resutl
                        lst_result.append(period)
                        ttt += f'Period {period} added...' + cfg.ln
                else:
                    ttt += f'Unknown format period {period} given...' + cfg.ln

        # Show all the periods in the result lst, if there
        if len(lst_result) > 0:
            ttt += 'The period(s) who are added are: ' + cfg.ln
            ttt += utils.lst_to_col(lst_result, align='left', col=8, width=3)
            ttt += cfg.ln

        cnsl.log(ttt, cfg.error)

    return lst_result

def type_options(t, lst, default=cfg.e, back=False, prev=False, 
                 exit=False, spacer=False):
    # Make lower case
    lst = [el.lower() for el in lst] 
    tt = t + cfg.ln

    # Make options
    for i, el in enumerate(lst):
        tt += f'  {i+1}) {el}' + cfg.ln
        
    while True:
        answ = ask(tt, default, back, prev, exit, spacer).lower()

        ttt = cfg.e

        # Check default if input is empthy and there is no default
        if answer.is_empty(answ) and default == cfg.e: 
            ttt += text.type_in + cfg.ln
        elif ( back and answer.is_back(answ) ) or \
             ( prev and answer.is_prev(answ) ):
            return answ
        elif answ in lst:
            return answ
        elif chk.is_int(answ) or \
             chk.is_float(answ):
            return lst[int(answ)-1]
        else:
            ttt = f'Option {answ} unknown. Try again...' + cfg.ln

        cnsl.log(ttt, True)

def day( t, default=cfg.e, back=False, prev=False, exit=False, spacer=False):
    while True:
        tt = cfg.e
        if cfg.info:
            tt += text.menu_info_select_a_day.strip() + cfg.ln + cfg.ln
        tt += t + cfg.ln

        answ = ask(tt, default, back, prev, exit, spacer)

        ttt = cfg.e

        # Check default if input is empthy and there is no default
        if answer.is_empty(answ) and default == cfg.e: 
            ttt += text.type_in + cfg.ln
        elif ( back and answer.is_back(answ) ) or \
             ( prev and answer.is_prev(answ) ):
            return answ
        elif answ in text.lst_mmdd:
            return answ
        else:
            ttt = f'Day {answ} unknown. Try again...'

        cnsl.log(ttt, cfg.error)

def month( t, default=cfg.e, back=False, prev=False, exit=False, spacer=False):
    while True:
        tt =  cfg.e
        if cfg.info:
            tt += text.menu_info_select_a_month.strip() + cfg.ln + cfg.ln
        tt += t + cfg.ln

        answ = ask(tt, default, back, prev, exit, spacer)

        ttt = cfg.e

        # Check default if input is empthy and there is no default
        if answer.is_empty(answ) and default == cfg.e: 
            ttt += text.type_in + cfg.ln
        elif ( back and answer.is_back(answ) ) or \
             ( prev and answer.is_prev(answ) ):
            return answ
        elif text.month_to_mm(answ) != -1:
            return text.month_to_mm(answ)
        else:
            ttt = f'Month {answ} unknown. Try again...'

        cnsl.log(ttt, cfg.error)

def period_2(t, default=cfg.e, back=False, prev=False, exit=False, spacer=False):

    lst = [ 'day', 'month' , 'period'
            #, 'season' 
    ]
    while True:
        option = type_options(t, lst, default, back, prev, exit, spacer).lower() 

        # Check default if input is empthy and there is no default
        if answer.is_empty(answ) and default == cfg.e: 
            tt = text.type_in + cfg.ln
        elif ( back and answer.is_back(answ) ) or \
             ( prev and answer.is_prev(answ) ):
            return answ

        if option in 'day':
            tt = 'To select a day. Type in a day in the format (=mmdd)'
            mmdd = day(tt, default, back, prev, exit, spacer)
            answ = f'****{mmdd}'

        elif option in 'month':
            tt = 'To select a month. Type in a month num or a name' 
            mm = month(tt, default, back, prev, exit, spacer)
            answ = f'****{mm}**'

        elif option == 'period':
            tt = 'Select a period' 
            per = period_1(tt, default, back, prev, exit, spacer)
            answ = per

        elif option == 'season':
            tt = 'Select a season' 
            season = season_type(tt, default, back, prev, exit, spacer)
            answ = season

        if answer.is_quit(answ): 
            return answ
        elif answer.is_prev(answ):
            continue
        else:
            return answ

def period_day_to_day( t, default, back=False, prev=False, exit=False, spacer=False):
    while True:
        tt = cfg.e
        if cfg.info:
            tt += 'Select a start day(<format:<mmdd>) and a end day (<format:<mmdd>). Separated with an -\n' 
            tt += 'Input format: mmdd-mmdd\n'
            tt += 'Example: 0501-0503' + cfg.ln + cfg.ln
        tt += t + cfg.ln

        answ = ask(tt, default, back, prev, exit, spacer)

        # Check default if input is empthy and there is no default
        if answer.is_empty(answ) and default == cfg.e: 
            ttt = text.type_in + cfg.ln
        elif ( back and answer.is_back(answ) ) or \
             ( prev and answer.is_prev(answ) ):
            return answ
        else:
            return answ

        cnsl.log(ttt, True)

def s4d_query(t, default=cfg.e, back=False, prev=False, exit=False, spacer=False):
    while True:
        tt = cfg.e
        if cfg.info:
            tt += text.menu_info_queries.strip() + cfg.ln + cfg.ln
        tt += t + cfg.ln

        answ = ask(tt, default, back, prev, exit, spacer)

        # Check default if input is empthy and there is no default
        if answer.is_empty(answ) and default == cfg.e: 
            ttt += text.type_in + cfg.ln
        elif ( back and answer.is_back(answ) ) or \
             ( prev and answer.is_prev(answ) ):
            return answ
        else:
            ok, ttt = s4d.query_ok(answ)
            if ok:
                return answ
            else:
                ttt = f'Error in query: "{answ}"! Check syntax.\n{ttt}'

        cnsl.log(ttt, cfg.error)

def file_type(t, default=cfg.e, back=False, prev=False, exit=False, spacer=False):
    lst = text.lst_output_options
    return type_options(t, lst, default, back, prev, exit, spacer)

def graph_type(t, default=cfg.e, back=False, prev=False, exit=False, spacer=False):
    lst = ['line', 'bar']
    return type_options(t, lst, default, back, prev, exit, spacer)

def season_type(t, default=cfg.e, back=False, prev=False, exit=False, spacer=False):
    lst = ['winter', 'spring', 'summer', 'autumn']
    return type_options(t, lst, default, back, prev, exit, spacer)

def file_name(t, default=cfg.e, back=False, prev=False, exit=False, spacer=False):
    answ = ask(t, default, back, prev, exit, spacer)

    # Check default if input is empthy and there is no default
    if answer.is_empty(answ) and default == cfg.e: 
        cnsl.log(text.type_in + cfg.ln, True)

    return answ

def period_compare(t, default=cfg.e, back=False, prev=False, exit=False, spacer=False):    
    lst = ['period <mmdd-mmdd>', 'years', 'season', 'month' , 'day']
    while True:
        option = type_options(t, lst, default, back, prev, exit, spacer)

        if ( back and answer.is_back(answ) ) or \
           ( prev and answer.is_prev(answ) ):
            return answ
        elif option in text.lst_season:
            tt = 'Select season to compare'
            answ = ('season', season_type(tt, default, back, prev, exit, spacer))

        elif option in text.lst_day:
            tt = 'Which day do you want to compare ?'
            answ = ('day', day( tt, default, back, prev, exit, spacer))

        elif option in text.lst_month:
            tt = 'Which month do you want to compare ?'
            answ = ('month', month( tt, default, back, prev, exit, spacer))

        elif option == 'years':
            tt = 'Which years do you want to compare ?'
            answ = ('year', 'year')

        elif option == 'period <mmdd-mmdd>':
            tt = 'Which period (from day to day) do you want to compare ?'
            answ = ('period', period_day_to_day( tt, default, back, prev, exit, spacer))

        if answer.is_prev(answ[1]):
            continue # Again
        else: 
            return answ

def lst_diy_cells(t=cfg.e, default=cfg.e, back=False, prev=False, exit=False, spacer=False):
    lst_cells = []
    while True:
        tt =  cfg.e
        if cfg.info:
            tt += text.menu_info_td_cells.strip() + cfg.ln + cfg.ln

        tt += t + cfg.ln
        tt += '# To add a table cell give one statistics cell' + cfg.ln
        tt += '# To add more statistics cells, separate the statistics with a comma' + cfg.ln
        tt += text.enter_next() + cfg.ln if len(lst_cells) > 0 else cfg.e
    
        answ = ask(tt, default, back, prev, exit, spacer)

        ttt = cfg.e
        if answer.is_empty(answ) and \
           len(lst_cells) == 0:
            ttt += text.type_in + cfg.ln
        elif answer.is_empty(answ) and \
             len(lst_cells) > 0:
            break # Done
        elif ( back and answer.is_back(answ) ) or \
             ( prev and answer.is_prev(answ) ):
            return answ
        else:
            # TODO a check for a correct cell
            lst = answ_to_lst(answ)
            lst_cells += lst
            for cell in lst: # See what cells who are added
                ttt += f'Statistics cell: {cell} added...\n'
        
        if len( lst_cells ) > 0:
            ttt += 'The statistics cells which are added are: \n'
            ttt += utils.lst_to_col( lst_cells, 'left', 4 )
            ttt += cfg.ln

        cnsl.log(ttt, True)

    return lst_cells


def lst_sel_cells(t, default=cfg.e, back=False, prev=False, exit=False, spacer=False):
    # Get titles
    lst = ['DIY (do it yourself) cells'] + [lstb[0] for lstb in defaults.lst_menu]
 
    answ = type_options(t, lst, default, back, prev, exit, spacer)

    if   answ == lst[0]: return lst_diy_cells(t, default, back, prev, exit, spacer)
    elif answ == lst[1]: return defaults.winter
    elif answ == lst[2]: return defaults.summer 
    elif answ == lst[3]: return defaults.winter_summer
    elif answ == lst[4]: return defaults.extremes
    elif answ == lst[5]: return defaults.counts
    elif answ == lst[6]: return defaults.default_1
     
    return answ 

def lst_entities( t, default=cfg.e, back=False, prev=False, exit=False, spacer=False):
    lst_result = [] # Result lst

    while True:
        tt = cfg.e
        if cfg.info:
            tt += text.menu_info_entities.strip() + cfg.ln + cfg.ln

        tt += t + cfg.ln
        tt += '# To add one weather entity, type in the enitity name. e.g. TX' + cfg.ln
        tt += '# To add more entities, give entity name separated by a comma. e.g TX, TG, TN' + cfg.ln
        tt += "# Press '*' to add all entities" + cfg.ln
        # Can do next?
        if len(lst_result) > 0: 
            tt += text.enter_next()

        answ = ask(tt, default, back, prev, exit, spacer)

        ttt, len_result = cfg.e, len(lst_result)
        if answer.is_empty(answ) and \
           len_result == 0:
            ttt += text.type_in + cfg.ln
        elif answer.is_empty(answ) and \
             len_result > 0:
            break
        elif ( back and answer.is_back(answ) ) or \
             ( prev and answer.is_prev(answ) ):
            return answ
        elif answ == '*':
            lst_result = data.knmi_entities
        else:
            # Make list
            lst_new = answ.split(',') if answ.find(',') != -1 else [answ]
            lst_new = [el.strip() for el in lst_new] # Strip whitespace

            # Walkthough the new enitities, if there
            for entity in lst_new:
                # Check correct enity
                ok = data.is_entity(entity)
                if ok:
                    # Check if entity already in lst result
                    if utils.s_in_lst(lst_result, entity):
                        ttt += f'Entity {entity} already added...' + cfg.ln
                    else:
                        # Add to lst resutl
                        lst_result.append(entity)
                        ttt += f'Entity {entity} added...' + cfg.ln
                else:
                    ttt += f'Unknown option {entity} given...' + cfg.ln

        if len(lst_result) == len(stations.lst_stations_map()):
            ttt += 'All available weather entities are added...' + cfg.ln
            break
        # Show the entities in the result lst, if there
        elif len(lst_result) > 0:
            ttt += 'All weather entities who are added are:' + cfg.ln
            ttt += utils.lst_to_col(lst_result, align='left', col=8, width=3)
            ttt += cfg.ln

        cnsl.log(ttt, True)

    return lst_result

def image_download_url(t, default=cfg.e, back=False, prev=False, exit=False, spacer=False):
    lst_num = []
    t = f'{text.menu_image_download_examples}\n{t}'

    while True:
        answ = ask(t, default, back, prev, exit, spacer)

        tt = cfg.e
        # Check default if input is empthy and there is no default
        if answer.is_empty(answ) and default == cfg.e: 
            tt += text.type_in + cfg.ln
        elif ( back and answer.is_back(answ) ) or \
             ( prev and answer.is_prev(answ) ):
            return answ
        else:
            # Check url answer
            if validators.url(answ) == True:
                return answ
            else:
                tt = f'Error in url: {answ}.' + cfg.ln
    
        cnsl.log(tt, True)

def date_time(t, default=cfg.e, back=False, prev=False, exit=False, spacer=False):
    t = f'Give <{t}> datetime [yyyy-mm-dd HH:MM:SS]'
    answ = ask(t, default, back, prev, exit, spacer)
    return answ

def lst_yyyymmdd(t, default=cfg.e, back=False, prev=False, exit=False, spacer=False):
    # Init result list with the dates
    lst_result = []

    while True:
        tt = cfg.e
        if cfg.info:
            tt += text.menu_info_yyyymmdd.strip() + cfg.ln + cfg.ln

        tt += t + cfg.ln

        # Next option
        if len(lst_result) > 0: 
            tt += text.enter_next()

        answ = ask(tt, default, back, prev, exit, spacer)

        # Reset ttt
        ttt = cfg.e

        if answer.is_empty(answ) and \
           len(lst_result) == 0:
            ttt += text.type_in + cfg.ln
        elif answer.is_empty(answ) and \
             len(lst_result) > 0:
            break
        elif ( prev and answer.is_prev(answ) ) or \
             ( back and answer.is_back(answ) ):
            return answ
        else:
            # Make a lst
            lst_new = answ.split(',') if answ.find(',') != -1 else [answ]

            # Remove whitespaces
            lst_new = [el.strip() for el in lst_new] 

            # Loop through dates in new list
            for yyyymmdd in lst_new:
                ok = chk.is_date(yyyymmdd)
                if ok:
                    if utils.s_in_lst(lst_result, yyyymmdd):
                        ttt += f'Date {yyyymmdd} already added...\n'
                    else:
                        lst_result.append(yyyymmdd)
                        ttt += f'Date {yyyymmdd} added...\n'
                else:
                    ttt += f'Unknown date format {yyyymmdd} given...\n'

            # What dates we have now?
            if len(lst_result) > 0:
                ttt += '\nAll dates who are added are: \n'
                ttt += utils.lst_to_col(lst_result, align='left', col=5, width=3)

        cnsl.log(ttt, True)

    return lst_result
