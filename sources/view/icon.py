# -*- coding: utf-8 -*-
'''HTML awesome icons'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 3 - GPLv3'
__version__    =  '0.0.8'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg

def i(icon=cfg.e, color=cfg.e, extra=cfg.e, size=cfg.e):
    klass  = icon
    klass += f' {color}' if color else cfg.e
    klass += f' {extra}' if extra else cfg.e
    klass += f' {size}'  if size  else cfg.e

    return f'<i class="{klass}"></i>'

def home(color=cfg.e, extra=cfg.e, size=cfg.e): return i('fas fa-home', color, extra, size)
def flag(color=cfg.e, extra=cfg.e, size=cfg.e): return i('fab fa-font-awesome-flag', color, extra, size)
def fire(color=cfg.e, extra=cfg.e, size=cfg.e): return i('fas fa-fire-alt', color, extra, size)
def cal_period(color=cfg.e, extra=cfg.e, size=cfg.e): return i('far fa-calendar-alt', color, extra, size)
def cal_day(color=cfg.e, extra=cfg.e, size=cfg.e): return i('fas fa-calendar-day', color, extra, size)
def sun(color=cfg.e, extra=cfg.e, size=cfg.e): return i('fas fa-sun', color, extra, size)
def temp_full(color=cfg.e, extra=cfg.e, size=cfg.e): return i('fas fa-thermometer-full', color, extra, size)
def temp_half(color=cfg.e, extra=cfg.e, size=cfg.e): return i('fas fa-thermometer-half', color, extra, size)
def temp_empty(color=cfg.e, extra=cfg.e, size=cfg.e): return i('fas fa-thermometer-empty', color, extra, size)
def wind(color=cfg.e, extra=cfg.e, size=cfg.e): return i('fas fa-wind', color, extra, size)
def wind_dir(color=cfg.e, extra=cfg.e, size=cfg.e): return i('fas fa-location-arrow', color, extra, size)
def shower_heavy(color=cfg.e, extra=cfg.e, size=cfg.e): return i('fas fa-cloud-showers-heavy', color, extra, size)
def compress(color=cfg.e, extra=cfg.e, size=cfg.e): return i('fas fa-compress', color, extra, size)
def compress_alt(color=cfg.e, extra=cfg.e, size=cfg.e): return i('fas fa-compress-arrows-alt', color, extra, size)
def cloud(color=cfg.e, extra=cfg.e, size=cfg.e): return i('fas fa-cloud', color, extra, size)
def drop_tint(color=cfg.e, extra=cfg.e, size=cfg.e): return i('fas fa-tint', color, extra, size)
def eye(color=cfg.e, extra=cfg.e, size=cfg.e): return i('fas fa-eye', color, extra, size)
def radiation(color=cfg.e, extra=cfg.e, size=cfg.e): return i('fas fa-radiation-alt', color, extra, size)
def umbrella(color=cfg.e, extra=cfg.e, size=cfg.e): return i('fas fa-umbrella', color, extra, size)
def sweat(color=cfg.e, extra=cfg.e, size=cfg.e): return i('far fa-grin-beam-sweat', color, extra, size)
def icicles(color=cfg.e, extra=cfg.e, size=cfg.e): return i('fas fa-icicles', color, extra, size)
def calculator(color=cfg.e, extra=cfg.e, size=cfg.e): return i('fas fa-calculator', color, extra, size)
def weather_all(color=cfg.e, extra=cfg.e, size=cfg.e): return i('fas fa-cloud-sun-rain', color, extra, size)
def ge(color=cfg.e, extra=cfg.e, size=cfg.e): return i('fas fa-greater-than-equal', color, extra, size)
def gt(color=cfg.e, extra=cfg.e, size=cfg.e): return i('fas fa-greater-than', color, extra, size)
def le(color=cfg.e, extra=cfg.e, size=cfg.e): return i('fas fa-less-than-equal', color, extra, size)
def lt(color=cfg.e, extra=cfg.e, size=cfg.e): return i('fas fa-less-than', color, extra, size)
def arrow_loc(color=cfg.e, extra=cfg.e, size=cfg.e): return i('fas fa-location-arrow', color, extra, size)
def arrow_up(color=cfg.e, extra=cfg.e, size=cfg.e): return i('fas fa-arrow-up', color, extra, size)
def arrow_left(color=cfg.e, extra=cfg.e, size=cfg.e): return i('fas fa-arrow-left', color, extra, size)
def arrow_down(color=cfg.e, extra=cfg.e, size=cfg.e): return i('fas fa-arrow-down', color, extra, size)
def arrow_right(color=cfg.e, extra=cfg.e, size=cfg.e): return i('fas fas fa-arrow-right', color, extra, size)
def binoculars(color=cfg.e, extra=cfg.e, size=cfg.e): return i('fas fa-binoculars', color, extra, size)
def day(color=cfg.e, extra=cfg.e, size=cfg.e): return i('fas fa-calendar-day', color, extra, size)
def minus(color=cfg.e, extra=cfg.e, size=cfg.e): return i('fas fa-minus', color, extra, size)
def plus(color=cfg.e, extra=cfg.e, size=cfg.e): return i('fas fa-plus', color, extra, size)
def wave_square(color=cfg.e, extra=cfg.e, size=cfg.e): return i('fas fa-wave-square', color, extra, size)
def copy(color=cfg.e, extra=cfg.e, size=cfg.e): return i('fas fa-copyright', color, extra, size)
def copy_light(color=cfg.e, extra=cfg.e, size=cfg.e): return i('far fa-copyright', color, extra, size)
def sort_down(color=cfg.e, extra=cfg.e, size=cfg.e): return i('fas fa-sort-amount-down-alt', color, extra, size)
def bars(color=cfg.e, extra=cfg.e, size=cfg.e): return i('fas fa-bars', color, extra, size)
def ellipsis(color=cfg.e, extra=cfg.e, size=cfg.e): return i('fas fa-ellipsis-v', color, extra, size)
# def ellipsis_alt(color=cfg.e, extra=cfg.e, size=cfg.e): return i('fas fa-ellipsis-v-alt', color, extra, size)
