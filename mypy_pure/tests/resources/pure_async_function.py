from mypy_pure.decorators import pure


@pure
async def pure_async_function() -> int:
    return 42


@pure
async def impure_async_function() -> None:
    print('This is impure')


class MyClass:
    @pure
    async def pure_async_method(self) -> int:
        return 42

    @pure
    async def impure_async_method(self) -> None:
        print('This is impure')
