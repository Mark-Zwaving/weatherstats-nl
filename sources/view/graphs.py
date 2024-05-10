'''Library for plotting graphs'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.1.9'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import pprint
import statistics
import math, sys, numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import sources.control.dayvalues.read as dayval_read
import sources.model.dayvalues.broker_period as broker_period
import sources.model.dayvalues.np_days as dayval_np_days
import sources.model.statistic.maximum as np_max
import sources.model.statistic.minimum as np_min
import sources.model.statistic.mean as np_mean
import sources.model.statistic.sum as np_sum
import sources.model.statistic.clima.mean as np_clima_mean
import sources.model.utils as util
import sources.model.convert as cvt
import sources.model.ymd as ymd
import sources.model.dayvalues.data as data
import sources.control.ask.answer as answer
import sources.control.fio as fio
import sources.view.text as text
import sources.view.color as col
import sources.view.console as cnsl

def txt_min_max_ave_sum(np_days, station, dict_graph, entity):
    t = ''
    # Print min, max extremes and average to print in the grpah
    if answer.is_yes(dict_graph[text.ask_graph_entity_min_max]): 

        # Get the min and max, ave and value
        min_act, min_day, _ = np_min.calculate(np_days, entity)
        max_act, max_day, _ = np_max.calculate(np_days, entity)    
        ave_act, _ = np_mean.calculate(np_days, entity)
        sum_act, _ = np_sum.calculate(np_days, entity)
        max_ymd = int(max_day[0, data.YYYYMMDD])
        min_ymd = int(min_day[0, data.YYYYMMDD])
        max_val = text.fix_for_entity(max_act, entity) 
        min_val = text.fix_for_entity(min_act, entity)
        ave_val = text.fix_for_entity(ave_act, entity)
        sum_val = text.fix_for_entity(sum_act, entity)

        # Get txt output
        max_txt = f'max={max_val} {max_ymd}'
        min_txt = f'min={min_val} {min_ymd}'
        ave_txt = f'mean={ave_val}'
        sum_txt = f'sum={sum_val}'
        
        t += f'{station.place} {entity} {ave_txt} {max_txt} '

        # Get the sum instead of min for specific entities
        if entity in ['sq', 'rh', 'ev24', 'q']: 
            t += sum_txt 
        else: 
            t += min_txt
        t += cfg.ln

    return t

def txt_clima_mean(np_days, station, dict_graph, entity):
    # Text to make for graph
    t = ''

    # Lst with the climta values for the days mmdd
    lst_clima_mmdd = []

    if answer.is_yes(dict_graph[text.ask_graph_entity_climate_ave]):
        tt  = f'[{ymd.now()}] Day climate {station.place} {text.ent_to_txt(entity)}' + cfg.ln
        tt += f'[{ymd.now()}] Calculate climate value {entity} for {station.place}...'
        cnsl.log(tt, True)

        # Make  list of climate values
        for yyyymmdd in np_days[:,data.YYYYMMDD]:
            # Get string date
            symd = str(int(yyyymmdd))

            # Period to select a day
            period  = f'****{symd[4:8]}'

            # Get days for period untill day mmdd
            ok, np_lst_period = broker_period.process(np_days, period)
            if not ok:
                continue 

            # Calculate climate mean untill given date
            clima_ave_raw = np_clima_mean.calculate(np_lst_period, entity)

            # Add clima raw to lst
            lst_clima_mmdd.append(clima_ave_raw)

            # Output txt for verbose
            txt_mmdd = datetime.strptime(symd, '%Y%m%d' ).strftime('%B %d').lower()
            txt_ave = text.fix_for_entity(clima_ave_raw, entity)
            clima_period = dict_graph[text.ask_graph_entity_climate_period]
            tt  = f'[{ymd.now()}] Climate value {entity} for <{txt_mmdd}> '
            tt += f'in period <{clima_period}> is {txt_ave}'
            cnsl.log(tt, cfg.verbose)

        # Clima average round correctly based on entity
        if len(lst_clima_mmdd) > 0:
            # Get all time average?
            clima_lst_ave = statistics.mean(lst_clima_mmdd)

            # Calculate average from the give list
            txt_clima_ave = text.fix_for_entity(clima_lst_ave, entity)

            t  = f'{station.place} {entity} climate mean={txt_clima_ave} '
            t += f'for period {dict_graph[text.ask_graph_entity_climate_yyyy_start]}-'
            t += f'{dict_graph[text.ask_graph_entity_climate_yyyy_end]}'
            t += cfg.ln
        else:
            cnsl.log(f'[{ymd.now()}] Error: list with clima values is empthy', cfg.error)

    return t, lst_clima_mmdd 

def text_diff( l ):
    mp, mm = max(l), min(l)
    return (mp - mm) / 15.0

def calculate( options ):
    ok = True 
    cnsl.log(f'[{ymd.now()}] Create graph <{options[text.ask_title]}>', True)

    # Size values are inches. And figure always in front
    plt.figure(figsize = (cvt.pixel_to_inch(options[text.ask_graph_width]),
                          cvt.pixel_to_inch(options[text.ask_graph_height])), 
               dpi=options[text.ask_graph_dpi])
    
    # Get the list of the stations
    lst_station = options[text.ask_lst_stations]

    # Color handling
    rnd_col = True if len(lst_station) > 1 else False
    if rnd_col:
        col_list = util.lst_shuffle(col.save_colors, 3)
        col_ndx, col_cnt = 0, len(col_list) - 1

    # Init help vars
    max_all, min_all, txt_graph = sys.float_info.min, sys.float_info.max, cfg.e

    # Walkthrough stations
    for station in lst_station:
        t  = f'[{ymd.now()}] Calculate graph <{options[text.ask_graph_title]}> '
        t += f'for period <{options[text.ask_period_1]}> '
        t += f'{station.wmo} {station.place}'
        cnsl.log(t, cfg.verbose)

        # Read data stations into np lst
        ok, np_lst_days = dayval_read.weatherstation(station, verbose=False)  
        if not ok: # No values to process
            continue

        # Walkthrough entities
        for dict_graph in options[text.ask_lst_graph_entities_options]:
            # Get the name of the entity
            entity = dict_graph[text.ask_graph_entity_name]

            # Show what is goign on, if verbose
            cnsl.log( f'[{ymd.now()}] Process weatherdata {station.place} for {entity}', cfg.verbose )

            # Remove NAN for the specific entities
            ok, np_lst_valid = dayval_np_days.rm_nan(np_lst_days, entity)

            # No valid data then continue
            if not ok:
                continue

            # Get np lst days for the given period
            period = options[text.ask_period_1]
            ok, np_lst_period = broker_period.process(np_lst_valid, period)

            # Get the min and max value to print a correct grpah
            min_act, _, _ = np_min.calculate(np_lst_period, entity)
            max_act, _, _ = np_max.calculate(np_lst_period, entity)

            # Get the real values for the specifi entites
            min_act = data.process_value(min_act, entity)
            max_act = data.process_value(max_act, entity)

            # Get the absolute min and max of all the values
            if min_act < min_all: min_all = min_act
            if max_act > max_all: max_all = max_act

            # Label, colors and lst_val, nice colors to be used
            txt_label = f'{station.place} {text.ent_to_txt(entity)}'
            color = col_list[col_ndx] if rnd_col else col.entity_to_color(entity)

            # Get min, max, ave and sum if asked for
            t = txt_min_max_ave_sum(np_lst_period, station, dict_graph, entity)
            cnsl.log(f'[{ymd.now()}] {t}', cfg.verbose)
            txt_graph += t # Add to graph txt
 
            # Calculation of climate averages
            t, lst_clima_raw = txt_clima_mean(np_lst_period, station, dict_graph, entity)
            cnsl.log(f'[{ymd.now()}] {t}', cfg.verbose)
            txt_graph += t # Add to graph txt

            # Update lsts for graphs
            # Get a list of all the dates in the period
            lst_ymd = [str(int(round(d))) for d in np_lst_period[:,data.YYYYMMDD].tolist()]

            # Get the lst values needed for the graph
            lst_ent_raw   = np_lst_period[:, data.column(entity)].tolist()
            lst_ent_val   = [data.process_value(val, entity) for val in lst_ent_raw]
            lst_ent_txt   = [text.fix_for_entity(val, entity) for val in lst_ent_raw]
            lst_clima_val = [data.process_value(val, entity) for val in lst_clima_raw]
            lst_clima_txt = [text.fix_for_entity(val, entity) for val in lst_clima_raw]

            # Plot the graph with the calculated values
            if dict_graph[text.ask_graph_entity_type] == 'line':
                plt.plot(lst_ymd, lst_ent_val,
                         label      = txt_label,
                         color      = color,
                         marker     = cfg.plot_marker_type,
                         linestyle  = cfg.plot_line_style,
                         linewidth  = cfg.plot_line_width,
                         markersize = cfg.plot_marker_size,
                         alpha      = 0.7)

            elif dict_graph[text.ask_graph_entity_type] == 'bar':
                plt.bar(lst_ymd, lst_ent_val,
                        label = txt_label,
                        color = color,
                        alpha = 0.5)

            # Climate averages always dotted lines
            if answer.is_yes(dict_graph[text.ask_graph_entity_climate_ave]):
                plt.plot(lst_ymd, lst_clima_val,
                         label      = f'Climate {txt_label}',
                         color      = color,
                         marker     = cfg.plot_clima_marker_type,
                         linestyle  = cfg.plot_clima_line_style,
                         linewidth  = cfg.plot_clima_line_width,
                         markersize = cfg.plot_clima_marker_size,
                         alpha      = 0.8)

            # Diff fo marker texts
            diff = 0.3

            # Add markers to graph values 
            if answer.is_yes(dict_graph[text.ask_graph_entity_marker_text]):
                # TODO No negative values for when graph is a bar
                for yymmdd, val, txt in zip(lst_ymd, lst_ent_val, lst_ent_txt):
                    plt.text(yymmdd, val + diff, txt,
                             color = cfg.plot_marker_color,
                             fontdict = cfg.plot_marker_font,
                             horizontalalignment = cfg.plot_marker_horizontalalignment,
                             alpha = cfg.plot_marker_alpha)

            # Add markers to climate graph values
            if answer.is_yes(dict_graph[text.ask_graph_entity_climate_ave_marker_txt]):
                for yymmdd, val, txt in zip(lst_ymd, lst_clima_val, lst_clima_txt):
                    plt.text(yymmdd, val + diff, txt,
                             color = cfg.plot_marker_color, 
                             fontdict = cfg.plot_marker_font,
                             horizontalalignment = cfg.plot_marker_horizontalalignment,
                             alpha = cfg.plot_marker_alpha)

            # Colors
            if rnd_col:
                col_ndx = 0 if col_ndx == col_cnt else col_ndx + 1

    # Give legend some space above (maximimum) entity 
    # !!!! optimize TODO TODO TODO
    spacer_def = 2 # Correction pffft
    spacer_max_yas = len(options[text.ask_lst_stations]) * len(options[text.ask_lst_graph_entities]) + spacer_def
    # spacer_min_yas = 0.5 # Not needed
    max_val_tick = int(round(math.ceil(max_all + spacer_max_yas))) # Maximum value
    min_val_tick = int(round(math.floor(min_all))) # Minimum value
    min_max_diff = max_val_tick - min_val_tick
    step_tick = 10 ** len(str(abs(min_max_diff))[:-2]) # TODO ? Calculating y steps in graph

    # Position text upper left 
    x_pos_tick = 0 # Left 
    y_pos_tick = max_val_tick + step_tick + step_tick  # Max y value
    lst_y_ticks = np.arange(min_val_tick, y_pos_tick + step_tick, step_tick )  # ! Plus step_tick
    lst_x_ticks = np.array(lst_ymd)

    # Add graph text to plot, if there
    if txt_graph: 
        plt.text(x_pos_tick,
                 y_pos_tick - 0.5, # Most left and almost at the top
                 txt_graph.rstrip(), # No enters at the end
                 fontdict = cfg.plot_add_txt_font,
                 color = '#555555',
                 backgroundcolor = '#eeeeee',
                 horizontalalignment = 'left',
                 verticalalignment = 'top')

    # Yas text ticks 
    plt.yticks(lst_y_ticks,
               **cfg.plot_yas_font, 
               color = cfg.plot_yas_color)

    # Xas text ticks
    plt.xticks(lst_x_ticks, 
            #    lst_ymd,
               **cfg.plot_xas_font,
               color = cfg.plot_xas_color,
               rotation = cfg.plot_xas_rotation)

    plt.title(options[text.ask_graph_title], 
              **cfg.plot_title_font, 
              color = cfg.plot_title_color)

    plt.xlabel(cfg.plot_xlabel_text, 
               **cfg.plot_xlabel_font,
               color = cfg.plot_xlabel_color)

    plt.ylabel(options[text.ask_graph_ylabel],
               **cfg.plot_ylabel_font,
               color = cfg.plot_ylabel_color)

    plt.legend(loc = cfg.plot_legend_loc, 
               prop = cfg.plot_legend_font,
               facecolor = cfg.plot_legend_facecolor, 
               shadow = cfg.plot_legend_shadow,
               frameon = cfg.plot_legend_frameon, 
               fancybox = cfg.plot_legend_fancybox)

    if cfg.plot_grid_on:
        plt.grid(color = cfg.plot_grid_color,
                 linestyle = cfg.plot_grid_linestyle,
                 linewidth = cfg.plot_grid_linewidth)

    if answer.is_yes(cfg.plot_tight_layout):
        plt.tight_layout()

    # Make path and save image
    fname = f'{options[text.ask_filename]}.{options[text.ask_graph_extension]}' 
    path, dir, _ = fio.mk_path_with_dates(cfg.dir_graphs, fname)
    fio.mk_dir(dir, verbose=False) # Create map always
    plt.savefig(path, dpi=options[text.ask_graph_dpi], format=options[text.ask_graph_extension])

    if answer.is_yes(cfg.plot_show): 
        plt.show()

    return ok, path
