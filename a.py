from typing import TypeVar, Protocol
from c import DataSet

T = TypeVar("T", covariant=True)
V = TypeVar("V", covariant=True)

class Join(Protocol[T, V]):
    pass

class SchemaA:
    a: int

class SchemaB:
    b: int

class SchemaC:
    c: int

class SchemaAB(SchemaA, SchemaB):
    pass

class SchemaABC(SchemaAB, SchemaC):
    pass

U = TypeVar("U")
W = TypeVar("W")

def foo(a: DataSet[U], b: DataSet[W]) -> DataSet[Join[U, W]]:
    return DataSet()

a: DataSet[SchemaAB] = foo(DataSet[SchemaA](), DataSet[SchemaB]())
b: DataSet[SchemaA] = foo(DataSet[SchemaA](), DataSet[SchemaB]())
c: DataSet[SchemaA] = foo(DataSet[SchemaA](), DataSet[SchemaC]())

d: DataSet[SchemaAB] = foo(DataSet[SchemaA](), DataSet[SchemaB]())
e: DataSet[SchemaABC] = foo(d, DataSet[SchemaC]())
