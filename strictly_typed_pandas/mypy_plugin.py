from mypy.plugin import Plugin
from mypy.types import Instance
from mypy.nodes import Context


DATASET_CLASSES = ["strictly_typed_pandas.dataset.DataSet"]
JOIN_METHODS = ["strictly_typed_pandas.dataset.DataSet.merge"]


def join_schemas(ctx):
    res = []
    for arg in ctx.default_return_type.args[0].args:
        for c in arg.type.mro[:-1]:
            res.append(c)
    res.append(ctx.default_return_type.args[0].type.mro[-1])
    ctx.default_return_type.args[0].type.mro = res
    return ctx.default_return_type


def turn_schemas_into_protocol(ctx):
    arg_types = []
    for arg in ctx.type.args:
        analyzed = ctx.api.analyze_type(arg)
        if isinstance(analyzed, Instance):
            for c in analyzed.type.mro[:-1]:
                c.is_protocol = True
        arg_types.append(analyzed)
    sym = ctx.api.lookup_qualified('DataSet', Context())
    return Instance(sym.node, arg_types)


class CustomPlugin(Plugin):
    def get_type_analyze_hook(self, fullname):
        if fullname in DATASET_CLASSES:
            return turn_schemas_into_protocol

    def get_method_hook(self, fullname: str):
        if fullname in JOIN_METHODS:
            return join_schemas


def plugin(version: str):
    return CustomPlugin
