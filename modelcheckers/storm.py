import subprocess
import json
import os
import re

from typing import Callable, Dict, List, Set, Tuple

from executors import MarkovState
from .modelchecker import ModelChecker, ModelCheckingStateResult
from symengine.lib.symengine_wrapper import sympify, Symbol

class StormModelChecker(ModelChecker):

    def __init__(self, is_valid: Callable[[str, int], bool]):
        super().__init__(is_valid)

    def __convert_json_to_result__(self, state):
        prob = state["v"]
        pc = int(state["s"]["pc"])
        del state["s"]["pc"]
        result = dict((var, value) for var, value in state["s"].items() if self.is_valid(sympify(var), value)) # remove uninit vars
        return ModelCheckingStateResult(result, prob)

    def __analyze_outfile__(self, outfile: str, target_pc: int, violation_pc: int) -> List[ModelCheckingStateResult]:
        results = []
        with open(outfile, "r") as filehandle:
            result_json = json.load(filehandle)
            for state in result_json:
                if state["s"]["pc"] == target_pc:
                    results.append(self.__convert_json_to_result__(state))
                elif state["s"]["pc"] == violation_pc:
                    results.append(ModelCheckingStateResult({}, state["v"], is_violation=True))
        return results

    def analyzeSteadyState(self, inputfile: str, symbols: Set[Symbol], tmp_folder: str, target_pc: int, violation_pc: int) -> List[ModelCheckingStateResult]:
        outfile = f"{tmp_folder}/out.json"
        results = None

        if len(symbols) > 0:
            raise Exception("Storm does currently not support parameters in steady-state style queries.")
        
        # ./storm --prism /data/out.prism --steadystate --exportresult /data/out.json --buildstateval
        cmd = ["storm", "--prism", inputfile, "--steadystate", "--exportresult", outfile, "--buildstateval"]
        completed = subprocess.run(cmd, capture_output=True, text=True)
        if completed.returncode > 0:
            print("FAILURE: Storm aborted with the following trace:")
            print(completed.stdout)
        else:
            results = self.__analyze_outfile__(outfile, target_pc, violation_pc) 
            times = re.findall(r"Time for model.*?\n", completed.stdout)
            for time in times:
                print("Storm: " + time)

        # try remove outfile
        if os.path.exists(outfile):
            os.remove(outfile)
        return results

    def analyzeProperties(self, inputfile: str, symbols: Set[Symbol], properties: List[str]) -> List[Tuple[str, str]]:
        results = None

        propstr = ""
        for property in properties:
            propstr += property + ";"

        stormexe = "storm"
        if len(symbols) > 0:
            stormexe += "-pars"
        
        cmd = [stormexe, "--prism", inputfile, "--prop", propstr]
        completed = subprocess.run(cmd, capture_output=True, text=True)
        if completed.returncode > 0:
            print("FAILURE: Storm aborted with the following trace:")
            print(completed.stdout)
        else:
            results = re.findall(r"Result \(.*\): (.*?)\n", completed.stdout)
            results = map(str.strip, results)
            results = zip(properties, results)

            times = re.findall(r"Time for model.*?\n", completed.stdout)
            for time in times:
                print("Storm: " + time)

        return results