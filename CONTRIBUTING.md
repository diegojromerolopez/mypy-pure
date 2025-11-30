# Contributing to mypy-pure

Thank you for your interest in contributing to mypy-pure! This document provides guidelines and instructions for contributing.

## Ways to Contribute

### 1. Expand the Blacklist

The most valuable contribution is adding more impure functions to the blacklist.

**What to add:**
- Standard library functions with side effects
- Common third-party library functions (requests, pandas, numpy, etc.)
- Database operations
- Network operations
- File system operations

**How to add:**

1. Edit `mypy_pure/configuration.py`
2. Add the function to the `BLACKLIST` set with its fully qualified name
3. Group it with similar functions and add a comment
4. Run tests to ensure nothing breaks

Example:
```python
# === requests library ===
'requests.get',
'requests.post',
'requests.put',
'requests.delete',
```

### 2. Report Bugs

Found a bug? Please open an issue with:
- A clear description of the problem
- Minimal code example that reproduces the issue
- Expected vs actual behavior
- Your Python and mypy versions

### 3. Suggest Features

Have an idea? Open an issue describing:
- The feature and why it's useful
- Example use cases
- Potential implementation approach (if you have one)

### 4. Improve Documentation

Help make the docs better:
- Fix typos or unclear explanations
- Add more examples
- Improve the README
- Add docstrings to code

## Development Setup

### Prerequisites

- Python 3.10 or higher
- Git

### Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/mypy-pure.git
cd mypy-pure

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate

# Install in development mode
pip install -e ".[dev]"
```

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest mypy_pure/tests/test_plugin.py

# Run with coverage
coverage run -m pytest
coverage report
```

## Code Style

We use:
- **black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

Run before committing:

```bash
# Format code
black mypy_pure

# Sort imports
isort mypy_pure

# Check linting
flake8 mypy_pure

# Type check
mypy mypy_pure
```

## Pull Request Process

1. **Fork** the repository
2. **Create a branch** for your changes: `git checkout -b feature/your-feature-name`
3. **Make your changes** following the code style guidelines
4. **Add tests** if applicable
5. **Run tests** to ensure everything passes
6. **Commit** with a clear message describing your changes
7. **Push** to your fork
8. **Open a Pull Request** with:
   - Clear description of changes
   - Why the changes are needed
   - Any related issues

## Adding Tests

When adding new blacklist entries, consider adding test cases:

1. Create a test resource file in `mypy_pure/tests/resources/`
2. Add a test method in `mypy_pure/tests/test_plugin.py`
3. Ensure the test fails without your blacklist entry
4. Ensure the test passes with your blacklist entry

Example test resource:
```python
from mypy_pure.decorators import pure
import requests

@pure
def fetch_data(url: str) -> dict:
    # This should be detected as impure
    return requests.get(url).json()
```

## Questions?

Feel free to open an issue for any questions about contributing!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
