'''Library contains functions for asking questions and to deal with the input
given by a user'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 3 - GPLv3'
__version__    =  '0.2.4'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import sys, config as cfg
import validators
import sources.view.text as text
import sources.model.weather_stations as weather_stations
import sources.model.utils as utils
import sources.model.daydata as daydata
import sources.model.select as select
import sources.model.validate as validate
import sources.model.ymd as ymd
import sources.model.search4days as s4d
import sources.view.console as cnsl
import sources.control.answer as answer

marker = '\n  ?  '
def ln(t):  return '\n' if t else cfg.e

def txt(t): return f'{t}{marker}'

def space(spacer, verbose): 
    cnsl.log(cfg.e, spacer and verbose) 

def answ_to_lst(answ):
    lst = [] # Make a list with table cells
    if answ.find(',') != -1:
        lst = [e.strip() for e in answ.split(',')] # Clean input
    else:
        lst = [answ.strip()]

    return lst

def any_key(t=cfg.e, spacer=False, verbose=True):
    '''Answer can be anything'''
    answ = text.clean(input(txt(t)))
    space(spacer, verbose)

    return answ

def question(t='...', default=cfg.e, back=False, prev=False, exit=False, spacer=False):
    t =  t[:-1] if t[-1] == '\n' else t
    if default != cfg.e: 
        t += f'\n{text.enter_default(default)}'
    if prev: 
        t += f'\n{text.enter_previous()}'
    if back: 
        t += f'\n{text.enter_back("main")}'
    if exit: 
        t += f'\n{text.enter_exit}'

    answ = any_key(t, spacer=spacer)

    if answer.is_quit(answ):
        cnsl.log('Goodbye!', True)
        sys.exit(0)
    elif default != cfg.e and answer.is_empty(answ):
        return default

    return answ

def y_or_n(t=cfg.e, default=cfg.e, back=False, prev=False, exit=False, spacer=False):
    t += '\nType in "y" for yess or "n" for no'
    while True:
        answ = question(t, default, back, prev, exit, spacer)

        tt = cfg.e
        if back and answer.is_back(answ):
            return answ
        elif prev and answer.is_prev(answ):
            return answ
        elif answ in text.lst_yess or answ in text.lst_no:
            return answ
        else:
            tt += 'Type in "y" or "n"...'

        cnsl.log(tt, True)

def is_yes(t=cfg.e, default=cfg.e, back=False, prev=False, exit=False, spacer=False):
    if answer.is_yes(
            y_or_n( t, default, back, prev, exit, spacer) 
        ):
        return True
    else:
        return False

def integer(t='Give an integer', default=cfg.e, back=False, prev=False, exit=True, spacer=False):

    while True:
        answ = question(t, default, back, prev, exit, spacer)

        ttt = cfg.e
        if prev and answer.is_prev(answ):
            return answ
        elif back and answer.is_back(answ):
            return answ
        elif validate.is_int(answ):
            return int(answ)
        else:
            ttt += f'{answ} is not an integer'        

        cnsl.log(ttt, True)

def open_with_app(path, options, back=False, prev=False, exit=False, spacer=False):
    t = f'\nOpen the file <type={options["file-type"]}> with your default application ?'
    answ = y_or_n( t, default=cfg.e, back=back, prev=prev, exit=exit, spacer=spacer )

    if answer.is_yes(answ):
        utils.exec_with_app(path)
    
    return answ

def back_to_main_menu(default=cfg.e, back=False, prev=False, exit=False, spacer=False):
    question(text.back_main, default, back, prev, exit, spacer)

def lst_places(t, default=cfg.e, back=False, prev=False, exit=False, spacer=False):
    lst_sel = []
    if len(weather_stations.lst_stations_map()) > 0:
        while True:
            tt = t + '\n'
            if cfg.info:
                tt += text.menu_info_stations + '\n'

            tt += 'To add one station, give a wmo-number or a city name\n'
            tt += 'To add more stations, give a wmo-number or a city name separated by a comma\n'
            tt += f"Press '*' to add all available weather stations\n"
            tt += f'{text.next_press_enter}' if len(lst_sel) > 0 else cfg.e

            answ = question(tt, default, back, prev, exit, spacer)

            ttt = cfg.e
            if answer.is_empty(answ) and len(lst_sel) == 0:
                ttt += text.type_in # Empthy list
            elif answer.is_empty(answ) and len(lst_sel) > 0:
                break # Done
            elif prev and answer.is_prev(answ):
                return answ
            elif back and answer.is_back(answ):
                return answ
            elif answ == '*':
                lst_sel = weather_stations.lst_stations_map()
            else:
                lst = answ_to_lst(answ)

                # Check and add all added stations
                for wmo_or_place in lst:
                    if weather_stations.wmo_or_place_in_map(wmo_or_place) :
                        station = weather_stations.wmo_or_place_to_station(wmo_or_place)
                        if weather_stations.station_in_list(station, lst_sel):
                            ttt += f'Station: {station.wmo} {station.place} already added...\n'
                        else:
                            lst_sel.append(station) # Append station object to lst
                            ttt += f'Station: {station.wmo} {station.place} added...\n'
                    else:
                        ttt += f'Station: {wmo_or_place} not found in list stations...\n'

            ttt += '\n'
            if len(lst_sel) == len(weather_stations.lst_stations_map()):
                ttt += 'All available weatherstations are  added...\n'
                break
            elif len(lst_sel) > 0:
                ttt += 'All weatherstation(s) who are added are: \n'
                ttt += text.lst_to_col([f'{station.wmo} {station.place}' for station in lst_sel], 'left', 4)

            cnsl.log(ttt, True)

    else:
        t = 'No weatherdata found in data map. Download weatherdata first...'
        cnsl.log(t, cfg.error)

    return lst_sel

def period_1( t=cfg.e, default=cfg.e, back=False, prev=False, exit=False, spacer=False):

    while True:
        tt = cfg.e
        if cfg.info:
            tt += text.menu_info_periods + '\n'
        tt += t

        answ = question(tt, default, back, prev, exit, spacer)

        if default and answer.is_empty(answ):
            return default
        elif answer.is_empty(answ):
            ttt = text.type_in
        elif prev and answer.is_prev(answ):
            return answ 
        elif back and answer.is_back(answ):
            return answ
        else:
            # Check validity date
            if select.days_period(period=answ, check_only=True):
                return answ
            else:
                ttt = f'Period of format {answ} is unknown... Press a key... '

        cnsl.log(ttt, cfg.error)

def period_2(t, default=cfg.e, back=False, prev=False, exit=False, spacer=False):

    lst = [ 'day', 'month' , 'period'
            #, 'season' 
    ]
    while True:
        option = type_options(t, lst, default, back, prev, exit, spacer).lower() 

        if prev and answer.is_prev(option):
            return option
        elif back and answer.is_back(option):
            return option

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
            tt += 'Example: 0501-0503\n' 
        tt += t

        answ = question(tt, default, back, prev, exit, spacer)

        if answer.is_empty(answ):
            ttt = text.type_in
        elif prev and answer.is_prev(answ):
            return answ
        elif back and answer.is_back(answ):
            return answ
        else:
            return answ

        cnsl.log(ttt, cfg.error)

def s4d_query(t, default=cfg.e, back=False, prev=False, exit=False, spacer=False):
    while True:
        tt = cfg.e
        if cfg.info:
            tt += text.menu_info_queries + '\n'
        tt += t

        answ = question(tt, default, back, prev, exit, spacer)

        if default and answer.is_empty(answ):
            return default 
        elif answer.is_empty(answ):
            ttt = text.type_in
        elif prev and answer.is_prev(answ):
            return answ
        elif back and answer.is_back(answ):
            return answ
        else:
            ok, ttt = s4d.query_ok(answ)
            if ok:
                return answ
            else:
                ttt = f'Error in query: "{answ}"! Check syntax.\n{ttt}'

        cnsl.log(ttt, cfg.error)

def type_options(t, lst, default=cfg.e, back=False, prev=False, exit=False, spacer=False):
    lst = [el.lower() for el in lst] # Make lower case
    tt = t + '\n'
    # Make options
    for i, el in enumerate(lst):
        tt += f'\t{i+1}) {el}'
        tt += ' (default)\n' if el == default else '\n'
        
    while True:
        answ = question(tt, default, back, prev, exit, spacer).lower()

        ttt = cfg.e
        if default and answer.is_empty(answ):
            return default
        elif answer.is_empty(answ):
            ttt += text.type_in
        elif prev and answer.is_prev(answ):
            return answ  
        elif back and answer.is_back(answ):
            return answ
        elif answ in lst:
            return answ
        elif validate.is_int(answ) or validate.is_float(answ):
            answi = int(answ)
            for i, el in enumerate(lst):
                if i + 1 == answi:
                    return lst[i]
        else:
            ttt = f'Unknown option: {answ} ?\nTry again.'

        cnsl.log(ttt, True)

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
    answ = question(t, default, back, prev, exit, spacer)

    if answer.is_empty(answ):
        return default

    return answ

def day( t, default=cfg.e, back=False, prev=False, exit=False, spacer=False):
    while True:
        tt = cfg.e
        if cfg.info:
            tt += text.menu_info_select_a_day + '\n'
        tt += t

        answ = question(tt, default, back, prev, exit, spacer)

        ttt = cfg.e
        if default:
            return default
        elif answer.is_empty(answ):
            ttt += text.type_in
        elif prev and answer.is_prev(answ):
            return answ
        elif back and answer.is_back(answ):
            return answ
        elif answ in text.lst_mmdd:
            return answ
        else:
            ttt = f'Day {answ} unknown ! Press a key to try again...'

        cnsl.log(ttt, cfg.error)

def month( t, default=cfg.e, back=False, prev=False, exit=False, spacer=False):
    while True:
        tt =  cfg.e
        if cfg.info:
            tt += text.menu_info_select_a_month + '\n'
        tt += t

        answ = question(tt, default, back, prev, exit, spacer)

        ttt = cfg.e
        if answer.is_empty(answ):
            ttt += text.type_in 
        elif prev and answer.is_prev(answ):
            return answ
        elif back and answer.is_back(answ):
            return answ
        elif text.month_to_mm(answ) != -1:
            return text.month_to_mm(answ)
        else:
            ttt = f'Month {answ} unknown ! Press a key to try again...'

        cnsl.log(ttt, cfg.error)

def period_compare(t, default=cfg.e, back=False, prev=False, exit=False, spacer=False):    
    lst = ['period <mmdd-mmdd>', 'years', 'season', 'month' , 'day']
    while True:
        option = type_options(t, lst, default, back, prev, exit, spacer)

        if prev and answer.is_prev(option):
            return option
        elif back and answer.is_back(option):
            return option
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
            tt += text.menu_info_td_cells + '\n'

        tt += 'To add one table cell give one statistics table cell option\n'
        tt += 'To add more table cells give table cell statistics separated by a comma\n'
        tt += f'{text.next_press_enter}' if len(lst_cells) > 0 else cfg.e
    
        answ = question(tt, default, back, prev, exit, spacer)

        ttt = cfg.e
        if answer.is_empty(answ) and len(lst_cells) == 0:
            ttt += text.type_in # Empthy list
        elif answer.is_empty(answ) and len(lst_cells) > 0:
            break # Done
        elif prev and answer.is_prev(answ):
            return answ
        elif back and answer.is_back(answ):
            return answ
        else:
            lst = answ_to_lst(answ)
            lst_cells += lst
            for cell in lst: # See what cells who are added
                ttt += f'Statistics cell: {cell} added...\n'

        ttt += '\n'
        
        if len( lst_cells ) > 0:
            ttt += 'All statistics cells which are added are: \n'
            ttt += text.lst_to_col( lst_cells, 'left', 4 )

        cnsl.log(ttt, True)

    return lst_cells

def lst_sel_cells(t, default=cfg.e, back=False, prev=False, exit=False, spacer=False):
    lst = [
        'diy <do it yourself> cells', 
        'winter statistics <default, see config.py>', 
        'summer statistics <default, see config.py>', 
        'winter and summer statistics <default, see config.py>', 
        'default extremes <see config.py>',
        'default counters <see config.py>',
        'default statistics 1 <see config.py>',
        'default statistics 2 <see config.py>'
    ]
 
    answ = type_options(t, lst, default, back, prev, exit, spacer)

    if   answ == lst[0]: return lst_diy_cells(t, default, back, prev, exit, spacer)
    elif answ == lst[1]: return cfg.lst_cells_winter
    elif answ == lst[2]: return cfg.lst_cells_summer 
    elif answ == lst[3]: return cfg.lst_cells_winter_summer
    elif answ == lst[4]: return cfg.lst_cells_my_extremes
    elif answ == lst[5]: return cfg.lst_cells_my_counts
    elif answ == lst[6]: return cfg.lst_cells_my_default_1
    elif answ == lst[7]: return cfg.lst_cells_my_default_2
     
    return answ 

def lst_entities( t, default=cfg.e, back=False, prev=False, exit=False, spacer=False):
    lst = []

    while True:
        tt = cfg.e
        if cfg.info:
            tt += text.menu_info_entities + '\n'
        tt += t + '\n'
        tt += 'To add one weather entity, type in the enitity name. e.g. TX\n'
        tt += 'To add one more entities, give entity name separated by a comma. e.g TX, TG, TN'
        if len(lst) > 0: tt += f'\n{text.next_press_enter}'

        answ = question(tt, default, back, prev, exit, spacer)

        ttt = cfg.e
        if answer.is_empty(answ) and len(lst) == 0:
            ttt += text.type_in
            continue # Again
        elif answer.is_empty(answ) and len(lst) > 0:
            break
        elif prev and answer.is_prev(answ):
            return answ 
        elif back and answer.is_back(answ):
            return answ
        else:
            l = answ.split(',') if answ.find(',') != -1 else [answ]
            l = [el.strip() for el in l]
            for entity in l:
                ok = daydata.is_entity(entity)
                if ok:
                    if utils.s_in_lst(lst, entity):
                        ttt += f'Entity {entity} is already added...\n'
                    else:
                        lst.append(entity)
                        ttt += f'Entity {entity} added...\n'
                else:
                    ttt += f'Unknown option {entity} given...\n'

            if len(lst) > 0:
                ttt += '\nAll weather entities who are added are: \n'
                ttt += text.lst_to_col(lst, align='left', col=5, width=3)

        cnsl.log(ttt, True)

    return lst

def image_download_url(t, default=cfg.e, back=False, prev=False, exit=False, spacer=False):
    lst_num = []
    t = f'{text.menu_image_download_examples}\n{t}'

    while True:
        answ = question(t, default, back, prev, exit, spacer)

        tt = cfg.e
        if answer.is_empty(answ):
            tt += text.type_in # Empthy list
        elif prev and answer.is_prev(answ):
            return answ
        elif back and answer.is_back(answ):
            return answ
        else:
            # Check url answer
            if validators.url(answ) == True:
                return answ
            else:
                tt = f'Error in url: {answ}.'
    
        cnsl.log(tt, True)

def date_time(t, default=cfg.e, back=False, prev=False, exit=False, spacer=False):
    t = f'Give a <{t}> datetime -> format [yyyy-mm-dd HH:MM:SS]'
    answ = question(t, default, back, prev, exit, spacer)
    return answ

def lst(lst_ask, name, default=cfg.e, back=False, prev=False, exit=False, spacer=False):

    # Options to ask in this function
    lst_stations     = []
    lst_sel_cel      = []
    lst_entity       = []
    s4d_querie       = cfg.e
    period1          = cfg.e
    period2          = cfg.e 
    period_compare_  = cfg.e 
    filetype         = cfg.e 
    filename         = name
    write_dayval     = cfg.e
    other            = cfg.e

    # Make option default list
    graph_title      = cfg.e
    graph_y_label    = cfg.e 
    graph_default    = cfg.plot_default 
    graph_width      = cfg.plot_width 
    graph_height     = cfg.plot_height 
    graph_cummul_val = cfg.plot_cummul_val 
    graph_extension  = cfg.plot_image_type 
    graph_dpi        = cfg.plot_dpi 
    graph_entities   = cfg.e 
    graph_entities_options = []

    # Animations and download images
    animation_download_url = cfg.e
    animation_start_dt     = cfg.e
    animation_end_dt       = cfg.e
    animation_download_interval = cfg.e
    animation_filename     = cfg.e
    animation_time         = cfg.e
    animation_verbose      = cfg.e

    rm_downloads = cfg.e
    gif_compress = cfg.e

    i, max = 0, len(lst_ask)
    while i < max:
        prev_act = False if i == 0 else prev # Can go to prev or not
        answ, quest = cfg.e, lst_ask[i]

        if quest == text.ask_download_url: 
            answ = animation_download_url = image_download_url(
                'Give a (image) download url ?', cfg.e, back, prev_act, exit, spacer
            )

        elif quest == text.ask_start_datetime: 
            add_seconds = 180 # Add seconds for start date and time
            yy, mm, dd = ymd.split_yyyymmdd( ymd.yyyymmdd_plus_second( second=add_seconds ) )
            HH, MM, SS = ymd.split_hh_mm_ss( ymd.hh_mm_ss_plus_second( second=add_seconds ) )
            answ = animation_start_dt = date_time( 
                'start', f'{yy}-{mm}-{dd} {HH}:{MM}:{SS}', back, prev_act, exit, spacer 
            )

        elif quest == text.ask_end_datetime: 
            add_seconds = 780 # Add seconds for end date and time
            yy, mm, dd = ymd.split_yyyymmdd( ymd.yyyymmdd_plus_second( second=add_seconds ) )
            HH, MM, SS = ymd.split_hh_mm_ss( ymd.hh_mm_ss_plus_second( second=add_seconds ) )
            answ = animation_end_dt = date_time( 
                'end', f'{yy}-{mm}-{dd} {HH}:{MM}:{SS}', back, prev_act, exit, spacer 
            )

        elif quest == text.ask_download_interval: 
            default = 10
            answ = animation_download_interval = integer(
                'Give the interval download time in minutes ?', default, back, prev_act, exit, spacer 
            ) 

        elif quest == text.ask_animation_name: 
            gif_ext = f'.{cfg.animation_ext}' # Animation extension
            default = f'animation-{ymd.yyyymmdd_now()}-{ymd.hhmmss_now()}.{gif_ext}'
            answ = animation_filename = question(
                'Give a name for the animation file or press enter for default ?', default, back, prev_act, exit, spacer 
            )
            if not animation_filename.lower().endswith( gif_ext ):
                animation_filename += gif_ext 

        elif quest == text.ask_animation_time: 
            answ = animation_time = float( 
                question( 
                    'Give a animation time for in the animation self <float> ?', cfg.animation_time, back, prev_act, exit, spacer 
                ) 
            )

        elif quest == text.ask_verbose: 
            answ = animation_verbose = is_yes(
                'Do you want to use the verbose option ?\n'
                'With verbose enabled the programm cannot do something else.\n'
                'Although wsstats can be started in another console.', 
                'y', back, prev_act, exit, spacer 
            )

        elif quest == text.ask_rm_downloads: 
            answ = rm_downloads = is_yes(
                'Do you want to remove the downloaded images ?', 'n', back, prev_act, exit, spacer
            )

        elif quest == text.ask_gif_compress: 
            answ = gif_compress = is_yes(
                'Do you want compress the animation file ?\nSoftware gifsicle needs to be installed on your OS...',
                 'n', back, prev_act, exit, spacer 
            )

        elif quest == text.ask_stations: # Ask for one or more stations
            answ = lst_stations = lst_places(
                'Select one (or more) weather station(s) ?', cfg.e, back, prev_act, exit, spacer 
            )

        elif quest == text.ask_per1: # Ask for period
            answ = period1 = period_1(
                f'Give the period for the calculation of {name} ?', default, back, prev_act, exit, spacer 
            ) 

        elif quest == text.ask_per2:
            answ = period2 = period_2(
                'Select a (day, month or period) in a period ?', default, back, prev_act, exit, spacer
            )
            
        elif quest == text.ask_per_compare:
            answ = period_compare_ = period_compare(
                'Give the period to compare ?', default, back, prev_act, exit, spacer 
            )

        elif quest == text.ask_diy_cells:
            answ = lst_sel_cel = lst_diy_cells(cfg.e, default, back, prev_act, exit, spacer)
            # Period 2 or not!
            if 'inf_period-2' in lst_sel_cel: # Add period 2 to question list
                lst_ask = lst_ask[:i].append(text.lst_period_2[0]) + lst_ask[i:]
                max = len(lst_ask)  # Update max
                
        elif quest == text.ask_select_cells: # Ask for type cells
            answ = lst_sel_cel = lst_sel_cells(
                'What will be the statistics cells ?', default, back, prev_act, exit, spacer 
            )

        elif quest == text.ask_write_dayval: # Rewrite or only make new non-existing files
            answ = write_dayval = type_options(
                'Do you want to add only new files or rewrite it all ?', 
                ['add', 'rewrite'], 'add', back, prev_act, exit, spacer
            )

        elif quest == text.ask_s4d_query:
            answ = s4d_querie = s4d_query(
                'Type in a query to search for days ?', default, back, prev_act, exit, spacer
            )

        elif quest == text.ask_file_type: # Ask for a file types
            answ = filetype = file_type(
                'Select output file type ?', cfg.default_output, back, prev_act, exit, spacer
            )

        elif quest == text.ask_filename: # Ask for a name
            if filetype not in text.lst_output_cnsl:  # Add query to title if there
                squery = f'-{text.query_sign_to_text(s4d_querie)}' if s4d_querie else cfg.e 
                tmp_per = f'-{period2}' if period2 else cfg.e
                tmp_name = f'{name}{squery}-{period1}{tmp_per}-{utils.now_for_file()}' 
                tmp_name = tmp_name.replace(' ', '-').replace('*', 'x').lower()
                answ = filename = file_name(
                    'Give a name for the output file ? <optional>', tmp_name, back, prev_act, exit, spacer 
                )
            else:
                filename=cfg.e

        # Graphs
        elif quest == text.ask_graph_title:
            answ = graph_title = question(
                'Give a title for the graph ?', 'My Graph Title', back, prev_act, exit, spacer 
            )

        elif quest == text.ask_graph_ylabel:
            answ = graph_y_label = question(
                'Give a y-as label for the graph ?', 'weatherdata', back, prev_act, exit, spacer 
            )

        elif quest == text.ask_graph_default:
            answ = graph_default = y_or_n(
                'Do you want to use default values ? See file -> config.py', cfg.plot_default, back, prev_act, exit, spacer
            )

        elif quest == text.ask_graph_width and answer.is_no(graph_default):
            answ = graph_width = integer(
                'Give the width (in pixels) for the graph ?', cfg.plot_width, back, prev_act, exit, spacer
            )

        elif quest == text.ask_graph_height and answer.is_no(graph_default):
            answ = graph_height = integer(
                'Give the height (in pixels) for the graph ?', cfg.plot_height, back, prev_act, exit, spacer
            )

        elif quest == text.ask_graph_cummul_val and answer.is_no(graph_default):
            answ = graph_cummul_val = y_or_n(
                'Do you want cummulative values for the graph ?', cfg.plot_cummul_val, back, prev_act, exit, spacer 
            )

        elif quest == text.ask_graph_type and answer.is_no(graph_default):
            answ = graph_type = type_options(
                'What type of image ?', ['png', 'jpg', 'ps', 'pdf', 'svg'], cfg.plot_image_type, back, prev_act, exit, spacer 
            )

        elif quest == text.ask_graph_dpi and answer.is_no(graph_default):
            answ = graph_dpi = integer(
                'Give the dpi ?', cfg.plot_dpi, back, prev_act, exit, spacer
            )

        elif quest == text.ask_graph_entities:
            answ = graph_entities = lst_entities(
                'Select weather entity(s) for the graph ?', default, back, prev_act, exit, spacer
            )

        elif quest == text.ask_graph_entities_options: 
            j = 0 
            graph_entities_options = [] 
            while j < len(graph_entities):
                graph_entity = graph_entities[j]
                # Defaults
                graph_type                    = cfg.plot_graph_type  
                graph_line_width              = cfg.plot_line_width
                graph_marker_size             = cfg.plot_marker_size
                graph_marker_txt              = cfg.plot_marker_txt
                graph_min_max_ave             = cfg.plot_min_max_ave_period
                graph_climate_yyyy_start      = cfg.climate_start_year
                graph_climate_yyyy_end        = cfg.climate_end_year
                graph_climate_ave             = cfg.plot_climate_ave
                graph_climate_ave_marker_txt  = cfg.plot_climate_marker_txt
                graph_climate_periode         = f'{cfg.climate_start_year}-{cfg.climate_end_year}'

                # Questions for traits of the entity
                k, max = 0, len( text.lst_ask_graph_entities )
                while k < max:
                    quest = text.lst_ask_graph_entities[k]

                    if quest == text.ask_graph_entity_type: 
                        answ = graph_type = type_options(
                            f'Which type graph do you want to use for {graph_entity} ?', ['line', 'bar'], 
                            cfg.plot_graph_type, back, prev_act, exit, spacer
                        )

                    elif quest == text.ask_graph_entity_marker_text: 
                        answ = graph_marker_txt = y_or_n(
                            f'Values next to the markers for {graph_entity} ?', 
                            cfg.plot_marker_txt, back, prev_act, exit, spacer
                        )

                    elif quest == text.ask_graph_entity_min_max: 
                        answ = graph_min_max_ave = y_or_n(
                            f'Calculate min, max and average value for {graph_entity} ?', 
                            cfg.plot_min_max_ave_period, back, prev_act, exit, spacer
                        )

                    elif quest == text.ask_graph_entity_climate_ave:
                        answ = graph_climate_ave = y_or_n(
                            f'Calculate and plot the climate averages for {graph_entity} ?', 
                            cfg.plot_climate_ave, back, prev_act, exit, spacer
                        )

                    elif quest == text.ask_graph_entity_climate_ave_marker_txt and answer.is_yes(graph_climate_ave):
                        answ = graph_climate_ave_marker_txt = y_or_n(
                            f'Values next to the markers for climate averages for {graph_entity} ?', 
                            cfg.plot_climate_marker_txt, back, prev_act, exit, spacer
                        )

                    elif quest == text.ask_graph_entity_climate_yyyy_start and answer.is_yes(graph_climate_ave):
                        sy, ey = cfg.climate_period.split('-')
                        answ = graph_climate_yyyy_start = integer(
                            f'Give a start year for the calculation of climate averages <yyyy> for {graph_entity} ?', 
                            sy, back, prev_act, exit, spacer
                        )

                    elif quest == text.ask_graph_entity_climate_yyyy_end and answer.is_yes(graph_climate_ave):
                        answ = graph_climate_yyyy_end = integer(
                            f'Give an end year for the calculation of climate average <yyyy> for {graph_entity} ?', 
                            ey, back, prev_act, exit, spacer
                        )

                    if prev_act and answer.is_prev(answ):
                        k -= 1
                        if k < 0:
                            j -= 1
                            break # Break this loop for now. Go back to above loop

                    elif back and answer.is_back(answ):
                        other = text.lst_back[0]
                        k = -1

                    else: # Next question
                        k += 1 

                graph_climate_periode = f'{graph_climate_yyyy_start}-{graph_climate_yyyy_end}'

                if k != -1:
                    graph_entities_options.append( 
                    {
                        text.ask_graph_entity:                         graph_entity, 
                        text.ask_graph_entity_type:                    graph_type, 
                        text.ask_graph_entity_line_width :             graph_line_width, 
                        text.ask_graph_entity_marker_size:             graph_marker_size, 
                        text.ask_graph_entity_marker_text:             graph_marker_txt,
                        text.ask_graph_entity_min_max:                 graph_min_max_ave, 
                        text.ask_graph_entity_climate_ave:             graph_climate_ave, 
                        text.ask_graph_entity_climate_ave_marker_txt:  graph_climate_ave_marker_txt,
                        text.ask_graph_entity_climate_yyyy_start:      graph_climate_yyyy_start, 
                        text.ask_graph_entity_climate_yyyy_end:        graph_climate_yyyy_end,
                        text.ask_graph_entity_climate_period:          graph_climate_periode
                    } )
                else:
                    continue

                if prev_act and answer.is_prev(answ):
                    j -= 1
                    if j < 0:
                        i -= 1
                        break

                elif back and answer.is_back(answ):
                    other = text.lst_back[0]

                else: # Next question (graphs)
                    j += 1

        if back and answer.is_back(answ):
            other = text.lst_back[0]

        elif prev_act and answer.is_prev(answ):
            i -= 1 

        else:
            i += 1 # Next question 

        if not answer.is_empty(other):
            break

    return { 
        text.ask_title:                   name, 
        text.ask_stations:                lst_stations,
        text.ask_period:                  period1, 
        text.ask_per2:                    period2, 
        text.ask_per_compare:             period_compare_,
        text.ask_clima_period:            cfg.climate_period, # TODO ASK for years and put in year in head of table
        text.ask_select_cells:            lst_sel_cel,
        text.ask_s4d_query:               s4d_querie, 
        text.ask_write_dayval:            write_dayval, 
        text.ask_file_type:               filetype,
        text.ask_filename:                filename,
        text.ask_entities:                lst_entity,

        # Graphs
        text.ask_graph_title:             graph_title,
        text.ask_graph_ylabel:            graph_y_label, 
        text.ask_graph_default:           graph_default,
        text.ask_graph_width:             graph_width,
        text.ask_graph_height:            graph_height,
        text.ask_graph_cummul_val:        graph_cummul_val,
        text.ask_graph_extension:         graph_extension,
        text.ask_graph_dpi:               graph_dpi, 
        text.ask_graph_entities:          graph_entities,
        text.ask_graph_entities_options:  graph_entities_options,

        # Animation and download images 
        text.ask_download_url:            animation_download_url,
        text.ask_start_datetime:          animation_start_dt,
        text.ask_end_datetime:            animation_end_dt,
        text.ask_download_interval:       animation_download_interval,
        text.ask_animation_name:          animation_filename,
        text.ask_animation_time:          animation_time,
        text.ask_rm_downloads:            rm_downloads,
        text.ask_gif_compress:            gif_compress,
        text.ask_verbose:                 animation_verbose,

        # Go back to menu or backward one question
        text.ask_other_menu:              other
    } 
