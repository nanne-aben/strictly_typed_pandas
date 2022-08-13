import pandas as pd
import numpy as np
import inspect

from typing import Any

from strictly_typed_pandas import DataSet
from strictly_typed_pandas.core.pandas_types import BackwardCompatibility


def is_backward_compatibility_type(dtype) -> bool:
    if isinstance(dtype, BackwardCompatibility):
        return True  # pragma: no cover

    if dtype not in [Any, np.integer]:
        if inspect.isclass(dtype) and issubclass(dtype, BackwardCompatibility):
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
