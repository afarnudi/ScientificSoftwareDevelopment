#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

def main():
    
    my_list = [1,2,3,4,5,'Ali',7,8,9]
    
    my_sum=0
    for item in my_list: 
        try:
            my_sum += float(item)
        except Exception:
            print(f'Could not add "{item}"')
         
    print(f'Sum = {my_sum}')

if __name__=='__main__':
    main()



   
   
