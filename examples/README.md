# mypy-pure Examples

This directory contains real-world examples demonstrating how to use `@pure` decorator effectively.

## Examples

### 1. [data_processing.py](data_processing.py)
**Data transformation pipelines**

Shows how to use `@pure` for data processing:
- Normalizing user data
- Filtering and transforming collections
- Building pure data pipelines

**Key benefits:**
- Easy to test (no mocks needed)
- Easy to parallelize (no shared state)
- Easy to cache (deterministic results)

### 2. [business_logic.py](business_logic.py)
**Business rules and calculations**

Demonstrates pure business logic:
- Price calculations with discounts
- Tax calculations
- Shipping cost calculations
- Order total calculations

**Key benefits:**
- Deterministic and testable
- Easy to reason about
- Safe to refactor
- Can be cached/memoized

### 3. [config_processing.py](config_processing.py)
**Configuration merging and validation**

Shows pure configuration handling:
- Merging default and user configs
- Validating configuration
- Normalizing values
- Environment-specific overrides

**Key benefits:**
- No file I/O in pure functions
- Easy to test with different combinations
- Deterministic behavior

## Running the Examples

Each example can be run standalone:

```bash
# Data processing
python examples/data_processing.py

# Business logic
python examples/business_logic.py

# Config processing
python examples/config_processing.py
```

## Type Checking

Run mypy on the examples to see purity checking in action:

```bash
mypy examples/
```

All examples should pass without purity violations since they only use pure functions.

## Common Patterns

### ✅ Pure Functions Should:
- Return the same output for the same inputs
- Not modify their arguments
- Not perform I/O operations
- Not access or modify global state
- Not call impure functions

### ❌ Avoid in Pure Functions:
- `print()`, logging
- File operations (`open()`, `Path.write_text()`)
- Network requests (`requests.get()`)
- Database operations
- Random number generation (without seed)
- Accessing current time/date
- Modifying mutable arguments

## Testing Pure Functions

Pure functions are extremely easy to test:

```python
def test_calculate_discount():
    # No setup needed, no mocks needed
    result = calculate_discount(100.0, 20.0)
    assert result == 80.0
    
    # Same inputs always give same outputs
    assert calculate_discount(100.0, 20.0) == 80.0
    assert calculate_discount(100.0, 20.0) == 80.0
```

## Learn More

- [README.md](../README.md) - Full documentation
- [CONTRIBUTING.md](../CONTRIBUTING.md) - How to contribute
