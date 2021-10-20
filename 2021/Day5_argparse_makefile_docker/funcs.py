#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def fibonacci(n):
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
    return a
