#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse


def main():
    os.system("clear")

    parser = argparse.ArgumentParser(prog="PROG")
    parser.add_argument("-d","--default")
    parser.add_argument("--store_const", action="store_const", const=2)
    parser.add_argument("--store_true", action="store_true")
    parser.add_argument("--store_false", action="store_false")
    parser.add_argument("--count", "-c", action="count", default=0)
    parser.add_argument("--version", action="version", version="%(prog)s 2.0")

    args = parser.parse_args()
    print(args)


if __name__ == "__main__":
    main()
