from mypy_pure import pure


@pure
def factorial(n: int) -> int:
    """Test recursive function - will be visited multiple times during analysis."""
    if n <= 1:
        return 1
    return n * factorial(n - 1)


@pure
def fibonacci(n: int) -> int:
    """Another recursive function."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
