Alog
====

.. image:: https://travis-ci.org/keitheis/alog.svg?branch=master
  :target: https://travis-ci.org/keitheis/alog

.. image:: https://codecov.io/gh/keitheis/alog/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/keitheis/alog

.. image:: http://img.shields.io/pypi/v/alog.svg?style=flat
   :target: https://pypi.python.org/pypi/alog

Python logging for Humans. Your goto logging module without panic.
With it you can log and debug without leaving coding flow.

**Warning:** No more `logger = logging.getLogger(__name__)` in your every file.

.. code-block::

  >>> import alog
  >>> alog.info("Hi.")
  2016-08-18 20:44:30,208 INFO  <stdin> Hi.
  >>> def test():
  ...     alog.info("Test 1")
  ...     alog.error("Test 2")
  ...
  >>> test()
  2016-08-18 20:45:19,372 INFO  <stdin:2> Test 1
  2016-08-18 20:45:19,372 ERROR <stdin:3> Test 2
  >>> alog.set_level("ERROR")
  >>> test()
  2016-08-18 20:45:41,788 ERROR <stdin:3> Test 2

Installation
------------

.. code-block::

  pip install alog

Features 
--------

 - Instant logging.
    No more context switch at a moment when you want to do logging.

 - Best default.
    Alog comes with best enough default.

 - Compatible with default Python logging module.
    Alog is built upon default Python logging module. You can configure it in
    the same way of default Python logging module.

 - No more **__name__** in every file you just want to do logging.
    It build the default module names on the fly. 

See alog v.s. Python default logging.
