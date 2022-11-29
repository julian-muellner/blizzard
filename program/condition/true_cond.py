from symengine.lib.symengine_wrapper import sympify
from .condition import Condition


class TrueCond(Condition):

    def simplify(self):
        return self

    def reduce(self, store):
        return []

    def subs(self, substitutions):
        pass

    def evaluate(self, state):
        return True

    def get_free_symbols(self):
        return set()

    def get_conjuncts(self):
        return [self]

    def __str__(self):
        return "true"

    def __eq__(self, obj):
        return isinstance(obj, TrueCond)

    def __hash__(self):
        return hash("TRUE")
