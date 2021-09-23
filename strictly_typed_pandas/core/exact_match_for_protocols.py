from typing import Generic, TypeVar


_SchemaCovariant = TypeVar("_SchemaCovariant", covariant=True)
_SchemaContravariant = TypeVar("_SchemaContravariant", contravariant=True)


class ExactMatchForProtocols(Generic[_SchemaCovariant, _SchemaContravariant]):
    '''
    Note that this class should only really be used internally in Strictly Typed Pandas.

    The strictly_typed_pandas mypy plugin transforms all schemas used within a DataSet[Schema] to a Protocol.
    However, Protocols don't act exactly like we want them to. Suppose we'd have:

    .. code-block:: python
        class SchemaA(Protocol):
            a: int

        class SchemaAB(Protocol):
            a: int
            b: int

    When T is covariant, mypy behaves in the following way:

    .. code-block:: python
        T = TypeVar('T', covariant=True)

        class DataSet[Generic[T]]:
            pass

        df_a: DataSet[SchemaA] = DataSet[SchemaA]()  # no error
        df_b: DataSet[SchemaAB] = DataSet[SchemaA]()  # mypy error
        df_c: DataSet[SchemaA] = DataSet[SchemaAB]()  # no error, even though we'd want one!

    When T is contravariant, mypy behaves in the following way:

    .. code-block:: python
        T = TypeVar('T', contravariant=True)

        class DataSet[Generic[T]]:
            pass

        df_a: DataSet[SchemaA] = DataSet[SchemaA]()  # no error
        df_b: DataSet[SchemaAB] = DataSet[SchemaA]()  # no error, even though we'd want one!
        df_c: DataSet[SchemaA] = DataSet[SchemaAB]()  # mypy error

    To get the behaviour we want, we'll combine them using ExactMatchForProtocols.

    .. code-block:: python
        T = TypeVar('T')

        class DataSet[Generic[T]]:
            _exact_match_for_protocols = ExactMatchForProtocols[T, T]

    Now we have:
    .. code-block:: python
        df_a: DataSet[SchemaA] = DataSet[SchemaA]()  # no error
        df_b: DataSet[SchemaAB] = DataSet[SchemaA]()  # mypy error
        df_c: DataSet[SchemaA] = DataSet[SchemaAB]()  # mypy error
    '''
    pass
