# -*- coding: utf-8 -*-
'''Library contains configuration options and a list with knmi stations'''
__author__     = 'Mark Zwaving'
__email__      = 'markzwaving@gmail.com'
__copyright__  = 'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    = 'GNU General Public License version 3 - GPLv3'
__version__    = '0.9.8' 
__maintainer__ = 'Mark Zwaving'
__status__     = 'Development'

################################################################################
import os, sys, time, numpy as np  # Python modules
################################################################################

verbose = False  # Print more(all) to screen
error   = True   # Print exceptions and errors to screen
info    = True   # Show examples and help info in menu by default
console = True   # Show always the calculated tables in the console 
log     = False  # Log to file 
debug   = False  # Debug mode

# To save the current weather and forecasts in the data/forecasts map,
# set save_forecasts to true
save_forecasts = True 

# Default output type file. Options: html, text and cmd
# cmd is output to screen only. Text en html writes texts/html files
default_output = 'html file'

# The <default> years/period for the calculations of climate averages
climate_start_year = 1991
climate_end_year   = 2020

# Do not change
climate_period = f'{climate_start_year}-{climate_end_year}'

# Set the time zone
timezone = 'Europe/Amsterdam'  

# csv separator
csv_sep = ';'

# Line width for #
txt_line_width = 80

################################################################################
# For HTML pages
# Add popup tables in html tables. True for yess, False for no
html_popup_table_show = True
# Give a max number for rows html popup table else html pages can become very large
html_popup_table_max_rows = 10  # -1 for all rows
# Remove whitespace from html pages source code
html_strip = True

################################################################################
# Config base maps
dir_app        = os.path.abspath(os.path.dirname(__file__))
dir_www        = os.path.abspath('/var/www/html')  # For a webserver
dir_data       = os.path.join(dir_app,  'data')
dir_statistics = os.path.join(dir_data, 'statistics')
dir_templates  = os.path.join(dir_data, 'templates')
dir_forecasts  = os.path.join(dir_data, 'forecasts')    # Downloaded forecasts
dir_thirdparty = os.path.join(dir_data, 'thirdparty')
dir_graphs     = os.path.join(dir_data, 'graphs')
dir_download   = os.path.join(dir_data, 'downloads')
dir_animation  = os.path.join(dir_data, 'animations')

dir_dayvalues     = os.path.join(dir_data, 'dayvalues') # Dayvalues
dir_dayvalues_zip = os.path.join(dir_dayvalues, 'zip')  # knmi zip files
dir_dayvalues_txt = os.path.join(dir_dayvalues, 'txt')  # knmi text files
dir_dayvalues_htm = os.path.join(dir_dayvalues, 'html') # knmi html files from text

dir_stats_txt   = os.path.join(dir_statistics, 'text')
dir_stats_htm   = os.path.join(dir_statistics, 'html')
dir_stats_csv   = os.path.join(dir_statistics, 'csv')
dir_stats_excel = os.path.join(dir_statistics, 'excel')

# Paths templates
html_template_dayvalues  = os.path.join(dir_templates, 'dayvalues.html')
html_template_statistics = os.path.join(dir_templates, 'statistics.html')

################################################################################
# KNMI Weather
knmi_ftp_pub = 'ftp://ftp.knmi.nl/pub_weerberichten/'
knmi_forecast_global_url   = f'{knmi_ftp_pub}basisverwachting.txt'
knmi_forecast_model_url    = f'{knmi_ftp_pub}guidance_meerdaagse.txt'
knmi_forecast_guidance_url = f'{knmi_ftp_pub}guidance_modelbeoordeling.txt'

