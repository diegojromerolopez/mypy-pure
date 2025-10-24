def compute_purity(calls: dict[str, set[str]], pure_functions: set[str], blacklist: set[str]) -> dict[str, bool]:
    purity: dict[str, bool] = {}

    def analyze(fn: str, visited: set[str]) -> bool:
        if fn in purity:
            return purity[fn]
        if fn in visited:
            return True  # avoid cycles
        visited.add(fn)

        # Check direct impure calls
        callees = calls.get(fn, set())
        for callee in callees:
            if callee in blacklist or f'builtins.{callee}' in blacklist:
                purity[fn] = False
                return False

        # Check recursive callees
        for callee in callees:
            if callee in pure_functions or callee in calls:
                if not analyze(callee, visited):
                    purity[fn] = False
                    return False

        purity[fn] = True
        return True

    for function in pure_functions:
        analyze(function, set())

    return purity
