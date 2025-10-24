from typing import Callable, ParamSpec, TypeVar, cast

P = ParamSpec('P')
R = TypeVar('R')


def pure(func: Callable[P, R]) -> Callable[P, R]:
    setattr(func, '__pure__', True)
    return cast(Callable[P, R], func)
