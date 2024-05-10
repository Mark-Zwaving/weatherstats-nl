# -*- coding: utf-8 -*-
'''Library contains configuration options and a list with knmi stations'''
__author__     = 'Mark Zwaving'
__email__      = 'markzwaving@gmail.com'
__copyright__  = 'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    = '0.1.4' 
__maintainer__ = 'Mark Zwaving'
__status__     = 'Development'

################################################################################
import os, sys, time, numpy as np  # Python modules
################################################################################

verbose = False  # Print more(all) to screen
error   = False  # Print exceptions and errors to screen
info    = True   # Show examples and help info in menu by default
console = True   # Show always the calculated tables in the console 
log     = False  # Log to file 

# The <default> years/period for the calculations of climate averages
climate_start_year = 1991
climate_end_year   = 2020

# Debug. Set true to see it all
# If true: verbose, error, info and console will all be set to true
debug = False 

# TODO: To automatic save the console output in an text file 
# to map: data/console/
# save_text = False 

# To save the current weather and forecasts in the data/forecasts map,
# set save_forecasts to true else False
save_forecasts = True 

# Default output type file. Options: html, text and cmd
# cmd is output to screen only. Text en html writes texts/html files
default_output = 'html'

# Set the time zone
timezone = 'Europe/Amsterdam'  

# csv separator
csv_sep  = ';'

# Spacer tab menu
spacer = '   '

################################################################################
# For HTML pages
# Add popup tables in html tables. True for yes, False for no
html_popup_table_show = True
# Give a max number for rows html popup table else html pages can become very large
html_popup_table_max_rows = 15  # -1 for all rows
# Remove whitespace from html pages source code
html_strip = True

################################################################################
# Config base maps
dir_app            = os.path.abspath(os.path.dirname(__file__))
dir_data           = os.path.join(dir_app,  'data')
dir_templates      = os.path.join(dir_data, 'templates')
dir_templates_htm  = os.path.join(dir_templates, 'html')
dir_templates_sql  = os.path.join(dir_templates, 'sql')
dir_forecasts      = os.path.join(dir_data, 'forecasts')  # Downloaded forecasts
dir_thirdparty     = os.path.join(dir_data, 'thirdparty') 
dir_graphs         = os.path.join(dir_data, 'graphs')
dir_download       = os.path.join(dir_data, 'downloads')
dir_animation      = os.path.join(dir_data, 'animations')
dir_sqlite         = os.path.join(dir_data, 'sqlite')
dir_dayvalues      = os.path.join(dir_data, 'dayvalues') # Dayvalues
dir_dayvalues_zip  = os.path.join(dir_dayvalues, 'zip')  # knmi zip files
dir_dayvalues_txt  = os.path.join(dir_dayvalues, 'txt')  # knmi text files
dir_dayvalues_htm  = os.path.join(dir_dayvalues, 'html') # knmi html files from text
dir_statistics     = os.path.join(dir_data, 'statistics')
dir_stats_htm      = os.path.join(dir_statistics, 'html')
dir_stats_txt      = os.path.join(dir_statistics, 'text')
dir_stats_cnsl     = os.path.join(dir_statistics, 'console')
dir_stats_csv      = os.path.join(dir_statistics, 'csv')
dir_stats_excel    = os.path.join(dir_statistics, 'excel')

# Paths templates
html_template_dayvalues  = os.path.join(dir_templates_htm, 'dayvalues.html')
html_template_statistics = os.path.join(dir_templates_htm, 'statistics.html')


# How many dir up is the html root, in the data/statistics map ?
# Define paths to css, img and js files in the created html-files.  
# Example statistics html: /WMO/YYYY/MM/DD/statistics-x-x.html
# Always 3 times map up: year, month and day
# The same for the daydavalues html: /WMO/YYYY/MM
path_to_html_root = './../../../' 

# How many dirs up is the thirdparty map ?
# Define path to thirdsparty software ysed for references in the created html files
# E.g: ./statistics/html/yyyy/mm/dd/ (=5x up)
# E.g: ./dayvalues/html/wmo/yyyy/mm/ (=5x up).  
# Dayvalues en statistics maps normally are alway the same
path_to_thirdparty = './../../../../../' 

# Path database TODO maybe later
db_dayvalues = os.path.join(dir_sqlite, 'weatherstats.db')

