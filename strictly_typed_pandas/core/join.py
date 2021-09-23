from typing import TypeVar, Protocol


_SchemaA = TypeVar("_SchemaA", covariant=True)
_SchemaB = TypeVar("_SchemaB", covariant=True)


class Join(Protocol[_SchemaA, _SchemaB]):
    '''
    Note that this class should only really be used internally in Strictly Typed Pandas.

    Join[] allows for function signatures such as:

    .. code-block:: python
        def join(left: DataSet[SchemaA], right: DataSet[SchemaB]) -> DataSet[Join[SchemaA, SchemaB]]:
            ...

        df_ab: DataSet[SchemaAB] = join(df_a, df_b)

    Join[] only works in this way:

    - for a small set of relevant methods in DataSet and IndexedDataSet
    - when the strictly_typed_pandas mypy plugin is enabled

    All relevant functionality is implemented in mypy_plugin.py.

    When the strictly_typed_pandas mypy plugin is not enabled, this class will function as an Any
    (since it's essentially an empty Protocol), thereby providing backward compatibility.
    '''
    pass
