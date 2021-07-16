import numpy as np
import warnings

from typing import Dict, Any, Set
from pandas.core.dtypes.common import is_dtype_equal
from pandas.api.extensions import ExtensionDtype

from strictly_typed_pandas.pandas_types import BooleanDtype, Int64Dtype, SparseDtype, StringDtype


def check_for_duplicate_columns(names_index: Set[str], names_data: Set[str]) -> None:
    intersection = names_index & names_data
    if len(intersection) > 0:
        msg = "The following column is present in both the index schema and the data schema: {}"
        raise TypeError(msg.format(intersection))


def check_index_for_unsupported_datatypes(schema: Dict[str, Any]) -> None:
    unsupported_dtypes = [bool, np.bool_, Int64Dtype, BooleanDtype, StringDtype]
    dtypes = [dtype for _, dtype in schema.items() if dtype in unsupported_dtypes or isinstance(dtype, SparseDtype)]
    if len(dtypes) > 0:
        msg = (
            "As of Pandas 1.2.4, there is no support for the following data types in the index: {}. While this " +
            "may change in future versions, we sugget you proceed with caution."
        )
        warnings.warn(msg.format(dtypes), SyntaxWarning)


def validate_schema(schema_expected: Dict[str, Any], schema_observed: Dict[str, Any]):
    _check_names(set(schema_expected.keys()), set(schema_observed.keys()))
    _check_dtypes(schema_expected, schema_observed)


def _check_names(names_expected: Set[str], names_observed: Set[str]) -> None:
    diff = names_observed - names_expected
    if diff:
        raise TypeError(
            "Data contains the following columns not present in schema: {diff}".format(
                diff=diff
            )
        )

    diff = names_expected - names_observed
    if diff:
        raise TypeError(
            "Schema contains the following columns not present in data: {diff}".format(
                diff=diff
            )
        )


def _check_dtypes(schema_expected: Dict[str, Any], schema_observed: Dict[str, Any]) -> None:
    for name, dtype_expected in schema_expected.items():
        dtype_observed = schema_observed[name]

        if dtype_expected in [object, np.object_, Any]:
            continue

        if dtype_expected == str and dtype_observed == object:
            continue  # pandas stores strings as objects by default

        if dtype_expected == str and isinstance(dtype_observed, StringDtype):
            continue  # since np.int64 == int, I'd say we should also support pd.StringDtype == str

        if isinstance(dtype_observed, np.dtype) and dtype_observed != np.object_:
            if dtype_observed == dtype_expected or np.issubdtype(dtype_observed, dtype_expected):
                continue

        if isinstance(dtype_expected, ExtensionDtype) and is_dtype_equal(dtype_expected, dtype_observed):
            continue

        if dtype_observed != object and isinstance(dtype_observed, dtype_expected):
            continue

        msg = "Column {name} is of type {dtype_observed}, but the schema suggests {dtype_expected}"

        if isinstance(dtype_observed, np.dtype):
            dtype_observed = "numpy." + str(dtype_observed)

        raise TypeError(
            msg.format(name=name, dtype_observed=dtype_observed, dtype_expected=dtype_expected)
        )
