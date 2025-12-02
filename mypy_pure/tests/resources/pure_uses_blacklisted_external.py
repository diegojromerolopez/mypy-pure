import external_blacklisted_but_pure

from mypy_pure import pure


@pure
def uses_blacklisted_pure() -> None:
    # This should be OK because __mypy_pure__ in the module whitelists it,
    # overriding the blacklist in mypy.ini
    external_blacklisted_but_pure.pure_but_blacklisted()
