from mypy_pure.decorators import pure


def custom_impure1() -> None:
    pass


def custom_impure2() -> None:
    pass


@pure
def pure_func() -> None:
    custom_impure1()
    custom_impure2()
