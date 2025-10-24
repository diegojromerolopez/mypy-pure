from __future__ import annotations

import ast
import configparser
import sys

from mypy.nodes import MypyFile
from mypy.options import Options
from mypy.plugin import Plugin

from mypy_pure.configuration import BLACKLIST
from mypy_pure.purity.analyzer import compute_purity
from mypy_pure.purity.visitor import PurityVisitor


class PurityPlugin(Plugin):
    def __init__(self, options: Options) -> None:
        super().__init__(options)
        self.__checked_files: set[str] = set()
        self.__blacklist = BLACKLIST.copy()
        self.__load_config(options)

    def __load_config(self, options: Options) -> None:
        if not options.config_file:
            return

        config = configparser.ConfigParser()
        try:
            config.read(options.config_file)
            if 'mypy-pure' in config:
                impure_funcs = config['mypy-pure'].get('impure_functions', '')
                for func in impure_funcs.split(','):
                    func = func.strip()
                    if func:
                        self.__blacklist.add(func)
        except Exception:
            pass

    def get_additional_deps(self, file: MypyFile) -> list[tuple[int, str, int]]:
        if file.fullname in self.__checked_files:
            return []

        # Skip stdlib and other system modules to avoid noise and performance hit
        # This list is heuristic.
        if file.fullname.startswith(('builtins', 'typing', 'sys', 'os', 'abc', 'enum', 'mypy.', '_')):
            return []

        self.__checked_files.add(file.fullname)

        try:
            # We need to read the source file again because MypyFile doesn't expose the raw source easily here,
            # and we want to parse it with ast.
            if not file.path:
                return []

            with open(file.path, 'r', encoding='utf-8') as f:
                source = f.read()

            tree = ast.parse(source, filename=file.path)
            visitor = PurityVisitor()
            visitor.visit(tree)

            if not visitor.pure_functions:
                return []

            purity_map = compute_purity(visitor.calls, set(visitor.pure_functions.keys()), self.__blacklist)

            for fn, lineno in visitor.pure_functions.items():
                if not purity_map.get(fn, True):
                    # Report error in a format mypy/editors understand
                    msg = (
                        f'{file.path}:{lineno}: '
                        f"error: Function '{fn}' is annotated as pure but calls impure functions.\n"
                    )
                    sys.stdout.write(msg)
                    sys.stdout.flush()

        except Exception as _exc:  # noqa
            # Silently fail or print debug info if needed
            # sys.stdout.write(f'AST Analysis failed for {file.fullname}: {e}\n')
            pass

        return []


def plugin(version: str) -> type[PurityPlugin]:
    return PurityPlugin
