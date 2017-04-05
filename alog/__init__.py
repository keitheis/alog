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
    default_logger = init_logger(config)
    critical = default_logger.critical
    fatal = critical
    error = default_logger.error
    exception = default_logger.exception
    warning = default_logger.warning
    warn = default_logger.warn
    info = default_logger.info
    debug = default_logger.debug
    log = default_logger.log


def turn_thread_name(on):
    if (default_logger.alog_config.get('custom_format') or
            default_logger.alog_config['showing_thread_name'] == bool(on)):
        return

    default_logger.alog_config['showing_thread_name'] = bool(on)
    if on:
        if default_logger.alog_config.get('showing_process_id'):
            fs = default_logger.alog_config['default_process_thread_format']
        else:
            fs = default_logger.alog_config['default_thread_format']
    elif default_logger.alog_config.get('showing_process_id'):
        fs = default_logger.alog_config['default_process_format']
    else:
        fs = default_logger.alog_config['default_format']
    set_format(fs, default_logger, is_default=True)


def turn_process_id(on):
    if (default_logger.alog_config.get('custom_format') or
            default_logger.alog_config['showing_process_id'] == bool(on)):
        return

    default_logger.alog_config['showing_process_id'] = bool(on)
    if on:
        if default_logger.alog_config.get('showing_thread_name'):
            fs = default_logger.alog_config['default_process_thread_format']
        else:
            fs = default_logger.alog_config['default_process_format']
    elif default_logger.alog_config.get('showing_thread_name'):
        fs = default_logger.alog_config['default_thread_format']
    else:
        fs = default_logger.alog_config['default_format']
    set_format(fs, default_logger, is_default=True)


def init_logger(alog_config, default_root_name=None):
    logger = Alogger(default_root_name)
    logger.alog_config = alog_config
    sh = StreamHandler()
    logger.addHandler(sh)
    set_format(logger.alog_config['default_format'], logger, is_default=True)
    return logger


def set_level(level, logger=None):
    logger = logger or default_logger
    for handler in logger.handlers:
        handler.setLevel(level)


def get_level(logger=None):
    logger = logger or default_logger
    for handler in logger.handlers:
        if handler.level:
            return handler.level


def set_format(fs, logger=None, is_default=False,
               time_strfmt="%Y-%m-%d %H:%M:%S"):
    logger = logger or default_logger
    formatter = Formatter(fs, time_strfmt) \
        if in_python2_runtime \
        else Formatter(fs, time_strfmt, "%")
    for handler in logger.handlers:
        handler.setFormatter(formatter)
    if not is_default:
        logger.alog_config['custom_format'] = fs


def get_format(logger=None):
    logger = logger or default_logger
    for handler in logger.handlers:
        if handler.formatter:
            return handler.formatter


def set_root_name(root_name, logger=None):
    logger = logger or default_logger
    logger.name = root_name
    logger.root_name = root_name


def pformat(*args, **kwargs):
    from pprint import pformat
    return "\n" + pformat(*args, **kwargs)


def disable(level):
    default_logger.manager.disable = level


reset()


def getLogger(*args, **kwargs):
    if any(args) or any(kwargs):
        from warnings import warn
        msg = "alog.getLogger always return alog.default_logger. " \
            "Use alog.getLogger() without arguments instead."
        warn(msg)
    return default_logger
