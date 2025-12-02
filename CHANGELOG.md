# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## 0.2.1 (2025-12-02)
### Bug Fixes
- **Fixed whitelist propagation bug**: Whitelisted functions are now properly treated as pure throughout the analysis. Previously, impure calls from whitelisted functions were incorrectly propagated to their callers.
- **Fixed `from mypy_pure import pure` support**: The `@pure` decorator now works correctly when imported as `from mypy_pure import pure` (in addition to `from mypy_pure.decorators import pure`).

### Improvements
- **100% test coverage**: Achieved complete test coverage for all plugin source code (446/446 statements).
- **Enhanced test suite**: Added comprehensive tests for:
  - Config file handling (missing config, bad syntax)
  - Module loading with `__mypy_pure__` (including dotted names, already-loaded modules, import errors)
  - Relative imports
  - Recursive functions
  - Whitelist priority over blacklist
  - Import aliases
- **Coverage configuration**: Test resource files are now excluded from coverage reporting for cleaner metrics.
- **Code quality improvements**: Minor refactoring for better readability (tuple to set for membership checks, trailing whitespace cleanup).
- Creation of **mypy-pure-examples** repository with examples of how to use the plugin.

## 0.2.0 (2025-11-30)
### Features
- **Auto-discovery via `__mypy_pure__`**: Libraries can now declare their pure functions using a `__mypy_pure__` list. The plugin automatically discovers and respects these declarations, enabling zero-configuration purity checking for library users.
- **Configuration options**: Added `pure_functions` (whitelist) and `impure_functions` (blacklist) configuration in `mypy.ini` under `[mypy-pure]` section, allowing users to customize purity analysis for their specific needs.
- **Improved error messages**: Error messages now show which specific function caused the impurity (e.g., `Function 'foo' is impure because it calls 'print'`) instead of a generic message, making debugging much easier.
- **Async function support**: Added `visit_AsyncFunctionDef` to properly analyze async functions and methods
- **Comprehensive function type support**: Pure decorator now works with:
  - Properties (`@property`)
  - Instance methods
  - Class methods (`@classmethod`)
  - Static methods (`@staticmethod`)
  - Async functions (`async def`)
  - Async methods
  - Nested/inner functions
- **Expanded blacklist**: Grew from ~85 to 230+ impure functions from Python's standard library including:
  - All major stdlib modules (logging, threading, multiprocessing, signal, etc.)
  - Network operations (http.client, urllib, ftplib, smtplib, etc.)
  - Database operations (sqlite3, dbm, shelve)
  - File operations (tempfile, pickle, pathlib)
  - System operations (gc, warnings, atexit)

### Improvements
- **Type aliases**: Introduced `FuncName`, `CallGraph`, `ImportAlias`, `ImportFullName`, and `LineNo` for better code readability and type safety
- **Refactored architecture**: Converted `compute_purity` into a `PurityChecker` class with proper encapsulation and private attributes
- Better organized blacklist with category comments
- More comprehensive test coverage (18 tests)

## 0.1.1 (2025-11-30)
### Fixes
- Add several impure functions to the mypy ini file, and use it in the tests.

## 0.1.0 (2025-10-24)
- First release.