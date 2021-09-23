import inspect

from typing import Any, Callable, Optional
from pandas.core.indexing import _iLocIndexer, _LocIndexer


immutable_error_msg = (
    "To ensure that the DataSet adheres to its schema, you cannot perform inplace modifications. You can either use " +
    "dataset.to_dataframe() to cast the DataSet to a DataFrame, or use operations that return a DataFrame, e.g. " +
    "df = df.assign(...)."
)


class _ImmutableiLocIndexer(_iLocIndexer):
    def __setitem__(self, key: Any, value: Any) -> None:
        raise NotImplementedError(immutable_error_msg)


class _ImmutableLocIndexer(_LocIndexer):
    def __setitem__(self, key: Any, value: Any) -> None:
        raise NotImplementedError(immutable_error_msg)


def _get_index_of_inplace_in_args(call: Callable) -> Optional[int]:
    signature = inspect.signature(call)
    parameters = signature.parameters.keys()

    if "inplace" in parameters:
        return [i for i, v in enumerate(parameters) if v == "inplace"][0]
    else:
        return None


def inplace_argument_interceptor(call: Callable) -> Callable:
    inplace_ind = _get_index_of_inplace_in_args(call)

    def func(*args, **kwargs):
        if inplace_ind is not None and inplace_ind < len(args) and args[inplace_ind]:
            raise NotImplementedError(immutable_error_msg)

        if "inplace" in kwargs and kwargs["inplace"]:
            raise NotImplementedError(immutable_error_msg)

        return call(*args, **kwargs)

    return func
