# -*- coding: utf-8 -*-
from __future__ import \
    absolute_import, division, print_function, unicode_literals

import sys
import logging

import alog


msg = "msg: Testing alog."


class AlogTestBase(object):

    @property
    def _alog(self):
        raise NotImplementedError("return a alog thing")

    def setup(self):
        alog.reset_global_alog()
        self._alog.set_level("INFO")

    def test_set_level(self):
        self._alog.set_level("WARNING")
        assert self._alog.get_level() == logging.WARNING

    def test_set_format(self):
        orig_format = self._alog.get_format()
        fs = "Test set format: %(asctime)s %(levelname)-5.5s" \
            " [%(pathname)s:%(lineno)s] %(message)s"
        self._alog.set_format(fs)
        self._alog.set_format(orig_format)

    def test_set_root_name(self):
        self._alog.set_root_name("alog")
        self._alog.info(msg)

    def test_critical(self):
        self._alog.critical(msg)

    def test_fatal(self):
        self._alog.fatal(msg)

    def test_error(self):
        self._alog.error(msg)

    def test_exception(self):
        try:
            raise Exception(msg)
        except Exception:
            exc_info = sys.exc_info()
            self._alog.exception(msg, exc_info=exc_info)

    def test_warning(self):
        self._alog.warning(msg)

    def test_warn(self):
        self._alog.warn(msg)

    def test_turn_thread_name(self):
        self._alog.turn_process_id(True)
        self._alog.turn_thread_name(True)

    def test_turn_thread_name_with_custom_format(self):
        self._alog.set_format("blah")
        self._alog.turn_thread_name(True)

    def test_turn_process_id_with_custom_format(self):
        self._alog.set_format("blah")
        self._alog.turn_process_id(True)

    def test_turn_log_datetime_with_custom_format(self):
        self._alog.set_format("blah")
        self._alog.turn_log_datetime(True)

    def test_not_turn_thread_name(self):
        self._alog.turn_thread_name(True)
        self._alog.turn_thread_name(False)

    def test_not_turn_process_id(self):
        self._alog.turn_process_id(True)
        self._alog.turn_process_id(False)

    def test_not_turn_process_id_and_turn_thread_name(self):
        self._alog.turn_thread_name(True)
        self._alog.turn_process_id(True)
        self._alog.turn_process_id(False)

    def test_turn_process_id_and_not_turn_thread_name(self):
        self._alog.turn_thread_name(True)
        self._alog.turn_process_id(True)
        self._alog.turn_thread_name(False)

    def test_info(self):
        self._alog.info(msg)

    def test_debug(self):
        self._alog.debug(msg)

    def test_log(self):
        level = logging.INFO
        self._alog.log(level, msg)

    def test_extra(self):
        self._alog.info(msg, extra={'Memo': "Extra testing."})

    def test_keyerror_in_extra(self):
        try:
            self._alog.info(msg, extra={'message': "Extra testing."})
        except KeyError:
            pass

    def test_pformat(self):
        msg = {'life is strange': True,
               'list is weird': list(range(10))}
        self._alog.info(alog.pformat(msg))

    def test_pdir(self):
        class Thing(object):
            pass
        thing = Thing()
        thing._private_thing = True
        thing.public_thing = True
        assert "public_thing" in str(self._alog.pdir(thing))
        assert "_private_thing" not in str(self._alog.pdir(thing))
