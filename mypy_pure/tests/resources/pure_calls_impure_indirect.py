import os

from mypy_pure.decorators import pure


def impure_parent() -> None:
    os.remove('file.txt')


@pure
def bad() -> None:
    impure_parent()