# JSON url 10 minute values.
knmi_json_data_10min = 'ftp://ftp.knmi.nl/pub_weerberichten/tabel_10Min_data.json'
# Select places to show with current measurements. -1 for all
# Possible options for knmi places
# 'Lauwersoog', 'Nieuw Beerta', 'Terschelling', 'Vlieland', 'Leeuwarden', 'Stavoren',
# 'Houtribdijk', 'Hoogeveen', 'Heino', 'Twente', 'Deelen', 'Hupsel', 'Herwijnen', 'Marknesse',
# 'De Bilt', 'Cabauw', 'Den Helder', 'Texelhors', 'Berkhout', 'IJmuiden', 'Wijk aan Zee',
# 'Voorschoten', 'Rotterdam', 'Hoek van Holland', 'Wilhelminadorp', 'Vlissingen', 'Westdorpe',
# 'Woensdrecht', 'Volkel', 'Eindhoven', 'Ell', 'Arcen', 'Maastricht-Aachen Airport'
knmi_json_places = [
    'Den Helder', 'Vlissingen', 'De Bilt', 'Nieuw Beerta',
    'Terschelling', 'Leeuwarden', 'Twente', 'Wilhelminadorp',
    'Arcen', 'Eindhoven', 'Woensdrecht', 'Rotterdam',
    'Voorschoten', 'Berkhout', 'Hoogeveen', 'Maastricht-Aachen Airport'
]
knmi_json_cols = 4  # Colums for the data

# Dayvalues knmi
knmi_dayvalues_url = 'https://cdn.knmi.nl/knmi/map/page/klimatologie/gegevens/daggegevens/etmgeg_{0}.zip'
knmi_dayvalues_notification = 'SOURCE DATA: ROYAL NETHERLANDS METEOROLOGICAL INSTITUTE (KNMI)'
knmi_dayvalues_skip_header = 52
knmi_dayvalues_skip_footer = 0
knmi_dayvalues_dummy_val = 99999999
knmi_dayvalues_missing_val = '     '
knmi_dayvalues_delimiter = ','
knmi_dayvalues_info_txt = 'data/dayvalues/txt/dayvalues.txt'
# For 'rh', 'rhx', 'sq' sometimes value is -1, that means meaurement value is below 0.05.
# Give replacement value for -1 here
knmi_dayvalues_low_measure_val = 0.025
knmi_data_format = 'knmi'  # used for data format

################################################################################
# Buienradar JSON data url
buienradar_json_data = 'https://data.buienradar.nl/2.0/feed/json'
# Select places to show with actual measurements. -1 for all
buienradar_json_places = [
    'Leeuwarden', 'Vlissingen', 'De Bilt', 'Groningen',
    'Maastricht', 'Nieuw Beerta', 'Twente', 'Arnhem',
    'Arcen', 'Eindhoven', 'Woensdrecht', 'Rotterdam',
    'Voorschoten', 'Lelystad', 'Hoorn Terschelling', 'Berkhout'
]
#  Possible options for buienradar places
#  'Arcen', 'Arnhem', 'Berkhout', 'Cadzand', 'De Bilt', 'Eindhoven', 'Ell', 'Euro platform',
#  'Gilze Rijen', 'Goes', 'Groningen', 'Hansweert', 'Heino', 'Herwijnen', 'Hoek van Holland',
#  'Hoorn Terschelling', 'Houtribdijk', 'Huibertgat', 'IJmond', 'IJmuiden', 'LE Goeree',
#  'Leeuwarden', 'Lelystad', 'Lopik-Cabauw', 'Maastricht', 'Nieuw Beerta', 'Oosterschelde',
#  'Rotterdam', 'Rotterdam Geulhaven Schaar', 'Stavenisse', 'Stavoren', 'Texelhors', 'Tholen',
#  'Twente', 'Vlieland', 'Vlissingen', 'Volkel', 'Voorschoten', 'Westdorpe', 'Wijk aan Zee',
#  'Woensdrecht', 'Zeeplatform F-3', 'Zeeplatform K13'
buienradar_json_cols = 4  # Colums for the data


################################################################################
# Default cells for seasons (winter, summer and winter-summer), extremes and 
# climate and own default lists
################################################################################
# Abbreviations
# See for weather entities eg. tx, tn et cetera info-entities.txt
# info: information (eg. places, period), cnt: count(er)
# ave: average or mean, max: maximum extreme, min: minimum extreme
# ndx: indexex (eg. hellmann, frost-sum, heat-ndx)  
# ge: greather than and equal, gt: greater than, eq: equal, ne: not equal
# le: less than and equal, lt: less than
# day: dayvalue (to get the dayvalues)

