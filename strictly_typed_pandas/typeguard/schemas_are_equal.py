import typeguard
import re

from typing import Any, TypeVar, get_type_hints

from strictly_typed_pandas.core.join import Join


def schemas_are_equal(schema_expected, schema_observed) -> bool:
    if schema_expected == Any or isinstance(schema_expected, TypeVar):
        return True

    # If schema_expected is a Join[...], it will be a _GenericAlias, so we cannot use isinstance(schema_expacted, Join)
    join_class_name = typeguard.qualified_name(Join)
    if re.match(f"^{join_class_name}\[.*\]$", str(schema_expected)):
        # Since we always use Joins in combination with TypeVars, we should just return True here
        return True

    return get_type_hints(schema_observed) == get_type_hints(schema_expected)
