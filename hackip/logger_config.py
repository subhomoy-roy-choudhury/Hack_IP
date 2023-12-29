import logging.config

# Define logging configuration dictionary
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'file_handler': {
            'class': 'logging.FileHandler',
            'filename': 'app.log',
            'formatter': 'standard',
            'level': 'INFO',
        },
    },
    'root': {
        'handlers': ['file_handler'],
        'level': 'INFO',
    },
}

# Function to setup logging
def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
