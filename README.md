# mypy-pure

![test](https://github.com/diegojromerolopez/mypy-pure/actions/workflows/test.yml/badge.svg)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/diegojromerolopez/mypy-pure/graphs/commit-activity)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/mypy-pure.svg)](https://pypi.python.org/pypi/mypy-pure/)
[![PyPI version mypy-pure](https://badge.fury.io/py/mypy-pure.svg)](https://pypi.python.org/pypi/mypy-pure/)
[![PyPI status](https://img.shields.io/pypi/status/mypy-pure.svg)](https://pypi.python.org/pypi/mypy-pure/)
[![PyPI download month](https://img.shields.io/pypi/dm/mypy-pure.svg)](https://pypi.python.org/pypi/mypy-pure/)

**Enforce functional purity in Python with static type checking.**

A mypy plugin that helps you write safer, more predictable code by detecting side effects in functions marked as `@pure`.

## Why mypy-pure?

Pure functions are:
- **Easier to test** - No mocks needed, same inputs always give same outputs
- **Easier to reason about** - No hidden state changes or side effects
- **Easier to refactor** - Can be moved, renamed, or reordered safely
- **Easier to parallelize** - No race conditions or shared state issues
- **Easier to cache** - Results can be memoized safely

But enforcing purity manually is error-prone. **mypy-pure** catches impure code at type-check time, before it reaches production.

## What is a Pure Function?

A pure function:
1. **Always returns the same output for the same inputs** (deterministic)
2. **Has no side effects** (no I/O, no mutations, no external state changes)

```python
# ✅ Pure - deterministic, no side effects
def add(x: int, y: int) -> int:
    return x + y

# ❌ Impure - side effect (I/O)
def add_and_log(x: int, y: int) -> int:
    print(f"Adding {x} + {y}")  # Side effect!
    return x + y
```

## Installation

```bash
pip install mypy-pure
```

Enable the plugin in your `mypy.ini` or `pyproject.toml`:

```ini
[mypy]
plugins = mypy_pure.plugin
```

## Quick Start

Mark functions as pure with the `@pure` decorator:

```python
from mypy_pure import pure

@pure
def calculate_total(prices: list[float], tax_rate: float) -> float:
    subtotal = sum(prices)
    return subtotal * (1 + tax_rate)
```

Run mypy to check for purity violations:

```bash
mypy your_code.py
```

## Examples

### ✅ Valid Pure Functions

```python
from mypy_pure import pure

@pure
def fibonacci(n: int) -> int:
    """Pure recursive function."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

@pure
def process_data(items: list[dict]) -> list[str]:
    """Pure data transformation."""
    return [item['name'].upper() for item in items if item['active']]

@pure
def calculate_discount(price: float, discount_pct: float) -> float:
    """Pure business logic."""
    return price * (1 - discount_pct / 100)
```

### ❌ Detected Impurity Violations

```python
from mypy_pure import pure
import os

@pure
def read_config() -> dict:
    # Error: Function 'read_config' is annotated as pure but calls impure functions.
    with open('config.json') as f:  # I/O is impure!
        return json.load(f)

@pure
def delete_temp_files(directory: str) -> None:
    # Error: Function 'delete_temp_files' is annotated as pure but calls impure functions.
    for file in os.listdir(directory):
        os.remove(file)  # File system modification is impure!

@pure
def log_and_calculate(x: int, y: int) -> int:
    # Error: Function 'log_and_calculate' is annotated as pure but calls impure functions.
    print(f"Calculating {x} + {y}")  # Logging is impure!
    return x + y
```

### More examples

More examples can be found in the [mypy-pure-examples](https://github.com/diegojromerolopez/mypy-pure-examples) repository.

## Advanced Usage

### Configuration Options

mypy-pure supports two configuration options in the `[mypy-pure]` section of your `mypy.ini`:

#### 1. `impure_functions` (Blacklist)

Add custom impure functions that should be flagged as side-effecting:

```ini
[mypy-pure]
impure_functions = my_module.send_email, analytics.track_event, cache.set
```

**Use cases:**
- Your own functions that have side effects
- Third-party library functions not in the built-in blacklist
- Project-specific impure operations

**Example:**

```python
# my_module.py
def send_email(to: str, subject: str) -> None:
    # Sends an email (side effect)
    ...

# main.py
from mypy_pure import pure
from my_module import send_email

@pure
def process_user(user: dict) -> dict:
    send_email(user['email'], 'Welcome')  # ❌ Error: calls impure function
    return user
```

#### 2. `pure_functions` (Whitelist)

Mark third-party library functions as pure, overriding the default assumption:

```ini
[mypy-pure]
pure_functions = requests.utils.quote, pandas.DataFrame.copy, my_lib.helper
```

**Use cases:**
- Pure utility functions from third-party libraries
- Functions you've verified have no side effects
- Overriding false positives

**Example:**

```python
from mypy_pure import pure
import requests.utils

@pure
def sanitize_url(url: str) -> str:
    # OK because requests.utils.quote is in pure_functions config
    return requests.utils.quote(url)
```

#### Combining Both

You can use both options together:

```ini
[mypy-pure]
# Blacklist your impure functions
impure_functions = my_module.send_email, my_module.log_event

# Whitelist pure third-party functions
pure_functions = requests.utils.quote, requests.utils.unquote
```

**Priority:** `pure_functions` (whitelist) takes precedence over `impure_functions` (blacklist).

### Library Authors: Auto-Discovery with `__mypy_pure__`

If you're a library author, you can declare your pure functions using the `__mypy_pure__` module-level list. This enables **zero-configuration** purity checking for your users.

#### Declaring Pure Functions

Add a `__mypy_pure__` list to your module:

```python
# my_library.py
__mypy_pure__ = [
    'pure_helper',
    'utils.calculate',
    'ClassName.method_name',
]

def pure_helper(x: int) -> int:
    """A pure utility function."""
    return x * 2

class utils:
    @staticmethod
    def calculate(a: int, b: int) -> int:
        """A pure calculation."""
        return a + b

def impure_logger(msg: str) -> None:
    """Not in __mypy_pure__, so treated as impure."""
    print(msg)
```

#### User Experience

Users of your library automatically benefit without any configuration:

```python
from mypy_pure import pure
import my_library

@pure
def process(x: int) -> int:
    # ✅ OK - pure_helper is in __mypy_pure__
    return my_library.pure_helper(x)

@pure
def log_process(x: int) -> int:
    # ❌ Error: Function 'log_process' is impure because it calls 'my_library.impure_logger'
    my_library.impure_logger(f"Processing {x}")
    return x
```

#### Benefits

- **Zero configuration** for library users
- **Self-documenting API** - pure functions are explicitly declared
- **Compile-time guarantees** - purity violations caught during type checking
- **Better IDE support** - users see which functions are safe to use in pure contexts

### Cross-Module References

Reference functions from other modules using fully qualified names:

```ini
[mypy-pure]
impure_functions = external_lib.impure_function
```

## Supported Function Types

mypy-pure works with all Python function and method types:

- ✅ Regular functions
- ✅ Instance methods
- ✅ Class methods (`@classmethod`)
- ✅ Static methods (`@staticmethod`)
- ✅ Async functions (`async def`)
- ✅ Async methods
- ✅ Property methods (`@property`)
- ✅ Nested/inner functions

## Built-in Impurity Detection

mypy-pure includes a comprehensive blacklist of 200+ impure functions from Python's standard library:

- **File I/O**: `open()`, `pathlib.Path.write_text()`, etc.
- **System operations**: `os.remove()`, `subprocess.run()`, etc.
- **Network**: `socket.socket()`, `urllib.request.urlopen()`, etc.
- **Logging**: `logging.info()`, `print()`, etc.
- **State modification**: `random.seed()`, `sys.exit()`, etc.
- **Databases**: `sqlite3.connect()`, etc.
- **And many more...**

[See full blacklist](mypy_pure/configuration.py)

## Limitations

mypy-pure performs **static analysis** and has some limitations:

### What it CAN detect:
- ✅ Direct calls to known impure functions
- ✅ Indirect calls through pure functions calling impure functions
- ✅ Deeply nested impure calls

### What it CANNOT detect:
- ❌ Mutations of mutable arguments (e.g., `list.append()`)
- ❌ Global variable modifications
- ❌ Impure functions not in the blacklist
- ❌ Dynamic function calls (e.g., `getattr()`, `eval()`)
- ❌ Side effects in third-party libraries (unless configured)

**Recommendation**: Use mypy-pure as a helpful guard rail, not a guarantee of purity. Combine it with code reviews and testing.

## Real-World Use Cases

### Data Processing Pipelines
```python
@pure
def transform_user_data(raw_data: dict) -> dict:
    """Pure transformation - easy to test and parallelize."""
    return {
        'id': raw_data['user_id'],
        'name': raw_data['full_name'].title(),
        'age': calculate_age(raw_data['birth_date']),
    }
```

### Business Logic
```python
@pure
def calculate_shipping_cost(
    weight_kg: float,
    distance_km: float,
    is_express: bool
) -> float:
    """Pure business logic - deterministic and testable."""
    base_cost = weight_kg * 0.5 + distance_km * 0.1
    return base_cost * 1.5 if is_express else base_cost
```

### Configuration Processing
```python
@pure
def merge_configs(default: dict, user: dict) -> dict:
    """Pure config merging - no file I/O."""
    return {**default, **user}
```

## Contributing

Contributions are welcome! Here's how you can help:

1. **Expand the blacklist** - Add more impure functions from stdlib or popular libraries
2. **Report bugs** - Open an issue if you find incorrect behavior
3. **Suggest features** - Ideas for improving purity detection
4. **Improve documentation** - Help make the docs clearer

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## Development

```bash
# Clone the repository
git clone https://github.com/diegojromerolopez/mypy-pure.git
cd mypy-pure

# Install dependencies
uv sync

# Run tests
pytest

# Run mypy
mypy mypy_pure
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

This project was created with the assistance of AI tools (ChatGPT and Antigravity/Gemini) and manually reviewed and refined.

## Related Projects

- [mypy](https://github.com/python/mypy) - Optional static typing for Python
- [mypy-raise](https://github.com/diegojromerolopez/mypy-raise) - A mypy plugin that enforces exception declarations in function signatures, ensuring functions explicitly declare all exceptions they may raise.
- [mypy-plugins-examples](https://github.com/diegojromerolopez/mypy-plugins-examples) - A project that contains some examples for my mypy-pure and mypy-raise plugins.

---

**Made with ❤️ for the Python community**
