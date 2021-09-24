from strictly_typed_pandas import DataSet

class SchemaA:
    a: int

class SchemaB:
    b: int

class SchemaAB(SchemaA, SchemaB):
    pass

df_a = DataSet[SchemaA]()
df_b = DataSet[SchemaB]()
df_ab: DataSet[SchemaAB] = df_a.merge(df_b)
