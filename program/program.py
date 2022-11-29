from typing import Any, Dict, List, Optional, Set
from symengine.lib.symengine_wrapper import sympify, Symbol

from program.assignment.poly_assignment import PolyAssignment
from program.endstatem.endstatem import EndStatem
from program.observestatem.observestatem import ObserveStatem

from .assignment.assignment import Assignment
from .assignment.dist_assignment import DistAssignment
from .type import Type, Finite, FiniteRange
from .ifstatem import IfStatem
from .whilestatem import WhileStatem
from utils import indent_string

class Program:
    max_pc: int
    variables: Set[Symbol]
    statements: List[Any]
    typedefs: Dict[Symbol, Type]

    def __init__(self, types, variables, statements):
        self.typedefs = {}
        self.add_types(types)
        self.variables = {sympify(v) for v in variables}
        self.statements = statements
        self.statements.append(EndStatem()) # sentinel node

        self.assign_pc()
        self.assign_next_stmt()
        
        # make sure every variable is properly constrained
        for v in self.variables:
            t = self.get_type(v)
            if (t is None) or (not isinstance(t, FiniteRange)):
                raise Exception(f"Variable {v} has no FiniteRange type annotation!")

        # make sure parameters can only occur in distributions, PRISM models only support params in trans. prob.
        self.symbols = self.__find_dist_parameters__(self.statements)
        if(len(self.symbols.intersection(self.variables)) > 0):
            raise Exception(f"Variables are not allowed as distribution parameters!")
        self.__check_parameters__(self.statements)

    def add_type(self, t: Type):
        if t is not None:
            self.typedefs[t.variable] = t

    def add_types(self, ts: [Type]):
        for t in ts:
            self.add_type(t)

    def get_type(self, variable) -> Optional[Type]:
        return self.typedefs.get(variable)

    def assign_pc(self) -> int:
        pc = 1
        for stmt in self.statements:
            pc = stmt.assign_pc(pc)
        self.max_pc = pc - 1

    def assign_next_stmt(self):
        block_length = len(self.statements)
        # next_stmt of end statement remains unset
        for i in range(block_length - 1):
            stmt = self.statements[i] 
            stmt.assign_next_stmt(self.statements[i + 1])

    def __find_dist_parameters__(self, stmts):
        """Extract all symbolic parameters from distributions in the list of statements"""
        all_symbols = set()
        for stmt in stmts:
            if isinstance(stmt, DistAssignment):
                all_symbols |= stmt.get_free_symbols()
            if isinstance(stmt, IfStatem):
                all_symbols |= self.__find_dist_parameters__(stmt.if_branch)
                if stmt.else_branch:
                    all_symbols |= self.__find_dist_parameters__(stmt.else_branch)
            if isinstance(stmt, WhileStatem):
                all_symbols |= self.__find_dist_parameters__(stmt.body)
        return all_symbols

    def __check_parameters__(self, stmts):
        """Check that every statement except distributions do not use parameters"""
        for stmt in stmts:
            stmt_symbols = []
            if isinstance(stmt, PolyAssignment):
                stmt_symbols = stmt.get_free_symbols()
            if isinstance(stmt, ObserveStatem):
                stmt_symbols = stmt.condition.get_free_symbols()
            if isinstance(stmt, IfStatem):
                stmt_symbols = stmt.condition.get_free_symbols()
                self.__check_parameters__(stmt.if_branch)
                if stmt.else_branch:
                    self.__check_parameters__(stmt.else_branch)
            if isinstance(stmt, WhileStatem):
                stmt_symbols = stmt.condition.get_free_symbols()
                self.__check_parameters__(stmt.body)

            if not (self.variables.issuperset(stmt_symbols)):
                raise Exception("Only parameters are allowed to use symbolic parameters.")

    def __str__(self):
        typedefs = "\n".join([str(t) for t in self.typedefs.values()])
        staments = "\n".join([str(i) for i in self.statements])

        string = ""
        if self.typedefs:
            string = f"types\n{indent_string(typedefs, 4)}\nend\n"
        string += f"{staments}"
        return string
