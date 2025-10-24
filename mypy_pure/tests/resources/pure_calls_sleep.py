import time

from mypy_pure.decorators import pure


@pure
def wait() -> None:
    time.sleep(1)
