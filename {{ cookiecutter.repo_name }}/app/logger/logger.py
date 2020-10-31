from datetime import datetime
import os
import logging
import logging.handlers
from pythonjsonlogger import jsonlogger
from pythonjsonlogger.jsonlogger import merge_record_extra
from pathlib import Path


logger_levels = ['INFO', 'DEBUG', 'ERROR', 'WARNING']


def get_logger_level(level):
    level = level.upper
    if level in logger_levels:
        return level
    return 'INFO'


def get_logger(logger_config):
    logger = Logger(__name__)
    logger.set_logger(logger_config)
    return logger


class Logger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)

    def set_logger(self, logger_config):
        logger_level = get_logger_level(logger_config['log_level'])
        self.logger.setLevel(logger_level)
        formatter = CustomJsonFormatter()

        handle = logger_config['log_handle'].lower()

        if handle == 'console' or handle == 'both':
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

        if handle == 'file' or handle == 'both':
            if logger_config['log_path'] is not None:
                log_folder = os.path.join(logger_config['log_path'], logger_config['log_file'])
                Path(log_folder).mkdir(parents=True, exist_ok=True)
                output_log_file = os.path.join(log_folder, logger_config['log_file'] + '.log')
                file_handler = logging.handlers.RotatingFileHandler(output_log_file, maxBytes=5000000, backupCount=100)
                logging.handlers.BaseRotatingHandler
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)

    def info(self, msg, event, req_id=None, status_code=None, res=None):
        if self.logger is not None:
            if status_code is None:
                self.logger.info(msg, extra={'event': event})
            else:
                self.logger.info(msg, extra={'event': event, 'status_code': status_code, 'req_id': req_id if req_id is not None else '', 'res': res if res is not None else ''})

    def debug(self, msg, event, req_id= None, status_code=None):
        if self.logger is not None:
            if status_code is None:
                self.logger.debug(msg, extra={'event': event})
            else:
                self.logger.debug(msg, extra={'event': event, 'status_code': status_code, 'req_id': req_id if req_id is not None else ''})

    def error(self, msg, event, error, req_id=None, status_code=None):
        if self.logger is not None:
            if status_code is None:
                self.logger.exception(msg, extra={'event': event, 'error': error})
            else:
                self.logger.exception(msg, extra={'event': event, 'status_code': status_code, 'req_id': req_id if req_id is not None else '', 'error': error})

    def warning(self, msg, event, req_id=None, status_code=None):
        if self.logger is not None:
            if status_code is None:
                self.logger.warning(msg, extra={'event': event})
            else:
                self.logger.warning(msg, extra={'event': event, 'status_code': status_code, 'req_id': req_id if req_id is not None else ''})


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        log_record['timestamp'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        log_record['level'] = record.levelname
        log_record['message'] = record.message
        merge_record_extra(record, log_record, reserved=self._skip_fields)
        if log_record['level'] == 'ERROR':
            log_record['nested_error'] = message_dict['exc_info']