from mypy_pure.decorators import pure


class MyClass:
    @pure
    def pure_instance_method(self) -> int:
        return 42

    @pure
    def impure_instance_method(self) -> None:
        print('This is impure')
