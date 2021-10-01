import typeguard

from mypy.plugin import Plugin

from strictly_typed_pandas import DataSet, IndexedDataSet
from strictly_typed_pandas.mypy_plugin.convert_schemas_into_protocols import (
    convert_dataset_schemas_into_protocols,
    convert_indexed_dataset_schemas_into_protocols,
)
from strictly_typed_pandas.mypy_plugin.join_schemas import join_schemas


_DATASET_CLASS = typeguard.qualified_name(DataSet)
_INDEXED_DATASET_CLASS = typeguard.qualified_name(IndexedDataSet)
_JOIN_FUNCTIONS = ["join", "merge"]
_JOIN_METHODS = (
    [f"{_DATASET_CLASS}.{method}" for method in _JOIN_FUNCTIONS] +
    [f"{_INDEXED_DATASET_CLASS}.{method}" for method in _JOIN_FUNCTIONS]
)


class CustomPlugin(Plugin):
    def get_type_analyze_hook(self, fullname):
        if fullname == _DATASET_CLASS:
            return convert_dataset_schemas_into_protocols
        if fullname == _INDEXED_DATASET_CLASS:
            return convert_indexed_dataset_schemas_into_protocols

    def get_method_hook(self, fullname: str):
        if fullname in _JOIN_METHODS:
            return join_schemas


def plugin(version: str):
    return CustomPlugin
