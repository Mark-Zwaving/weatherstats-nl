# -*- coding: utf-8 -*-
'''Library contain functions to make the footer for a 2d matrix table.'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU General Public License version 2 - GPLv2'
__version__    =  '0.0.3'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import sources.view.text as text

def row(options):
    '''Makes the footer'''
    foot_htm, foot_txt, foot_csv, ftyp = cfg.e, cfg.e, cfg.e, options[text.ask_file_type]

    if ftyp in text.lst_output_htm:
        foot_htm += f'''
        </tbody><tfoot>
        <tr><td class="text-muted" colspan="{options[text.ask_colspan]}">
        <small> {text.create_by_notification_html().replace("<br>", " ")} </small>
        </td></tr>
        </tfoot></table>'''

    if ftyp in text.lst_output_txt_cnsl:
        foot_txt += cfg.knmi_dayvalues_notification

    return foot_htm, foot_txt, foot_csv