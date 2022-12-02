from lark import Transformer, Tree, Token
from program import Program
from program.assignment import DistAssignment, PolyAssignment
from program.condition import Condition, Atom, Not, And, Or, TrueCond, FalseCond
from program.distribution import distribution_factory, Distribution
from program.ifstatem import IfStatem
from program.observestatem.observestatem import ObserveStatem
from program.whilestatem import WhileStatem
from program.type import type_factory, Type
from utils import get_unique_var
from .exceptions import ParseException


class StructureTransformer(Transformer):
    """
    Lark transformer which transform the parse tree returned by lark into our own representations
    """
    def __init__(self):
        super().__init__()
        self.program_variables = set()

    def program(self, args) -> Program:
        """
        Constructs the most outer data wrapper
        """
        tree = Tree("program", args)
        td = list(tree.find_data("typedefs"))
        s = list(tree.find_data("main")).pop()
        typedefs = td[0].children if td else []
        statements = s.children[0] if s.children else []

        return Program(typedefs, self.program_variables, statements)

    def dist(self, args):
        dist_name = str(args[0])
        parameters = [str(p) for p in args[1:]]
        return distribution_factory(dist_name, parameters)

    def if_statem(self, args) -> IfStatem:
        condition = args[0]
        if_branch = args[1]
        if len(args) > 2:
            else_branch = args[2]
        else:
            else_branch = None
        return IfStatem(condition, if_branch, else_branch)
        
    def while_statem(self, args) -> WhileStatem:
        condition = args[0]
        body = args[1]
        return WhileStatem(condition, body)

    def observe_statem(self, args) -> ObserveStatem:
        condition = args[0]
        return ObserveStatem(condition)

    def typedef(self, args) -> Type:
        var = str(args[0])
        name = str(args[1].children[0])
        params = [str(a) for a in args[1].children[1:]]
        return type_factory(name, params, var)

    def statems(self, args) -> []:
        statements = []
        for a in args:
            if type(a) is list:
                statements += a
            else:
                statements.append(a)
        return statements

    def atom(self, args) -> Condition:
        if len(args) == 1 and args[0].type == "TRUE":
            return TrueCond()
        if len(args) == 1 and args[0].type == "FALSE":
            return FalseCond()

        poly1 = str(args[0])
        cop = str(args[1])
        poly2 = str(args[2])
        return Atom(poly1, cop, poly2)

    def condition(self, args) -> Condition:
        if len(args) == 1:
            return args[0]
        if len(args) == 2:
            cond = args[1]
            return Not(cond)
        if len(args) == 3:
            cond1 = args[0]
            binop = str(args[1])
            cond2 = args[2]
            if binop == "&&":
                return And(cond1, cond2)
            elif binop == "||":
                return Or(cond1, cond2)
        raise ParseException("Error in condition")

    def assign(self, args):
        assert (len(args) == 3)
        var = str(args[0])
        self.program_variables.add(var)
        value = args[2]
        if isinstance(value, Distribution):
            return DistAssignment(var, value)
        else:
            return PolyAssignment(var, str(value))
