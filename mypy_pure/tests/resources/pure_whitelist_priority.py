from mypy_pure import pure


@pure
def uses_print() -> None:
    """This calls print which is blacklisted, but we'll whitelist it in config."""
    print('This should be OK because print is whitelisted')
