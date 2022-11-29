from .condition import Condition
from .true_cond import TrueCond


class And(Condition):
    cond1: Condition
    cond2: Condition

    def __init__(self, cond1, cond2):
        self.cond1 = cond1
        self.cond2 = cond2

    def simplify(self):
        self.cond1 = self.cond1.simplify()
        self.cond2 = self.cond2.simplify()
        if isinstance(self.cond1, TrueCond):
            return self.cond2
        if isinstance(self.cond2, TrueCond):
            return self.cond1
        return self

    def reduce(self, store):
        return self.cond1.reduce(store) + self.cond2.reduce(store)

    def subs(self, substitutions):
        self.cond1.subs(substitutions)
        self.cond2.subs(substitutions)

    def evaluate(self, state):
        return self.cond1.evaluate(state) and self.cond2.evaluate(state)

    def get_conjuncts(self):
        return self.cond1.get_conjuncts() + self.cond2.get_conjuncts()

    def get_free_symbols(self):
        return self.cond1.get_free_symbols() | self.cond2.get_free_symbols()

    def __str__(self):
        return f"({self.cond1} ∧ {self.cond2})"

    def __eq__(self, obj):
        return isinstance(obj, And) and (self.cond1, self.cond2) == (obj.cond1, obj.cond2)

    def __hash__(self):
        return hash(("AND", self.cond1, self.cond2))
