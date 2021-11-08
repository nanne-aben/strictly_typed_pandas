import pandas as pd
import inspect

from typing import Any, Dict, Generic, Literal, Tuple, TypeVar, Union
from typeguard import typeguard_ignore
from abc import ABC, abstractmethod
from enum import Enum


Params = TypeVar("Params")


class BackwardCompatibility(pd.api.extensions.ExtensionDtype):
    name = "object"

    def __init__(self, *args, **kwargs) -> None:
        pass  # pragma: no cover


class PandasTypeWithArgument(ABC, Generic[Params]):
    _params: Dict[str, Any] = {}
    _create_pandas_type = BackwardCompatibility

    def __setattr__(self, name: str, value: Any) -> None:
        object.__setattr__(self, name, value)

        if name == "__orig_class__" and hasattr(self.__orig_class__, "__args__"):  # type: ignore
            args = value.__args__
            self._continue_initialization(args)

    def _continue_initialization(self, args: Any) -> Any:
        unpacked_args = self._unpack_args(args)
        n = len(unpacked_args)
        if (n % 2) != 0:
            raise TypeError(
                "PandasTypeWithArgument expects an even number of parameters, found {n} instead."
            )

        params = {}
        for i in range(0, n, 2):
            key, value = self._unpack_key_value_pair(
                key=unpacked_args[i],
                value=unpacked_args[i+1],
            )
            params[key] = value

        self._params = params

    def _unpack_args(self, args: Any) -> Any:
        '''
        Up to Python 3.9, we cannot have a variable number of arguments, so we use tuples as follows:
            PandasTypeWithArgument[
                Tuple[
                    Literal[], Literal[],
                    Literal[], Literal[],
                    ...
                ]
            ]

        In the future, we'll use variadic generics (once they are supported). Then we'll get:
            PandasTypeWithArgument[
                Literal[], Literal[],
                Literal[], Literal[],
                ...
            ]

        We can distinguish these two cases by checking whether the first arg is a tuple or a literal.
        '''
        if self._is_tuple(args[0]):
            return self._unpack_tuple(args[0])
        else:
            return args

    def _unpack_key_value_pair(self, key: Any, value: Any) -> Tuple[str, Any]:
        '''
        For example:
            (Literal['id'], Literal[1234]) -> ('id', 1234)
            (Literal['categories'], Literal['a', 'b']) -> ('categories', ['a', 'b'])
            (Literal['period'], pd.offsets.MonthEnd) -> ('period', pd.offsets.MonthEnd())
        '''
        key = self._unpack_literal(key)

        if self._is_literal(value):
            value = self._unpack_literal(value)

        if inspect.isclass(value):
            value = value()

        return key, value

    def _is_tuple(self, value: Any) -> bool:
        if not hasattr(value, "__origin__"):
            return False
        else:
            return value.__origin__ == tuple

    def _unpack_tuple(self, tup: Any) -> Any:
        return tup.__args__

    def _is_literal(self, value: Any) -> bool:
        if not hasattr(value, "__origin__"):
            return False
        else:
            return value.__origin__ == Literal

    @typeguard_ignore  # typeguard mixes up Tuple and tuple, so disabling it for now
    def _unpack_literal(
        self, literal: Any
    ) -> Union[int, str, bool, bytes, Enum, Tuple[Union[int, str, bool, bytes, Enum]]]:
        '''
        Unpacks literals into either int, str, bool, bytes, enum, or a tuple thereof, e.g.:
            Literal['a'] -> 'a'
            Literal['a', 'b', 'c'] -> ('a', 'b', 'c')
        '''
        value = literal.__args__

        if len(value) == 1:
            value = value[0]

        return value

    def create_pandas_type(self):
        return self._create_pandas_type(**self._params)


class DatetimeTZDtype(PandasTypeWithArgument[Params]):
    if hasattr(pd, "DatetimeTZDtype"):
        _create_pandas_type = pd.DatetimeTZDtype  # type: ignore


class CategoricalDtype(PandasTypeWithArgument[Params]):
    if hasattr(pd, "CategoricalDtype"):
        _create_pandas_type = pd.CategoricalDtype  # type: ignore


class PeriodDtype(PandasTypeWithArgument[Params]):
    if hasattr(pd, "PeriodDtype"):
        _create_pandas_type = pd.PeriodDtype  # type: ignore


class SparseDtype(PandasTypeWithArgument[Params]):
    if hasattr(pd, "SparseDtype"):
        _create_pandas_type = pd.SparseDtype  # type: ignore


class IntervalDtype(PandasTypeWithArgument[Params]):
    if hasattr(pd, "IntervalDtype"):
        _create_pandas_type = pd.IntervalDtype  # type: ignore


class StringDtype(PandasTypeWithArgument[Params]):
    if hasattr(pd, "StringDtype"):
        _create_pandas_type = pd.StringDtype  # type: ignore
