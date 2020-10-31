import os
import constants.constants as const

SVC_NAME = const.SVC_NAME

MODEL_CONFIG = {
    'model_path': os.getenv('MODEL_PATH', 'data/model/crnn_model.h5')
}

LOGGER_CONFIG = {
    'log_level': os.getenv('LOG_LEVEL', 'DEBUG'),
    'log_handle': os.getenv('LOG_HANDLE', 'file'),
    'log_path': os.getenv('LOG_PATH', 'log/'),
    'log_file': os.getenv('LOG_FILE', SVC_NAME)
}

SERVICE_CONFIG = {
    'port': os.getenv('PORT', 8000),
    'workers': os.getenv('WORKERS', 1)
}