from mypy_pure import pure


@pure
def uses_dotted_names() -> None:
    # Module declares external_module_with_pure.pure_func as pure
    # This tests the else branch in __load_module_pure_functions (line 65)
    pass
