import external_module_with_pure

from mypy_pure import pure


@pure
def uses_external_pure() -> None:
    external_module_with_pure.pure_func()


@pure
def uses_external_nested_pure() -> None:
    # This should also be OK because Nested.pure_func is in __mypy_pure__
    external_module_with_pure.Nested.pure_func()
