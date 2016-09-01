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

If you're new to logging, see `Why logging (instead of print)`_.

Installation
------------

.. code-block::

  pip install alog

Features 
--------

- Instant logging by good enough defaults.

  You can do logging with every new project/module right away without worrying
  about context switch to how to integrate Python logging module. Alog comes 
  with these defaults you can rely:

    - A default logger.
    - Logging level: logging.INFO
    - Logging format::

      "%(asctime)s %(levelname)-5.5s [parent_module.current_module:%(lineno)s]%(message)s"

- No more **__name__** in every file whenever you just want to do logging.

  It build the default module names on the fly. 

- Compatible with default Python logging module.

  Alog is built upon default Python logging module. You can configure it in
  the same way of default Python logging module.


Comparing `alog` with Python default `logging` module
-----------------------------------------------------

Comparing `alog`::

    In [1]: import alog

    In [2]: alog.info("Hello alog!")
    2016-09-01 02:20:34,729 INFO  <IPython> Hello alog!

with `logging` module::

    In [1]: import logging

    In [2]: logging.basicConfig(
       ...:     level=logging.INFO,
       ...:     format="%(asctime)s %(levelname)-5.5s "
       ...:            "[%(name)s:%(lineno)s] %(message)s")

    In [3]: # In every file you want to do log, otherwise %(names)s won't work.
    In [4]: logger = logging.getLogger(__name__)

    In [5]: logger.info("Hello log!")
    2016-09-01 02:16:30,432 INFO  [__main__:1] Hello log!


Why logging (instead of print)
------------------------------

  The main goal of logging is to figure out what was going on and get its
  insight. `print`, by default, has only do pure output. No timestamp, no 
  which module it is in, and no level control, comparing to logging.

  Lets try with `aproject/models/user.py`::

    class User:
        def __init__(self, user_id, username):
            ...
            print(username)
            ...

  What you got output of `print`::
  
    >>> admin = User(1, "admin")
    "admin"

  Now, use alog instead::

    import alog

    class User:
        def __init__(self, user_id, username):
            ...
            alog.info(username)
            ...

  What you got output of `alog.info`::
  
    >>> admin = User(1, "admin")
    2016-09-01 01:32:58,063 INFO  [models.user:6] admin

  In the output of hundreds of lines, this helps (a lot).

  What if you have alread use print a log? That's as easy::

    import alog

    print = alog.info

    ... # A lot of print code no needed to change
