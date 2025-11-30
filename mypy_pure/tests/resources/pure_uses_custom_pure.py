from mypy_pure import pure


def custom_pure_function() -> None:
    """This function is marked as pure via config."""
    pass


@pure
def uses_custom_pure() -> None:
    """This should NOT error because custom_pure_function is in pure_functions config."""
    custom_pure_function()
