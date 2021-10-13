#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from fibonacci import fibonacci
import os


def main():
    os.system("clear")
    print(fibonacci(int(sys.argv[1])))


if __name__ == "__main__":
    main()
