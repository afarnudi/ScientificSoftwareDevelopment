#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

def main():
    
    x_list = ["hello", 1, 2, 4.5, 'B']
    
    for x in x_list:
        if type(x) is not int:
          raise TypeError("Only integers are allowed")

if __name__=='__main__':
    main()




   
   
   
   