Alog
====

.. image:: https://travis-ci.com/keitheis/alog.svg?branch=master
  :target: https://travis-ci.com/keitheis/alog

.. image:: https://codecov.io/gh/keitheis/alog/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/keitheis/alog

.. image:: http://img.shields.io/pypi/v/alog.svg?style=flat
   :target: https://pypi.org/pypi/alog

Your goto Python logging without panic on context swtich.

**Warning:** No more ``logger = logging.getLogger(__name__)`` in your every file.

.. code-block:: python

  >>> import alog
  >>> alog.info("Hi.")
  2016-12-18 20:44:30 INFO  <stdin> Hi.
  >>> def test():
  ...     alog.info("Test 1")
  ...     alog.error("Test 2")
  ...
  >>> test()
  2016-12-18 20:45:19 INFO  <stdin:2> Test 1
  2016-12-18 20:45:19 ERROR <stdin:3> Test 2
  >>> alog.set_level("ERROR")
  >>> test()
  2016-12-18 20:45:41 ERROR <stdin:3> Test 2

If you're new to logging, see `Why should you use logging instead of print`_.

Installation
------------

.. code-block::

  pip install alog

Features 
--------

- Instant logging with expected defaults.

  You can do logging instantly by reading a small piece of README.
  Alog comes with useful defaults:

  - A default logger.
  - Logging level: ``logging.INFO``
  - Logging format::

    "%(asctime)s %(levelname)-5.5s [parent_module.current_module:%(lineno)s]%(message)s",
    "%Y-%m-%d %H:%M:%S"

- No more **__name__** whenever you start to do logging in a module.

  Alog builds the default module names on the fly. 

- Compatible with default Python ``logging`` module.

  Alog is built upon default Python logging module. You can configure it by
  the same way of default Python logging module when it's needed.


Comparing ``alog`` with Python default ``logging`` module
---------------------------------------------------------

Comparing ``alog`` :

.. code-block:: python

    In [1]: import alog

    In [2]: alog.info("Hello alog!")
    2016-11-23 12:20:34 INFO  <IPython> Hello alog!

with ``logging`` module:

.. code-block:: python

    In [1]: import logging

    In [2]: logging.basicConfig(
       ...:     level=logging.INFO,
       ...:     format="%(asctime)s %(levelname)-5.5s "
       ...:            "[%(name)s:%(lineno)s] %(message)s")

    In [3]: # In every file you want to do log, otherwise %(names)s won't work.
    In [4]: logger = logging.getLogger(__name__)

    In [5]: logger.info("Hello log!")
    2016-11-23 12:16:30 INFO  [__main__:1] Hello log!


Tips
----

.. code-block:: python

    import alog

    a_complex_json_dict = {...}  # or a_complex_dict
    alog.info(alog.pformat(a_complex_dict))

    restaurant = Restaurant(...)
    alog.info(alog.pdir(restaurant))
    # or just skip attributes starts with "__":
    alog.info(alog.pdir(restaurant, str_not_startswith="__"))
    # instead of
    alog.info([attr for attr in dir(restaurant) if attr.startswith("_")])

    # Play threads?
    alog.turn_logging_thread_name(on=True)
    # Processes?
    alog.turn_logging_process_id(on=True)
    # No datetime wanted?
    alog.turn_logging_datetime(on=False)

Why should you use logging instead of print
-------------------------------------------

The main goal of logging is to figure out what was going on and to get the
insight. ``print``, by default, does simply pure string output. No timestamp,
no module hint, and no level control, comparing to a pretty logging record.

Lets start with ``aproject/models/user.py`` :

.. code-block:: python

  class User:
      def __init__(self, user_id, username):
          ...
          print(username)
          ...

What you got output of ``print`` :

.. code-block:: python

  >>> admin = User(1, "admin")
  "admin"


Now use ``alog`` :

.. code-block:: python

  import alog

  class User:
      def __init__(self, user_id, username):
          ...
          alog.info(username)
          ...

What you got output of ``alog.info`` :

.. code-block:: python

  >>> admin = User(1, "admin")
  2016-11-23 11:32:58 INFO  [models.user:6] admin

In the output of hundreds of lines, it helps (a lot).

What if you have used ``print`` a log? That's as easy:

.. code-block:: python

  import alog

  print = alog.info

  ... # A lot of print code no needed to change

