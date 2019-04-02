from logging import (
    StreamHandler,
)
from logging import (  # noqa for imported levels
    INFO,
    ERROR,
    WARNING,
    DEBUG,
)

from .alogger import (
    Alogger
)


pdir = Alogger.pdir
pformat = Alogger.pformat


def default_alog_config():
    format_config = {
        "default_format":
            "%(levelname)-5.5s %(pathname)s%(lineno)s%(message)s",
        "default_thread_format": (
            "%(levelname)-5.5s %(threadName)s "
            "%(pathname)s%(lineno)s%(message)s"),
        "default_process_format": (
            "%(levelname)-5.5s PID:%(process)d "
            "%(pathname)s%(lineno)s%(message)s"),
        "default_process_thread_format": (
            "%(levelname)-5.5s PID:%(process)d:"
            "%(threadName)s %(pathname)s%(lineno)s%(message)s"
        )
    }

    config = {
        "custom_format": None,
        "showing_thread_name": False,
        "showing_process_id": False,
        "showing_log_datetime": None,
    }
    config.update(format_config)
    return config


def reset_global_alog():
    # It will be executed in the end of this module to set up global stuff.
    global default_logger
    global config
    global critical
    global fatal
    global error
    global exception
    global warning
    global warn
    global info
    global debug
    global log
    config = default_alog_config()
    default_logger = init_alogger(config)
    critical = default_logger.critical
    fatal = critical
    error = default_logger.error
    exception = default_logger.exception
    warning = default_logger.warning
    warn = default_logger.warn
    info = default_logger.info
    debug = default_logger.debug
    log = default_logger.log
    default_logger.turn_logging_datetime(on=True)


def init_alogger(alog_config, default_root_name=None):
    logger = Alogger(default_root_name)
    logger.alog_config = alog_config
    sh = StreamHandler()
    logger.addHandler(sh)
    set_format(logger.alog_config['default_format'], logger, is_default=True)
    return logger


def getLogger(*args, **kwargs):
    if any(args) or any(kwargs):
        from warnings import warn
        msg = "alog.getLogger always return alog.default_logger. " \
            "Use alog.getLogger() without arguments instead."
        warn(msg)
    return default_logger


# --- Alogger APIs --- #


def turn_logging_datetime(on, alogger=None):
    alogger = alogger or default_logger
    return alogger.turn_logging_datetime(on)


def turn_logging_thread_name(on, alogger=None):
    alogger = alogger or default_logger
    return alogger.turn_logging_thread_name(on)


def turn_logging_process_id(on, alogger=None):
    alogger = alogger or default_logger
    return alogger.turn_logging_process_id(on)


def set_level(level, alogger=None):
    alogger = alogger or default_logger
    return alogger.set_level(level)


def get_level(alogger=None):
    alogger = alogger or default_logger
    return alogger.get_level()


def set_format(fs, alogger=None, is_default=False,
               time_strfmt="%Y-%m-%d %H:%M:%S"):
    alogger = alogger or default_logger
    alogger.set_format(fs, is_default=is_default, time_strfmt=time_strfmt)


def get_format(logger=None):
    logger = logger or default_logger
    for handler in logger.handlers:
        if handler.formatter:
            return handler.formatter


def set_root_name(root_name, alogger=None):
    alogger = alogger or default_logger
    alogger.set_root_name(root_name)


def disable(level, alogger=None):
    alogger = alogger or default_logger
    alogger.disable(level)


reset_global_alog()
