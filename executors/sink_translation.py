from typing import ClassVar, Dict, List, Set, Tuple
from symengine.lib.symengine_wrapper import Expr, Symbol
from program.endstatem.endstatem import EndStatem

from program.ifstatem import IfStatem
from program.observestatem.observestatem import ObserveStatem
from program.program import Program
from program.type.finite_range import FiniteRange
from program.whilestatem import WhileStatem
from program.assignment.dist_assignment import DistAssignment
from program.assignment.poly_assignment import PolyAssignment
from executors.executor import Executor

# Notes regarding the encoding:
# Initially, every program variable is set to lower_bound - 1, so that we can detect if a variable might be uninitialized at the end, PC is set to 0
# The state encoding is quite obvious, but the pc always talks about the line AFTER execution
# All terminal states have PC = program.max_pc
# The sink state has PC program.max_pc + 1 and all variables are else set to their lower bound - 1
# The violation state has PC (-1) and all variables set to their lower bound - 1

class MCState:
    state: Tuple[Tuple[Symbol, int]]
    pc: int

    def __init__(self, state: Dict[Symbol, int], pc: int):
        self.state = tuple(state.items())
        self.pc = pc

    def __str__(self):
        txt = "("
        for key, value in self.state:
            txt += f"{key}: {value}, "
        return txt + f"{self.pc} )"

    def __eq__(self, other):
        if self.pc != other.pc:
            return False
        
        return self.state == other.state

    def __hash__(self):
        return hash((self.pc, self.state))

class SinkTranslation(Executor):
    """Translate a program into a Markov chain that has a sink state. 
    Expected visit times of non-terminal states is reachability probability"""
    states: Set[MCState]
    transitions: Dict[MCState, Set[Tuple[MCState, Expr]]] # map states to their outgoing edges
    program: Program
    violation_state: MCState # state where violated assertions go
    sink_state: MCState # state where everything is going in the end

    def __init__(self, program: Program):
        self.states = set()
        self.transitions = {} 
        self.program = program

    def convertProgram(self):
        # empty state
        empty_state =  {}
        for v in self.program.variables:
            assert(isinstance(self.program.get_type(v), FiniteRange))
            empty_state[v] = self.program.get_type(v).lower - 1

        # sink states
        self.sink_state = MCState(empty_state, self.program.max_pc + 1)
        self.states.add(self.sink_state)
        self.__add_transition__(self.sink_state, self.sink_state, 1)

        # construct violation state
        self.violation_state = MCState(empty_state, -1)
        self.states.add(self.violation_state)
        self.__add_transition__(self.violation_state, self.sink_state, 1)

        # kick off execution
        stmt = self.program.statements[0]
        initial = MCState(empty_state, stmt.pc - 1)
        self.states.add(initial)
        self.execute(stmt, (empty_state, initial))
        return self.__convert_to_prism__()

    def executeIf(self, stmt: IfStatem, ctx):
        state, _ = ctx
        cond = stmt.condition.evaluate(state)
        if cond:
            return [(stmt.if_branch[0], ctx)]
        else:
            return [(stmt.else_branch[0], ctx)]

    def executeWhile(self, stmt: WhileStatem, ctx):
        state, _ = ctx
        cond = stmt.condition.evaluate(state)
        if cond:
            return [(stmt.body[0], ctx)]
        else:
            return [(stmt.next_stmt, ctx)]

    def executeDistAssign(self, stmt: DistAssignment, ctx):
        state, pred = ctx
        possible_values = stmt.distribution.get_support_with_probability()
        continuations = []
        
        for (val, prob) in possible_values:
            state_copy = state.copy()
            self.__assert_variable_constraints__(stmt.variable, val)
            state_copy[stmt.variable] = val
            mc_state = MCState(state_copy, stmt.pc)

            self.__add_transition__(pred, mc_state, prob)
            if mc_state in self.states:
                continue

            self.states.add(mc_state)
            continuations.append((stmt.next_stmt, (state_copy, mc_state)))
        return continuations

    def executePolyAssign(self, stmt: PolyAssignment, ctx):
        state, pred = ctx

        e = stmt.evaluate_right_side(state)
        self.__assert_variable_constraints__(stmt.variable, e)
        state[stmt.variable] = int(e)
        mc_state = MCState(state, stmt.pc)
        
        self.__add_transition__(pred, mc_state, 1)
        if mc_state in self.states:
            return

        self.states.add(mc_state)
        return [(stmt.next_stmt, (state, mc_state))]

    def executeObserve(self, stmt: ObserveStatem, ctx):
        state, pred = ctx
        cond = stmt.condition.evaluate(state)
        if cond:
            return [(stmt.next_stmt, ctx)]
        else:
            self.__add_transition__(pred, self.violation_state, 1)
            return []

    def executeEnd(self, stmt: EndStatem, ctx):
        # add tranistion into end state, only change PC
        state, pred = ctx
        mc_state = MCState(state, stmt.pc)
        self.__add_transition__(pred, mc_state, 1)
        self.states.add(mc_state)

        # add transition to sink state
        self.__add_transition__(mc_state, self.sink_state, 1)
        return []

    def __add_transition__(self, origin: MCState, end: MCState, prob: Expr):
        if origin in self.transitions:
            set = self.transitions[origin]
            set.add((end, prob))
        else:
            lst = {(end, prob)}
            self.transitions[origin] = lst

    def __str__(self):
        txt = ""
        lst = sorted(self.transitions.items(), key=lambda k: k[0].pc) # sort by pc of origin
        for s0, edges in lst:
            for (s1, p) in edges:
                txt += f"{s0} ---({p})--> {s1}\n"
        return txt

    def __convert_to_prism__(self):
        prism = "dtmc\n\n"
        for p in self.program.symbols:
            prism += f"const double {p};\n"
        
        prism += "\nmodule generated\n"

        # Variable definitions
        prism += " " * 4 + f"pc: [-1..{self.program.max_pc + 1}] init 0;\n"
        for v in self.program.variables:
            t = self.program.get_type(v)
            assert(isinstance(t, FiniteRange))
            prism += " " * 4 + f"{v} : [{t.lower - 1}..{t.upper}] init {t.lower - 1};\n"

        prism += "\n"

        # transitions
        lst = sorted(self.transitions.items(), key=lambda k: k[0].pc) # sort by pc of origin
        for s0, edges in lst:
            guard = self.__encode_state__(s0)
            rhs = ""
            for i, (s1, p) in enumerate(edges):
                if i != 0:
                    rhs += " + "
                rhs += f"{p}: {self.__encode_state__(s1, primed=True)}"
            prism += " " * 4 + f"[] {guard} -> {rhs};\n"
        
        return prism + "endmodule\n\n"
    
    def __encode_state__(self, mc_state: MCState, primed: bool = False):
        prime = ""
        if primed:
            prime = "'"
        state = f"(pc{prime}={mc_state.pc})"
        for (v, val) in mc_state.state:
            state += f"&({v}{prime}={val})"
        return state

    def __assert_variable_constraints__(self, variable: Symbol, value: int):
        if not value.is_integer:
            raise Exception(f"Variable {variable} is assigned non-integer value {value}")
        t = self.program.get_type(variable)
        if not (value >= t.lower and value <= t.upper):
            raise Exception(f"Variable {variable} is assigned value {value} out of its declared range!")
