#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

def main():
    
    while True:
        try:
            n = input("Please enter an integer: ")
            n = int(n)
            break
        except ValueError:
            print("Not a valid integer! Please try again ...")
    print("Great, you successfully entered an integer!")
            

if __name__=='__main__':
    main()




   
   
   
   
