================================================================
Strictly Typed Pandas: static type checking of pandas DataFrames
================================================================

I love Pandas! But in production code I’m always a bit wary when I see:

.. code-block:: python

    import pandas as pd

    def foo(df: pd.DataFrame) -> pd.DataFrame:
        # do stuff
        return df

Because… How do I know which columns are supposed to be in `df`?

Using `strictly_typed_pandas`, we can be more explicit about what these data should look like.

.. code-block:: python

    from strictly_typed_pandas import DataSet

    class Schema:
        id: int
        name: str

    def foo(df: DataSet[Schema]) -> DataSet[Schema]:
        # do stuff
        return df

Where `DataSet`:
    * is a subclass of `pd.DataFrame` and hence has the same functionality as `DataFrame`.
    * validates whether the data adheres to the provided schema upon its initialization.
    * is immutable, so its schema cannot be changed using inplace modifications.

The `DataSet[Schema]` annotations are compatible with:
    * `mypy` for type checking during linting-time (i.e. while you write your code).
    * `typeguard` for type checking during run-time (i.e. while you run your unit tests).

To get the most out of `strictly_typed_pandas`, be sure to:
    * set up `mypy` in your IDE.
    * run your unit tests with `pytest --typeguard-packages=foo.bar` (where `foo.bar` is your package name).

Installation
============

.. code-block:: bash

    pip install strictly-typed-pandas


Documentation
=================
For example notebooks and API documentation, please see our `ReadTheDocs <https://strictly-typed-pandas.readthedocs.io/>`_.

FAQ
===

| **How is this different from Dataenforce / Pandera?**
| The main difference: `strictly_typed_pandas` works really well with `mypy`, allowing you to catch many of the errors during linting-time (i.e. while your coding), rather than during run-time.
|
| **Why use Python if you want static typing?**
| There are just so many good packages for data science in Python. Rather than sacrificing all of that by moving to a different language, I'd like to make the Pythonverse a little bit better.
|
| **I found a bug! What should I do?**
| Great! Contact me and I'll look into it.
|
| **I have a great idea to improve strictly_typed_pandas! How can we make this work?**
| Awesome, drop me a line!
