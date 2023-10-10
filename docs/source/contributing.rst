============
Contributing
============

We welcome contributions! To set up your development environment, we recommend using pyenv. You can find more on how to install ``pyenv`` and ``pyenv-virtualen`` here:

* https://github.com/pyenv/pyenv
* https://github.com/pyenv/pyenv-virtualenv

To set up the environment, run:

.. code-block:: bash

    pyenv install 3.11
    pyenv virtualenv 3.11 strictly_typed_pandas
    pyenv activate strictly_typed_pandas
    pip install -r requirements.txt
    pip install -r requirements-dev.txt

For a list of currently supported Python versions, we refer to ``.github/workflows/build.yml``.

---------------
Pre-commit hook
---------------
We use ``pre-commit`` to run a number of checks on the code before it is committed. To install the pre-commit hook, run:

.. code-block:: bash

    pre-commit install
