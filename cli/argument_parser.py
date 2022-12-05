from argparse import ArgumentParser as ArgParser
import glob


class ArgumentParser:

    def __init__(self):
        self.argument_parser = ArgParser(description="Convert a given PP into a PRISM format")
        self.argument_parser.add_argument(
            "benchmarks",
            metavar="benchmarks",
            type=str,
            nargs="+",
            help="A list of benchmarks"
        )
        self.argument_parser.add_argument(
            "--convert",
            type=str,
            nargs="*",
            help="If set we convert the programs to PRISM format. Optional: Pass variables that should be kept in final states."
        )
        self.argument_parser.add_argument(
            "--analyze",
            type=str,
            nargs="*",
            help="Analyze the given program and extract posterior over list of variables given in argument. Example: --analyze x y z"
        )
        self.argument_parser.add_argument(
            "--out",
            type=str,
            help="Write the result of a call to a file given as argument. Works only for the last benchmark."
        )
        self.argument_parser.add_argument(
            "--checker",
            type=str,
            choices=["storm", "prism"],
            default="storm",
            help="Select the model checker used to discharge the resulting query."
        )
        self.argument_parser.add_argument(
            "--style",
            type=str,
            choices=["steadystate", "property"],
            default="steadystate",
            help="Select how the model checker will be run on the query. Either use steady-state probabilities or run property-by-property queries."
        )

    def parse_args(self):
        args = self.argument_parser.parse_args()
        args.benchmarks = [b for bs in map(glob.glob, args.benchmarks) for b in bs]

        if len(args.benchmarks) == 0:
            raise Exception("No benchmark given. Run with '--help' for more information.")

        return args

    def get_defaults(self):
        return self.argument_parser.parse_args({"benchmarks": []})
