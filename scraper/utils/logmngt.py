import logging
import sys

def get_logger(name, cfg):
    name = name.ljust(8)
    if logging.getLogger(name).hasHandlers():
        return logging.getLogger(name)
    logger = logging.getLogger(name)
    level_name = 'INFO'
    if name in cfg and 'loglevel' in cfg[name]:
        level_name = cfg[name]['loglevel']
    elif 'loglevel' in cfg:
        level_name = cfg['loglevel']

    logger.setLevel(logging.getLevelName(level_name))

    formatter = logging.Formatter('%(asctime)s - [%(filename)15.15s:%(lineno)3s ] - %(levelname)s - %(message)s', "%Y%m%d %H%M%S")
    logging.addLevelName(logging.DEBUG, 'DEBUG ')
    logging.addLevelName(logging.INFO, 'INFO  ')
    logging.addLevelName(logging.WARNING, '*WARN ')
    logging.addLevelName(logging.ERROR, '*ERROR')

    # Create a console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
