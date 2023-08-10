'''Library for plotting graphs'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 3 - GPLv3'
__version__    =  '0.1.5'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import statistics
import math, sys, numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from threading import Thread
import sources.model.stats as stats
import sources.model.daydata as daydata
import sources.model.utils as utils
import sources.model.utils as util
import sources.model.convert as cvt
import sources.model.ymd as ymd
import sources.control.answer as answer
import sources.control.fio as fio
import sources.view.text as text
import sources.view.color as col
import sources.view.console as cnsl

def text_diff( l ):
    mp, mm = max(l), min(l)
    return (mp - mm) / 15.0

def calculate( options ):
    # { 
    # 'title': name, 
    # 'lst-stations': stations,
    # 'period': per_1, 
    # 'period-2': per_2, 
    # 'period-cmp': per_cmp,
    # 'lst-sel-cells': lst_sel_cel,
    # 's4d-query': s4d, 
    # 'rewrite': rewrite, 
    # 'file-type': f_type,
    # 'file-name': f_name,
    # 'graph-title': graph_title,
    # 'graph-y-label': graph_y_label, 
    # 'graph-default': graph_default,
    # 'graph-width': graph_width,
    # 'graph-height': graph_height,
    # 'graph-cummul-val': graph_cummul_val,
    # 'graph-type': graph_type,
    # 'graph-dpi': graph_dpi, 
    # 'graph-lst-entities-options': graph_lst_entities_options,
    # 'quit': quit
    # } 
    # {
    # 'entity': entity, 
    # 'line-bar': line_bar, 
    # 'line-width': line_width, 
    # 'marker-size': marker_size, 
    # 'marker-text': marker_txt,
    # 'min-max-ave-period': min_max_ave_period,  yn
    # 'climate-ave': climate_ave, yn
    # 'climate-ave-marker-txt': climate_ave_marker_txt,  yn
    # 'climate-yyyy-start': climate_yyyy_start, 
    # 'climate-yyyy-end': climate_yyyy_end,
    # 'climate-periode': climate_periode
    # }

    ok = True 
    t = f'[{ymd.now()}] Create <{options[text.ask_title]}>'
    cnsl.log(t, True)

    # Size values are inches. And figure always in front
    plt.figure( 
        figsize = ( 
            cvt.pixel_to_inch( options[text.ask_graph_width]  ),
            cvt.pixel_to_inch( options[text.ask_graph_height] ) 
        ),
        dpi=options[text.ask_graph_dpi]
    )

    # Color handling
    rnd_col = True if len(options[text.ask_stations]) > 1 else False
    if rnd_col:
        col_list = util.lst_shuffle(col.save_colors, 3)
        col_ndx, col_cnt = 0, len(col_list) - 1

    sub_txt = cfg.e
    max_all, min_all = sys.float_info.min, sys.float_info.max

    for station in options[text.ask_stations]:
        t  = f'[{ymd.now()}] Calculate graph <{options[text.ask_graph_title]}> '
        t += f'for period <{options[text.ask_period]}> '
        t += f'{station.wmo} {station.place}'
        cnsl.log(t, cfg.verbose)

        ok, np_data_2d = daydata.read(station, verbose=False)  # Read data stations
        if not ok: continue 

        # Get days from a station for the given period
        days = stats.Days( station, np_data_2d, options[text.ask_period] )
        lst_ymd = days.lst_yyyymmdd() # Date lst

        for graph in options[text.ask_graph_entities]:
            entity = graph['entity'].upper()
            cnsl.log( f'Process weatherdata {station.place} for {entity}', cfg.verbose )
            np_entity_1d = days.np_period_2d[:, daydata.etk(entity)] # Get the values needed for the graph

            # Cumulative sum of values, if chosen
            if answer.is_yes(options[text.ask_graph_cummul_val]): 
                np_entity_1d = np.cumsum(np_entity_1d)

            # Label, colors and lst_val
            label = f'{station.place} {text.ent_to_txt(entity)}'
            color = col_list[col_ndx] if rnd_col else col.entity_to_color(entity)
            lst_val = [ daydata.rounding(el, entity) for el in list(np_entity_1d) ]

            # Min/ max for ranges in graphs
            min_act, max_act = min(lst_val), max(lst_val)
            if min_act < min_all: min_all = min_act
            if max_act > max_all: max_all = max_act

            if answer.is_yes(graph['min-max-ave-period']):
                # Calculate extremes and make correct output    
                min_act, min_day, _ = days.min(entity)
                max_act, max_day, _ = days.max(entity)        
                ave_act, _ = days.average( entity )
                sum_act, _ = days.sum( entity )
                max_val = f'max={ text.fix_ent(max_act, entity) } at { int(max_day[daydata.etk("yyyymmdd")]) }'
                min_val = f'min={ text.fix_ent(min_act, entity) } at { int(min_day[daydata.etk("yyyymmdd")]) }'
                ave_val = f'mean={ text.fix_ent(ave_act, entity) }'
                sum_val = f'sum={ text.fix_ent(sum_act, entity) }'

                ttt = f'{station.place} {entity} '
                if entity in ['SQ', 'RH', 'EV24', 'Q']: 
                    ttt += f'{ave_val} {max_val} {sum_val}' 
                else: 
                    ttt += f'{ave_val} {max_val} {min_val}' 
                cnsl.log(ttt, cfg.verbose)
                sub_txt += ttt + '\n'
 
            if answer.is_yes( graph['climate-ave'] ):
                label_clima = f'Day climate {station.place} {text.ent_to_txt(entity)}'
                ttt = f'Calculate climate value {entity} for {station.place}...'
                cnsl.log(ttt, True)

                lst_clima = []
                for yyyymmdd in lst_ymd:
                    mmdd = yyyymmdd[4:8]  # What day it is ? 

                    period_days = f'{graph["climate-yyyy-start"]}-{graph["climate-yyyy-end"]}{mmdd}*'
                    days_clima = stats.Days(station, np_data_2d, period_days) # Make new object
                    ave_raw, _ = days_clima.average(entity)

                    lst_clima.append(ave_raw) # Append raw data with)out correct rounding
                    txt_mmdd = datetime.strptime(yyyymmdd, '%Y%m%d' ).strftime('%B %d').lower()

                    ttt  = f'Climate value {entity} for <{txt_mmdd}> in period <{graph["climate-periode"]}> '
                    ttt += f'is { text.fix_ent(ave_raw, entity) }'
                    cnsl.log(ttt, cfg.verbose)

                # Clima average round correctly based on entity
                if len(lst_clima) > 0:
                    clima_ave = statistics.mean(lst_clima) # Calculate average
                    ttt  = f'{station.place} {entity} mean={text.fix_ent(clima_ave, entity)} climate period '
                    ttt += f'from { graph["climate-yyyy-start"] } to { graph["climate-yyyy-end"] }'
                    cnsl.log(ttt, cfg.verbose)
                    sub_txt += ttt + '\n'
                else:
                    cnsl.log('List with clima values is empthy', cfg.error)

                # Round correctly all climate values based on ent
                lst_clima = [ daydata.rounding(val, entity) for val in lst_clima ]
                cnsl.log(' ', cfg.verbose)

            if graph['line-bar'] == 'line':
                plt.plot( 
                    lst_ymd,
                    lst_val,
                    label      = label,
                    color      = color,
                    marker     = cfg.plot_marker_type,
                    linestyle  = cfg.plot_line_style,
                    linewidth  = cfg.plot_line_width,
                    markersize = cfg.plot_marker_size,
                    alpha      = 0.7 
                )

            elif graph['line-bar'] == 'bar':
                plt.bar( 
                    lst_ymd, 
                    lst_val, 
                    label = label, 
                    color = color, 
                    alpha = 0.5 
                )

            # Climate averages always dotted lines
            if answer.is_yes(graph['climate-ave']):
                plt.plot(
                    lst_ymd, 
                    lst_clima,
                    label  = label_clima,
                    color  = color,
                    marker = cfg.plot_clima_marker_type,
                    linestyle  = cfg.plot_clima_line_style,
                    linewidth  = cfg.plot_clima_line_width,
                    markersize = cfg.plot_clima_marker_size,
                    alpha      = 0.8 
                )

            # Marker texts
            diff = 0.2 if graph['line-bar'] == 'line' else 0.1
            if answer.is_yes( graph['marker-text'] ):
                # TODO No negative values for when graph is a bar

                for lst_yyyymmdd, lst_values, lst_txt in zip( lst_ymd, lst_val, lst_val ):
                    plt.text( 
                        lst_yyyymmdd, lst_values+diff, lst_txt,
                        color = cfg.plot_marker_color, **cfg.plot_marker_font,
                        horizontalalignment = cfg.plot_marker_horizontalalignment,
                        alpha = cfg.plot_marker_alpha 
                    )

            if answer.is_yes( graph['climate-ave-marker-txt'] ):
                for lst_yyyymmdd, lst_values, lst_txt in zip( lst_ymd, lst_clima, lst_clima ):
                    plt.text(
                        lst_yyyymmdd, lst_values+diff, lst_txt,
                        color = cfg.plot_marker_color, **cfg.plot_marker_font,
                        horizontalalignment = cfg.plot_marker_horizontalalignment,
                        alpha = cfg.plot_marker_alpha 
                    )

            if rnd_col:
                col_ndx = 0 if col_ndx == col_cnt else col_ndx + 1

    # Give legend some space above (maximimum) entity 
    # !!!! optimize TODO TODO TODO
    spacer_def = 2 # Correction pffft
    spacer_max_yas = len(options[text.ask_stations]) * len(options[text.ask_graph_entities]) + spacer_def
    # spacer_min_yas = 0.5 # Not needed
    max_val_tick = int( round( math.ceil(  max_all + spacer_max_yas ))) # Maximum value
    min_val_tick = int( round( math.floor( min_all ))) # Minimum value
    min_max_diff = max_val_tick - min_val_tick
    step_tick = 10 ** len( str( abs(min_max_diff) )[:-2] ) # TODO ? Calculating y steps in graph

    # Position text upper left 
    x_pos_tick = 0  # Left
    y_pos_tick = max_val_tick + step_tick + step_tick  # Max y value
    y_ticks = np.arange( min_val_tick, y_pos_tick + step_tick, step_tick )  # ! Plus step_tick
    x_ticks = np.array( lst_ymd )

    # print( x_pos_tick, y_pos_tick )

    if sub_txt: # Add text to plot, if there
        plt.text( 
            x_pos_tick, 
            y_pos_tick - 0.5, # Most left and almost at the top
            sub_txt, 
            **cfg.plot_add_txt_font, 
            color = '#555555', 
            horizontalalignment = 'left', 
            verticalalignment   = 'top' 
        )

    plt.yticks( 
        y_ticks, 
        **cfg.plot_yas_font, 
        color = cfg.plot_yas_color 
    )

    plt.xticks(
        x_ticks, 
        **cfg.plot_xas_font, 
        color    = cfg.plot_xas_color, 
        rotation = cfg.plot_xas_rotation 
    )

    plt.title( 
        options[text.ask_graph_title], 
        **cfg.plot_title_font, 
        color = cfg.plot_title_color 
    )

    plt.xlabel( 
        cfg.plot_xlabel_text, 
        **cfg.plot_xlabel_font, 
        color = cfg.plot_xlabel_color 
    )

    plt.ylabel( 
        options[text.ask_graph_ylabel], 
        **cfg.plot_ylabel_font, 
        color = cfg.plot_ylabel_color 
    )

    plt.legend( 
        loc       = cfg.plot_legend_loc, 
        prop      = cfg.plot_legend_font,
        facecolor = cfg.plot_legend_facecolor, 
        shadow    = cfg.plot_legend_shadow,
        frameon   = cfg.plot_legend_frameon, 
        fancybox  = cfg.plot_legend_fancybox 
    )

    if cfg.plot_grid_on:
        plt.grid( 
            color     = cfg.plot_grid_color,
            linestyle = cfg.plot_grid_linestyle,
            linewidth = cfg.plot_grid_linewidth 
        )

    if answer.is_yes( cfg.plot_tight_layout ):
        plt.tight_layout()

    # Make path and save image
    fname = f'{options[text.ask_filename]}.{options[text.ask_graph_type]}' 
    path, dir, _ = utils.mk_path_with_dates( cfg.dir_graphs, fname )
    fio.mk_dir( dir, verbose=False ) # Create map always
    plt.savefig( path, dpi=options[text.ask_graph_dpi], format=options[text.ask_graph_type] )

    if answer.is_yes( cfg.plot_show ): 
        plt.show()

    return ok, path
