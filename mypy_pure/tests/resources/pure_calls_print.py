from mypy_pure.decorators import pure


@pure
def log() -> None:
    print('Hello')
