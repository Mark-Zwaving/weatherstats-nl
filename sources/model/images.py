'''Library has functions for ahandling functions'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.0.3'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'
import config as cfg
import sources.control.fio as fio
import sources.model.utils as utils
import sources.view.console as cnsl
import sources.view.text as text
import sources.model.ymd as ymd
import shutil, os

def compress_gif(
        path, # Name of image to compress
        verbose=cfg.verbose
    ):
    '''Function compressess a gif image.
       Python libraries used: pygifsicle, imageio
       Install command imageio: python3 -m pip install imageio
       Install command: python3 -m pip install pygifsicle
       Application gifsicle is needed for the compression of a gif-image
       Instal gifsicle on your OS too
       Example linux debian: install command: sudo apt-get install gifsicle
    '''
    ok = False
    cnsl.log( text.head('Start compress file' ), verbose)
    cnsl.log( f'[{ymd.now()}] File: {utils.str_max(path)}', verbose )
    cnsl.log( f'[{ymd.now()}] Compressed file {cfg.copy_compressed}', verbose )

    if os.path.isfile( path ): 
        try: # Check for pygifsicle
            import pygifsicle 
        except:
            cnsl.log('Python library pygifsicle is not installed', True)
            cnsl.log('Install library with command: python3 -m pip install pygifsicle', True)
            cnsl.log('Install on your os the following programm: gifsicle', True)
            cnsl.log('Example install on debian: sudo apt-get install gifsicle', True)
        else:
            path_copy = path.replace(cfg.animation_ext, '') # Remove .gif
            path_copy = f'{path}-compressed.{cfg.animation_ext}' # Name for a copy file 
            shutil.copyfile( path, path_copy )   # Copy the original file to a copy file
            try:
                pygifsicle.optimize( path_copy ) # Compress the copy file
            except Exception as e:
                cnsl.log( f'Error in images compress_gif()\n{e}', cfg.error )
                fio.delete( path_copy, verbose=False ) # Remove the copy  
            else:
                ok = True  # All went well 
                if not cfg.copy_compressed:  # Replace original with the compressed file 
                    fio.delete( path, verbose=False ) # Remove the original uncompressed animation file 
                    shutil.copyfile( path_copy, path )  # Copy the compressed copy to the real animation file 
                    fio.delete( path_copy, verbose=False ) # Remove the double compressed copy

                cnsl.log( f'[{ymd.now()}] Compress successful', verbose ) 
    else:
        cnsl.log(f'[{ymd.now()}] Path {path} is not a file', verbose) 

    cnsl.log(text.foot('End compress file'), verbose ) 

    return ok