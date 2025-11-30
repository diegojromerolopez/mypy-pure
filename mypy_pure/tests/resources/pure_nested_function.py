from mypy_pure.decorators import pure


@pure
def outer_function() -> int:
    @pure
    def pure_nested() -> int:
        return 42

    @pure
    def impure_nested() -> None:
        print('This is impure')

    return pure_nested()


@pure
def outer_calls_impure_nested() -> None:
    @pure
    def impure_nested() -> None:
        print('This is impure')

    impure_nested()
