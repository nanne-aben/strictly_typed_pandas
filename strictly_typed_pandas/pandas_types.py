import pandas as pd


# for backward compatability with pandas 0.23 - 0.25
class BackwardCompatibility(pd.api.extensions.ExtensionDtype):
    name = "object"

    def __init__(self, *args, **kwargs) -> None:
        pass  # pragma: no cover


if hasattr(pd, "StringDtype"):
    StringDtype = pd.StringDtype
else:  # pragma: no cover
    class StringDtype(BackwardCompatibility):  # type: ignore
        pass


if hasattr(pd, "DatetimeTZDtype"):
    DatetimeTZDtype = pd.DatetimeTZDtype
else:  # pragma: no cover
    class DatetimeTZDtype(BackwardCompatibility):  # type: ignore
        pass


if hasattr(pd, "CategoricalDtype"):
    CategoricalDtype = pd.CategoricalDtype
else:  # pragma: no cover
    class CategoricalDtype(BackwardCompatibility):  # type: ignore
        pass


if hasattr(pd, "PeriodDtype"):
    PeriodDtype = pd.PeriodDtype
else:  # pragma: no cover
    class PeriodDtype(BackwardCompatibility):  # type: ignore
        pass


if hasattr(pd, "SparseDtype"):
    SparseDtype = pd.SparseDtype
else:  # pragma: no cover
    class SparseDtype(BackwardCompatibility):  # type: ignore
        pass


if hasattr(pd, "IntervalDtype"):
    IntervalDtype = pd.IntervalDtype
else:  # pragma: no cover
    class IntervalDtype(BackwardCompatibility):  # type: ignore
        pass


if hasattr(pd, "Int64Dtype"):
    Int64Dtype = pd.Int64Dtype
else:  # pragma: no cover
    class Int64Dtype(BackwardCompatibility):  # type: ignore
        pass


if hasattr(pd, "BooleanDtype"):
    BooleanDtype = pd.BooleanDtype
else:  # pragma: no cover
    class BooleanDtype(BackwardCompatibility):  # type: ignore
        pass
