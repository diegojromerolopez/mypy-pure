from mypy_pure.decorators import pure


class MyClass:
    @classmethod
    @pure
    def pure_class_method(cls) -> int:
        return 42

    @classmethod
    @pure
    def impure_class_method(cls) -> None:
        print('This is impure')
