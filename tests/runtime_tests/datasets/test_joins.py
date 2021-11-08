import pytest
import pandas as pd

from typing import get_type_hints

from strictly_typed_pandas import DataSet, IndexedDataSet


class IndexSchema:
    id_a: int
    id_b: str


class IndexSchemaReversedOrder:
    id_b: str
    id_a: int


class IndexSchemaNoOverlap:
    id: int


class SchemaA:
    a: int


class SchemaB:
    b: int


class SchemaAB(SchemaA, SchemaB):
    pass


def test_joins():
    df_a = DataSet[SchemaA]()
    df_b = DataSet[SchemaB]()

    df_ab = df_a.join(df_b)
    assert get_type_hints(df_ab._schema) == get_type_hints(SchemaAB)

    df_ab = df_a.merge(df_b, left_index=True, right_index=True)
    assert get_type_hints(df_ab._schema) == get_type_hints(SchemaAB)


def test_indexed_dataset_joins():
    df_a = IndexedDataSet[IndexSchema, SchemaA]()
    df_b = IndexedDataSet[IndexSchemaReversedOrder, SchemaB]()

    df_ab = df_a.join(df_b)
    assert get_type_hints(df_ab._index_schema) == get_type_hints(IndexSchema)
    assert get_type_hints(df_ab._schema) == get_type_hints(SchemaAB)

    df_ab = df_a.merge(df_b, left_index=True, right_index=True)
    assert get_type_hints(df_ab._index_schema) == get_type_hints(IndexSchema)
    assert get_type_hints(df_ab._schema) == get_type_hints(SchemaAB)


def test_join_with_empty_schema():
    df_a = DataSet()
    df_b = DataSet[SchemaB]()
    with pytest.raises(TypeError):
        df_a.join(df_b)
    with pytest.raises(TypeError):
        df_b.join(df_a)

    df_a = (
        pd.DataFrame(
            {
                "id_a": [1, 2, 3],
                "id_b": ["1", "2", "3"],
            }
        )
        .set_index(["id_a", "id_b"])
        .pipe(IndexedDataSet)
    )
    df_b = IndexedDataSet[IndexSchema, SchemaB]()
    with pytest.raises(TypeError):
        df_a.join(df_b)
    with pytest.raises(TypeError):
        df_b.join(df_a)


def test_joins_with_non_overlapping_index():
    df_a = IndexedDataSet[IndexSchema, SchemaA]()
    df_b = IndexedDataSet[IndexSchemaNoOverlap, SchemaB]()

    with pytest.raises(ValueError):
        df_a.join(df_b)

    with pytest.raises(ValueError):
        df_b.join(df_a)
