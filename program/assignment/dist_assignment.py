from symengine.lib.symengine_wrapper import Expr

from .assignment import Assignment
from program.distribution import Distribution


class DistAssignment(Assignment):
    distribution: Distribution

    def __init__(self, var, dist):
        super().__init__(var)
        self.distribution = dist

    def __str__(self):
        result = str(self.pc) + ": " + str(self.variable) + " = " + str(self.distribution)
        return result

    def get_free_symbols(self):
        symbols = self.distribution.get_free_symbols()
        return symbols

    def subs(self, substitutions):
        self.distribution.subs(substitutions)

    def evaluate_right_side(self, state):
        return self.distribution.sample(state)

    def get_support(self):
        result = self.distribution.get_support()
        return result

