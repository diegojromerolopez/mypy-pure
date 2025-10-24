from mypy_pure.decorators import pure


@pure
def good() -> int:
    return 1 + 1
