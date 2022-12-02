from typing import Dict, Set, Tuple
from symengine.lib.symengine_wrapper import Expr, Symbol

from program import Program

from .markovstate import MarkovState

class MarkovChain:
    states: Set[MarkovState]
    transitions: Dict[MarkovState, Set[Tuple[MarkovState, Expr]]] # map states to their outgoing edges

    def __init__(self):
        self.states = set()
        self.transitions = {} 

    def add_state(self, state: MarkovState) -> None:
        self.states.add(state)

    def has_state(self, state: MarkovState) -> bool:
        return state in self.states

    def get_num_states(self) -> int:
        return len(self.states)

    def add_transition(self, origin: MarkovState, end: MarkovState, prob: Expr) -> None:
        if origin in self.transitions:
            set = self.transitions[origin]
            set.add((end, prob))
        else:
            lst = {(end, prob)}
            self.transitions[origin] = lst

    # TODO: pass dict of range instead of program 
    def convert_to_prism(self, program: Program, pc_lower_bound, pc_upper_bound) -> str:
        prism = "dtmc\n\n"
        for p in program.symbols:
            prism += f"const double {p};\n"
        
        prism += "\nmodule generated\n"

        # Variable definitions
        prism += " " * 4 + f"pc: [{pc_lower_bound}..{pc_upper_bound}] init 0;\n"
        for v in program.variables:
            t = program.get_type(v)
            prism += " " * 4 + f"{v} : [{t.lower - 1}..{t.upper}] init {t.lower - 1};\n"
        prism += "\n"

        # transitions
        lst = sorted(self.transitions.items(), key=lambda k: k[0].pc) # sort by pc of origin
        for s0, edges in lst:
            guard = s0.get_prism_encoding()
            rhs = ""
            for i, (s1, p) in enumerate(edges):
                if i != 0:
                    rhs += " + "
                rhs += f"{p}: {s1.get_prism_encoding(primed=True)}"
            prism += " " * 4 + f"[] {guard} -> {rhs};\n"
        
        return prism + "endmodule\n\n"

    def __str__(self):
        txt = ""
        lst = sorted(self.transitions.items(), key=lambda k: k[0].pc) # sort by pc of origin
        for s0, edges in lst:
            for (s1, p) in edges:
                txt += f"{s0} ---({p})--> {s1}\n"
        return txt