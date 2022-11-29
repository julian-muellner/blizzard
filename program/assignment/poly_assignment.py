from typing import List
import random
from symengine.lib.symengine_wrapper import Expr, sympify

from utils import float_to_rational, get_monoms
from .assignment import Assignment
from .exceptions import EvaluationException


class PolyAssignment(Assignment):
    polynomial: Expr

    def __init__(self, variable, polynomial):
        super().__init__(variable)

        expanded_poly = sympify(polynomial).expand()
        monoms = get_monoms(expanded_poly, with_constant=True)
        term = 0
        for coeff, monom in monoms:
            ncoeff = coeff
            if coeff.is_Float:
                ncoeff = float_to_rational(coeff)
            term += sympify(ncoeff) * sympify(monom)
        self.polynomial = sympify(term)

    def __str__(self):
        result = str(self.pc) + ": " + str(self.variable) + " = " + str(self.polynomial)
        return result

    def subs(self, substitutions):
        self.polynomials = self.polynomial.subs(substitutions)

    def evaluate_right_side(self, state):
        p = self.polynomial.subs(state)
        if not p.is_Number:
            raise EvaluationException(f"Polynomial {self.polynomial} is not a number in state {state}")
        return p

    def get_free_symbols(self, with_condition=True, with_default=True):
        symbols = self.polynomial.free_symbols
        return symbols

    def get_support(self):
        result = set(self.polynomial)
        return result

