from argparse import Namespace
from executors import TranslationExecutor
from .action import Action
from program import Program
from cli.common import parse_program
from symengine.lib.symengine_wrapper import sympify

class ConvertAction(Action):
    cli_args: Namespace
    program: Program

    def __init__(self, cli_args: Namespace):
        self.cli_args = cli_args

    def __call__(self, *args, **kwargs):
        benchmark = args[0]
        self.program = parse_program(benchmark)

        # make sure all target variables are program variables
        if len(self.cli_args.convert) == 0:
            target_variables = self.program.variables
        else:
            target_variables = {sympify(v) for v in self.cli_args.convert}
            if not self.program.variables.issuperset(target_variables):
                raise Exception(f"Conversion variables are not proper program variables.")
        
        conversion = TranslationExecutor(self.program, enable_sink=False, analyze_vars=target_variables) 

        prism = conversion.convertProgram()
        print(self.program)
        print("\n" * 1 + "#" * 80 + "\n" * 1)
        print(prism)
        print("\n" + "#" * 80 + "\n")
        print(f"Resulting program has {conversion.get_num_states()} states")

        if self.cli_args.out is not None:
            with open(self.cli_args.out, "w") as f:
                f.write(prism)
