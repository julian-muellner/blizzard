from typing import List
from symengine.lib.symengine_wrapper import sympify, Expr, One

from .distribution import Distribution


class DiscreteUniform(Distribution):
    values: List[Expr]

    def set_parameters(self, parameters):
        if len(parameters) != 2:
            raise RuntimeError("Uniform distribution requires 2 parameters")
        if not parameters[0].is_Integer or not parameters[1].is_Integer:
            raise RuntimeError("For discrete uniform only integer parameters are supported")
        values = list(range(int(parameters[0]), int(parameters[1]) + 1))
        self.values = [sympify(v) for v in values]

    def subs(self, substitutions):
        return

    def get_free_symbols(self):
        return set()

    def get_support_with_probability(self):
        result = set()
        for v in self.values:
            result.add((v, One()/len(self.values)))
        return result

    def __str__(self):
        return f"DiscreteUniform({self.values[0]}, {self.values[-1]})"
