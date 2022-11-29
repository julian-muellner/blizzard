from .condition import Condition


class Not(Condition):
    cond: Condition

    def __init__(self, cond):
        self.cond = cond

    def simplify(self):
        self.cond = self.cond.simplify()
        return self

    def reduce(self, store):
        return self.cond.reduce(store)

    def subs(self, substitutions):
        self.cond.subs(substitutions)

    def evaluate(self, state):
        return not self.cond.evaluate(state)

    def get_free_symbols(self):
        return self.cond.get_free_symbols()

    def get_conjuncts(self):
        return [self]

    def __str__(self):
        return f"¬({self.cond})"

    def __eq__(self, obj):
        return isinstance(obj, Not) and self.cond == obj.cond

    def __hash__(self):
        return hash(("NOT", self.cond))