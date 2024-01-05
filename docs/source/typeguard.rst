Typeguard
=========

We use typeguard in strictly typed pandas to as an additional runtime check, as described in earlier sections. As per typeguard 3.0.0, a number of breaking changes were introduced, which we couldn't reconcile with strictly typed pandas. Other packages that depend on typeguard 2.13.3 are in a similar situation.

However, the ``typeguard<=2.13.3`` requirement became problematic over time, as it meant people could not use strictly typed pandas together with packages that depend on ``typeguard>=3.0.0``. For this reason, we have decided to vendor typeguard in ``strictly_typed_pandas==0.2.0``, meaning that we include typeguard within the strictly typed pandas code base, rather than having it as a dependency.

In this document, we outline how you can use typeguard with ``strictly_typed_pandas>=0.2.0``.

With typeguard 2.13.3 (backwards compatibility)
-----------------------------------------------

To support backwards compatibility, we allow you to use typeguard with ``strictly_typed_pandas>=0.2.0`` by simply installing ``typeguard==2.13.3``, without any other changes required. This can be done by running:

.. code-block:: bash

    pip install typeguard==2.13.3

You can use all functionality from typeguard as before:

Decorator
^^^^^^^^^

.. code-block:: python

    from typeguard import typechecked

    @typechecked
    def foo(df: DataSet[Person]) -> DataSet[Person]:
        ...

Import hook
^^^^^^^^^^^

.. code-block:: python

    from typeguard import install_import_hook

    install_import_hook('my_app')
    from my_app import some_module  # import only AFTER installing the hook, or it won't take effect

Pytest plugin
^^^^^^^^^^^^^

.. code-block:: bash

    pytest --typeguard-packages=my_app

With the vendored typeguard version (recommended)
-------------------------------------------------

We recommend that you use the vendored typeguard version, as it is the most future-proof solution.

Decorator
^^^^^^^^^

You can use the vendored version as follows:

.. code-block:: python

    from strictly_typed_pandas.typeguard import typechecked

    @typechecked
    def foo(df: DataSet[Person]) -> DataSet[Person]:
        ...

If you also want to use a second typeguard version in your project (e.g. ``typeguard>=3.0.0``), you can pip install that version and then you can use the following:

.. code-block:: python

    from typeguard import typechecked as typechecked_vanilla

    @typechecked_vanilla
    def foo(a: int) -> int:
        ...

Note that ``@typechecked_vanilla`` will not work with strictly typed pandas types; you can only use it for projects that do not use strictly typed pandas.

Import hook
^^^^^^^^^^^

The import hook is currently not supported in the vendored version. It should be possible to add support for this, but we have not done so yet. If you would like to use the import hook, please open an issue.

Of course, you can still use the import hook with the vanilla version, as follows:

.. code-block:: python

    from typeguard import install_import_hook

    install_import_hook('my_app')
    from my_app import some_module  # import only AFTER installing the hook, or it won't take effect

Pytest plugin
^^^^^^^^^^^^^

To use the vendored version of the pytest plugin, you can use the following:

.. code-block:: bash

    pytest --stp-typeguard-packages=my_app

If you also want to use a second typeguard version in your project (e.g. ``typeguard>=3.0.0``), you can pip install that version and then you can use the following:

.. code-block:: bash

    pytest --typeguard-packages=my_other_app

You can also use them at the same time:

.. code-block:: bash

    pytest --stp-typeguard-packages=my_app --typeguard-packages=my_other_app

Please don't define the same package in both flags, this will raise an error.
