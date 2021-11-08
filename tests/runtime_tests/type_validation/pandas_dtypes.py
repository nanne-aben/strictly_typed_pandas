import pandas as pd
import numpy as np

from typing import Tuple, Literal

from strictly_typed_pandas.core.pandas_types_with_argument import (
    DatetimeTZDtype,
    PeriodDtype,
    SparseDtype,
    CategoricalDtype,
    IntervalDtype,
    StringDtype,
)


# for backward compatability with pandas 0.23 - 0.25
class BackwardCompatibility:
    def __init__(self, *args, **kwargs):
        pass


# ----------------------------------------
# These pandas dtypes have required params
# ----------------------------------------
if hasattr(pd, "PeriodDtype"):
    period = pd.PeriodDtype
    period_day = PeriodDtype[Tuple[Literal["freq"], Literal["D"]]]
    period_month = PeriodDtype[Tuple[Literal["freq"], pd.offsets.MonthEnd]]
else:
    period = BackwardCompatibility  # type: ignore
    period_day = BackwardCompatibility  # type: ignore
    period_month = BackwardCompatibility  # type: ignore

if hasattr(pd, "DatetimeTZDtype"):
    datetime_tz = pd.DatetimeTZDtype
    datetime_tz_utc = DatetimeTZDtype[Tuple[Literal["tz"], Literal["UTC"]]]
    datetime_tz_gmt = DatetimeTZDtype[Tuple[Literal["tz"], Literal["GMT"]]]
else:
    datetime_tz = BackwardCompatibility  # type: ignore
    datetime_tz_utc = BackwardCompatibility  # type: ignore
    datetime_tz_gmt = BackwardCompatibility  # type: ignore

# ----------------------------------------
# These pandas dtypes have optional params
# ----------------------------------------
if hasattr(pd, "SparseDtype"):
    sparse = pd.SparseDtype
    sparse_int64 = SparseDtype[Tuple[Literal["dtype"], np.int64]]
    sparse_float64 = SparseDtype[Tuple[Literal["dtype"], np.float64]]
else:
    sparse = BackwardCompatibility  # type: ignore
    sparse_int64 = BackwardCompatibility  # type: ignore
    sparse_float64 = BackwardCompatibility  # type: ignore

if hasattr(pd, "CategoricalDtype"):
    categorical = pd.CategoricalDtype
    categorical_abc = CategoricalDtype[Tuple[Literal["categories"], Literal["a", "b", "c"]]]
    categorical_def = CategoricalDtype[Tuple[Literal["categories"], Literal["d", "e", "f"]]]
else:
    categorical = BackwardCompatibility  # type: ignore
    categorical_abc = BackwardCompatibility  # type: ignore
    categorical_def = BackwardCompatibility  # type: ignore

if hasattr(pd, "IntervalDtype"):
    interval = pd.IntervalDtype
    interval_int64 = IntervalDtype[
        Tuple[
            Literal["subtype"], Literal["int64"],
            Literal["closed"], Literal["right"],
        ]
    ]
    interval_float64 = IntervalDtype[
        Tuple[
            Literal["subtype"], Literal["float64"],
            Literal["closed"], Literal["right"],
        ]
    ]
else:
    interval = BackwardCompatibility  # type: ignore
    interval_int64 = BackwardCompatibility  # type: ignore
    interval_float64 = BackwardCompatibility  # type: ignore

if hasattr(pd, "StringDtype"):
    string = pd.StringDtype
    string_python = StringDtype[Tuple[Literal["storage"], Literal["python"]]]
    string_pyarrow = StringDtype[Tuple[Literal["storage"], Literal["pyarrow"]]]
else:
    string = BackwardCompatibility  # type: ignore
    string_python = BackwardCompatibility  # type: ignore
    string_pyarrow = BackwardCompatibility  # type: ignore

# --------------------------------------------------
# These pandas dtypes are initialized without params
# --------------------------------------------------
if hasattr(pd, "Int64Dtype"):
    int64 = pd.Int64Dtype  # amongst others, e.g. pd.Int8Dtype
else:
    int64 = BackwardCompatibility  # type: ignore

if hasattr(pd, "BooleanDtype"):
    boolean = pd.BooleanDtype
else:
    boolean = BackwardCompatibility  # type: ignore
