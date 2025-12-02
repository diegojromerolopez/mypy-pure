from mypy_pure import decorators


@decorators.pure
def pure_func() -> None:
    pass
