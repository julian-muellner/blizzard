import subprocess
import json
import os
import re

from typing import Dict, List, Tuple

from .modelchecker import ModelChecker, ModelCheckingStateResult

class PrismModelChecker(ModelChecker):
    def __init__(self):
        None

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
            for state, result in zip(stateio, resultio):
                variable_states = self.__parse_csv__(state)
                variable_states = map(int, variable_states)
                state = dict(zip(ordering, variable_states))

                if state["pc"] == target_pc:
                    del state["pc"]
                    results.append(ModelCheckingStateResult(state, float(result)))
                elif state["pc"] == violation_pc:
                    results.append(ModelCheckingStateResult({}, float(result), is_violation=True))
        return results

    def analyzeSteadyState(self, inputfile: str, tmp_folder: str, target_pc: int, violation_pc: int) -> List[ModelCheckingStateResult]:
        resultfile = f"{tmp_folder}/out.txt"
        statefile = f"{tmp_folder}/states.txt"
        results = None

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

    def analyzeProperties(self, inputfile: str, properties: List[str]) -> List[Tuple[str, float]]:
        results = None

        propstr = ""
        for property in properties:
            propstr += property + ";"
        
        cmd = ["prism", inputfile, "-pf", propstr]
        completed = subprocess.run(cmd, capture_output=True, text=True)
        if completed.returncode > 0:
            print("FAILURE: Prism aborted with the following trace:")
            print(completed.stdout)
        else:
            results = re.findall(r"Result: (\S*) .*\n", completed.stdout)
            results = map(float, results)
            results = zip(properties, results)

            times = re.findall(r"Time for .*?\n", completed.stdout)
            for time in times:
                print("Prism: " + time)

        return results