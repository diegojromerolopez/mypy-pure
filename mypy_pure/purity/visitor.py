import ast

from mypy_pure.purity.types import (
    CallGraph,
    FuncName,
    ImportAlias,
    ImportFullName,
    LineNo,
)


class PurityVisitor(ast.NodeVisitor):
    PURE_DECORATOR_FULLNAME = 'mypy_pure.decorators.pure'

    def __init__(self) -> None:
        self.__imports: dict[ImportAlias, ImportFullName] = {}  # alias -> fullname
        self.__calls: CallGraph = {}  # func_name -> set(callees)
        self.__pure_functions_lineno: dict[FuncName, LineNo] = {}  # func_name -> lineno
        self.__current_function: FuncName | None = None

    @property
    def calls(self) -> CallGraph:
        return self.__calls

    @property
    def pure_functions_lineno(self) -> dict[FuncName, LineNo]:
        return self.__pure_functions_lineno

    @property
    def imports(self) -> dict[ImportAlias, ImportFullName]:
        return self.__imports

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            name = alias.asname or alias.name
            self.__imports[name] = alias.name
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        module = node.module or ''
        for alias in node.names:
            name = alias.asname or alias.name
            if module:
                fullname = f'{module}.{alias.name}'
            else:
                fullname = alias.name
            self.__imports[name] = fullname
        self.generic_visit(node)

    def __resolve_name(self, node: ast.AST) -> str | None:
        if isinstance(node, ast.Name):
            return self.__imports.get(node.id, node.id)
        elif isinstance(node, ast.Attribute):
            base = self.__resolve_name(node.value)
            if base:
                return f'{base}.{node.attr}'
        return None

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.__handle_function_def(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self.__handle_function_def(node)

    def __handle_function_def(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        # Check for @pure decorator
        is_pure = False
        for decorator in node.decorator_list:
            dec_name = self.__resolve_name(decorator)
            if dec_name == self.PURE_DECORATOR_FULLNAME:
                is_pure = True
            elif isinstance(decorator, ast.Name) and decorator.id == 'pure':
                # Check if 'pure' is imported from the right place
                imported_from = self.__imports.get('pure')
                if imported_from in {self.PURE_DECORATOR_FULLNAME, 'mypy_pure.pure'}:
                    is_pure = True  # pragma: no cover
                # Or if it's just 'pure' and we assume it's the one (for simple cases)

            elif isinstance(decorator, ast.Attribute) and decorator.attr == 'pure':
                # Handle @decorators.pure
                base = self.__resolve_name(decorator.value)  # pragma: no cover
                if base == 'mypy_pure.decorators':  # pragma: no cover
                    is_pure = True  # pragma: no cover

        if is_pure:
            self.__pure_functions_lineno[node.name] = node.lineno

        prev_function = self.__current_function
        self.__current_function = node.name
        self.__calls[node.name] = set()

        self.generic_visit(node)

        self.__current_function = prev_function

    def visit_Call(self, node: ast.Call) -> None:
        if self.__current_function is None:
            self.generic_visit(node)
            return

        callee_name = None
        if isinstance(node.func, ast.Name):
            callee_name = self.__imports.get(node.func.id, node.func.id)
        elif isinstance(node.func, ast.Attribute):
            base = self.__resolve_name(node.func.value)
            if base:
                callee_name = f'{base}.{node.func.attr}'

        if callee_name:
            self.__calls[self.__current_function].add(callee_name)

        self.generic_visit(node)
