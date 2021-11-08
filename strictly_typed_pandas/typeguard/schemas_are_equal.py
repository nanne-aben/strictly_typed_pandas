from typing import Any, TypeVar, get_type_hints

from strictly_typed_pandas.core.join import Join


def schemas_are_equal(schema_expected, schema_observed) -> bool:
    if schema_expected == Any or isinstance(schema_expected, TypeVar):
        return True

    if hasattr(schema_expected, "__origin__") and schema_expected.__origin__ == Join:
        # Since we always use Joins in combination with TypeVars, we should just return True here
        return True

    return get_type_hints(schema_observed) == get_type_hints(schema_expected)
