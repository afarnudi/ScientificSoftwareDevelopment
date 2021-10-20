#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

print("\nNumber of arguments:, {}".format(len(sys.argv)))
print("Argument list:\n\t", end="")
for arg in sys.argv:
    print(arg, end=" ")
print("\n")
