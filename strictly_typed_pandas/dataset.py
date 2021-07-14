import pandas as pd
import inspect

from abc import ABC, abstractmethod
from typing import Any, Union, Callable, Generic, TypeVar, Tuple, get_type_hints, overload

from strictly_typed_pandas.immutable import (
    _ImmutableiLocIndexer, _ImmutableLocIndexer, immutable_error_msg, inplace_argument_interceptor
)
from strictly_typed_pandas.validate_schema import (
    check_for_duplicate_columns, check_index_for_unsupported_datatypes, validate_schema
)
from strictly_typed_pandas.create_empty_dataframe import create_empty_dataframe, create_empty_indexed_dataframe


dataframe_functions = dict(inspect.getmembers(pd.DataFrame, predicate=inspect.isfunction))
dataframe_member_names = dict(inspect.getmembers(pd.DataFrame)).keys()


class DataSetBase(pd.DataFrame, ABC):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        if self.columns.duplicated().any():
            msg = "DataSet has duplicate columns: {cols}".format(
                cols=self.columns[self.columns.duplicated()]
            )
            raise TypeError(msg)

        # In Python 3.6, self._schema_annotations is set before __init__() is called, hence we continue here
        if hasattr(self, "_schema_annotations"):
            self._continue_initialization()

    def __setattr__(self, name: str, value: Any) -> None:
        object.__setattr__(self, name, value)

        if name == "__orig_class__" and hasattr(self.__orig_class__, "__args__"):
            self._schema_annotations = value.__args__

            # In Python 3.7 and above, self._schema_annotations is set after the __init__() is wrapped up, hence we
            # continue from here
            if hasattr(self, "shape"):
                self._continue_initialization()

        if name in self.columns and name not in dataframe_member_names:
            raise NotImplementedError(immutable_error_msg)

    def __setitem__(self, key: Any, value: Any):
        raise NotImplementedError(immutable_error_msg)

    def __getattribute__(self, name: str) -> Any:
        attribute = object.__getattribute__(self, name)
        if name in dataframe_functions:
            return inplace_argument_interceptor(attribute)
        else:
            return attribute

    @property
    def iloc(self) -> _ImmutableiLocIndexer:
        return _ImmutableiLocIndexer("iloc", self)  # type: ignore

    @property
    def loc(self) -> _ImmutableLocIndexer:
        return _ImmutableLocIndexer("loc", self)  # type: ignore

    @abstractmethod
    def _continue_initialization(self) -> None:
        pass  # pragma: no cover

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self)

    def to_frame(self) -> pd.DataFrame:
        return self.to_dataframe()


T = TypeVar("T")
V = TypeVar("V")


class DataSet(Generic[T], DataSetBase):
    '''
    DataSet allows for static type checking of pandas DataFrames, for example:

    class Schema:
        a: int

    DataSet[Schema]({"a": [1, 2, 3]})

    DataSet is a subclass of pd.DataFrame, hence it is initialized with the same parameters as a DataFrame.
    '''
    def _continue_initialization(self) -> None:
        schema_expected = get_type_hints(self._schema_annotations[0])

        if self.shape == (0, 0):
            df = create_empty_dataframe(schema_expected)
            super().__init__(df)
        else:
            schema_observed = dict(zip(self.columns, self.dtypes))
            validate_schema(schema_expected, schema_observed)


class IndexedDataSet(Generic[T, V], DataSetBase):
    '''
    IndexedDataSet allows for static type checking of indexed pandas DataFrames, for example:

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
    '''
    def _continue_initialization(self) -> None:
        schema_index_expected = get_type_hints(self._schema_annotations[0])
        schema_data_expected = get_type_hints(self._schema_annotations[1])

        check_for_duplicate_columns(
            set(schema_index_expected.keys()),
            set(schema_data_expected.keys())
        )

        if self.shape == (0, 0) and self.index.shape == (0,):
            df = create_empty_indexed_dataframe(schema_index_expected, schema_data_expected)
            super().__init__(df)
        else:
            check_index_for_unsupported_datatypes(schema_index_expected)

            schema_data_observed = dict(zip(self.columns, self.dtypes))
            schema_index_observed = {
                name: self.index.get_level_values(i).dtype
                for i, name in enumerate(self.index.names)
            }

            validate_schema(schema_index_expected, schema_index_observed)
            validate_schema(schema_data_expected, schema_data_observed)
