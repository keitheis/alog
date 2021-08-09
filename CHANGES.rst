1.2.0 (2021-08-09)
==================

 - Support Python 3.9
 - Remove Python 3.4 and 3.5 support.

1.1.0 (2020-02-10)
==================

 - Support Python 3.8
 - Fix broken ``set_format`` function when formatter argument is given.

1.0.0 (2019-04-03)
==================

 - Renamed:

   - ``turn_logging_datetime(on=True)``
   - ``turn_logging_thread_name(on=False)``
   - ``turn_logging_process_id(on=False)``

 - Support most same APIs between alog and Alogger.
 - Add ``alog.pdir()`` for handy replacing ``[attr for attr in dir(obj)
   if not attr.startswith("_")]``.

0.9.13 (2017-06-18)
===================

 - Fix not able to ``turn_log_datetime(on=False)``.

0.9.12 (2017-06-16)
===================

 - Support not showing_log_datetime by ``turn_log_datetime(on=False)``.

0.9.11 (2017-04-07)
===================

 - Add ``alog.getLogger()`` for handy replacing ``logging.getLogger``.

0.9.10 (2017-03-27)
===================

 - Default logging format asctime to "%Y-%m-%d %H:%M:%S" instead of
   "%Y-%m-%d,%H:%M:%S.%f".
 - Update package info and usage (setup.py, README, ...).

0.9.9 (2016-08-28)
==================

 - Update to turn_thread_name and turn_process_id.

0.9.8 (2016-08-27)
==================

 - Support showing_thread_name and showing_process_id.
 - Support global reset.

0.9.7 (2016-08-17)
==================

 - Better paths log for None default root name.

0.9.6 (2016-08-16)
==================

 - First public release.