# Options examples what can be shown
# Examples - info cells
# inf_copyright, inf_place, inf_province, inf_country, inf_period, inf_month, 
# inf_num, inf_period-2

# Examples normal statistics 
# ave_tg, sum_sq, sum_rh

# Examples extremes 
# max_tx, max_tg, max_tn, max_t10n, min_tx, min_tg, min_tn, 
# min_t10n, max_rh, max_sq, max_rhx, max_px, max_pn, min_px, min_pn, max_ux, 
# max_ug, max_un, min_ux, min_ug, min_un

# Examples indexes
# ndx_hellmann, ndx_ijnsen, ndx_frost-sum, ndx_heat-ndx

# Examples counters
# cnt_tx_ge_20, cnt_tx_ge_25, cnt_tx_ge_30, cnt_tx_ge_35, cnt_tx_ge_40, cnt_tg_ge_18, 
# cnt_tg_ge_20, cnt_sq_ge_10, cnt_rh_ge_10, cnt_tx_lt_0, cnt_tg_lt_0, cnt_tn_lt_0, 
# cnt_tn_lt_-5, cnt_tn_lt_-10, cnt_tn_lt_-15, cnt_tn_lt_-20

# Examples climates <beta>
# clima_ave_tg, clima_ave_tx, clima_ave_tn, clima_sum_sq, clima_sum_rh 

# Examples normal day values
# inf_num, inf_place, inf_province, inf_period, inf_day, 
# day_tx, day_tg, day_tn, day_t10n, day_sq, day_sp, day_rh, day_rhx,
# day_dr, day_pg, day_px, day_pn, day_ug, day_ux, day_un, day_ng, day_ddvec,
# day_fhvec, day_fg, day_fhx, day_fhn, day_fxx, day_vvx, day_vvn, day_q

# Menu default options lst 
# Default cells winter
lst_cells_winter = [
    'inf_place', 'inf_province', 'inf_period', 'ave_tg', 'clima_ave_tg', 
    'min_tx', 'min_tg', 'min_tn', 'min_t10n', 'ndx_hellmann', 'ndx_frost-sum', # 'ndx_ijnsen', 
    'sum_sq', 'clima_sum_sq', 'sum_rh', 'clima_sum_rh', 
    'cnt_tx_lt_0', 'cnt_tg_lt_0', 'cnt_tn_lt_0', 'cnt_tn_lt_-5', 
    'cnt_tn_lt_-10', 'cnt_tn_lt_-15', 'cnt_tn_lt_-20', 'cnt_rh_ge_10' 
]

# Default cells summer
lst_cells_summer = [ 
    'inf_place', 'inf_province', 'inf_period', 'ave_tg', 'clima_ave_tg', 
    'max_tx', 'max_tg', 'max_tn', 'ndx_heat-ndx', 
    'sum_sq', 'clima_sum_sq', 'sum_rh', 'clima_sum_rh', 
    'cnt_sq_ge_10', 'cnt_rh_ge_10',
    'cnt_tx_ge_25', 'cnt_tx_ge_30', 'cnt_tx_ge_35', 'cnt_tx_ge_40', 
    'cnt_tg_ge_18', 'cnt_tg_ge_20'
]

# Default cells winter and summer
lst_cells_winter_summer = [
    'inf_place', 'inf_province', 'inf_period', 'ave_tg', 'clima_ave_tg',
    'max_tx', 'max_tg', 'max_tn', 'ndx_heat-ndx', 
    'min_tx', 'min_tg', 'min_tn', 'min_t10n', 
    'ndx_hellmann', 'ndx_frost-sum', # 'ndx_ijnsen', 
    'sum_sq', 'sum_rh', 'cnt_sq_ge_10', 'cnt_rh_ge_10', 
    'cnt_tx_ge_20',  'cnt_tx_ge_25', 'cnt_tx_ge_30', 'cnt_tx_ge_35', 'cnt_tx_ge_40', 
    'cnt_tg_ge_18', 'cnt_tg_ge_20', 'cnt_tx_lt_0', 'cnt_tg_lt_0', 'cnt_tn_lt_0', 
    'cnt_tn_lt_-5', 'cnt_tn_lt_-10', 'cnt_tn_lt_-15', 'cnt_tn_lt_-20'
]

