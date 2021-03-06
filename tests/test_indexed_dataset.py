import pytest
import pandas as pd
import numpy as np  # type: ignore

from strictly_typed_pandas import IndexedDataSet
from strictly_typed_pandas.pandas_types import StringDtype


class IndexSchema:
    a: int
    b: str


class DataSchema:
    c: int
    d: str


class AlternativeIndexSchema:
    a: int


class AlternativeDataSchema:
    f: int


def test_empty_indexed_dataset() -> None:
    df = IndexedDataSet[IndexSchema, DataSchema]()

    assert df.shape[0] == 0
    assert np.all(df.index.names == ["a", "b"])
    assert np.all(df.columns == ["c", "d"])

    assert df.index.get_level_values(0).dtype == int
    assert df.index.get_level_values(1).dtype == object

    assert df.dtypes[0] == int
    assert df.dtypes[1] == object or isinstance(df.dtypes[1], StringDtype)


def test_indexed_dataset() -> None:
    (
        pd.DataFrame(
            {
                "a": [1, 2, 3],
                "b": ["a", "b", "c"],
                "c": [1, 2, 3],
                "d": ["a", "b", "c"]
            }
        )
        .set_index(["a", "b"])
        .pipe(IndexedDataSet[IndexSchema, DataSchema])
    )


def test_overlapping_columns():
    with pytest.raises(TypeError):
        IndexedDataSet[IndexSchema, IndexSchema]()


def foo(df: IndexedDataSet[IndexSchema, DataSchema]) -> IndexedDataSet[IndexSchema, DataSchema]:
    return df


def test_typeguard_indexed_dataset() -> None:
    foo(IndexedDataSet[IndexSchema, DataSchema]())

    with pytest.raises(TypeError):
        foo(IndexedDataSet[AlternativeIndexSchema, AlternativeDataSchema]())  # type: ignore

    with pytest.raises(TypeError):
        foo(pd.DataFrame())  # type: ignore
