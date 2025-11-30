from mypy_pure.decorators import pure


class MyClass:
    @staticmethod
    @pure
    def pure_static_method() -> int:
        return 42

    @staticmethod
    @pure
    def impure_static_method() -> None:
        print('This is impure')
