import os

from mypy_pure.decorators import pure


@pure
def bad() -> None:
    os.remove('file.txt')
