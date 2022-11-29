from symengine.lib.symengine_wrapper import sympify, Expr
from .condition import Condition


class FalseCond(Condition):

    def simplify(self):
        return self

    def reduce(self, store):
        return []

    def get_conjuncts(self):
        return [self]

    def subs(self, substitutions):
        pass

    def evaluate(self, state):
        return False

    def get_free_symbols(self):
        return set()

    def __str__(self):
        return "false"

    def __eq__(self, obj):
        return isinstance(obj, FalseCond)

    def __hash__(self):
        return hash("FALSE")