# My Default option 1, another option, will be in the menu option lst
lst_cells_my_default_1 = [ 
    'inf_place', 'inf_province', 'inf_period', 'ave_tg', 'clima_ave_tg', 
    'max_tx', 'max_tg', 'max_tn', 'max_t10n', 'max_fhx', 'max_px', 
    'sum_sq', 'clima_sum_sq', 'sum_rh', 'clima_sum_rh', 
    'min_tx', 'min_tg', 'min_tn', 'min_t10n', 'min_pn', 'min_un',
    'cnt_tx_ge_20', 'cnt_tn_lt_0'
]

# My Default option 2, another option, will be in the menu option lst
lst_cells_my_default_2 = [ 
    'inf_place', 'inf_province', 'inf_period', 'ave_tg', 'clima_ave_tg', 
    'max_tx', 'min_tn', 'sum_sq', 'clima_sum_sq', 'sum_rh', 'clima_sum_rh',
    'cnt_tx_ge_30', 'cnt_tx_lt_0', 'cnt_tn_lt_0'
]

# Example spring ?
lst_cells_spring = [ 
    'inf_place', 'inf_period', 'ave_tg', 'clima_ave_tg',  
    'max_tx', 'min_tx', 'max_tn', 'min_tn', 
    'ndx_heat-ndx', 'ndx_frost-sum', 'sum_sq', 'sum_rh', 
    'cnt_tx_>_20', 'cnt_tn_<_0', 'cnt_tn_<_-5'
]

# Default cells for the extrems
lst_cells_my_extremes = [
    'inf_place', 'inf_period', 
    'max_tx', 'max_tg', 'max_tn', 'max_t10n', 
    'min_tx', 'min_tg', 'min_tn', 'min_t10n',
    'max_rh', 'max_rhx','max_fg', 'max_fhx',  
    'max_px', 'max_pg', 'min_pg', 'min_pn', 
    'min_ux', 'min_ug', 'min_un', 
    'max_ev24', 'max_q'
]

# Default cells for to count days
lst_cells_my_counts = [
    'inf_place', 'inf_period', 
    'cnt_tx_ge_20', 'cnt_tx_ge_25', 'cnt_tx_ge_30', 'cnt_tx_ge_35', 
    'cnt_tx_ge_40', 'cnt_tg_ge_18', 'cnt_tg_ge_20', 
    'cnt_tx_lt_0', 'cnt_tg_lt_0', 'cnt_tn_lt_0', 'cnt_tn_lt_-5', 
    'cnt_tn_lt_-10', 'cnt_tn_lt_-15', 'cnt_tn_lt_-20'
]

# Default cells to show in search for days
lst_cells_s4d_default = [
    'inf_num', 'inf_place', 'inf_province', 'inf_period', 'inf_day', 
    'day_tx', 'day_tg', 'day_tn', 'day_t10n', 'day_sq', 'day_sp', 'day_rh', 'day_rhx',
    'day_dr', 'day_pg', 'day_px', 'day_pn', 'day_ug', 'day_ux', 'day_un', 'day_ng', 'day_ddvec',
    'day_fhvec', 'day_fg', 'day_fhx', 'day_fhn', 'day_fxx', 'day_vvx', 'day_vvn', 'day_q',
    'day_ev24'
]

# All the cells for making dayvalues
lst_cells_dayvalues = [
    'tx', 'tg', 'tn', 't10n', 'ddvec', 'fhvec', 'fg', 'fhx', 'fhn', 'fxx', 
    'sq', 'sp', 'rh', 'rhx',  'dr', 'px', 'pg', 'pn', 'ux', 'ug', 'un', 
    'vvx', 'vvn', 'ng', 'q', 'ev24'
]

################################################################################
# Download base urls for images 
# Base knmi download url for 10 min images 
knmi_base_url_act_img  = 'https://cdn.knmi.nl/knmi/map/page/weer/actueel-weer/'
# Base Weerplaza download url for 10 min images 
plaza_url_base_act_img = 'https://oud.weerplaza.nl/gdata/10min'

