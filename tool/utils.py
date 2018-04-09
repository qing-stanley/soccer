# -*- coding: utf-8 -*-

import logging

# Logger
def init_logger(name, debug=True):

    format_log  = '[%(name)s] [%(asctime)s] [%(levelname)s] %(message)s'
    format_date = '%Y-%m-%d %H:%M:%S'

    logger    = logging.getLogger(name)
    handler   = logging.StreamHandler() # sys.stderr
    formatter = logging.Formatter(fmt=format_log, datefmt=format_date)

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # DEBUG < INFO < WARNING < ERROR
    if debug:
        logger.setLevel(logging.DEBUG) 
    else:
        logger.setLevel(logging.INFO)

    return logger

