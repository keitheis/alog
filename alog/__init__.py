from logging import (
    StreamHandler,
    Formatter,
)

from .alogger import (
    in_python2_runtime,
    Alogger
)


def default_alog_config():
    return {
        "custom_format": None,
        "showing_thread_name": False,
        "showing_process_id": False,
        "default_format":
            "%(asctime)s %(levelname)-5.5s %(pathname)s%(lineno)s%(message)s",
        "default_thread_format": (
            "%(asctime)s %(levelname)-5.5s %(threadName)s "
            "%(pathname)s%(lineno)s%(message)s"),
        "default_process_format": (
            "%(asctime)s %(levelname)-5.5s PID:%(process)d "
            "%(pathname)s%(lineno)s%(message)s"),
        "default_process_thread_format": (
            "%(asctime)s %(levelname)-5.5s PID:%(process)d:"
            "%(threadName)s %(pathname)s%(lineno)s%(message)s"
        )
    }


config = None


def reset():
    global alogger
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
    alogger = init_logger(config)
    critical = alogger.critical
    fatal = critical
    error = alogger.error
    exception = alogger.exception
    warning = alogger.warning
    warn = alogger.warn
    info = alogger.info
    debug = alogger.debug
    log = alogger.log


def turn_thread_name(on):
    if (alogger.alog_config.get('custom_format') or
            alogger.alog_config['showing_thread_name'] == bool(on)):
        return

    alogger.alog_config['showing_thread_name'] = bool(on)
    if on:
        if alogger.alog_config.get('showing_process_id'):
            fs = alogger.alog_config['default_process_thread_format']
        else:
            fs = alogger.alog_config['default_thread_format']
    elif alogger.alog_config.get('showing_process_id'):
        fs = alogger.alog_config['default_process_format']
    else:
        fs = alogger.alog_config['default_format']
    set_format(fs, alogger, is_default=True)


def turn_process_id(on):
    if (alogger.alog_config.get('custom_format') or
            alogger.alog_config['showing_process_id'] == bool(on)):
        return

    alogger.alog_config['showing_process_id'] = bool(on)
    if on:
        if alogger.alog_config.get('showing_thread_name'):
            fs = alogger.alog_config['default_process_thread_format']
        else:
            fs = alogger.alog_config['default_process_format']
    elif alogger.alog_config.get('showing_thread_name'):
        fs = alogger.alog_config['default_thread_format']
    else:
        fs = alogger.alog_config['default_format']
    set_format(fs, alogger, is_default=True)


def init_logger(alog_config, default_root_name=None):
    logger = Alogger(default_root_name)
    logger.alog_config = alog_config
    sh = StreamHandler()
    logger.addHandler(sh)
    set_format(logger.alog_config['default_format'], logger, is_default=True)
    return logger


def set_level(level, logger=None):
    logger = logger or alogger
    for handler in logger.handlers:
        handler.setLevel(level)


def get_level(logger=None):
    logger = logger or alogger
    for handler in logger.handlers:
        if handler.level:
            return handler.level


def set_format(fs, logger=None, is_default=False,
               time_strfmt="%Y-%m-%d %H:%M:%S"):
    logger = logger or alogger
    formatter = Formatter(fs, time_strfmt) \
        if in_python2_runtime \
        else Formatter(fs, time_strfmt, "%")
    for handler in logger.handlers:
        handler.setFormatter(formatter)
    if not is_default:
        logger.alog_config['custom_format'] = fs


def get_format(logger=None):
    logger = logger or alogger
    for handler in logger.handlers:
        if handler.formatter:
            return handler.formatter


def set_root_name(root_name, logger=None):
    logger = logger or alogger
    logger.name = root_name
    logger.root_name = root_name


def pformat(*args, **kwargs):
    from pprint import pformat
    return "\n" + pformat(*args, **kwargs)


def disable(level):
    alogger.manager.disable = level


reset()


def getLogger(name=None):
    if name:
        from logging import getLogger as logging_getLogger
        return logging_getLogger(name)
    return alogger
