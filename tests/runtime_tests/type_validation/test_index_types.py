import numpy as np
import pytest

import tests.runtime_tests.type_validation.pandas_dtypes as pdt

from typing import Any

from strictly_typed_pandas import IndexedDataSet

from tests.runtime_tests.type_validation.utils import is_backward_compatibility_type


class DataSchema:
    b: str


def test_supported_index_data_type():
    dtypes = [
        pdt.datetime_tz_utc, pdt.period_day, pdt.categorical, pdt.categorical_abc,
        pdt.interval, pdt.interval_float64, str, int, float,
        np.int, np.float, np.datetime64, np.timedelta64, Any, object, np.object
    ]
    for dtype in dtypes:
        if is_backward_compatibility_type(dtype):
            continue  # pragma: no cover

        class IndexSchema:
            a: dtype

        IndexedDataSet[IndexSchema, DataSchema]()


def test_unsupported_index_data_type():
    dtypes = [
        bool, np.bool_, pdt.sparse, pdt.sparse_int64
    ]
    for dtype in dtypes:
        class IndexSchema:
            a: dtype

        with pytest.raises(TypeError):
            IndexedDataSet[IndexSchema, DataSchema]()
