# mypy-pure

A mypy plugin that enforces purity in Python functions.

## Disclaimer

This project has been created using the support of the following AI tools:
- ChatGPT
- Antigravity (Gemini)

After that, it has been manually reviewed and fixed.

## What is a Pure Function?

A pure function is a function that has the following properties:
1.  **Deterministic**: Its return value is the same for the same arguments.
2.  **No Side Effects**: It does not cause any observable side effects (e.g., modifying global variables, I/O operations, database writes).

This mypy plugin helps enforcing statically the second property by detecting calls to known impure functions within functions decorated with `@pure`.

## Installation

Install:

```bash
pip install mypy-pure
```

Enable it in your `mypy.ini`:

```ini
[mypy]
plugins = mypy_pure.plugin
```

## Usage

Pure function (no side-effects):

```python
from mypy_pure.decorators import pure

@pure
def add(x: int, y: int) -> int:
    return x + y
```

Impure function (with side-effects):

```python
import os
from mypy_pure.decorators import pure

@pure
def bad() -> None:
    os.remove("file.txt")
```

## Configuration

You can configure additional impure functions in your `mypy.ini` file:

```ini
[mypy-pure]
impure_functions = my_module.impure_func, another_module.bad_func
```
