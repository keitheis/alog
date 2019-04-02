# -*- coding: utf-8 -*-
from __future__ import \
    absolute_import, division, print_function, unicode_literals

import alog

from .base import AlogTestBase

msg = "msg: Testing alog."


class TestAlog(AlogTestBase):

    @property
    def _alog(self):
        return alog

    def test_getLogger_with_argument(self):
        logger = alog.getLogger("whatever_argument")
        assert logger == alog.default_logger
        logger = alog.getLogger(whatever_keyword_argument="")
        assert logger == alog.default_logger

    def test_getLogger_without_name_given(self):
        logger = alog.getLogger()
        assert logger == alog.default_logger

    def test_disable_level(self):
        self._alog.disable("INFO")
