import pandas as pd
import numpy as np  # type: ignore

import tests.runtime_tests.type_validation.pandas_dtypes as pdt

from typing import Any

from tests.runtime_tests.type_validation.utils import check_list_of_types


def test_numeric_base_python_types():
    check_list_of_types(int, [np.int64, np.int_, np.integer, int], [float, np.float])
    check_list_of_types(float, [np.float64, np.float_, float], [int, np.int_])
    check_list_of_types(bool, [np.bool_, bool], [int, np.int_])


def test_numpy_types():
    check_list_of_types(np.int64, [np.int64, np.int_, np.integer, int], [float, np.float_])
    check_list_of_types(np.float64, [np.float64, np.float_, float], [int, np.int_])
    check_list_of_types(np.bool, [np.bool_, bool], [int, np.int_])
    check_list_of_types(
        np.datetime64, [np.datetime64],
        [np.timedelta64, pdt.datetime_tz_utc, np.int_]
    )
    check_list_of_types(np.timedelta64, [np.timedelta64], [np.datetime64, np.int64])


def test_pandas_types_without_any_arguments():
    check_list_of_types(pdt.int64, [pdt.int64], [pdt.interval, np.int64, int])
    check_list_of_types(pdt.boolean, [pdt.boolean], [pdt.int64, np.bool, bool])


def test_pandas_types_with_optional_arguments():
    check_list_of_types(pdt.categorical, [pdt.categorical], [pdt.categorical_abc, pdt.int64, np.int, int])
    check_list_of_types(
        pdt.categorical_abc,
        [pdt.categorical, pdt.categorical_abc],
        [pdt.categorical_def, pdt.int64, np.int, int]
    )

    check_list_of_types(pdt.interval, [pdt.interval], [pdt.interval_float64, pdt.int64, np.int, int])
    check_list_of_types(
        pdt.interval_int64,
        [pdt.interval, pdt.interval_int64],
        [pdt.interval_float64, pdt.int64, np.int, int]
    )

    check_list_of_types(pdt.sparse, [pdt.sparse], [pdt.sparse_int64, np.int64, int])
    check_list_of_types(pdt.sparse_int64, [pdt.sparse, pdt.sparse_int64], [pdt.sparse_float64, np.int64, int])


def test_pandas_types_with_required_arguments():
    check_list_of_types(pdt.datetime_tz_utc, [pdt.datetime_tz_utc], [np.datetime64, pdt.datetime_tz_gmt, np.int])
    check_list_of_types(pdt.period_day, [pdt.period_day], [np.datetime64, pdt.period_month, np.int])


def test_strings():
    check_list_of_types(str, [str, pdt.string, pdt.string_python], [pdt.string_pyarrow, int, np.int, pdt])
    check_list_of_types(pdt.string, [str, pdt.string, pdt.string_python], [pdt.string_pyarrow, int, np.int])

    check_list_of_types(pdt.string_pyarrow, [str, pdt.string, pdt.string_pyarrow], [pdt.string_python, int, np.int])
    check_list_of_types(pdt.string_python, [str, pdt.string, pdt.string_python], [pdt.string_pyarrow, int, np.int])

    # as long as this is true
    df = pd.DataFrame({"a": ["a", "b", "c"]})
    assert df.dtypes[0] == object
    # we'll need to do this
    check_list_of_types(object, [str], [pdt.string, pdt.string_python, pdt.string_pyarrow])


def test_pandas_types_with_arguments_backward_compatibility():
    # Using notation such as 'DateTimeTZDtype(tz="UTC") as a type is not recommended anymore.
    # Use DateTimeTZDtype[Tuple[Literal["tz"], Literal["UTC"]]] instead.
    # Testing the old syntax here for backward compatibility.
    check_list_of_types(
        pdt.datetime_tz(tz="UTC"),
        [pdt.datetime_tz(tz="UTC")],
        [np.datetime64, pdt.datetime_tz(tz="GMT"), np.int]
    )
    check_list_of_types(
        pdt.period(freq="D"),
        [pdt.period(freq="D")],
        [np.datetime64, pdt.period(freq="W"), np.int]
    )
    check_list_of_types(
        pdt.sparse(dtype=np.int64),
        [pdt.sparse(dtype=np.int64)],
        [np.int64, pdt.sparse(dtype=np.float64), int]
    )


def test_any():
    check_list_of_types(Any, [], [int, np.int_])
    check_list_of_types(object, [], [int, np.int_])
    check_list_of_types(np.object, [], [int, np.int_])
