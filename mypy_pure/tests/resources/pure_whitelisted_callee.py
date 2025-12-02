from mypy_pure import pure


def impure_func() -> None:
    print('impure')


@pure
def uses_whitelisted_callee() -> None:
    impure_func()