# Webserver 
webserver = False  # Set to true to save the html files to a (local) webserver 
dir_web = '/var/www/html/weatherstats.nl' # Enter a map for a webserver
# ! If webserver set to True. 
# Do not forget to copy/move the whole thirdparty directory (with bootstrap, js-files et cet.) 
# to your webserver directory too.
# For statistics (html)
#  - Copy the css, img en js maps in the data/statistics map 
#    to the statistics map on the webserver (eg: /var/www/html/weatherstats/statististics)
# For dayvalues (html)
#  - Copy the css, img en js maps and the files index.html and dummy.html 
#    to the dayvalues map on the webserver.
#    (eg: /var/www/html/weatherstats/dayvalues)
#    In the html files update the relatieve paths to the thirdparty maps

if webserver: # Oké, let's save the html files on the webserver
    dir_www = os.path.abspath(dir_web) 
    dir_dayvalues_htm = os.path.join(dir_www, 'dayvalues') # knmi html files from text
    dir_stats_htm  = os.path.join(dir_www, 'statistics')
    dir_thirdparty = os.path.join(dir_www, 'thirdparty')
    # Note html map on the webserver is skipped
    path_to_thirdparty = './../../../../' # 4xup

################################################################################
# KNMI Weather
knmi_ftp_pub               = 'ftp://ftp.knmi.nl/pub_weerberichten/'
knmi_forecast_global_url   = f'{knmi_ftp_pub}basisverwachting.txt'
knmi_forecast_model_url    = f'{knmi_ftp_pub}guidance_meerdaagse.txt'
knmi_forecast_guidance_url = f'{knmi_ftp_pub}guidance_modelbeoordeling.txt'

# JSON url 10 minute values
knmi_json_data_10min       = 'ftp://ftp.knmi.nl/pub_weerberichten/tabel_10Min_data.json'

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
knmi_dayvalues_url          = 'https://cdn.knmi.nl/knmi/map/page/klimatologie/gegevens/daggegevens/etmgeg_{0}.zip'
knmi_dayvalues_notification = 'SOURCE DATA: ROYAL NETHERLANDS METEOROLOGICAL INSTITUTE (KNMI)'
knmi_dayvalues_skip_header  = 52
knmi_dayvalues_skip_footer  = 0
knmi_dayvalues_dummy_val    = 99999999
knmi_dayvalues_missing_val  = '     '
knmi_dayvalues_delimiter    = ','
knmi_dayvalues_info_txt     = 'data/dayvalues/txt/dayvalues.txt'
# For 'rh', 'rhx', 'sq' sometimes value is -1, that means meaurement value is below 0.05.
# Give replacement value for -1 here
knmi_dayvalues_low_measure_val = 0.025
knmi_data_format            = 'knmi'  # used for data format

################################################################################
# Buienradar JSON data url
buienradar_json_data   = 'https://data.buienradar.nl/2.0/feed/json'
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
gif_compress    = False       # Compress output animation gifs
copy_compressed = False       # When compress is true keep a copy for the compressed file
remove_download = False       # Delete the dowloaded images after the aniamtion is made 

################################################################################
# Plotting default values
# Use of default values (below) ? Or add values at runtime ?
plot_default = 'y'
plot_show = 'n'  # Show the graph directly after it is made. yess (y) or no (n)
plot_tight_layout = 'y'  # Use of matplotlib.tight_layout(). yess (y) or no (n)
# Plot resolutions default.
# Example month -> width 1600 x height 900. More days may need more width
plot_width = 1280  # Width (px) plotted image
plot_height = 720  # Height (px) plotted image
# Images dpi (dots per inches) for printing on paper
plot_dpi = 100  # Higher will increase de point size. Make width/height higher too
plot_image_type  = 'png'    # Default image type
plot_graph_type  = 'line'   # bar or line
plot_line_width  = 1        # Width line
plot_line_style  = 'solid'  # Linestyle
plot_marker_size = 3        # Dot sizes
plot_marker_type = 'o'      # Type marker
plot_marker_txt  = 'n'      # Markertext. yess (y) or no (n)
plot_cummul_val  = 'n'      # Cummulative values. yess (y) or no (n)
# Adding climate averages to plot. yess (y) or no (n)
plot_climate_ave = 'n'
plot_climate_marker_txt = 'n'  # Adding markers next to the climate markers..
# Adding climate min, max and averages to plot. yess (y) or no (n)
plot_min_max_ave_period = 'n'
plot_clima_line_style   = 'dotted'
plot_clima_line_width   =  1
plot_clima_marker_type  = '.'
plot_clima_marker_size  =  2
plot_xas_rotation       = 60

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
plot_marker_font  = { 'family': 'DejaVu Sans',
                      'weight': 'normal',
                      'size': 'small',
                      'variant': 'small-caps' }
plot_marker_horizontalalignment = 'center'
plot_marker_verticalalignment   = 'top'
plot_marker_alpha = 0.9

