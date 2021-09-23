import pandas as pd

from typing import Generic, List, TypeVar, Union, get_type_hints, overload
from pandas._typing import FrameOrSeries

from strictly_typed_pandas.core.dataset.base import DataSetBase
from strictly_typed_pandas.core.join import Join
from strictly_typed_pandas.core.exact_match_for_protocols import ExactMatchForProtocols
from strictly_typed_pandas.core.validate_schema import (
    check_for_duplicate_columns, check_index_for_unsupported_datatypes, validate_schema
)
from strictly_typed_pandas.core.create_empty_dataframe import create_empty_indexed_dataframe


_IndexSchema = TypeVar("_IndexSchema")
_Schema = TypeVar("_Schema")
_OtherSchema = TypeVar("_OtherSchema")

class IndexedDataSet(Generic[_IndexSchema, _Schema], DataSetBase):
    '''
    `IndexedDataSet` allows for static type checking of indexed pandas DataFrames, for example:

    .. code-block:: python

        class IndexSchema:
            a: int

        class DataSchema:
            b: str

        df = (
            pd.DataFrame(
                {
                    "a": [1, 2, 3],
                    "b": ["1", "2", "3"]
                }
            )
            .set_index(["a"])
            .pipe(IndexedDataSet[IndexSchema, DataSchema])
        )

    Where `IndexedDataSet`:
        * is a subclass of `pd.DataFrame` and hence has the same functionality as `DataFrame`.
        * validates whether the data adheres to the provided schema upon its initialization.
        * is immutable, so its schema cannot be changed using inplace modifications.

    The `IndexedDataSet[Schema]` annotations are compatible with:
        * `mypy` for type checking during linting-time (i.e. while you write your code).
        * `typeguard` for type checking during run-time (i.e. while you run your unit tests).
    '''
    _exact_match_for_index_schema: ExactMatchForProtocols[_IndexSchema, _IndexSchema]
    _exact_match_for_schema: ExactMatchForProtocols[_Schema, _Schema]
    _index_schema = None
    _schema = None

    def _continue_initialization(self) -> None:
        self._index_schema = self._schema_annotations[0]
        self._schema = self._schema_annotations[1]

        index_schema_expected = get_type_hints(self._index_schema)
        schema_expected = get_type_hints(self._schema)

        check_for_duplicate_columns(
            set(index_schema_expected.keys()),
            set(schema_expected.keys())
        )

        if self.shape == (0, 0) and self.index.shape == (0,):
            df = create_empty_indexed_dataframe(index_schema_expected, schema_expected)
            super().__init__(df)
        else:
            check_index_for_unsupported_datatypes(index_schema_expected)

            schema_observed = dict(zip(self.columns, self.dtypes))
            index_schema_observed = {
                name: self.index.get_level_values(i).dtype
                for i, name in enumerate(self.index.names)
            }

            validate_schema(index_schema_expected, index_schema_observed)
            validate_schema(schema_expected, schema_observed)

    def _create_joined_indexed_dataset(
        self, df: pd.DataFrame, right: 'IndexedDataSet[_IndexSchema, _OtherSchema]'
        ) -> 'IndexedDataSet[_IndexSchema, Join[_Schema, _OtherSchema]]':
        schemas = {
            "IndexSchemaA": self._index_schema,
            "SchemaA": self._schema,
            "IndexSchemaB": right._index_schema,
            "SchemaB": right._schema,
        }
        for name, schema in schemas.items():
            if schema is None:
                raise TypeError(
                    f"During an operation of the form: \n" +
                    "df_a: IndexedDataSet[IndexSchemaA, SchemaA]\n" +
                    "df_b: IndexedDataSet[IndexSchemaB, SchemaB]\n" +
                    "join(df_a, df_b)\n" +
                    "The schema {name} could not be found. Please make sure that you " +
                    "initialize using IndexedDataSet[IndexSchemaA, SchemaA](), not IndexedDataSet()."
                )

        IndexSchema = self._index_schema
        JoinedSchema = self._create_joined_schema(right)
        return IndexedDataSet[IndexSchema, JoinedSchema](df)  # type: ignore

    @overload
    def merge(self, right: FrameOrSeries, *args, **kwargs) -> pd.DataFrame: ...

    @overload
    def merge( # type: ignore
        self, right: 'IndexedDataSet[_IndexSchema, _OtherSchema]', *args, **kwargs
        ) -> 'IndexedDataSet[_IndexSchema, Join[_Schema, _OtherSchema]]': ...

    def merge(self, right, *args, **kwargs):
        df = super().merge(right, *args, **kwargs)
        if isinstance(right, IndexedDataSet):
            df = self._create_joined_indexed_dataset(df, right)
        return df

    @overload
    def join(self, other: Union[pd.DataFrame, pd.Series, List[pd.DataFrame]], *args, **kwargs) -> pd.DataFrame: ...

    @overload
    def join( # type: ignore
        self, other: 'IndexedDataSet[_IndexSchema, _OtherSchema]', *args, **kwargs
        ) -> 'IndexedDataSet[_IndexSchema, Join[_Schema, _OtherSchema]]': ...

    def join(self, other, *args, **kwargs):
        df = super().join(other, *args, **kwargs)
        if isinstance(other, IndexedDataSet):
            df = self._create_joined_indexed_dataset(df, other)
        return df
