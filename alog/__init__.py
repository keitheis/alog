import os
import sys
from logging import (
    Logger, StreamHandler, Formatter,
)
PY2 = sys.version_info[0] == 2
if PY2:  # pragma: no cover
    from logging import LogRecord as logRecordFactory
else:  # pragma: no cover
    from logging import _logRecordFactory as logRecordFactory


def default_config():
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
config = default_config()


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
    config = default_config()
    alogger = init_logger()
    alogger.aconfig = config
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
    if (alogger.aconfig.get('custom_format') or
            alogger.aconfig['showing_thread_name'] == bool(on)):
        return

    alogger.aconfig['showing_thread_name'] = bool(on)
    if on:
        if alogger.aconfig.get('showing_process_id'):
            fs = alogger.aconfig['default_process_thread_format']
        else:
            fs = alogger.aconfig['default_thread_format']
    elif alogger.aconfig.get('showing_process_id'):
        fs = alogger.aconfig['default_process_format']
    else:
        fs = alogger.aconfig['default_format']
    set_format(fs, alogger, is_default=True)


def turn_process_id(on):
    if (alogger.aconfig.get('custom_format') or
            alogger.aconfig['showing_process_id'] == bool(on)):
        return

    alogger.aconfig['showing_process_id'] = bool(on)
    if on:
        if alogger.aconfig.get('showing_thread_name'):
            fs = alogger.aconfig['default_process_thread_format']
        else:
            fs = alogger.aconfig['default_process_format']
    elif alogger.aconfig.get('showing_thread_name'):
        fs = alogger.aconfig['default_thread_format']
    else:
        fs = alogger.aconfig['default_format']
    set_format(fs, alogger, is_default=True)


class Alogger(Logger):

    aconfig = config

    def __init__(self, root_name, *args, **kwargs):
        self.root_name = root_name
        super(Alogger, self).__init__(root_name, *args, **kwargs)

    def _alog_fn(self, fn):
        if 'ipython-input-' in fn:  # pragma: no cover
            return "<IPython"
        elif fn == '<stdin>':  # pragma: no cover
            return '<stdin'

        paths = []
        if self.root_name:
            found = False
            for term in fn.split(os.sep):
                if not found and term == self.root_name:
                    found = True
                elif found:
                    paths.append(term)
        if not paths:
            paths = fn.split(os.sep)
            if len(paths) > 2:
                paths = paths[-2:]

        return "[" + ".".join(paths).replace(".py", "")

    def makeRecord(self, name, level, fn, lno, msg, args, exc_info,
                   func=None, extra=None, sinfo=None):
        """
        A factory method which can be overridden in subclasses to create
        specialized LogRecords.
        """
        alog_fn = self._alog_fn(fn)
        if (not lno) or lno == 1:  # pragma: no cover
            lno = ""
        else:
            lno = ":{}".format(lno)

        lno += '] ' if '[' in alog_fn else '> '

        if alog_fn in ('<IPython>', '<stdin>'):  # pragma: no cover
            if func != '<module>':
                alog_fn = "{}({})".format(alog_fn, func)

        lrargs = [name, level, alog_fn, lno, msg, args, exc_info, func]
        if not PY2:  # pragma: no cover
            lrargs.append(sinfo)
        rv = logRecordFactory(*lrargs)
        if extra is not None:
            for key in extra:
                if (key in ["message", "asctime"]) or (key in rv.__dict__):
                    raise KeyError(
                        "Attempt to overwrite %r in LogRecord" % key)
                rv.__dict__[key] = extra[key]
        return rv


def init_logger(default_root_name=None):
    logger = Alogger(default_root_name)
    sh = StreamHandler()
    logger.addHandler(sh)
    set_format(logger.aconfig['default_format'], logger, is_default=True)
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
    formatter = \
        Formatter(fs, time_strfmt) if PY2 else Formatter(fs, time_strfmt, "%")
    for handler in logger.handlers:
        handler.setFormatter(formatter)
    if not is_default:
        logger.aconfig['custom_format'] = fs


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
