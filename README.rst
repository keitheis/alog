====
Alog
====

Python logging for Humans.
It's very easy to use in an application setting.

For example
===========

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


In IPython

.. code-block::

  In [1]: >>> import alog
     ...: >>> alog.info("Hi.")
     ...: >>> alog.error("Och!")
     ...: >>> alog.set_level("ERROR")
     ...: >>> alog.info("Hi.")
     ...: >>> alog.error("Och!")
     ...:
  2016-08-18 20:42:57,801 INFO  <IPython:2> Hi.
  2016-08-18 20:42:57,801 ERROR <IPython:3> Och!
  2016-08-18 20:42:57,802 ERROR <IPython:6> Och!
