#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def main():
    try:
        numer = input()
        k = 5//numer  # raises divide by zero exception.
        print(k)
    except ZeroDivisionError:
        print("Can't divide by zero")


if __name__=='__main__':
    main()
