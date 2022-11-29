from typing import Dict

from symengine.lib.symengine_wrapper import sympify, Zero, Symbol

from .or_cond import Or
from .false_cond import FalseCond
from .condition import Condition
from .exceptions import ArithmConversionException, NormalizingException, EvaluationException
from utils import get_unique_var, get_valid_values, evaluate_cop
from program.type import Finite


class Atom(Condition):

    def __init__(self, poly1, cop, poly2):
        self.poly1 = sympify(poly1)
        self.cop = cop
        self.poly2 = sympify(poly2)

    def simplify(self):
        return self

    def subs(self, substitutions):
        self.poly1 = self.poly1.subs(substitutions)
        self.poly2 = self.poly2.subs(substitutions)

    def evaluate(self, state):
        poly1 = self.poly1.subs(state)
        poly2 = self.poly2.subs(state)
        if not poly1.is_Number or not poly2.is_Number:
            raise EvaluationException(f"Atom {self} cannot be fully evaluated with state {state}")
        result = evaluate_cop(float(poly1), self.cop, float(poly2))
        return result

    def is_reduced(self):
        return self.poly1.is_Symbol and self.poly2.is_Integer

    def reduce(self, store: Dict["Atom", Symbol]):
        if self.is_reduced():
            return []

        if self in store:
            self.poly1 = store[self].copy()
            self.poly2 = Zero()
            return []

        new_var = sympify(get_unique_var(name="r"))
        store[self.copy()] = new_var
        alias = self.poly1 - self.poly2
        self.poly1 = new_var
        self.poly2 = Zero()
        return [(new_var, alias)]

    def get_conjuncts(self):
        return [self]

    def get_free_symbols(self):
        return self.poly1.free_symbols | self.poly2.free_symbols

    def __str__(self):
        return f"{self.poly1} {self.cop} {self.poly2}"

    def __eq__(self, obj):
        return isinstance(obj, Atom) and (self.poly1, self.cop, self.poly2) == (obj.poly1, obj.cop, obj.poly2)

    def __hash__(self):
        return hash((self.poly1, self.cop, self.poly2))
