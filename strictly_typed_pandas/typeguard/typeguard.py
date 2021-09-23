import typeguard

from strictly_typed_pandas import DataSet, IndexedDataSet
from strictly_typed_pandas.typeguard.check_dataset import check_dataset
from strictly_typed_pandas.typeguard.check_indexed_dataset import check_indexed_dataset


typeguard.origin_type_checkers[DataSet] = check_dataset
typeguard.origin_type_checkers[IndexedDataSet] = check_indexed_dataset
