from mypy.plugin import Plugin
from mypy.types import Instance
from mypy.nodes import Context


def foo(ctx):
    res = []
    for arg in ctx.default_return_type.args[0].args:
        for c in arg.type.mro[:-1]:
            res.append(c)
    res.append(ctx.default_return_type.args[0].type.mro[-1])
    ctx.default_return_type.args[0].type.mro = res
    return ctx.default_return_type


def foo2(ctx):
    arg_types = []
    for arg in ctx.type.args:
        analyzed = ctx.api.analyze_type(arg)
        if isinstance(analyzed, Instance):
            for superclass in analyzed.type.mro[:-1]:
                superclass.is_protocol = True
        arg_types.append(analyzed)
    sym = ctx.api.lookup_qualified('DataSet', Context())
    return Instance(sym.node, arg_types)

class CustomPlugin(Plugin):
    def get_function_hook(self, fullname: str):
        if fullname == 'a.foo':
            return foo

    def get_type_analyze_hook(self, fullname):
        # print(fullname)
        if fullname == "c.DataSet":
            return foo2


def plugin(version: str):
    return CustomPlugin
