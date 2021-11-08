import inspect
import pandas as pd
import numpy as np  # type: ignore

from typing import Any, Callable, Dict
from pandas.api.extensions import ExtensionDtype

from strictly_typed_pandas.core.pandas_types_with_argument import PandasTypeWithArgument
from strictly_typed_pandas.core.pandas_types import StringDtype


def create_empty_dataframe(schema: Dict[str, Any]) -> pd.DataFrame:
    res = dict()
    for name, dtype in schema.items():
        if dtype == Any:
            dtype = object

        if inspect.isclass(dtype) and issubclass(dtype, ExtensionDtype):
            dtype = dtype().name

        if isinstance(dtype, ExtensionDtype):
            dtype = dtype.name

        if isinstance(dtype, Callable) and isinstance(dtype(), PandasTypeWithArgument):  # type: ignore
            dtype = dtype().create_pandas_type()

        if dtype == np.datetime64:
            dtype = "datetime64[ns]"

        if dtype == np.timedelta64:
            dtype = "timedelta64[ns]"

        if dtype == str:
            dtype = StringDtype.name

        res[name] = pd.Series([], dtype=dtype)

    return pd.DataFrame(res)


def create_empty_indexed_dataframe(index_schema: Dict[str, Any], data_schema: Dict[str, Any]) -> pd.DataFrame:
    df_index = create_empty_dataframe(index_schema)
    df_data = create_empty_dataframe(data_schema)
    return (
        pd.concat([df_index, df_data], axis=1)
        .set_index(list(index_schema.keys()))
    )
