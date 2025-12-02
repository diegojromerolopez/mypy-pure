from mypy_pure import pure


@pure
def is_even(n: int) -> bool:
    if n == 0:
        return True
    return is_odd(n - 1)


@pure
def is_odd(n: int) -> bool:
    if n == 0:
        return False
    return is_even(n - 1)
