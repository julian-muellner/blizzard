#!/usr/bin/env python3

import time
from cli import ArgumentParser
from cli.actions import ActionFactory


def main():
    start = time.time()
    args = ArgumentParser().parse_args()

    try:
        action = ActionFactory.create_action(args)
        for benchmark in args.benchmarks:
            action(benchmark)
    except Exception as e:
        print(e)
        exit()

    print(f"Elapsed time: {time.time() - start} s")


if __name__ == "__main__":
    main()
