import os

from mypy_pure.decorators import pure


def impure_leaf() -> None:
    os.remove('file.txt')


def intermediate_2() -> None:
    impure_leaf()


def intermediate_1() -> None:
    intermediate_2()


@pure
def bad() -> None:
    intermediate_1()
