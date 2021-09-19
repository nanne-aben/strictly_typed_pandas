from typing import TypeVar, Protocol


T = TypeVar("T", covariant=True)
V = TypeVar("V", covariant=True)


class Join(Protocol[T, V]):
    pass
