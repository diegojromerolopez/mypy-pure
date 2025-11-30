from mypy_pure.decorators import pure


class MyClass:
    @property
    @pure
    def pure_property(self) -> int:
        return 42

    @property
    @pure
    def impure_property(self) -> None:
        print('This is impure')
        return None
