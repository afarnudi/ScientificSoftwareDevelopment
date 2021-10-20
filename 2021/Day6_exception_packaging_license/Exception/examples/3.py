#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

def generate_file():
    pass

def main():
    user_file_name = input("Please enter file name: ")
    
    try:
        read_file =  open(user_file_name, 'r')
    except Exception as e:
        print(e)
        print('Generating file')
        generate_file()
        sys.exit()
        read_file =  open(user_file_name, 'r')
        
    nums = read_file.read()
    print(nums)


if __name__=='__main__':
    main()