# KNMI download image urls 
knmi_url_windforce     = f'{knmi_base_url_act_img}windkracht.png'
knmi_url_windspeed     = f'{knmi_base_url_act_img}windsnelheid.png'
knmi_url_windmax       = f'{knmi_base_url_act_img}maxwindkm.png'
knmi_url_temperature   = f'{knmi_base_url_act_img}temperatuur.png'
knmi_url_rel_moist     = f'{knmi_base_url_act_img}relvocht.png'
knmi_url_view          = f'{knmi_base_url_act_img}zicht.png'
# Weerplaza download image urls 
plaza_url_temp_10cm    = f'{plaza_url_base_act_img}/GMT_T10C_latest.png'  # Temp 10cm
plaza_url_weerbeeld    = f'{plaza_url_base_act_img}/nl_10min.jpg'         # Weerbeeld
plaza_url_temp_2meter  = f'{plaza_url_base_act_img }/GMT_TTTT_latest.png' # Temp 2 meter

# Dowload url list
lst_weather_images_url = [
    knmi_url_windforce,
    knmi_url_windspeed,
    knmi_url_windmax,
    knmi_url_temperature,
    knmi_url_rel_moist,
    knmi_url_view, 
    plaza_url_temp_10cm, 
    plaza_url_weerbeeld, 
    plaza_url_temp_2meter
]

################################################################################
# Animation config
animation_time  = 0.5         # Default animation time zip for animations
animation_ext   = 'gif'       # Default Extension for animation. Do not change.
animation_name  = 'animation' # Default base-name for the animation file
# To use compress: programm gifsicle needs to be installed on your system
gif_compress    = True # Compress output animation gifs
# Delete the dowloaded images after the aniamtion is made 
remove_download = False

################################################################################
# Plotting default values
# Use of default values (below) ? Or add values at runtime ?
plot_default = 'y'
plot_show = 'n'  # Show the plot directly -> matplotlib.show(). yess (y) or no (n)
plot_tight_layout = 'y'  # Use of matplotlib.tight_layout(). yess (y) or no (n)
# Plot resolutions default.
# Example month -> width 1600 x height 900. More days may need more width
plot_width = 1280  # Width (px) plotted image
plot_height = 720  # Height (px) plotted image
# Images dpi (dots per inches) for printing on paper
plot_dpi = 100  # Higher will increase de point size. Make width/height higher too
plot_image_type = 'png'    # Default image type
plot_graph_type = 'line'   # bar or line
plot_line_width = 1       # Width line
plot_line_style = 'solid'  # Linestyle
plot_marker_size = 3       # Dot sizes
plot_marker_type = 'o'     # Type marker
plot_marker_txt = 'n'   # Markertext. yess (y) or no (n)
plot_cummul_val = 'n'      # Cummulative values. yess (y) or no (n)
# Adding climate averages to plot. yess (y) or no (n)
plot_climate_ave = 'n'
plot_climate_marker_txt = 'n'  # Adding markers next to the climate markers..
# Adding climate min, max and averages to plot. yess (y) or no (n)
plot_min_max_ave_period = 'y'
plot_clima_line_style = 'dotted'
plot_clima_line_width = 1
plot_clima_marker_type = '.'
plot_clima_marker_size = 2
plot_xas_rotation = 60

# Base Style Plotting
# 'bmh', 'classic', 'dark_background', 'fast', 'fivethirtyeight',
# 'ggplot', 'grayscale', 'seaborn-bright', 'seaborn-colorblind',
# 'seaborn-dark-palette', 'seaborn-dark', 'seaborn-darkgrid',
# 'seaborn-deep', 'seaborn-muted', 'seaborn-notebook', 'seaborn-paper',
# 'seaborn-pastel', 'seaborn-poster', 'seaborn-talk', 'seaborn-ticks',
# 'seaborn-white', 'seaborn-whitegrid', 'seaborn', 'Solarize_Light2',
# 'tableau-colorblind10'
# 'fivethirtyeight', set to False for no default styling
plt_style = 'fivethirtyeight'

