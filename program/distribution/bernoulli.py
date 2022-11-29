from symengine.lib.symengine_wrapper import Expr, Zero, One
from .distribution import Distribution
from .exceptions import EvaluationException

class Bernoulli(Distribution):
    p: Expr

    def set_parameters(self, parameters):
        if len(parameters) != 1:
            raise RuntimeError("Bernoulli distribution requires 1 parameter")
        self.p = parameters[0]

    def subs(self, substitutions):
        self.p = self.p.subs(substitutions)

    def get_free_symbols(self):
        return self.p.free_symbols

    def get_support_with_probability(self):
        return {(Zero(), One() - self.p), (One(), self.p)}

    def __str__(self):
        return f"Bernoulli({self.p})"
