import ast
import configparser
import importlib
import sys

from mypy.nodes import MypyFile
from mypy.options import Options
from mypy.plugin import Plugin

from mypy_pure.configuration import BLACKLIST
from mypy_pure.purity.checker import compute_purity
from mypy_pure.purity.types import FuncName
from mypy_pure.purity.visitor import PurityVisitor


class PurityPlugin(Plugin):
    def __init__(self, options: Options) -> None:
        super().__init__(options)
        self.__checked_files: set[str] = set()
        self.__blacklist: set[FuncName] = BLACKLIST.copy()
        self.__whitelist: set[FuncName] = set()  # Pure functions from config
        self.__loaded_modules: set[str] = set()
        self.__load_config(options)

    def __load_config(self, options: Options) -> None:
        if not options.config_file:  # pragma: no cover
            return

        config = configparser.ConfigParser()
        try:
            config.read(options.config_file)
            if 'mypy-pure' in config:
                # Load impure functions (blacklist)
                impure_funcs = config['mypy-pure'].get('impure_functions', '')
                for func in impure_funcs.split(','):
                    func = func.strip()
                    if func:
                        self.__blacklist.add(func)

                # Load pure functions (whitelist)
                pure_funcs = config['mypy-pure'].get('pure_functions', '')
                for func in pure_funcs.split(','):
                    func = func.strip()
                    if func:
                        self.__whitelist.add(func)
        except (OSError, configparser.Error):  # pragma: no cover
            # If config file can't be read or parsed, continue with defaults
            pass

    def __load_module_pure_functions(self, module_name: str) -> None:
        if module_name in self.__loaded_modules:
            return

        self.__loaded_modules.add(module_name)
        try:
            module = importlib.import_module(module_name)
            if hasattr(module, '__mypy_pure__'):
                pure_funcs = getattr(module, '__mypy_pure__')
                if isinstance(pure_funcs, (list, tuple, set)):
                    for func in pure_funcs:
                        if isinstance(func, str):
                            # If it's just the function name, prepend module name
                            if '.' not in func:
                                self.__whitelist.add(f'{module_name}.{func}')
                            else:
                                self.__whitelist.add(func)
        except (ImportError, AttributeError, Exception):
            # Module not found, no __mypy_pure__, or other import issues
            pass

    def get_additional_deps(self, file: MypyFile) -> list[tuple[int, str, int]]:
        """
        Mypy hook that is called for each file to determine additional dependencies.

        We use this hook as an entry point to analyze the file for purity violations.
        It is called for every file that mypy checks.

        Args:
            file: The MypyFile object representing the file being checked.

        Returns:
            A list of additional dependencies (always empty in our case, as we only use this for analysis).
        """
        if file.fullname in self.__checked_files:  # pragma: no cover
            return []

        # Skip stdlib and other system modules to avoid noise and performance hit
        # This list is heuristic.
        if file.fullname.startswith(('builtins', 'typing', 'sys', 'os', 'abc', 'enum', 'mypy.', '_')):
            return []

        self.__checked_files.add(file.fullname)

        try:
            # We need to read the source file again because MypyFile doesn't expose the raw source easily here,
            # and we want to parse it with ast.
            if not file.path:  # pragma: no cover
                return []

            with open(file.path, 'r', encoding='utf-8') as f:
                source = f.read()

            tree = ast.parse(source, filename=file.path)
            visitor = PurityVisitor()
            visitor.visit(tree)

            if not visitor.pure_functions_lineno:
                return []

            # Auto-discover pure functions from imported modules
            # We look at the imports found by the visitor
            for alias, fullname in visitor.imports.items():
                # fullname might be 'module.submodule.function' or just 'module'
                # We try to load the top-level module and submodules
                parts = fullname.split('.')
                current_module = parts[0]
                self.__load_module_pure_functions(current_module)
                for part in parts[1:]:
                    current_module = f'{current_module}.{part}'
                    self.__load_module_pure_functions(current_module)

            purity_map, impure_calls_map = compute_purity(
                calls=visitor.calls,
                pure_functions=set(visitor.pure_functions_lineno.keys()),
                blacklist=self.__blacklist,
                whitelist=self.__whitelist,
            )

            for fn, lineno in visitor.pure_functions_lineno.items():
                if not purity_map.get(fn, True):
                    # Get the impure functions that were called
                    impure_funcs = impure_calls_map.get(fn, set())
                    if impure_funcs:
                        # Format the list of impure functions
                        impure_list = ', '.join(f"'{f}'" for f in sorted(impure_funcs))
                        msg = (
                            f'{file.path}:{lineno}: '
                            f"error: Function '{fn}' is impure because it calls {impure_list}\n"
                        )
                    else:  # pragma: no cover
                        # Fallback to generic message if no specific calls tracked
                        # This shouldn't happen with current implementation
                        msg = (
                            f'{file.path}:{lineno}: '
                            f"error: Function '{fn}' is annotated as pure but calls impure functions.\n"
                        )
                    sys.stdout.write(msg)
                    sys.stdout.flush()

        except Exception as _exc:  # pragma: no cover  # noqa
            # Silently fail or print debug info if needed
            # sys.stdout.write(f'AST Analysis failed for {file.fullname}: {e}\n')
            pass

        return []


def plugin(version: str) -> type[PurityPlugin]:
    return PurityPlugin
