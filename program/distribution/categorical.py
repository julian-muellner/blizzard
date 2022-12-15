from typing import List
from symengine.lib.symengine_wrapper import sympify, Expr, One

from .distribution import Distribution

class Categorical(Distribution):
    values: List[Expr]

    def set_parameters(self, parameters):
        if len(parameters) == 0:
            raise RuntimeError("Categorical distribution requires >=1 parameters")
        s = sum(parameters)
        if s.is_Number and s != 1:
            raise RuntimeError("Categorical distribution parameters need to sum up to 1")
        self.probabilities = parameters

    def subs(self, substitutions):
        self.probabilities = [p.subs(substitutions) for p in self.probabilities]

    def get_free_symbols(self):
        symbols = set()
        for p in self.probabilities:
            symbols = symbols.union(p.free_symbols)
        return symbols

    def get_support_with_probability(self):
        result = set()
        for val, prob in enumerate(self.probabilities):
            result.add((sympify(val), prob))
        return result

    def __str__(self):
        return f"Categorical({', '.join([str(p) for p in self.probabilities])})"
