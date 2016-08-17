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


class Alogger(Logger):
    def __init__(self, root_name, *args, **kwargs):
        self.root_name = root_name
        super(Alogger, self).__init__(root_name, *args, **kwargs)

    def _alog_fn(self, fn):
        if 'ipython-input-' in fn:
            return "IPython"
        elif fn == '<stdin>':
            return 'stdin'

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

        return ".".join(paths).replace(".py", "")

    def makeRecord(self, name, level, fn, lno, msg, args, exc_info,
                   func=None, extra=None, sinfo=None):
        """
        A factory method which can be overridden in subclasses to create
        specialized LogRecords.
        """
        alog_fn = self._alog_fn(fn)
        if lno == 1:
            lno = ""

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
    fs = "%(asctime)s %(levelname)-5.5s [%(pathname)s:%(lineno)s] %(message)s"
    set_format(fs, logger=logger)
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


def set_format(fs, logger=None):
    logger = logger or alogger
    formatter = Formatter(fs, None) if PY2 else Formatter(fs, None, "%")
    for handler in logger.handlers:
        handler.setFormatter(formatter)


def get_format(logger=None):
    logger = logger or alogger
    for handler in logger.handlers:
        if handler.formatter:
            return handler.formatter


def set_root_name(root_name, logger=None):
    logger = logger or alogger
    logger.name = root_name
    logger.root_name = root_name


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


def disable(level):
    alogger.manager.disable = level
