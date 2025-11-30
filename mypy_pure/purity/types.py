from typing import TypeAlias

FuncName: TypeAlias = str
LineNo: TypeAlias = int
CallGraph: TypeAlias = dict[FuncName, set[FuncName]]
ImportAlias: TypeAlias = str
ImportFullName: TypeAlias = str
