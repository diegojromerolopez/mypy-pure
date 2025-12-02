"""Module that will be blacklisted but declares itself pure."""

__mypy_pure__ = ['pure_but_blacklisted']


def pure_but_blacklisted() -> None:
    pass
