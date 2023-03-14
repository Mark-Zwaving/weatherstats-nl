# -*- coding: utf-8 -*-
'''HTML awesome icons'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 3 - GPLv3'
__version__    =  '0.0.5'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

def i(icon='', color='', extra='', size=''):
    klass  = icon
    klass += f' {color}' if color else ''
    klass += f' {extra}' if extra else ''
    klass += f' {size}'  if size  else ''

    return f'<i class="{klass}"></i>'

def home(color='', extra='', size=''): return i('fas fa-home', color, extra, size)
def flag(color='', extra='', size=''): return i('fab fa-font-awesome-flag', color, extra, size)
def fire(color='', extra='', size=''): return i('fas fa-fire-alt', color, extra, size)
def cal_period(color='', extra='', size=''): return i('far fa-calendar-alt', color, extra, size)
def cal_day(color='', extra='', size=''): return i('fas fa-calendar-day', color, extra, size)
def sun(color='', extra='', size=''): return i('fas fa-sun', color, extra, size)
def temp_full(color='', extra='', size=''): return i('fas fa-thermometer-full', color, extra, size)
def temp_half(color='', extra='', size=''): return i('fas fa-thermometer-half', color, extra, size)
def temp_empty(color='', extra='', size=''): return i('fas fa-thermometer-empty', color, extra, size)
def wind(color='', extra='', size=''): return i('fas fa-wind', color, extra, size)
def wind_dir(color='', extra='', size=''): return i('fas fa-location-arrow', color, extra, size)
def shower_heavy(color='', extra='', size=''): return i('fas fa-cloud-showers-heavy', color, extra, size)
def compress(color='', extra='', size=''): return i('fas fa-compress', color, extra, size)
def compress_alt(color='', extra='', size=''): return i('fas fa-compress-arrows-alt', color, extra, size)
def cloud(color='', extra='', size=''): return i('fas fa-cloud', color, extra, size)
def drop_tint(color='', extra='', size=''): return i('fas fa-tint', color, extra, size)
def eye(color='', extra='', size=''): return i('fas fa-eye', color, extra, size)
def radiation(color='', extra='', size=''): return i('fas fa-radiation-alt', color, extra, size)
def umbrella(color='', extra='', size=''): return i('fas fa-umbrella', color, extra, size)
def sweat(color='', extra='', size=''): return i('far fa-grin-beam-sweat', color, extra, size)
def icicles(color='', extra='', size=''): return i('fas fa-icicles', color, extra, size)
def calculator(color='', extra='', size=''): return i('fas fa-calculator', color, extra, size)
def weather_all(color='', extra='', size=''): return i('fas fa-cloud-sun-rain', color, extra, size)
def ge(color='', extra='', size=''): return i('fas fa-greater-than-equal', color, extra, size)
def gt(color='', extra='', size=''): return i('fas fa-greater-than', color, extra, size)
def le(color='', extra='', size=''): return i('fas fa-less-than-equal', color, extra, size)
def lt(color='', extra='', size=''): return i('fas fa-less-than', color, extra, size)
def arrow_loc(color='', extra='', size=''): return i('fas fa-location-arrow', color, extra, size)
def arrow_up(color='', extra='', size=''): return i('fas fa-arrow-up', color, extra, size)
def arrow_left(color='', extra='', size=''): return i('fas fa-arrow-left', color, extra, size)
def arrow_down(color='', extra='', size=''): return i('fas fa-arrow-down', color, extra, size)
def arrow_right(color='', extra='', size=''): return i('fas fas fa-arrow-right', color, extra, size)
def binoculars(color='', extra='', size=''): return i('fas fa-binoculars', color, extra, size)
def day(color='', extra='', size=''): return i('fas fa-calendar-day', color, extra, size)

def minus(color='', extra='', size=''): return i('fas fa-minus', color, extra, size)
def plus(color='', extra='', size=''): return i('fas fa-plus', color, extra, size)
def wave_square(color='', extra='', size=''): return i('fas fa-wave-square', color, extra, size)

def copy(color='', extra='', size=''): return i('fas fa-copyright', color, extra, size)
def copy_light(color='', extra='', size=''): return i('far fa-copyright', color, extra, size)

def sort_down(color='', extra='', size=''): return i('fas fa-sort-amount-down-alt', color, extra, size)

def bars(color='', extra='', size=''): return i('fas fa-bars', color, extra, size)
def ellipsis(color='', extra='', size=''): return i('fas fa-ellipsis-v', color, extra, size)
# def ellipsis_alt(color='', extra='', size=''): return i('fas fa-ellipsis-v-alt', color, extra, size)
