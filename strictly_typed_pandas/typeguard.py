import inspect
import typeguard
from typing import Any, Tuple, Union
from strictly_typed_pandas import DataSet, IndexedDataSet


def check_dataset(value: Any, origin_type: Any, args: Tuple[Any, ...],  memo: typeguard.TypeCheckMemo) -> None:
    schema_expected = args[0]
    if not isinstance(value, DataSet):
        msg = "Type must be a DataSet[{schema_expected}]; got {class_observed} instead".format(
                schema_expected=typeguard.qualified_name(schema_expected),
                class_observed=typeguard.qualified_name(value)
            )
        if memo.config.typecheck_fail_callback:
            memo.config.typecheck_fail_callback(typeguard.TypeCheckError(msg), memo)
        else:
            raise TypeError(msg)

    schema_observed = value.__orig_class__.__args__[0]
    if schema_observed != schema_expected:
        msg = "Type must be a DataSet[{schema_expected}]; got DataSet[{schema_observed}] instead".format(
                schema_expected=typeguard.qualified_name(schema_expected),
                schema_observed=typeguard.qualified_name(schema_observed)
            )
        if memo.config.typecheck_fail_callback:
            memo.config.typecheck_fail_callback(typeguard.TypeCheckError(msg), memo)
        else:
            raise TypeError(msg)


def check_indexed_dataset(value: Any, origin_type: Any, args: Tuple[Any, ...],  memo: typeguard.TypeCheckMemo) -> None:
    schema_index_expected = args[0]
    schema_data_expected = args[1]
    if not isinstance(value, IndexedDataSet):
        msg = (
            "Type must be a IndexedDataSet[{schema_index_expected},{schema_data_expected}];" +
            "got {class_observed} instead"
        ).format(
                schema_index_expected=typeguard.qualified_name(schema_index_expected),
                schema_data_expected=typeguard.qualified_name(schema_data_expected),
                class_observed=typeguard.qualified_name(value)
            )

        if memo.config.typecheck_fail_callback:
            memo.config.typecheck_fail_callback(typeguard.TypeCheckError(msg), memo)
        else:
            raise TypeError(msg)

    schema_index_observed = value.__orig_class__.__args__[0]
    schema_data_observed = value.__orig_class__.__args__[1]
    if schema_index_observed != schema_index_expected or schema_data_observed != schema_data_expected:
        msg = (
            "Type must be a IndexedDataSet[{schema_index_expected},{schema_data_expected}];" +
            "got IndexedDataSet[{schema_index_observed},{schema_data_observed}] instead"
        ).format(
              schema_index_expected=typeguard.qualified_name(schema_index_expected),
              schema_data_expected=typeguard.qualified_name(schema_data_expected),
              schema_index_observed=typeguard.qualified_name(schema_index_observed),
              schema_data_observed=typeguard.qualified_name(schema_data_observed)
        )
        if memo.config.typecheck_fail_callback:
            memo.config.typecheck_fail_callback(typeguard.TypeCheckError(msg), memo)
        else:
            raise TypeError(msg)


def check_dataset_lookup(origin_type: Any,
                         args: Tuple[Any, ...], extras: Tuple[Any, ...]) -> Union[typeguard.TypeCheckerCallable, None]:

    if not inspect.isclass(origin_type):
        return None

    if issubclass(origin_type, DataSet):
        return check_dataset
    if issubclass(origin_type, IndexedDataSet):
        return check_indexed_dataset

    return None


typeguard.checker_lookup_functions.append(check_dataset_lookup)
typechecked = typeguard.typechecked
