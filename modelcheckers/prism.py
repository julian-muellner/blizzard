import subprocess
import json
import os
import re

from typing import Callable, Dict, List, Tuple, Set

from .modelchecker import ModelChecker, ModelCheckingStateResult
from symengine.lib.symengine_wrapper import sympify, Symbol

class PrismModelChecker(ModelChecker):
    def __init__(self, is_valid: Callable[[str, int], bool]):
        super().__init__(is_valid)

    def __parse_csv__(self, csv: str) -> List[str]:
        """
        Expect list of values in parenthesis, return the values. 
        String may contain other things as well, first matching parenthesis are used
        Example: "xyxsd(a,b,c)" return ['a', 'b', 'c']
        """
        start_idx = csv.find("(") + 1
        end_idx = csv.find(")")
        return csv[start_idx:end_idx].split(",")

    def __analyze_outfile__(self, statefile: str, resultfile: str, target_pc: int, violation_pc: int) -> List[ModelCheckingStateResult]:
        results = []
        with open(statefile, "r") as stateio, open(resultfile, "r") as resultio:
            # extract ordering
            ordering = self.__parse_csv__(stateio.readline())
            for state, prob in zip(stateio, resultio):
                variable_states = self.__parse_csv__(state)
                variable_states = map(int, variable_states)
                state = dict(zip(ordering, variable_states))
                prob = prob.strip()

                if state["pc"] == target_pc:
                    del state["pc"]
                    result = dict((var, value) for var, value in state.items() if self.is_valid(sympify(var), value)) # remove uninit vars
                    results.append(ModelCheckingStateResult(result, prob))
                elif state["pc"] == violation_pc:
                    results.append(ModelCheckingStateResult({}, prob, is_violation=True))
        return results

    def analyzeSteadyState(self, inputfile: str, symbols: Set[Symbol], tmp_folder: str, target_pc: int, violation_pc: int) -> List[ModelCheckingStateResult]:
        resultfile = f"{tmp_folder}/out.txt"
        statefile = f"{tmp_folder}/states.txt"
        results = None

        if len(symbols) > 0:
            raise Exception("Prism does currently not support parameters in steady-state style queries.")

        # PRISM OUTPUT Format:
        # Statefile has one line of variable ordering and then the states
        # Resultfile has the result for each state in the same order as the statefile
        # Hence statefile[0] has ordering
        # resultfile[i] has result for state statefile[i + 1]
        
        # prism bounded-rw.prism -exportsteadystate out.txt -exportstates states.txt
        cmd = ["prism", inputfile, "-exportsteadystate", resultfile, "-exportstates", statefile]
        completed = subprocess.run(cmd, capture_output=True, text=True)
        if completed.returncode > 0:
            print("FAILURE: Prism aborted with the following trace:")
            print(completed.stdout)
        else:
            results = self.__analyze_outfile__(statefile, resultfile, target_pc, violation_pc) 
            times = re.findall(r"Time for .*?\n", completed.stdout)
            for time in times:
                print("Prism: " + time)

        # try remove files
        if os.path.exists(statefile):
            os.remove(statefile)
        if os.path.exists(resultfile):
            os.remove(resultfile)
        return results

    def analyzeProperties(self, inputfile: str, symbols: Set[Symbol], properties: List[str]) -> List[Tuple[str, str]]:
        results = None

        propstr = ""
        for property in properties:
            propstr += property + ";"

        cmd = ["prism", inputfile, "-pf", propstr]
        if len(symbols) > 0:
            cmd.append("-param")
            
            paramstr = ""
            for i, symbol in enumerate(symbols):
                if i == 0:
                    paramstr += str(symbol)
                else:
                    paramstr += f",{str(symbol)}"
            cmd.append(paramstr)
        
        completed = subprocess.run(cmd, capture_output=True, text=True)
        if completed.returncode > 0:
            print("FAILURE: Prism aborted with the following trace:")
            print(completed.stdout)
        else:
            if len(symbols) > 0:
                results = re.findall(r"Result \(probability\): \(.*\): \{(.*)\}.*\n", completed.stdout)
            else:
                results = re.findall(r"Result: (\S*) .*\n", completed.stdout)
            results = map(str.strip, results)
            results = zip(properties, results)

            times = re.findall(r"Time for .*?\n", completed.stdout)
            for time in times:
                print("Prism: " + time)

        return results