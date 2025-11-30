__mypy_pure__ = [
    'pure_func',
    'Nested.pure_func',
]


def pure_func() -> None:
    pass


class Nested:
    @staticmethod
    def pure_func() -> None:
        pass


def impure_func() -> None:
    print('impure')
