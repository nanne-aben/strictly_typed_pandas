==========
Unit tests
==========

To run all tests:

.. code-block:: bash

    pip install -e .
    pip install -r requirements-dev.txt
    coverage run -m pytest --mypy-only-local-stub --typeguard-packages=strictly_typed_pandas,tests
    coverage report -m

Note that the static typing tests require you to reinstall strictly_typed_pandas every time you make a change to the code.

Limiting the testing time of static typing tests
================================================

Note that we only have two static typing tests:

* one with the mypy plugin enabled
* one without the mypy plugin enabled

It seems like each test requires mypy to fully check all dependencies from scratch, resulting in a testing time of roughly 40s per test. For this reason, we opted for two large tests rather than many small tests, therey greatly reducing the overall testing time.
