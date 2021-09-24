import typeguard

from strictly_typed_pandas import IndexedDataSet
from strictly_typed_pandas.typeguard.schemas_are_equal import schemas_are_equal


def _raise_not_an_indexed_dataset(argname, value):
    class_observed = typeguard.qualified_name(value)
    raise TypeError(f"Type of {argname} must be an IndexedDataSet; got {class_observed} instead.")


def _raise_improperly_annotated_dataset(argname, expected_type):  # pragma: no cover
    expected_type = typeguard.qualified_name(expected_type)
    raise TypeError(f"Type of {argname} must be IndexedDataSet[IndexSchema, DataSchema]; got {expected_type} instead.")


def _raise_schema_observed_is_none(argname, schema_index_expected, schema_data_expected):
    schema_index_expected = typeguard.qualified_name(schema_index_expected)
    schema_data_expected = typeguard.qualified_name(schema_data_expected)
    raise TypeError(
        f"The IndexedDataSet {argname} lacks one or more schemas. It has likely been initialized as " +
        "IndexedDataSet(). Please initialize it as " +
        f"IndexedDataSet[{schema_index_expected}, {schema_data_expected}]() instead."
    )


def _raise_schemas_are_not_equal(
    argname, schema_index_expected, schema_data_expected, schema_index_observed, schema_data_observed
):
    schema_index_expected = typeguard.qualified_name(schema_index_expected)
    schema_data_expected = typeguard.qualified_name(schema_data_expected)
    schema_index_observed = typeguard.qualified_name(schema_index_observed)
    schema_data_observed = typeguard.qualified_name(schema_data_observed)
    raise TypeError(
        f"Type of {argname} must be a IndexedDataSet[{schema_index_expected},{schema_data_expected}];" +
        f"got IndexedDataSet[{schema_index_observed},{schema_data_observed}] instead"
    )


def check_indexed_dataset(argname: str, value, expected_type, memo: typeguard._TypeCheckMemo) -> None:
    if not isinstance(value, IndexedDataSet):
        _raise_not_an_indexed_dataset(argname, value)

    if not hasattr(expected_type, "__args__") or len(expected_type.__args__) != 2:
        # This should never happen in the current implementation of typeguard, but it can't hurt to check
        _raise_improperly_annotated_dataset(argname, expected_type)  # pragma: no cover

    schema_index_expected = expected_type.__args__[0]
    schema_data_expected = expected_type.__args__[1]
    schema_index_observed = value._index_schema
    schema_data_observed = value._schema

    if schema_index_observed is None or schema_data_observed is None:
        _raise_schema_observed_is_none(argname, schema_index_expected, schema_data_expected)

    if not schemas_are_equal(schema_index_expected, schema_index_observed):
        _raise_schemas_are_not_equal(
            argname, schema_index_expected, schema_data_expected, schema_index_observed, schema_data_observed
        )

    if not schemas_are_equal(schema_data_expected, schema_data_observed):
        _raise_schemas_are_not_equal(
            argname, schema_index_expected, schema_data_expected, schema_index_observed, schema_data_observed
        )
