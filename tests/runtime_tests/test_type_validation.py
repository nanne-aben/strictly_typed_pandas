import pandas as pd
import numpy as np  # type: ignore
import pytest

from typing import Any, Callable

from strictly_typed_pandas import DataSet, IndexedDataSet
from strictly_typed_pandas.core.pandas_types import (
    BackwardCompatibility,
    BooleanDtype,
    CategoricalDtype,
    DatetimeTZDtype,
    Int64Dtype,
    IntervalDtype,
    PeriodDtype,
    SparseDtype,
    StringDtype
)


def is_backward_compatibility_type(dtype) -> bool:
    if isinstance(dtype, BackwardCompatibility):
        return True  # pragma: no cover

    if dtype not in [Any, np.integer]:
        if isinstance(dtype, Callable) and isinstance(dtype(), BackwardCompatibility):  # type: ignore
            return True  # pragma: no cover

    return False


def are_they_equal(observed, expected):
    if is_backward_compatibility_type(observed) or is_backward_compatibility_type(expected):
        return np.nan  # pragma: no cover

    class SchemaExpected:
        a: expected

    class SchemaObserved:
        a: observed

    df = DataSet[SchemaObserved]()

    try:
        DataSet[SchemaExpected](df)
    except TypeError:
        return False

    return True


def check_list_of_types(observed, expected_to_match, expected_to_fail):
    expected_to_match += [object, np.object_, Any]
    matches = pd.Series([are_they_equal(observed, expected) for expected in expected_to_match])
    assert matches.dropna().all()

    fails = pd.Series([are_they_equal(observed, expected) for expected in expected_to_fail])
    assert not fails.dropna().any()


def test_numeric_base_python_types():
    check_list_of_types(int, [np.int64, np.int_, np.integer, int], [float, np.float])
    check_list_of_types(float, [np.float64, np.float_, float], [int, np.int_])
    check_list_of_types(bool, [np.bool_, bool], [int, np.int_])


def test_numpy_types():
    check_list_of_types(np.int64, [np.int64, np.int_, np.integer, int], [float, np.float_])
    check_list_of_types(np.float64, [np.float64, np.float_, float], [int, np.int_])
    check_list_of_types(np.bool, [np.bool_, bool], [int, np.int_])
    check_list_of_types(np.datetime64, [np.datetime64], [np.timedelta64, DatetimeTZDtype(tz="UTC"), np.int_])
    check_list_of_types(np.timedelta64, [np.timedelta64], [np.datetime64, np.int64])


def test_pandas_types():
    check_list_of_types(
        DatetimeTZDtype(tz="UTC"),
        [DatetimeTZDtype(tz="UTC")],
        [np.datetime64, DatetimeTZDtype(tz="GMT"), np.int]
    )
    check_list_of_types(CategoricalDtype, [CategoricalDtype], [Int64Dtype, np.int, int])
    check_list_of_types(
        PeriodDtype(freq="D"),
        [PeriodDtype(freq="D")],
        [np.datetime64, PeriodDtype(freq="W"), np.int]
    )
    check_list_of_types(
        SparseDtype(dtype=np.int64),
        [SparseDtype(dtype=np.int64)],
        [np.int64, SparseDtype(dtype=np.float64), int]
    )
    check_list_of_types(IntervalDtype, [IntervalDtype], [Int64Dtype, np.int, int])
    check_list_of_types(Int64Dtype, [Int64Dtype], [IntervalDtype, np.int64, int])
    check_list_of_types(BooleanDtype, [BooleanDtype], [IntervalDtype, np.bool, bool])


def test_strings():
    check_list_of_types(str, [str, StringDtype], [int, np.int])
    check_list_of_types(StringDtype, [str, StringDtype], [int, np.int])

    # as long as this is true
    df = pd.DataFrame({"a": ["a", "b", "c"]})
    assert df.dtypes[0] == object
    # we'll need to do this
    check_list_of_types(object, [str], [StringDtype])


def test_any():
    check_list_of_types(Any, [], [int, np.int_])
    check_list_of_types(object, [], [int, np.int_])
    check_list_of_types(np.object, [], [int, np.int_])


class DataSchema:
    b: str


def test_supported_index_data_type():
    dtypes = [
        DatetimeTZDtype(tz="UTC"), CategoricalDtype, PeriodDtype(freq="D"), IntervalDtype, str, int, float, np.int,
        np.float, np.datetime64, np.timedelta64, Any, object, np.object
    ]
    for dtype in dtypes:
        if is_backward_compatibility_type(dtype):
            continue  # pragma: no cover

        class IndexSchema:
            a: dtype

        IndexedDataSet[IndexSchema, DataSchema]()


def test_unsupported_index_data_type():
    dtypes = [bool, np.bool_, SparseDtype(dtype=np.int64), Int64Dtype, BooleanDtype, StringDtype]
    for dtype in dtypes:
        class IndexSchema:
            a: dtype

        with pytest.raises(TypeError):
            IndexedDataSet[IndexSchema, DataSchema]()
