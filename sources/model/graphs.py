'''Library for plotting graphs'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU Lesser General Public License (LGPL)'
__version__    =  '0.1.5'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import math, sys, numpy as np
import matplotlib.pyplot as plt
import sources.model.stats as stats
import sources.model.daydata as daydata
import sources.model.utils as utils
import sources.view.text as text
import sources.view.color as col
import common.model.util as util
import common.model.convert as cvt
import common.model.ymd as ymd
import common.control.answer as answer
import common.control.fio as fio
import common.view.console as cnsl
from datetime import datetime
import statistics

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

    t = f'[{ymd.now()}] Create <{options["title"]}>'
    cnsl.log(t, True)

    # Size values are inches. And figure always in front
    plt.figure( 
        figsize = ( 
            cvt.pixel_to_inch( options['graph-width']  ),
            cvt.pixel_to_inch( options['graph-height'] ) 
        ),
        dpi=options['graph-dpi']
    )

    # Color handling
    rnd_col = True if len(options['lst-stations']) > 1 else False
    if rnd_col:
        col_list = util.lst_shuffle(col.save_colors, 3)
        col_ndx, col_cnt = 0, len(col_list) - 1

    sub_txt = ''
    max_all, min_all = sys.float_info.min, sys.float_info.max

    for station in options['lst-stations']:
        t  = f'[{ymd.now()}] Calculate graph <{options["graph-title"]}> '
        t += f'for period <{options["period"]}> '
        t += f'{station.wmo} {station.place}'
        cnsl.log(t, cfg.verbose)

        ok, np_data_2d = daydata.read(station, verbose=False)  # Read data stations
        if not ok: continue 

        # Get days from a station for the given period
        days = stats.Days( station, np_data_2d, options['period'] )
        lst_ymd = days.lst_yyyymmdd() # Date lst

        min_tot, max_tot = sys.float_info.max, sys.float_info.min

        for graph in options['graph-lst-entities-types']:
            entity = graph['entity'].upper()
            cnsl.log( f'Process weatherdata {station.place} for {entity}', cfg.verbose )
            np_entity_1d = days.np_period_2d[:, daydata.etk(entity)] # Get the values needed for the graph

            # Cumulative sum of values, if chosen
            if answer.yes(options['graph-cummul-val']): 
                np_entity_1d = np.cumsum(np_entity_1d)

            # Label, colors and lst_val
            label = f'{station.place} {text.entity_to_text(entity)}'
            color = col_list[col_ndx] if rnd_col else col.entity_to_color(entity)
            lst_val = [ daydata.rounding(el, entity) for el in list(np_entity_1d) ]

            # Min/ max for ranges in graphs
            min_tot_act, max_tot_act = min(lst_val), max(lst_val)
            if min_tot_act < min_all: min_all = min_tot_act
            if max_tot_act > max_all: max_all = max_tot_act

            if answer.yes(graph['min-max-ave-period']):
                # Calculate extremes and make correct output    
                min_act, _, _ = days.min(entity)
                max_act, _, _ = days.max(entity)        
                ave_act, _ = days.average( entity )
                sum_act, _ = days.sum( entity )
                max_val = f'max={ text.fix_entity(max_act, entity) }'
                min_val = f'min={ text.fix_entity(min_act, entity) }'
                ave_val = f'mean={ text.fix_entity(ave_act, entity) }'
                sum_val = f'sum={ text.fix_entity(sum_act, entity) }'

                ttt = f'{station.place} {entity}: '
                if entity in ['SQ', 'RH', 'EV24', 'Q']: 
                    ttt += f'{max_val}  {sum_val}  {ave_val}' 
                else: 
                    ttt += f'{max_val}  {min_val}  {ave_val}' 
                cnsl.log(ttt, cfg.verbose)
                sub_txt += ttt + '\n'

            if answer.yes( graph['climate-ave'] ):
                label_clima = f'Day climate {station.place} {text.entity_to_text(entity)}'
                ttt = f'Calculate climate value {entity} for {station.place} (might take a while...)'
                cnsl.log(ttt, True)

                lst_clima = []
                for f_ymd in np_ymd:
                    yyyymmdd = cvt.fl_to_s(f_ymd)
                    mmdd = yyyymmdd[4:8]  # What day it is ? 

                    period_days = f'{graph["climate-yyyy-start"]}-{graph["climate-yyyy-end"]}{mmdd}*'
                    days_clima = stats.Days(station, np_data_2d, period_days) # Make new object
                    ave_raw, _ = days_clima.average(entity)

                    lst_clima.append(ave_raw) # Append raw data with)out correct rounding
                    txt_mmdd = datetime.strptime(yyyymmdd, '%Y%m%d' ).strftime('%B %d').lower()

                    ttt  = f'Climate value {entity} for <{txt_mmdd}> in period <{graph["climate-periode"]}> '
                    ttt += f'is { text.fix_entity(ave_raw, entity) }'
                    cnsl.log(ttt, cfg.verbose)

                # Clima average round correctly based on entity
                if len(lst_clima) > 0:
                    clima_ave = statistics.mean(lst_clima) # Calculate average
                    ttt  = f'{station.place} {entity}: '
                    ttt += f'climate mean={text.fix_entity(clima_ave, entity)} '
                    ttt += f'<{ graph["climate-yyyy-start"] }-{ graph["climate-yyyy-end"] }>'
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
            if answer.yes(graph['climate-ave']):
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
            if answer.yes( graph['marker-text'] ):
                # TODO No negative values for when graph is a bar

                for lst_yyyymmdd, lst_values, lst_txt in zip( lst_ymd, lst_val, lst_val ):
                    plt.text( 
                        lst_yyyymmdd, lst_values+diff, lst_txt,
                        color = cfg.plot_marker_color, **cfg.plot_marker_font,
                        horizontalalignment = cfg.plot_marker_horizontalalignment,
                        alpha = cfg.plot_marker_alpha 
                    )

            if answer.yes( graph['climate-ave-marker-txt'] ):
                for lst_yyyymmdd, lst_values, lst_txt in zip( lst_ymd, lst_clima, lst_clima ):
                    plt.text(
                        lst_yyyymmdd, lst_values+diff, lst_txt,
                        color = cfg.plot_marker_color, **cfg.plot_marker_font,
                        horizontalalignment = cfg.plot_marker_horizontalalignment,
                        alpha = cfg.plot_marker_alpha 
                    )

            if rnd_col:
                col_ndx = 0 if col_ndx == col_cnt else col_ndx + 1

    # Diff_val = max - min1
    # Give legend some space above entities 
    add_space = ( len( options['lst-stations'] ) + 1 ) * ( len( options['graph-lst-entities-types'] ) ) 

    # !!!! TODO BUGGY MAX MIN VALUES
    max_tick  = math.ceil( max_all ) # Alltime maximum
    min_tick  = math.floor( min_all ) # Alltime minimum
    step_tick = math.floor( abs( abs( max_tick ) - abs( min_tick ) ) / 10 )
    step_tick = 1 if step_tick < 1 else step_tick # min step = 1
    y_pos_txt = max_tick + add_space * step_tick + 1  # Under the edgeplt.show()
    x_pos_txt = 0
    y_ticks = np.arange(min_tick, y_pos_txt, step_tick)  # 1-10 % ranges
    x_ticks = lst_ymd

    if sub_txt: # Add text to plot, if there
        plt.text( 
            x_pos_txt,
            y_pos_txt - step_tick - step_tick, # Most left and at the top
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
        options['graph-title'], 
        **cfg.plot_title_font, 
        color = cfg.plot_title_color 
    )

    plt.xlabel( 
        cfg.plot_xlabel_text, 
        **cfg.plot_xlabel_font, 
        color = cfg.plot_xlabel_color 
    )

    plt.ylabel( 
        options['graph-y-label'], 
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

    if answer.yes(cfg.plot_tight_layout):
        plt.tight_layout()

    # Make path and save image
    path, dir, _ = utils.mk_path_with_dates( 
        cfg.dir_graphs, f'{options["file-name"]}.{options["graph-type"]}'
    )
    fio.mk_dir(dir, verbose=False) # Create map always

    plt.savefig(path, dpi = options['graph-dpi'], format = options['graph-type'] )

    if answer.yes(cfg.plot_show): 
        plt.show()

    return path
 