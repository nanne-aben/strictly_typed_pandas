import pandas as pd


if hasattr(pd, "_typing"):
    from pandas._typing import FrameOrSeries
else:  # pragma: no cover
    FrameOrSeries = Union[pd.DatetimeIndex, pd.Series]  # type: ignore