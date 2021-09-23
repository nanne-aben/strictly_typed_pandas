from mypy.plugin import Plugin

from strictly_typed_pandas.mypy_plugin.convert_schemas_into_protocols import (
    convert_dataset_schemas_into_protocols,
    convert_indexed_dataset_schemas_into_protocols,
)
from strictly_typed_pandas.mypy_plugin.join_schemas import join_schemas


DATASET_CLASS = "strictly_typed_pandas.dataset.dataset.DataSet"
INDEXED_DATASET_CLASS = "strictly_typed_pandas.dataset.indexeddataset.IndexedDataSet"
JOIN_METHODS = (
    [f"{DATASET_CLASS}.{method}" for method in ["join", "merge"]] +
    [f"{INDEXED_DATASET_CLASS}.{method}" for method in ["join"]]
)


class CustomPlugin(Plugin):
    def get_type_analyze_hook(self, fullname):
        if fullname == DATASET_CLASS:
            return convert_dataset_schemas_into_protocols
        if fullname == INDEXED_DATASET_CLASS:
            return convert_indexed_dataset_schemas_into_protocols

    def get_method_hook(self, fullname: str):
        if fullname in JOIN_METHODS:
            return join_schemas


def plugin(version: str):
    return CustomPlugin
