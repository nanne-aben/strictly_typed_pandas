import pandas as pd
from strictly_typed_pandas import DataSet


class Schema:
    a: int


class Schema2:
    a: int
    b: int


a: DataSet[Schema] = pd.DataFrame({'a': [1]}).abs()