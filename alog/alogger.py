import os
import sys
from logging import (
    Logger,
    Formatter,
    getLevelName
)

in_python2_runtime = sys.version_info[0] == 2
if in_python2_runtime:  # pragma: no cover
    from logging import LogRecord as logRecordFactory
else:  # pragma: no cover
    from logging import _logRecordFactory as logRecordFactory


class Alogger(Logger):

    # --- Logger competiable methods --- #

    def __init__(self, root_name, *args, **kwargs):
        self.root_name = root_name
        super(Alogger, self).__init__(root_name, *args, **kwargs)

    def _alog_fn(self, fn):
        if 'ipython-input-' in fn:  # pragma: no cover
            return "<IPython"
        if fn == '<stdin>':  # pragma: no cover
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

        lno += '] ' if alog_fn.startswith('[') else '> '

        if alog_fn in ('<IPython>', '<stdin>'):  # pragma: no cover
            if func != '<module>':
                alog_fn = "{}({})".format(alog_fn, func)

        lrargs = [name, level, alog_fn, lno, msg, args, exc_info, func]
        if not in_python2_runtime:  # pragma: no cover
            lrargs.append(sinfo)
        rv = logRecordFactory(*lrargs)
        if extra is not None:
            for key in extra:
                if (key in ["message", "asctime"]) or (key in rv.__dict__):
                    raise KeyError(
                        "Attempt to overwrite %r in LogRecord" % key)
                rv.__dict__[key] = extra[key]
        return rv

    # --- alog APIs --- #

    def _get_logger_showing_fs(self):
        if self.alog_config.get('showing_thread_name'):
            if self.alog_config.get('showing_process_id'):
                fs = self.alog_config['default_process_thread_format']
            else:
                fs = self.alog_config['default_thread_format']
        elif self.alog_config.get('showing_process_id'):
            fs = self.alog_config['default_process_format']
        else:
            fs = self.alog_config['default_format']
        return fs

    def turn_logging_datetime(self, on):
        if (
            self.alog_config.get('custom_format') or
            self.alog_config['showing_log_datetime'] == bool(on)
        ):
            return

        fs = self._get_logger_showing_fs()
        if on:
            fs = "%(asctime)s " + fs
        self.set_format(fs, is_default=True)

    def turn_logging_thread_name(self, on):
        if (
            self.alog_config.get('custom_format') or
            self.alog_config['showing_thread_name'] == bool(on)
        ):
            return

        self.alog_config['showing_thread_name'] = bool(on)
        fs = self._get_logger_showing_fs()
        self.set_format(fs, is_default=True)

    def turn_logging_process_id(self, on):
        if (
            self.alog_config.get('custom_format') or
            self.alog_config['showing_process_id'] == bool(on)
        ):
            return

        self.alog_config['showing_process_id'] = bool(on)
        fs = self._get_logger_showing_fs()
        self.set_format(fs, is_default=True)

    @staticmethod
    def pformat(*args, **kwargs):
        from pprint import pformat
        return "\n" + pformat(*args, **kwargs)

    @classmethod
    def pdir(cls, obj, str_not_startswith="_"):
        dired = [attr for attr in dir(obj)
                 if not attr.startswith(str_not_startswith)]
        return cls.pformat(dired)

    def set_level(self, level, logger=None):
        logger = logger or self
        for handler in logger.handlers:
            handler.setLevel(level)

    def get_level(self, logger=None):
        logger = logger or self
        for handler in logger.handlers:
            if handler.level:
                return handler.level

    def get_format(self, logger=None):
        from warnings import warn
        msg = "`get_format()` actually return a Formatter. " \
            "Use `get_formatter()` instead."
        warn(msg)
        alogger = logger or self
        return alogger.get_formatter()

    def get_formatter(self, logger=None):
        alogger = logger or self
        for handler in alogger.handlers:
            if handler.formatter:
                return handler.formatter

    def set_formatter(self, formatter, alogger=None):
        alogger = alogger or self
        for handler in alogger.handlers:
            handler.setFormatter(formatter)

    def set_format(self, fs, alogger=None, is_default=False,
                   time_strfmt="%Y-%m-%d %H:%M:%S"):
        alogger = alogger or self
        formatter = Formatter(fs, time_strfmt) \
            if in_python2_runtime \
            else Formatter(fs, time_strfmt, "%")
        alogger.set_formatter(formatter, alogger=alogger)
        if not is_default:
            alogger.alog_config['custom_format'] = fs

    def set_root_name(self, root_name, logger=None):
        logger = logger or self
        logger.name = root_name
        logger.root_name = root_name

    def disable(self, level):
        self.manager.disable = getLevelName(level)
