from typing import Any, TypeVar, get_type_hints


def _get_type_hints_from_join(join):
    for arg in join.__args__:
        pass


def schemas_are_equal(schema_expected, schema_observed) -> bool:
    if schema_expected == Any or isinstance(schema_expected, TypeVar):
        return True

    # Since Join is a Protocol, we cannot use isinstance(schema_expacted, Join), hence the following hack:
    if str(schema_expected).startswith("strictly_typed_pandas.core.join.Join["):
        type_hints_schema_expected = _get_type_hints_from_join(schema_expected)
    else:
        type_hints_schema_expected = get_type_hints(schema_expected)

    return get_type_hints(schema_observed) == type_hints_schema_expected
