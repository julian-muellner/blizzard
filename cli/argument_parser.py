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
            help="A list of benchmarks to convert"
        )
        self.argument_parser.add_argument(
            "--convert",
            type=str,
            help="If set we convert the programs to PRISM format, argument: filename"
        )
        self.argument_parser.add_argument(
            "--analyze",
            type=str,
            help="If set we run a model checker and dump the result to a file, argument: filename"
        )
        # TODO: select model checker

    def parse_args(self):
        args = self.argument_parser.parse_args()
        args.benchmarks = [b for bs in map(glob.glob, args.benchmarks) for b in bs]

        if len(args.benchmarks) == 0:
            raise Exception("No benchmark given. Run with '--help' for more information.")

        return args

    def get_defaults(self):
        return self.argument_parser.parse_args({"benchmarks": []})
