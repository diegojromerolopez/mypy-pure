from mypy_pure.decorators import pure


@pure
def a() -> int:
    return 1


@pure
def b() -> int:
    return a()
