#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from funcs import fibonacci
import os
import argparse


def main():
    os.system("clear")
    parser = argparse.ArgumentParser(
        "Fibonacci Calculator", description="Calculate Fibonacci numbers"
    )
    parser.add_argument("num", help="Print the n'th Fibonacci number.", type=int)

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="store_true")
    group.add_argument("-q", "--quiet", action="store_true")

    args = parser.parse_args()

    result = fibonacci(args.num)
    if args.verbose:
        print(f"The {args.num}'th Fibonacci number is {result}")
    elif args.quiet:
        print(result)
    else:
        print(f"Fib({args.num}) = {result}")


if __name__ == "__main__":
    main()
