from pathlib import Path

from logging import getLogger
from logging.config import dictConfig

LOGGER_FPATH = Path(__file__).resolve().parents[2] / 'app.log'

CONFIG_DICT = {
        'version': 1,
        'formatters': {
            'detailed': {
                'format': '%(process)d %(asctime)s %(filename)s %(lineno)d %(''levelname)s: %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
            'file': {
                'class': 'logging.FileHandler',
                'filename': LOGGER_FPATH,
                'mode': 'a',
                'formatter': 'detailed',
            },
        },
        'loggers': {
            'tc_logger': {
                'handlers': ['file'],
                'level': 'DEBUG'
            }
        }
    }

dictConfig(CONFIG_DICT)
logger = getLogger('tc_logger')
