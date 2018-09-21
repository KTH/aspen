__author__ = 'tinglev'

import os
import coloredlogs

def init_logging():
    field_style_override = coloredlogs.DEFAULT_FIELD_STYLES
    level_style_override = coloredlogs.DEFAULT_LEVEL_STYLES
    logging_level = 'INFO'
    if 'DEBUG' in os.environ:
        logging_level = 'DEBUG'
    field_style_override['levelname'] = {"color": "magenta", "bold": True}
    level_style_override['debug'] = {'color': 'blue'}
    coloredlogs.install(level=logging_level,
                        fmt='%(asctime)s %(name)s %(levelname)s %(message)s',
                        level_styles=level_style_override,
                        field_styles=field_style_override)
