---
name: Blacklist Addition
about: Suggest adding a function to the impure blacklist
title: '[BLACKLIST] Add <function_name>'
labels: blacklist, enhancement
assignees: ''
---

## Function to Add
**Fully qualified name:** `module.submodule.function_name`

## Why is it impure?
Explain what side effects this function has:
- [ ] File I/O
- [ ] Network I/O
- [ ] Database operations
- [ ] System state modification
- [ ] Logging/printing
- [ ] Other: ___________

## Example
Show an example of why this should be caught:

```python
from mypy_pure.decorators import pure

@pure
def my_function():
    # This should be detected as impure
    module.function_name()  # <-- Side effect here
```

## Documentation
Link to official documentation (if available):
https://docs.python.org/...

## Additional Context
Any other relevant information.
