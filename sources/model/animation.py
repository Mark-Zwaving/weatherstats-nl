# -*- coding: utf-8 -*-
'''Library contains functions for converting elements'''
__author__     = 'Mark Zwaving'
__email__      = 'markzwaving@gmail.com'
__copyright__  = 'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    = '0.1.1'
__maintainer__ = 'Mark Zwaving'
__status__     = 'Development'

import config as cfg
import sources.control.fio as fio
import sources.model.ymd as ymd
import sources.model.utils as utils
import sources.view.console as cnsl
import sources.view.text as text
import os, imageio

# Function creates an image animation
def create(
        path,          # File name for the animation image
        lst_images,    # List with all the images for the animation
        animation_time = cfg.animation_time, # Interval time for the image
        verbose        = cfg.verbose # Show output on screen
    ):
    '''Function create an anmiation file, using imageio'''
    ok = False
    cnsl.log(text.head(f'Start make animation'), verbose)
    cnsl.log(f'[{ymd.now()}] Animation file: {utils.str_max(path)}', verbose)
    cnsl.log(f'[{ymd.now()}] Animation interval: {animation_time} seconds', verbose)

    # if there are images
    if len(lst_images) > 0:
        # Always make animation path before saving
        animation_map = os.path.dirname(path)
        ok = fio.mk_dir(animation_map, False) 
        if ok:
            # Read imageio data in data lst from paths list
            try: 
                lst_data = [imageio.imread(img) for img in lst_images if os.path.exists(img)]
                imageio.mimsave(
                    # Result animation file
                    path,
                    # Images data list for animation
                    lst_data,
                    # Animation time
                    duration=animation_time ) 
            except Exception as e:
                cnsl.log(f'Error in animation create()\n{e}', cfg.error)
            else:
                cnsl.log('Make animation successful', verbose)
                ok = True
    else:
        cnsl.log('No images given to create an animation.', verbose)

    cnsl.log(text.foot('End make animation'), verbose)

    return ok, path