# Fonts
# http://jonathansoma.com/lede/data-studio/matplotlib/list-all-fonts-available-in-matplotlib-plus-samples/1

# Style for marker texts
plot_marker_color = '#333333'
plot_marker_font = {'family': 'DejaVu Sans',
                    'weight': 'normal',
                    'size': 'small',
                    'variant': 'small-caps'
                    }
plot_marker_horizontalalignment = 'center'
plot_marker_verticalalignment = 'top'
plot_marker_alpha = 0.9

# Style for added texts (extremes, min, max mean)
plot_add_txt_font = {'family': 'monospace',
                     'weight': 'normal',
                     'style': 'normal',
                     'size': '9',
                     'variant': 'normal'}

# Style grid in plot
plot_grid_on = True  # True for a grid or False for no grid
plot_grid_color = '#cccccc'
plot_grid_linestyle = 'dotted'
plot_grid_linewidth = 1

# Style titel
plot_title_color = '#333333'
plot_title_font = {'family': 'DejaVu Sans',
                   'weight': 'bold',
                   'size': '14',
                   'variant': 'normal'}
# Style xlabel
plot_xlabel_text = 'DATES'
plot_xlabel_color = '#555555'
plot_xlabel_font = {'family': 'monospace',
                    'weight': 'normal',
                    'size': '10',
                    'variant': 'small-caps'}

# Style values/dates on the x-as
plot_xas_color = '#555555'
plot_xas_font = {'family': 'monospace',
                 'weight': 'normal',
                 'size': '9',
                 'variant': 'normal'}

# Style ylabel
plot_ylabel_color = '#555555'
plot_ylabel_font = {'family': 'monospace',
                    'weight': 'normal',
                    'size': '11',
                    'variant': 'small-caps'}

# Style values/dates on the y-as
plot_yas_color = '#555555'
plot_yas_font = {'family': 'monospace',
                 'weight': 'normal',
                 'size': '9',
                 'variant': 'small-caps'}

# Style legend
plot_legend_font = {'family': 'DejaVu Sans',
                    'weight': 'normal',
                    'style': 'normal',
                    'size': '9',
                    'variant': 'normal'}  # Does not work

plot_legend_loc = 'upper right'
plot_legend_facecolor = None
plot_legend_shadow = None
plot_legend_frameon = None
plot_legend_fancybox = None

################################################################################
# Constants do not change
data_comment_sign = '#'
data_dtype = np.float64  # Data type for reading data files
data_min_year = 1901  # Minumum year of possible data
np_empthy = np.array([[]])
np_no_data = np.array([[]])
no_data_given = '.'
data_empthy = ''
txt_no_data = '.'
txt_data_error = 'x'
no_val = '.'  # Replacement for no output
empthy = '.'

# Descending min or max
html_max = True
html_min = False

fl_max = sys.float_info.min  # Minimum possible value
fl_min = sys.float_info.max  # Maximum possible value

# Give language for app. Under contruction. TODO
# 'NL' for Netherlands/Dutch, 'EN' for English, Default is English
lang = 'EN' # Select language. Only english
translate = False # Translation active or not

# No download flooding from a server.
# Time to wait after downloading a file. Always min = 0.2 seconds
download_interval_time = 0.3 # Seconds.
download_max_num = 10000 # Max number downloads, flood protection

# The webpage/ip for checking an internet connection
check_ip_1 = '42.251.36.14' # google.com
check_ip_2 = '95.101.74.93' # NU.nl
check_ip_3 = '1.1.1.1' 
check_ip_4 = '8.8.8.8' 
check_port_80  = 80
check_port_ssl = 443
check_port_dns = 53
check_timeout = 500 # Milli secs

################################################################################
# Vars below do not change
hour_day     =  24
day_week     =   7
sec_minute   =  60
sec_hour     =  sec_minute * sec_minute
sec_day      =  hour_day * sec_hour
sec_week     =  day_week * sec_day
hour_minute  =  sec_minute
day_minute   =  hour_day * hour_minute

# Startup time for running this app (!more or less)
app_start_time = time.time() 

# Copyright notification weatherstats 
created_by_notification = 'Created by weatherstats-nl at %s' 
