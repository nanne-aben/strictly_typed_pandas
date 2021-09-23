import typeguard

from typing import Any, TypeVar, get_type_hints

from strictly_typed_pandas.core.join import Join


def schemas_are_equal(schema_expected, schema_observed) -> bool:
    if schema_expected == Any or isinstance(schema_expected, TypeVar):
        return True

    if str(schema_expected).startswith("strictly_typed_pandas.core.join.Join["):
        return True  # this could be done a bit more neatly

    return get_type_hints(schema_observed) == get_type_hints(schema_expected)
