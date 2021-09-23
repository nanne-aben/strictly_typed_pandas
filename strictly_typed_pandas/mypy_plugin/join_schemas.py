def _get_schemas_and_all_their_superclasses(ctx, schemas):
    res = []
    for schema in schemas:
        class_and_superclasses = schema.type.mro[:-1]
        for c in class_and_superclasses:
            res.append(c)

    # can we replace this by 'object'?
    res.append(ctx.default_return_type.args[0].type.mro[-1])

    return res


def join_schemas(ctx):
    dataset = ctx.default_return_type
    join = dataset.args[0]
    schemas = join.args
    schemas_extended = _get_schemas_and_all_their_superclasses(schemas)

    # update join to be a subclass of these schemas
    ctx.default_return_type.args[0].type.mro = schemas_extended
    return ctx.default_return_type
