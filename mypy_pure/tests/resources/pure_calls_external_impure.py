import external_module  # type: ignore[import-not-found]

from mypy_pure.decorators import pure


@pure
def pure_func() -> None:
    external_module.external_impure()
