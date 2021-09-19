from strictly_typed_pandas import DataSet

class SchemaA:
    a: int
    id: int

class SchemaB:
    b: int
    id: int

class SchemaC:
    c: int
    id: int

class SchemaAB(SchemaA, SchemaB):
    pass

class SchemaABC(SchemaAB, SchemaC):
    pass


df_a = DataSet[SchemaA]({'a': [1], 'id': [1]})
df_b = DataSet[SchemaB]({'b': [1], 'id': [1]})
df: DataSet[SchemaAB] = df_a.merge(df_b, on='id')

df2: DataSet[SchemaAB] = df_a.join(df_b)

