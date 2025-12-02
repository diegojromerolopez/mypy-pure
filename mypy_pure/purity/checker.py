from mypy_pure.purity.types import CallGraph, FuncName


class PurityChecker:
    def __init__(
        self,
        calls: CallGraph,
        pure_functions: set[FuncName],
        blacklist: set[FuncName],
        whitelist: set[FuncName] | None = None,
    ) -> None:
        self.__calls = calls
        self.__pure_functions = pure_functions
        self.__blacklist = blacklist
        self.__whitelist = whitelist or set()
        self.__purity: dict[FuncName, bool] = {}
        self.__visited: set[FuncName] = set()
        self.__impure_calls: dict[FuncName, set[FuncName]] = {}

    def run(self) -> tuple[dict[FuncName, bool], dict[FuncName, set[FuncName]]]:
        """Run purity analysis and return purity map and impure calls."""
        for function in self.__pure_functions:
            self.__analyze(function)
        return self.__purity, self.__impure_calls

    def __analyze(self, fn: FuncName) -> bool:
        if fn in self.__purity:
            return self.__purity[fn]
        if fn in self.__visited:
            return True  # pragma: no cover # avoid cycles

        self.__visited.add(fn)
        try:
            # Check direct impure calls
            callees: set[FuncName] = self.__calls.get(fn, set())
            for callee in callees:
                # If function is in whitelist, it's pure - skip blacklist check
                if callee in self.__whitelist or f'builtins.{callee}' in self.__whitelist:
                    continue  # pragma: no cover

                # Check blacklist
                if callee in self.__blacklist or f'builtins.{callee}' in self.__blacklist:
                    self.__purity[fn] = False
                    if fn not in self.__impure_calls:
                        self.__impure_calls[fn] = set()
                    self.__impure_calls[fn].add(callee)
                    # Continue checking to find all impure calls
                    continue

            # Check recursive callees
            for callee in callees:
                # Skip whitelisted functions in recursive analysis too
                if callee in self.__whitelist or f'builtins.{callee}' in self.__whitelist:
                    continue

                if callee in self.__pure_functions or callee in self.__calls:
                    if not self.__analyze(callee):
                        self.__purity[fn] = False
                        if fn not in self.__impure_calls:
                            self.__impure_calls[fn] = set()
                        # Propagate impure calls from callee
                        if callee in self.__impure_calls:
                            self.__impure_calls[fn].update(self.__impure_calls[callee])
                        else:  # pragma: no cover
                            # Callee itself is the impure one
                            self.__impure_calls[fn].add(callee)

            # Only set to True if we haven't found it to be False
            if fn not in self.__purity:
                self.__purity[fn] = True
            return self.__purity[fn]
        finally:
            self.__visited.remove(fn)


def compute_purity(
    calls: CallGraph,
    pure_functions: set[FuncName],
    blacklist: set[FuncName],
    whitelist: set[FuncName] | None = None,
) -> tuple[dict[FuncName, bool], dict[FuncName, set[FuncName]]]:
    """
    Compute purity of functions.

    Returns:
        Tuple of (purity_map, impure_calls_map)
        - purity_map: dict mapping function names to their purity status
        - impure_calls_map: dict mapping impure function names to the set of impure functions they call
    """
    checker = PurityChecker(calls, pure_functions, blacklist, whitelist)
    return checker.run()
