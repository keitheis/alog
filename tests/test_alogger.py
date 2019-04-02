from __future__ import \
    absolute_import, division, print_function, unicode_literals

import alog

from .base import AlogTestBase

msg = "msg: Testing alog."


class TestAlog(AlogTestBase):

    @property
    def _alog(self):
        return alog.default_logger
