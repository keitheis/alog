import sys
import logging

import alog


msg = "msg: Testing alog."


class TestAlog(object):

    def setup(self):
        alog.reset()

    def test_set_level(self):
        alog.set_level("WARNING")
        assert alog.get_level() == logging.WARNING

    def test_set_format(self):
        orig_format = alog.get_format()
        fs = "Test set format: %(asctime)s %(levelname)-5.5s" \
            " [%(pathname)s:%(lineno)s] %(message)s"
        alog.set_format(fs)
        alog.set_format(orig_format)

    def test_set_root_name(self):
        alog.set_root_name("alog")
        alog.info(msg)

    def test_critical(self):
        alog.critical(msg)

    def test_fatal(self):
        alog.fatal(msg)

    def test_error(self):
        alog.error(msg)

    def test_exception(self):
        try:
            raise Exception(msg)
        except Exception:
            exc_info = sys.exc_info()
            alog.exception(msg, exc_info=exc_info)

    def test_warning(self):
        alog.warning(msg)

    def test_warn(self):
        alog.warn(msg)

    def test_turn_thread_name(self):
        alog.turn_process_id(True)
        alog.turn_thread_name(True)

    def test_turn_thread_name_with_custom_format(self):
        alog.set_format("blah")
        alog.turn_thread_name(True)

    def test_turn_process_id_with_custom_format(self):
        alog.set_format("blah")
        alog.turn_process_id(True)

    def test_not_turn_thread_name(self):
        alog.turn_thread_name(True)
        alog.turn_thread_name(False)

    def test_not_turn_process_id(self):
        alog.turn_process_id(True)
        alog.turn_process_id(False)

    def test_not_turn_process_id_and_turn_thread_name(self):
        alog.turn_thread_name(True)
        alog.turn_process_id(True)
        alog.turn_process_id(False)

    def test_turn_process_id_and_not_turn_thread_name(self):
        alog.turn_thread_name(True)
        alog.turn_process_id(True)
        alog.turn_thread_name(False)

    def test_info(self):
        alog.info(msg)

    def test_debug(self):
        alog.debug(msg)

    def test_log(self):
        level = logging.INFO
        alog.log(level, msg)

    def test_extra(self):
        alog.info(msg, extra={'Memo': "Extra testing."})

    def test_keyerror_in_extra(self):
        try:
            alog.info(msg, extra={'message': "Extra testing."})
        except KeyError:
            pass

    def test_pformat(self):
        msg = {'life is strange': True,
               'list is weird': list(range(10))}
        alog.info(alog.pformat(msg))

    def test_disable(self):
        alog.disable("INFO")

    def test_getLogger_with_argument(self):
        logger = alog.getLogger("whatever_argument")
        assert logger == alog.alogger
        logger = alog.getLogger(whatever_keyword_argument="")
        assert logger == alog.alogger

    def test_getLogger_without_name_given(self):
        logger = alog.getLogger()
        assert logger == alog.alogger
