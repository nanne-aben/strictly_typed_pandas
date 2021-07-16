import typeguard

from strictly_typed_pandas import DataSet, IndexedDataSet


def check_dataset(argname: str, value, expected_type, memo: typeguard._TypeCheckMemo) -> None:
    schema_expected = expected_type.__args__[0]
    if not isinstance(value, DataSet):
        msg = "Type of {argname} must be a DataSet[{schema_expected}]; got {class_observed} instead"
        raise TypeError(
            msg.format(
                argname=argname,
                schema_expected=typeguard.qualified_name(schema_expected),
                class_observed=typeguard.qualified_name(value)
            )
        )

    schema_observed = value.__orig_class__.__args__[0]
    if schema_observed != schema_expected:
        msg = "Type of {argname} must be a DataSet[{schema_expected}]; got DataSet[{schema_observed}] instead"
        raise TypeError(
            msg.format(
                argname=argname,
                schema_expected=typeguard.qualified_name(schema_expected),
                schema_observed=typeguard.qualified_name(schema_observed)
            )
        )


def check_indexed_dataset(argname: str, value, expected_type, memo: typeguard._TypeCheckMemo):
    schema_index_expected = expected_type.__args__[0]
    schema_data_expected = expected_type.__args__[1]
    if not isinstance(value, IndexedDataSet):
        msg = (
            "Type of {argname} must be a IndexedDataSet[{schema_index_expected},{schema_data_expected}];" +
            "got {class_observed} instead"
        )
        raise TypeError(
            msg.format(
                argname=argname,
                schema_index_expected=typeguard.qualified_name(schema_index_expected),
                schema_data_expected=typeguard.qualified_name(schema_data_expected),
                class_observed=typeguard.qualified_name(value)
            )
        )

    schema_index_observed = value.__orig_class__.__args__[0]
    schema_data_observed = value.__orig_class__.__args__[1]
    if schema_index_observed != schema_index_expected or schema_data_observed != schema_data_expected:
        msg = (
            "Type of {argname} must be a IndexedDataSet[{schema_index_expected},{schema_data_expected}];" +
            "got IndexedDataSet[{schema_index_observed},{schema_data_observed}] instead"
        )
        raise TypeError(
            msg.format(
                argname=argname,
                schema_index_expected=typeguard.qualified_name(schema_index_expected),
                schema_data_expected=typeguard.qualified_name(schema_data_expected),
                schema_index_observed=typeguard.qualified_name(schema_index_observed),
                schema_data_observed=typeguard.qualified_name(schema_data_observed)
            )
        )


typeguard.origin_type_checkers[DataSet] = check_dataset
typeguard.origin_type_checkers[IndexedDataSet] = check_indexed_dataset
typechecked = typeguard.typechecked
