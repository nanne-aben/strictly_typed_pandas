import inspect
from abc import ABC
from typing import Any, Generic, TypeVar, get_type_hints

import pandas as pd

from strictly_typed_pandas.create_empty_dataframe import (
    create_empty_dataframe,
    create_empty_indexed_dataframe,
)
from strictly_typed_pandas.immutable import (
    _ImmutableiLocIndexer,
    _ImmutableLocIndexer,
    immutable_error_msg,
    inplace_argument_interceptor,
)
from strictly_typed_pandas.validate_schema import check_for_duplicate_columns, validate_schema

dataframe_functions = dict(inspect.getmembers(pd.DataFrame, predicate=inspect.isfunction))
dataframe_member_names = dict(inspect.getmembers(pd.DataFrame)).keys()


class DataSetBase(pd.DataFrame, ABC):
    def __init__(self, *args, **kwargs) -> None:
        """This class is a subclass of `pd.DataFrame`, hence it is initialized with the
        same parameters as a `DataFrame`.

        See the Pandas `DataFrame` documentation for more information.
        """
        super().__init__(*args, **kwargs)

        if self.columns.duplicated().any():
            msg = "DataSet has duplicate columns: {cols}".format(
                cols=self.columns[self.columns.duplicated()]
            )
            raise TypeError(msg)

    def __setattr__(self, name: str, value: Any) -> None:
        object.__setattr__(self, name, value)

        if name in self.columns and name not in dataframe_member_names:
            raise NotImplementedError(immutable_error_msg)

    def __setitem__(self, key: Any, value: Any):
        raise NotImplementedError(immutable_error_msg)

    def __getattribute__(self, name: str) -> Any:
        if name in dataframe_functions:
            attribute = dataframe_functions[name].__get__(self, type(self))
            return inplace_argument_interceptor(attribute)
        else:
            return object.__getattribute__(self, name)

    @property
    def iloc(self) -> _ImmutableiLocIndexer:  # type: ignore
        return _ImmutableiLocIndexer("iloc", self)  # type: ignore

    @property
    def loc(self) -> _ImmutableLocIndexer:  # type: ignore
        return _ImmutableLocIndexer("loc", self)  # type: ignore

    def to_dataframe(self) -> pd.DataFrame:
        """Converts the object to a pandas `DataFrame`."""
        return pd.DataFrame(self)

    def to_frame(self) -> pd.DataFrame:
        """Synonym of to to_dataframe(): converts the object to a pandas `DataFrame`."""
        return self.to_dataframe()


T = TypeVar("T")
V = TypeVar("V")


class DataSet(Generic[T], DataSetBase):
    """`DataSet` allows for static type checking of pandas DataFrames, for example:

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
        * `typeguard` (<3.0) for type checking during run-time (i.e. while you run your unit tests).
    """

    _schema_annotations = None

    def __class_getitem__(cls, item):
        """Allows us to define a schema for the ``DataSet``."""
        cls = super().__class_getitem__(item)
        cls._schema_annotations = item
        return cls

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if DataSet._schema_annotations is None:
            return

        schema_expected = get_type_hints(DataSet._schema_annotations)
        DataSet._schema_annotations = None

        if self.shape == (0, 0):
            df = create_empty_dataframe(schema_expected)
            super().__init__(df)
        else:
            schema_observed = dict(zip(self.columns, self.dtypes))
            validate_schema(schema_expected, schema_observed)


class IndexedDataSet(Generic[T, V], DataSetBase):
    """`IndexedDataSet` allows for static type checking of indexed pandas DataFrames,
    for example:

    .. code-block:: text

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
        * `typeguard` (<3.0) for type checking during run-time (i.e. while you run your unit tests).
    """

    _schema_index = None
    _schema_data = None

    def __class_getitem__(cls, item):
        """Allows us to define a schema for the ``DataSet``."""
        cls = super().__class_getitem__(item)
        cls._schema_index = item[0]
        cls._schema_data = item[1]
        return cls

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if IndexedDataSet._schema_index is None or IndexedDataSet._schema_data is None:
            return

        schema_index_expected = get_type_hints(IndexedDataSet._schema_index)
        schema_data_expected = get_type_hints(IndexedDataSet._schema_data)
        IndexedDataSet._schema_index = None
        IndexedDataSet._schema_data = None

        check_for_duplicate_columns(
            set(schema_index_expected.keys()), set(schema_data_expected.keys())
        )

        if self.shape == (0, 0) and self.index.shape == (0,):
            df = create_empty_indexed_dataframe(schema_index_expected, schema_data_expected)
            super().__init__(df)
        else:
            schema_data_observed = dict(zip(self.columns, self.dtypes))
            schema_index_observed = {
                name: self.index.get_level_values(i).dtype
                for i, name in enumerate(self.index.names)
            }

            if all(name is None for name in self.index.names):
                raise TypeError("No named columns in index. Did you remember to set the index?")

            validate_schema(schema_index_expected, schema_index_observed)
            validate_schema(schema_data_expected, schema_data_observed)
