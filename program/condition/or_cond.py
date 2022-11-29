from .condition import Condition
from .false_cond import FalseCond


class Or(Condition):
    cond1: Condition
    cond2: Condition

    def __init__(self, cond1, cond2):
        self.cond1 = cond1
        self.cond2 = cond2

    def simplify(self):
        self.cond1 = self.cond1.simplify()
        self.cond2 = self.cond2.simplify()
        if isinstance(self.cond1, FalseCond):
            return self.cond2
        if isinstance(self.cond2, FalseCond):
            return self.cond1
        return self

    def reduce(self, store):
        return self.cond1.reduce(store) + self.cond2.reduce(store)

    def subs(self, substitutions):
        self.cond1.subs(substitutions)
        self.cond2.subs(substitutions)

    def evaluate(self, state):
        return self.cond1.evaluate(state) or self.cond2.evaluate(state)

    def get_free_symbols(self):
        return self.cond1.get_free_symbols() | self.cond2.get_free_symbols()

    def get_conjuncts(self):
        return [self]

