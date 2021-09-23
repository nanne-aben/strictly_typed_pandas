from functools import partial
from mypy.types import Instance
from mypy.nodes import Context


def _convert_schema_into_protocol(ctx, schema):
    analyzed = ctx.api.analyze_type(schema)
    if not isinstance(analyzed, Instance):
        return analyzed

    class_and_its_superclasses = analyzed.type.mro[:-1]
    for c in class_and_its_superclasses:
        c.is_protocol = True

    return analyzed


def _create_dataset(ctx, dataset_class_name):
    sym = ctx.api.lookup_qualified(dataset_class_name, Context())
    return sym.node


def _convert_schemas_into_protocols(ctx, dataset_class_name):
    schemas = ctx.type.args
    protocols = [_convert_schema_into_protocol(ctx, schema) for schema in schemas]
    dataset = _create_dataset(ctx, dataset_class_name)
    return Instance(dataset, protocols)


convert_dataset_schemas_into_protocols = partial(
    _convert_schemas_into_protocols,
    dataset_class_name="DataSet",
)
convert_indexed_dataset_schemas_into_protocols = partial(
    _convert_schemas_into_protocols,
    dataset_class_name="IndexedDataSet",
)
