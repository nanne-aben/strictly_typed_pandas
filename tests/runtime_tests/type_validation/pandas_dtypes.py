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


# ----------------------------------------
# These pandas dtypes have required params
# ----------------------------------------
period = pd.PeriodDtype
period_day = PeriodDtype[Tuple[Literal["freq"], Literal["D"]]]
period_month = PeriodDtype[Tuple[Literal["freq"], pd.offsets.MonthEnd]]

datetime_tz = pd.DatetimeTZDtype
datetime_tz_utc = DatetimeTZDtype[Tuple[Literal["tz"], Literal["UTC"]]]
datetime_tz_gmt = DatetimeTZDtype[Tuple[Literal["tz"], Literal["GMT"]]]

# ----------------------------------------
# These pandas dtypes have optional params
# ----------------------------------------
sparse = pd.SparseDtype
sparse_int64 = SparseDtype[Tuple[Literal["dtype"], np.int64]]
sparse_float64 = SparseDtype[Tuple[Literal["dtype"], np.float64]]

categorical = pd.CategoricalDtype
categorical_abc = CategoricalDtype[Tuple[Literal["categories"], Literal["a", "b", "c"]]]
categorical_def = CategoricalDtype[Tuple[Literal["categories"], Literal["d", "e", "f"]]]


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

string = pd.StringDtype
string_python = StringDtype[Tuple[Literal["storage"], Literal["python"]]]
string_pyarrow = StringDtype[Tuple[Literal["storage"], Literal["pyarrow"]]]

# --------------------------------------------------
# These pandas dtypes are initialized without params
# --------------------------------------------------
int64 = pd.Int64Dtype  # amongst others, e.g. pd.Int8Dtype
boolean = pd.BooleanDtype
