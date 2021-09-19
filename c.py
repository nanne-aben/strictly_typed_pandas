from typing import Generic, TypeVar

X = TypeVar("X", covariant=True)

class DataSet(Generic[X]):
    pass
