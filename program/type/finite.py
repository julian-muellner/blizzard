from typing import FrozenSet, Tuple
from symengine.lib.symengine_wrapper import sympify, Expr, Integer
from .type import Type


class Finite(Type):
    values: FrozenSet[Expr]
    __ordered_values__: Tuple
    binary: bool

    def __init__(self, parameters, variable=None):
        if len(parameters) == 0:
            raise RuntimeError("Finite type requires >=1 parameters")
        self.values = frozenset({sympify(p) for p in parameters})
        self.__ordered_values__ = tuple(sorted([v for v in self.values]))
        self.binary = len(self.values) <= 2 and all([v == 0 or v == 1 for v in self.values])
        if variable:
            self.variable = sympify(variable)

    def __str__(self):
        return f"{self.variable} : Finite({', '.join([str(v) for v in self.values])})"