# Style for added texts (extremes, min, max mean)
plot_add_txt_font = { 'family': 'monospace',
                      'weight': 'normal',
                      'style': 'italic',
                      'size': '9',
                      'variant': 'normal' }

# Style grid in plot
plot_grid_on        = True  # True for a grid or False for no grid
plot_grid_color     = '#cccccc'
plot_grid_linestyle = 'dotted'
plot_grid_linewidth = 1

# Style titel
plot_title_color = '#333333'
plot_title_font  = { 'family': 'DejaVu Sans',
                     'weight': 'bold',
                     'size': '14',
                     'variant': 'normal' }
# Style xlabel
plot_xlabel_text  = 'DATES'
plot_xlabel_color = '#555555'
plot_xlabel_font  = { 'family': 'monospace',
                      'weight': 'normal',
                      'size': '10',
                      'variant': 'small-caps' }

# Style values/dates on the x-as
plot_xas_color = '#555555'
plot_xas_font  = { 'family': 'monospace',
                   'weight': 'normal',
                   'size': '9',
                   'variant': 'normal' }

# Style ylabel
plot_ylabel_color = '#555555'
plot_ylabel_font  = { 'family': 'monospace',
                      'weight': 'normal',
                      'size': '11',
                      'variant': 'small-caps' }

# Style values/dates on the y-as
plot_yas_color = '#555555'
plot_yas_font  = { 'family': 'monospace',
                   'weight': 'normal',
                   'size': '9',
                   'variant': 'small-caps' }

# Style legend
plot_legend_font = { 'family': 'DejaVu Sans',
                     'weight': 'normal',
                     'style': 'normal',
                     'size': '9',
                     'variant': 'normal' }  # Does not work

plot_legend_loc       = 'upper right'
plot_legend_facecolor = None
plot_legend_shadow    = None
plot_legend_frameon   = None
plot_legend_fancybox  = None

################################################################################
# Constants do not change
data_comment_sign = '#'
data_dtype     = np.float64  # Data type for reading data files
data_min_year  = 1901  # Minumum year of possible data
np_empthy_1d   = np.array([])
np_empthy_2d   = np.array([[]])
nv = no_val    = '.'  # Replacement for no output
txt_data_error = 'x' 
date_false     = -1 
T = True
F = False
e = empthy = ''  # Empthy false var
ln = '\n' # A system specific text enter character

# Descending min or max
html_max = True
html_min = False

fl_max = sys.float_info.min  # Minimum possible value
fl_min = sys.float_info.max  # Maximum possible value

# Give language for app. Under contruction. TODO
# 'NL' for Netherlands/Dutch, 'EN' for English, Default is English
lang      = 'EN'  # Select language. Only english
translate = False # Translation active or not

# No download flooding from a server.
# Time to wait after downloading a file. Always min = 0.2 seconds
download_flood_protection_active = True
download_interval_time = 0.1 # Seconds.
download_max_num = 10000 # Max number downloads, flood protection

# The webpage/ip for checking an internet connection
check_ip_1     = '42.251.36.14'  # google.com
check_ip_2     = '95.101.74.93'  # NU.nl
check_ip_3     = '1.1.1.1' 
check_ip_4     = '8.8.8.8' 
check_port_80  = 80
check_port_ssl = 443
check_port_dns = 53
check_timeout  = 500 # Milli secs

################################################################################
################################################################################
# Vars below do not change
hour_day        = 24
day_week        =  7
sec_minute      = 60
sec_hour        = sec_minute * sec_minute
sec_day         = hour_day * sec_hour
sec_week        = day_week * sec_day
hour_minute     = sec_minute
day_minute      = hour_day * hour_minute
sec_nano        = 1000000000
sec_nano_hour   = sec_hour * sec_nano
sec_nano_day    = sec_day * sec_nano
sec_nano_week   = sec_week * sec_nano 
sec_nano_minute = sec_minute * sec_nano 

 # Separator for the statistics cell entities
cells_separator = '_' 

# Set all tor True
if debug:
    verbose = error = console = info = True

# Database
connect_db = False

climate_period = f'{climate_start_year}-{climate_end_year}'

# Startup time for running this app (!more or less)
app_start_time = time.time() 

lst_forbidden_file_chars = ['"',"'",'\\','`','*','{','}','[',']','(',')','>','<','#','+','.','!','$','\'']

# Copyright notification weatherstats 
created_by_notification = 'Created by weatherstats-nl at %s' 
created_by_notification_html = '''
    Created by <a href="https://github.com/Mark-Zwaving/weatherstats-nl" target="_blank">weatherstats-nl</a> at %s
'''
  