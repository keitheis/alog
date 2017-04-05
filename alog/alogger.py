import os
import sys
from logging import Logger

in_python2_runtime = sys.version_info[0] == 2
if in_python2_runtime:  # pragma: no cover
    from logging import LogRecord as logRecordFactory
else:  # pragma: no cover
    from logging import _logRecordFactory as logRecordFactory


class Alogger(Logger):

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
