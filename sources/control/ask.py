'''Library contains functions for asking questions and to deal with the input
given by a user'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 3 - GPLv3'
__version__    =  '0.2.3'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import sys, config as cfg
import sources.view.text as text
import sources.model.weather_stations as weather_stations
import sources.model.utils as utils
import sources.model.daydata as daydata
import sources.model.select as select
import sources.view.console as cnsl
import sources.control.answer as answer
import sources.model.validate as validate

marker = '\n  ?  '
def ln(t):  return '\n' if t else ''

def txt(t): return f'{t}{marker}'

def space(spacer, verbose): 
    cnsl.log('', spacer and verbose) 

def answ_to_lst(answ):
    lst = [] # Make a list with table cells
    if answ.find(',') != -1:
        lst = [e.strip() for e in answ.split(',')] # Clean input
    else:
        lst = [answ.strip()]

    return lst

def any_key(t='', spacer=False, verbose=True):
    '''Answer can be anything'''
    answ = text.clean(input(txt(t)))
    space(spacer, verbose)

    return answ

def question(t='...', default='', back=False, prev=False, exit=False, spacer=False):
    t =  t[:-1] if t[-1] == '\n' else t
    if default: 
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

    return answ

def y_or_n(t='', default='', back=False, prev=False, exit=True, spacer=False):
    t += '\nType in "y" for yess or "n" for no'
    while True:
        answ = question(t, default, back, prev, exit, spacer)

        tt = ''
        if answer.is_empty(answ):
            return default
        elif back and answer.is_back(answ):
            return answ
        elif prev and answer.is_prev(answ):
            return answ
        elif answ in text.lst_yess or answ in text.lst_no:
            return answ
        else:
            tt += 'Type in "y" or "n"...'

        cnsl.log(tt, True)

def is_yes(t='', default='', back=False, prev=False, exit=True, spacer=False):
    if answer.is_yes(
            y_or_n( t, default, back, prev, exit, spacer) 
        ):
        return True
    else:
        return False

def integer(t='Give an integer', default='', back=False, prev=False, exit=True, spacer=False):

    while True:
        answ = question(t, default, back, prev, exit, spacer)

        ttt = ''
        if answer.is_empty(answ):
            return default
        elif prev and answer.is_prev(answ):
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
    answ = y_or_n(t, default='', back=back, prev=prev, exit=exit, spacer=spacer)

    if answer.is_yes(answ):
        utils.exec_with_app(path)
    else:
        return answ

def back_to_main_menu(default='', back=False, prev=False, exit=True, spacer=False):
    question(text.back_main, default, back, prev, exit, spacer)

def lst_places(t, default='', back=False, prev=False, exit=False, spacer=False):
    lst_sel = []
    if len(weather_stations.lst_stations_map()) > 0:
        while True:
            tt = ''
            if cfg.info:
                tt += text.menu_info_stations + '\n'

            tt += 'To add one station, give a wmo-number or a city name\n'
            tt += 'To add more stations, give a wmo-number or a city name separated by a comma\n'
            tt += f"Press '*' to add all available weather stations\n"
            tt += f'{text.next_press_enter}' if len(lst_sel) > 0 else ''

            answ = question(tt, default, back, prev, exit, spacer)

            ttt = ''
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

def period_1( t='', default='', back=False, prev=False, exit=False, spacer=False):

    while True:
        tt = ''
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

def period_2(t, default='', back=False, prev=False, exit=False, spacer=False):

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

def period_day_to_day( t, default, back, prev, exit, spacer):
    while True:
        tt = ''
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

def s4d_query(t, default='', back=False, prev=False, exit=False, spacer=False):
    while True:
        tt = ''
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
            ok, ttt = utils.query_ok(answ)
            if ok:
                return answ
            else:
                ttt = f'Error in query: "{answ}"! Check syntax.\n{ttt}'

        cnsl.log(ttt, cfg.error)

def type_options(t, lst, default='', back=False, prev=False, exit=False, spacer=False):
    lst = [el.lower() for el in lst] # Make lower case
    tt = t + '\n'
    # Make options
    for i, el in enumerate(lst):
        tt += f'\t{i+1}) {el}'
        tt += ' (default)\n' if el == default else '\n'
        
    while True:
        answ = question(tt, default, back, prev, exit, spacer).lower()

        ttt = ''
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

def file_type(t, default='', back=False, prev=False, exit=False, spacer=False):
    lst = text.lst_output_options
    return type_options(t, lst, default, back, prev, exit, spacer)

def graph_type(t, default='', back=False, prev=False, exit=False, spacer=False):
    lst = ['line', 'bar']
    return type_options(t, lst, default, back, prev, exit, spacer)

def season_type(t, default='', back=False, prev=False, exit=False, spacer=False):
    lst = ['winter', 'spring', 'summer', 'autumn']
    return type_options(t, lst, default, back, prev, exit, spacer)

def file_name(t, default='', back=False, prev=False, exit=False, spacer=False):
    answ = question(t, default, back, prev, exit, spacer)

    if answer.is_empty(answ):
        return default

    return answ

def day( t, default='', back=False, prev=False, exit=False, spacer=False):
    while True:
        tt = ''
        if cfg.info:
            tt += text.menu_info_select_a_day + '\n'
        tt += t

        answ = question(tt, default, back, prev, exit, spacer)

        ttt = ''
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

def month( t, default='', back=False, prev=False, exit=False, spacer=False):
    while True:
        tt =  ''
        if cfg.info:
            tt += text.menu_info_select_a_month + '\n'
        tt += t

        answ = question(tt, default, back, prev, exit, spacer)

        ttt = ''
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

def period_compare(t, default='', back=False, prev=False, exit=False, spacer=False):    
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

def lst_diy_cells(t='', default='', back=False, prev=False, exit=False, spacer=False):
    lst_cells = []
    while True:
        tt =  ''
        if cfg.info:
            tt += text.menu_info_td_cells + '\n'

        tt += 'To add one table cell give one statistics table cell option\n'
        tt += 'To add more table cells give table cell statistics separated by a comma\n'
        tt += f'{text.next_press_enter}' if len(lst_cells) > 0 else ''
    
        answ = question(tt, default, back, prev, exit, spacer)

        ttt = ''
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

def lst_sel_cells(t, default='', back=False, prev=False, exit=False, spacer=False):
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

def lst_entities( t, default='', back=False, prev=False, exit=False, spacer=False):
    lst = []

    while True:
        tt = ''
        if cfg.info:
            tt += text.menu_info_entities + '\n'
        tt += t + '\n'
        tt += 'To add one weather entity, type in the enitity name. e.g. TX\n'
        tt += 'To add one more entities, give entity name separated by a comma. e.g TX, TG, TN'
        if len(lst) > 0: tt += f'\n{text.next_press_enter}'

        answ = question(tt, default, back, prev, exit, spacer)

        ttt = ''
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

def image_download_url(back=False, prev=False, exit=False, spacer=False):
    lst_num = []
    t = 'Select a download image url\n'
    for ndx, url in enumerate(cfg.lst_weather_images_url):
        num = f'{ndx+1}'
        t += f'  {num} {url}\n'
        lst_num.append(num)

    while True:
        answ = question(t, default='', back=back, prev=prev, exit=exit, spacer=spacer)

        tt = ''
        if answer.is_empty(answ):
            tt += text.type_in # Empthy list
        elif prev and answer.is_prev(answ):
            return answ
        elif back and answer.is_back(answ):
            return answ
        elif answ in lst_num:
            return cfg.lst_weather_images_url[int(answ)-1]
        else:
            tt = f'Answer given {answ} is unknown'
    
        cnsl.log(tt, True)

def date_time(t, back=False, prev=False, exit=False, spacer=False):
    t = f'Give a <{t}> datetime -> format [yyyy-mm-dd HH:MM:SS]'
    answ = question(t, '', back=back, prev=prev, exit=exit, spacer=spacer)
    return answ

def interval_download(back=False, prev=False, exit=False, spacer=False):
    t = 'Give the interval download time in minutes'
    answ = integer(t, 10, back=True, prev=True, exit=True, spacer=True) 
    return answ

def animation_name(back=False, prev=False, exit=False, spacer=False):
    t = f'Give a name for the animation file or press enter for default'
    answ = question(t, '', back=back, prev=prev, exit=exit, spacer=spacer)
    return answ 

def animation_time(back=False, prev=False, exit=False, spacer=False):
    t = f'Give a animation time for the animation <float>'
    answ = question(t, cfg.animation_time, back=back, prev=prev, exit=exit, spacer=spacer)
    
    if answer.is_empty(answ):
        return cfg.animation_time
    else:
        return float(answ)

def remove_downloads(back=False, prev=False, exit=False, spacer=False):
    while True:
        t  = 'Do you want to remove the downloaded images?'
        answ = y_or_n(t, '', back=back, prev=prev, exit=exit, spacer=spacer)

        if answer.is_yes(answ):
            return True 
        elif answer.is_no(answ):
            return False
        elif prev and answer.is_prev(answ):
            return answ
        elif back and answer.is_back(answ):
            return answ
        
        cnsl.log(f'Wrong answer {answ} given ?', True)

def gif_compress(back=False, prev=False, exit=False, spacer=False):
    while True:
        t  = 'Do you want compress the animation file ?\n'
        t += 'Gifsicle needs to be installed on your OS'
        answ = y_or_n(t, '', back=back, prev=prev, exit=exit, spacer=spacer)

        if answer.is_yes(answ):
            return True 
        elif answer.is_no(answ):
            return False
        elif prev or answer.is_prev(answ):
            return answ
        elif back and answer.is_back(answ):
            return answ
        
        cnsl.log(f'Wrong answer {answ} given ?', True)

def animation_verbose(back=False, prev=False, exit=False, spacer=False):
    while True:
        t  = 'Do you want to use the verbose option ?\n'
        t += 'With verbose enabled the programm cannot do something else.\n'
        t += 'Although wsstats can be started in another console.'
        answ = y_or_n(t, '', back, prev, exit, spacer)
        if answer.is_yes(answ):
            return True 
        elif answer.is_no(answ):
            return False
        elif prev and answer.is_prev(answ):
            return answ
        elif back and answer.is_back(answ):
            return answ

        cnsl.log(f'Wrong answer {answ} given ?', True)

def lst(lst_ask, name, default='', back=False, prev=False, exit=False, spacer=False):
    # Max options to aks in this function
    lst_stations, lst_sel_cel, lst_entity, quit = [], [], [], False
    s4d, per_1, per_2, per_cmp, f_type, f_name = '', '', '', '', '', name
    write, other = '', ''
    # Make option default list
    graph_title, graph_y_label = '', '' 
    graph_default = cfg.plot_default
    graph_width = cfg.plot_width
    graph_height = cfg.plot_height
    graph_cummul_val = cfg.plot_cummul_val
    graph_type = cfg.plot_image_type
    graph_dpi = cfg.plot_dpi
    graph_lst_entities_options = []

    # Animations
    anim_image_download_url = ''
    anim_start_datetime = ''
    anim_end_datetime = ''
    anim_interval_download = ''
    anim_animation_name = ''
    anim_animation_time = ''
    anim_remove_downloads = ''
    anim_gif_compress = ''
    anim_verbose = ''

    i, max = 0, len(lst_ask)
    while i < max:
        prev_act = False if i == 0 else prev # Can go to prev or not
        answ, quest = '', lst_ask[i]

        if quest == 'image-download-url': 
            anim_image_download_url = image_download_url(back, prev_act, exit, spacer)
            answ = anim_image_download_url
            
        elif quest == 'start-datetime': 
            anim_start_datetime = date_time('start', back, prev_act, exit, spacer)
            answ = anim_start_datetime

        elif quest == 'end-datetime': 
            anim_end_datetime = date_time('end', back, prev_act, exit, spacer)
            answ = anim_end_datetime
        
        elif quest == 'interval-download': 
            anim_interval_download = interval_download(back, prev_act, exit, spacer)
            answ = anim_interval_download

        elif quest == 'animation-name': 
            anim_animation_name = animation_name(back, prev_act, exit, spacer)
            answ = anim_animation_name

        elif quest == 'animation-time': 
            anim_animation_time = animation_time(back, prev_act, exit, spacer)
            answ = anim_animation_time
        
        elif quest == 'remove-downloads': 
            anim_remove_downloads = remove_downloads(back, prev_act, exit, spacer)
            answ = anim_remove_downloads
        
        elif quest == 'gif-compress': 
            anim_gif_compress = gif_compress(back, prev_act, exit, spacer)
            answ = anim_gif_compress
        
        elif quest == 'verbose': 
            anim_verbose = animation_verbose(back, prev_act, exit, spacer)
            answ = anim_verbose

        elif quest == 'lst-stations': # Ask for one or more stations
            t = 'Select one (or more) weather station(s) ?'
            lst_stations = lst_places(t, default, back, prev_act, exit, spacer)
            answ = lst_stations

        elif quest in text.lst_period_1: # Ask for period
            t = f'Give the period for the calculation of {name}'
            per_1 = period_1(t, default, back, prev_act, exit, spacer)
            answ = per_1
    
        elif quest == 'period-cmp':
            t = f'Give the period to compare ?'
            per_cmp = period_compare(t, default, back, prev_act, exit, spacer)
            answ = per_cmp

        elif quest == 'lst-diy-cells':
            lst_sel_cel = lst_diy_cells('', default, back, prev_act, exit, spacer)
            answ = lst_sel_cel
            # Period 2 or not!
            if 'inf_period-2' in lst_sel_cel: # Add period 2 to question list
                lst_ask = lst_ask[:i].append(text.lst_period_2[0]) + lst_ask[i:]
                max = len(lst_ask)  # Update max

        elif quest == 'lst-sel-cells': # Ask for type cells
            t = 'What will be the statistics cells ?'
            lst_sel_cel = lst_sel_cells(t, default, back, prev_act, exit, spacer )
            answ = lst_sel_cel

        elif quest == 'write': # Rewrite or only make new non-existing files
            t, lst = 'Do you want to add only new files or rewrite it all ?', ['add', 'rewrite']
            write = type_options(t, lst, 'add', back, prev_act, exit, spacer )
            answ = write

        elif quest == 's4d-query':
            t = 'Type in a query to search for days ?'
            s4d = s4d_query(t, default, back, prev_act, exit, spacer)
            answ = s4d 

        elif quest == 'file-type': # Ask for a file types
            default = cfg.default_output
            t = 'Select output type ? '
            f_type = file_type(t, default, back, prev_act, exit, spacer)
            answ = f_type

        elif quest in text.lst_period_2:
            t = 'Select a (day, month or period) period'
            per_2 = period_2(t, default, back, prev_act, exit, spacer)
            answ = per_2

        elif quest == 'file-name': # Ask for a name
            if f_type not in text.lst_output_cnsl:  # Add query to title if there
                squery = f'-{text.query_sign_to_text(s4d)}' if s4d else '' 
                tmp_per = f'-{per_2}' if per_2 else ''
                tmp_name = f'{name}{squery}-{per_1}{tmp_per}-{utils.now_for_file()}' 
                tmp_name = tmp_name.replace(' ', '-').replace('*', 'x').lower()

                t = 'Give a name for the output file ? <optional>'
                f_name = file_name(t, tmp_name, back, prev_act, exit, spacer) 
                answ = f_name
            else:
                f_name=''

        elif quest == 'lst-entities':
            t = 'Select weather entity(s) ?'
            lst_entity = lst_entities(t, default, back, prev_act, exit, spacer)
            answ = lst_entity

        elif quest == 'graph-title':
            t = 'Give a title for the graph'
            graph_title = question(t, default, back, prev_act, exit, spacer)
            answ = graph_title

        elif quest == 'graph-y-label':
            t = 'Give a y-as label for the graph'
            graph_y_label = question(t, default, back, prev_act, exit, spacer)
            answ = graph_y_label

        elif quest == 'graph-default':
            t = 'Do you want to use default values ? See file -> config.py'
            graph_default = y_or_n(t, cfg.plot_default, back, prev_act, exit, spacer)
            answ = graph_default

        elif answer.is_no(graph_default) and quest == 'graph-width':
            t = 'Give the width (in pixels) for the graph ?'
            graph_width = integer(t, cfg.plot_width, back, prev_act, exit, spacer)
            answ = graph_width

        elif answer.is_no(graph_default) and quest == 'graph-height':
            t = 'Give the height (in pixels) for the graph ?'
            graph_height = integer(t, cfg.plot_height, back, prev_act, exit, spacer)
            answ = graph_height

        elif answer.is_no(graph_default) and quest == 'graph-cummul-val':
            t = 'Do you want cummulative values for the graph ?'
            graph_cummul_val = y_or_n(t, cfg.plot_cummul_val, back, prev_act, exit, spacer)
            answ = graph_cummul_val

        elif answer.is_no(graph_default) and quest == 'graph-type':
            t, lst_ext = 'What type of image ? ', ['png', 'jpg', 'ps', 'pdf', 'svg']
            graph_type = type_options(t, lst_ext, cfg.plot_image_type, back, prev_act, exit, spacer)
            answ = graph_type

        elif answer.is_no(graph_default) and quest == 'graph-dpi':
            t = 'Give the dpi ?'
            graph_dpi = integer(t, cfg.plot_dpi, back, prev_act, exit, spacer)
            answ = graph_dpi

        # There must be a list with entities
        elif quest == 'graph-lst-entities-types':
            j = 0 
            while j < len(lst_entity):
                entity = lst_entity[j]

                # Defaults
                line_bar = cfg.plot_graph_type 
                line_width = cfg.plot_line_width
                marker_size = cfg.plot_marker_size
                marker_txt = cfg.plot_marker_txt
                min_max_ave_period = cfg.plot_min_max_ave_period
                climate_yyyy_start = ''
                climate_yyyy_end = ''
                climate_ave = cfg.plot_climate_ave
                climate_ave_marker_txt = cfg.plot_climate_marker_txt
                climate_periode = ''
                lst_ask_graph = [ 
                    'line-bar', 'marker-txt', 'min-max-ave-period', 'climate-ave', 
                    'climate-ave-marker-txt', 'climate-periode', 'climate-yyyy-start', 'climate-yyyy-end'
                ]
                k, max = 0, len( lst_ask_graph )
                while k < max:
                    quest = lst_ask_graph[k]

                    if quest == 'line-bar':
                        t, lst_lb = f'Which type graph do you want to use for {entity} ?', ['line', 'bar']
                        line_bar = type_options(t, lst_lb, cfg.plot_graph_type, back, prev_act, exit, spacer)
                        answ = line_bar

                    elif quest == 'marker-txt':
                        t = f'Values next to the markers for {entity} ?'
                        marker_txt = y_or_n(t, cfg.plot_marker_txt, back, prev_act, exit, spacer)
                        answ = marker_txt

                    elif quest == 'min-max-ave-period': 
                        t = f'Calculate min, max and average value for {entity} ?'
                        min_max_ave_period = y_or_n(t, cfg.plot_min_max_ave_period, back, prev_act, exit, spacer)
                        answ = min_max_ave_period

                    elif quest == 'climate-ave':
                        t = f'Calculate and plot the climate averages for {entity} ?'
                        climate_ave = y_or_n(t, cfg.plot_climate_ave, back, prev_act, exit, spacer)
                        answ = climate_ave

                    elif answer.is_yes(climate_ave) and quest == 'climate-ave-marker-txt':
                        t = f'Values next to the markers for climate averages for {entity} ?'
                        climate_ave_marker_txt = y_or_n(t, cfg.plot_climate_marker_txt, back, prev_act, exit, spacer)
                        answ = climate_ave_marker_txt

                    elif answer.is_yes(climate_ave) and quest == 'climate-yyyy-start':
                        sy, ey = cfg.climate_period.split('-')
                        t = f'Give a start year for the calculation of climate averages <yyyy> for {entity} ?'
                        climate_yyyy_start = integer(t, sy, back, prev_act, exit, spacer)
                        answ = climate_yyyy_start

                    elif answer.is_yes(climate_ave) and quest == 'climate-yyyy-end':                
                        t = f'Give an end year for the calculation of climate average <yyyy> for {entity} ?'
                        climate_yyyy_end = integer(t, ey, back, prev_act, exit, spacer)
                        answ = climate_yyyy_end
                        climate_periode = f'{climate_yyyy_start}-{climate_yyyy_end}'

                    if prev and answer.is_prev(answ):
                        k -= 1
                        if k < 0:
                            break 
                    elif back and answer.is_back(answ):
                        other = answer
                    else: # Next question
                        k += 1 

                graph_lst_entities_options.append( {
                    'entity': entity, 
                    'line-bar': line_bar, 
                    'line-width': line_width, 
                    'marker-size': marker_size, 
                    'marker-text': marker_txt,
                    'min-max-ave-period': min_max_ave_period, 
                    'climate-ave': climate_ave, 
                    'climate-ave-marker-txt': climate_ave_marker_txt,
                    'climate-yyyy-start': climate_yyyy_start, 
                    'climate-yyyy-end': climate_yyyy_end,
                    'climate-periode': climate_periode
                } )

                if prev and answer.is_prev(answ):
                    j -= 1
                    if j < 0:
                        break
                elif back and answer.is_back(answ):
                    other = answer
                else: # Next question
                    j += 1

        if back and answer.is_back(answ):
            other = answer

        elif prev and answer.is_prev(answ):
            i = i - 1 if i > 0 else 0 

        else:
            i += 1 # Next question

        if not answer.is_empty(other):
            break

    return { 
        'title': name, 
        'lst-stations': lst_stations,
        'period': per_1, 
        'period-2': per_2, 
        'period-cmp': per_cmp,
        'clima-period': cfg.climate_period, # TODO ASK for years and put in year in head of table
        'lst-sel-cells': lst_sel_cel,
        's4d-query': s4d, 
        'write': write, 
        'file-type': f_type,
        'file-name': f_name,
        # Graphs
        'graph-title': graph_title,
        'graph-y-label': graph_y_label, 
        'graph-default': graph_default,
        'graph-width': graph_width,
        'graph-height': graph_height,
        'graph-cummul-val': graph_cummul_val,
        'graph-type': graph_type,
        'graph-dpi': graph_dpi, 
        'graph-lst-entities-types': graph_lst_entities_options,

        # Animation
        'image-download-url': anim_image_download_url,
        'start-datetime': anim_start_datetime,
        'end-datetime': anim_end_datetime,
        'interval-download': anim_interval_download,
        'animation-name': anim_animation_name,
        'animation-time': anim_animation_time,
        'remove-downloads': anim_remove_downloads,
        'gif-compress': anim_gif_compress,
        'verbose': anim_verbose,
        'other': other
    } 
