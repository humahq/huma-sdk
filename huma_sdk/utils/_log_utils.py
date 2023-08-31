import logging
import traceback
from logging.config import dictConfig


def log_level_name(log_level: logging) -> int:
    if log_level == logging.NOTSET: return "NOTSET"
    if log_level == logging.DEBUG: return "DEBUG"
    if log_level == logging.INFO: return "INFO"
    if log_level == logging.WARNING: return "WARNING"
    if log_level == logging.ERROR: return "ERROR"
    if log_level == logging.CRITICAL: return "CRITICAL"
    return "DEBUG"


def root_logger_setup(log_level: logging) -> logging.Logger:
    """This will setup the default formatters and handlers for logging"""
    # Define the dictionary config for logging
    logging_config = dict(
        version=1,
        formatters={
            'f': {'format': '[%(levelname)s] (%(name)s/%(module)s:%(funcName)s:%(lineno)d) %(message)s'}},
        handlers={
            'h': {'class': 'logging.StreamHandler', 'formatter': 'f'}},
        root={
            'handlers': ['h'],
            'level': log_level_name(log_level),
            'propagate': True,
            'disabled': False}
    )

    # Now load the config
    dictConfig(logging_config)
    return logging.getLogger()


def get_logger(name=None, level=logging.DEBUG):
    """This will return a logger with a default formatter"""
    new_logger = root_logger_setup(level) if not logging.getLogger().hasHandlers() else logging.getLogger(name)
    return new_logger


def log_exception(mesg, logger, exc=None):
    """Critical/panic message and raise Runtime Error immediately"""
    logger.critical('Exception: ' + mesg)
    if exc:
        logger.critical('Exception: ' + traceback.format_exc())


def test():
    """Test the Logging methods"""
    # Now create a logger
    my_log = get_logger(name=__name__, level=logging.INFO)
    my_log.debug('Test debug log message SHOULD NOT SEE')
    my_log.info('Test information log message')
    my_log.warning('Test warning log message')
    my_log.error('Test error log message')
    my_log.critical('Test critical log message')
    # Test log levels
    my_log2 = get_logger(name="test_logger2")
    my_log2.debug('Test debug log message SHOULD NOT SEE')
    my_log2.info('Test information log message')
    # Test named logger
    my_name_log = get_logger('log_test')
    my_name_log.info('log message')
    # Test the log_exception method
    try:
        6/0
    except ZeroDivisionError as exc:
        log_exception('OMG: this is bad...', my_name_log, exc)
    print('Success!')

if __name__ == '__main__':
    test()