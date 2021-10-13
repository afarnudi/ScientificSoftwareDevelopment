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

    args = parser.parse_args()

    result = fibonacci(args.num)
    print(f"Fib({args.num}) = {result}")


if __name__ == "__main__":
    main()
