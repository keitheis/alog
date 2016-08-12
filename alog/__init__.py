import os
import sys
import warnings
from logging import (
    Logger, StreamHandler, Formatter,
)
PY2 = sys.version_info[0] == 2
if PY2:  # pragma: no cover
    from logging import LogRecord as logRecordFactory
else:  # pragma: no cover
    from logging import _logRecordFactory as logRecordFactory


root_project_folder_name = "alog"


class Alogger(Logger):
    def __init__(self, project_folder_name, *args, **kwargs):
        self.project_folder_name = project_folder_name
        super(Alogger, self).__init__(project_folder_name, *args, **kwargs)

    def makeRecord(self, name, level, fn, lno, msg, args, exc_info,
                   func=None, extra=None, sinfo=None):
        """
        A factory method which can be overridden in subclasses to create
        specialized LogRecords.
        """
        found = False
        paths = []
        print(fn)
        for term in fn.split(os.sep):
            if not found and term == self.project_folder_name:
                found = True
            elif found:
                paths.append(term)

        dotted_fn = ".".join(paths).replace(".py", "")

        lrargs = [name, level, dotted_fn, lno, msg, args, exc_info, func]
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


def init_logger():
    alogger = Alogger(root_project_folder_name)
    sh = StreamHandler()
    alogger.addHandler(sh)
    fs = "%(asctime)s %(levelname)-5.5s [%(pathname)s:%(lineno)s] %(message)s"
    set_format(fs, logger=alogger)
    return alogger


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


def set_project_folder_name(project_folder_name, logger=None):
    logger = logger or alogger
    logger.name = project_folder_name
    logger.project_folder_name = project_folder_name


alogger = init_logger()


def critical(msg, *args, **kwargs):
    alogger.critical(msg, *args, **kwargs)

fatal = critical


def error(msg, *args, **kwargs):
    alogger.error(msg, *args, **kwargs)


def exception(msg, *args, **kwargs):
    kwargs['exc_info'] = 1
    error(msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    alogger.warning(msg, *args, **kwargs)


def warn(msg, *args, **kwargs):
    warnings.warn("The 'warn' function is deprecated, "
                  "use 'warning' instead", DeprecationWarning, 2)
    warning(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    alogger.info(msg, *args, **kwargs)


def debug(msg, *args, **kwargs):
    alogger.debug(msg, *args, **kwargs)


def log(level, msg, *args, **kwargs):
    alogger.log(level, msg, *args, **kwargs)


def disable(level):
    alogger.manager.disable = level
