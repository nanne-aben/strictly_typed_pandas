import typeguard

from strictly_typed_pandas import DataSet
from strictly_typed_pandas.typeguard.schemas_are_equal import schemas_are_equal


def _raise_not_a_dataset(argname, value):
    class_observed = typeguard.qualified_name(value)
    raise TypeError(f"Type of {argname} must be a DataSet; got {class_observed} instead.")


def _raise_improperly_annotated_dataset(argname, expected_type):  # pragma: no cover
    expected_type = typeguard.qualified_name(expected_type)
    raise TypeError(f"Type of {argname} must be DataSet[Schema]; got {expected_type} instead.")


def _raise_schema_observed_is_none(argname, schema_expected):
    schema_expected = typeguard.qualified_name(schema_expected)
    raise TypeError(
        f"The DataSet {argname} has no associated schema. It has likely been initialized as DataSet(). " +
        f"Please initialize it as DataSet[{schema_expected}]() instead."
    )


def _raise_schemas_are_not_equal(argname, schema_expected, schema_observed):
    schema_expected = typeguard.qualified_name(schema_expected)
    schema_observed = typeguard.qualified_name(schema_observed)
    raise TypeError(f"Type of {argname} must be a DataSet[{schema_expected}]; got DataSet[{schema_observed}] instead")


def check_dataset(argname: str, value, expected_type, memo: typeguard._TypeCheckMemo) -> None:
    if not isinstance(value, DataSet):
        _raise_not_a_dataset(argname, value)

    if not hasattr(expected_type, "__args__") or len(expected_type.__args__) != 1:
        # This should never happen in the current implementation of typeguard, but it can't hurt to check
        _raise_improperly_annotated_dataset(argname, expected_type)  # pragma: no cover

    schema_expected = expected_type.__args__[0]
    schema_observed = value._schema

    if schema_observed is None:
        _raise_schema_observed_is_none(argname, schema_expected)

    if not schemas_are_equal(schema_expected, schema_observed):
        _raise_schemas_are_not_equal(argname, schema_expected, schema_observed)
