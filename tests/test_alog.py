import sys
import logging

import alog


msg = "msg: Testing alog."


class TestAlog(object):

    def test_set_level(self):
        alog.set_level("WARNING")
        assert alog.get_level() == logging.WARNING

    def test_set_format(self):
        orig_format = alog.get_format()
        fs = "Test set format: %(asctime)s %(levelname)-5.5s" \
            " [%(pathname)s:%(lineno)s] %(message)s"
        alog.set_format(fs)
        alog.set_format(orig_format)

    def test_set_project_folder_name(self):
        alog.set_project_folder_name("alog")

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

    def test_disable(self):
        alog.disable("INFO")
