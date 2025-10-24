from mypy_pure.decorators import pure


def custom_impure() -> None:
    pass


@pure
def bad() -> None:
    custom_impure()
