"""Module with __mypy_pure__ containing only dotted names."""

__mypy_pure__ = [
    'external_module_with_pure.pure_func',  # Fully qualified name
    'external_module_with_pure.Nested.pure_func',  # Fully qualified nested name
]
