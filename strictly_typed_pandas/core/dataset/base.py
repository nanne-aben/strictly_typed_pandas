import pandas as pd
import inspect

from abc import ABC, abstractmethod
from typing import Any

from strictly_typed_pandas.core.immutable import (
    _ImmutableiLocIndexer, _ImmutableLocIndexer, immutable_error_msg, inplace_argument_interceptor
)


_dataframe_functions = dict(inspect.getmembers(pd.DataFrame, predicate=inspect.isfunction))
_dataframe_member_names = dict(inspect.getmembers(pd.DataFrame)).keys()


class DataSetBase(pd.DataFrame, ABC):
    def __init__(self, *args, **kwargs) -> None:
        '''
        This class is a subclass of `pd.DataFrame`, hence it is initialized with the same parameters as a `DataFrame`.
        See the Pandas `DataFrame` documentation for more information.
        '''
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

        if name in self.columns and name not in _dataframe_member_names:
            raise NotImplementedError(immutable_error_msg)

    def __setitem__(self, key: Any, value: Any):
        raise NotImplementedError(immutable_error_msg)

    def __getattribute__(self, name: str) -> Any:
        attribute = object.__getattribute__(self, name)
        if name in _dataframe_functions:
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

    def _create_joined_schema(self, right: 'DataSetBase'):
        SchemaA = self._schema
        SchemaB = right._schema
        class JoinedSchema(SchemaA, SchemaB):  # type: ignore
            pass
        return JoinedSchema

    def to_dataframe(self) -> pd.DataFrame:
        '''
        Converts the object to a pandas `DataFrame`.
        '''
        return pd.DataFrame(self)

    def to_frame(self) -> pd.DataFrame:
        '''
        Synonym of to to_dataframe(): converts the object to a pandas `DataFrame`.
        '''
        return self.to_dataframe()
