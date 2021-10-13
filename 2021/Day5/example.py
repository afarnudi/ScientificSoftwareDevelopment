#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from funcs import fibonacci as fib


#print(sys.argv)
if sys.argv[1] == '-h':
    print("The help")
    sys.exit()


print(fib(int(sys.argv[1])))



