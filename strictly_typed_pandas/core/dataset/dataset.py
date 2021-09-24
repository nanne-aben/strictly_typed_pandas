import pandas as pd

from typing import Generic, List, TypeVar, Union, get_type_hints, overload
from pandas._typing import FrameOrSeries

from strictly_typed_pandas.core.dataset.base import DataSetBase
from strictly_typed_pandas.core.join import Join
from strictly_typed_pandas.core.exact_match_for_protocols import ExactMatchForProtocols
from strictly_typed_pandas.core.validate_schema import validate_schema
from strictly_typed_pandas.core.create_empty_dataframe import create_empty_dataframe


_Schema = TypeVar("_Schema")
_OtherSchema = TypeVar("_OtherSchema")


class DataSet(Generic[_Schema], DataSetBase):
    '''
    `DataSet` allows for static type checking of pandas DataFrames, for example:

    .. code-block:: python

        class Schema:
            a: int

        DataSet[Schema]({"a": [1, 2, 3]})

    Where `DataSet`:
        * is a subclass of `pd.DataFrame` and hence has the same functionality as `DataFrame`.
        * validates whether the data adheres to the provided schema upon its initialization.
        * is immutable, so its schema cannot be changed using inplace modifications.

    The `DataSet[Schema]` annotations are compatible with:
        * `mypy` for type checking during linting-time (i.e. while you write your code).
        * `typeguard` for type checking during run-time (i.e. while you run your unit tests).
    '''
    _exact_match_for_schema: ExactMatchForProtocols[_Schema, _Schema]
    _schema = None

    def _continue_initialization(self) -> None:
        self._schema = self._schema_annotations[0]
        schema_expected = get_type_hints(self._schema)

        if self.shape == (0, 0):
            df = create_empty_dataframe(schema_expected)
            super().__init__(df)
        else:
            schema_observed = dict(zip(self.columns, self.dtypes))
            validate_schema(schema_expected, schema_observed)

    def _create_joined_dataset(
        self, df: pd.DataFrame, right: 'DataSet[_OtherSchema]'
    ) -> 'DataSet[Join[_Schema, _OtherSchema]]':
        schemas = {
            "SchemaA": self._schema,
            "SchemaB": right._schema,
        }
        for name, schema in schemas.items():
            if schema is None:
                raise TypeError(
                    "During an operation of the form: \n" +
                    "df_a: DataSet[SchemaA]\n" +
                    "df_b: DataSet[SchemaB]\n" +
                    "join(df_a, df_b)\n" +
                    f"The schema {name} could not be found. Please make sure that you " +
                    "initialize using DataSet[SchemaA](), not DataSet()."
                )

        JoinedSchema = self._create_joined_schema(right)
        return DataSet[JoinedSchema](df)  # type: ignore

    @overload
    def merge(  # type: ignore
        self, right: 'DataSet[_OtherSchema]', *args, **kwargs) -> 'DataSet[Join[_Schema, _OtherSchema]]': ...

    @overload
    def merge(self, right: FrameOrSeries, *args, **kwargs) -> pd.DataFrame: ...

    def merge(self, right, *args, **kwargs):
        df = super().merge(right, *args, **kwargs)
        if isinstance(right, DataSet):
            df = self._create_joined_dataset(df, right)
        return df

    @overload
    def join(  # type: ignore
        self, other: 'DataSet[_OtherSchema]', *args, **kwargs) -> 'DataSet[Join[_Schema, _OtherSchema]]': ...

    @overload
    def join(self, other: Union[pd.DataFrame, pd.Series, List[pd.DataFrame]], *args, **kwargs) -> pd.DataFrame: ...

    def join(self, other, *args, **kwargs):
        df = super().join(other, *args, **kwargs)
        if isinstance(other, DataSet):
            df = self._create_joined_dataset(df, other)
        return df
