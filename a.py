from typing import overload

@overload
def foo(a: int) -> int: ...

@overload
def foo(a: str) -> str: ...

def foo(a):
    return a

a: int = foo(1)
b: str = foo(1)
