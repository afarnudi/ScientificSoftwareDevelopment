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
    parser.add_argument("-p","--print", help="Print Fibonacci number up to the n'th number", action= "store_true")
    args = parser.parse_args()

    result = fibonacci(args.num)
    if args.print=='True':
        for i in range(2,args.num+1):
            print(fibonacci(i),end=' ')
    else:
        print(f"Fib({args.num}) = {result}")


if __name__ == "__main__":
    main()
