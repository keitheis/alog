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


showing_thread_name = False
showing_process_id = False


def reset():
    global alogger
    global showing_thread_name
    global showing_process_id
    global critical
    global fatal
    global error
    global exception
    global warning
    global warn
    global info
    global debug
    global log
    showing_thread_name = False
    showing_process_id = False
    alogger = init_logger()
    critical = alogger.critical
    fatal = critical
    error = alogger.error
    exception = alogger.exception
    warning = alogger.warning
    warn = alogger.warn
    info = alogger.info
    debug = alogger.debug
    log = alogger.log


class Alogger(Logger):

    custom_format = None
    _default_format = \
        "%(asctime)s %(levelname)-5.5s %(pathname)s%(lineno)s%(message)s"
    _default_thread_format = ("%(asctime)s %(levelname)-5.5s %(threadName)s "
                              "%(pathname)s%(lineno)s%(message)s")
    _default_process_format = ("%(asctime)s %(levelname)-5.5s PID:%(process)d "
                               "%(pathname)s%(lineno)s%(message)s")
    _default_process_thread_format = (
        "%(asctime)s %(levelname)-5.5s PID:%(process)d:"
        "%(threadName)s %(pathname)s%(lineno)s%(message)s"
    )
    _showing_thread_name = showing_thread_name
    _showing_process_id = showing_process_id

    def __init__(self, root_name, *args, **kwargs):
        self.root_name = root_name
        super(Alogger, self).__init__(root_name, *args, **kwargs)

    @property
    def default_format(self):
        return self._default_format

    @property
    def showing_thread_name(self):
        return self._showing_thread_name

    @showing_thread_name.setter
    def showing_thread_name(self, value):
        self._showing_thread_name = bool(value)
        if self.custom_format:
            return

        if self.showing_thread_name:
            fs = self._default_process_thread_format \
                if self.showing_process_id else self._default_thread_format
            set_format(fs, self, is_default=True)
        else:
            fs = self._default_process_format \
                if self.showing_process_id else self.default_format
            set_format(fs, self, is_default=True)

    @property
    def showing_process_id(self):
        return self._showing_process_id

    @showing_process_id.setter
    def showing_process_id(self, value):
        self._showing_process_id = bool(value)
        if self.custom_format:
            return

        if self.showing_process_id:
            fs = self._default_process_thread_format \
                if self.showing_thread_name else self._default_process_format
            set_format(fs, self, is_default=True)
        else:
            fs = self._default_thread_format \
                if self.showing_thread_name else self.default_format
            set_format(fs, self, is_default=True)

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
        if showing_process_id != self.showing_process_id:
            self.showing_process_id = showing_process_id
        if showing_thread_name != self.showing_thread_name:
            self.showing_thread_name = showing_thread_name
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
    set_format(logger.default_format, logger, is_default=True)
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


def set_format(fs, logger=None, is_default=False):
    logger = logger or alogger
    formatter = Formatter(fs, None) if PY2 else Formatter(fs, None, "%")
    for handler in logger.handlers:
        handler.setFormatter(formatter)
    if not is_default:
        logger.custom_format = fs


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
