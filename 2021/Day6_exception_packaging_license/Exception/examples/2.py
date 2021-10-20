#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

def main():
    user_file_name = input("Please enter file name: ")
    
    try:
        read_file =  open(user_file_name, 'r')
    except:
        print(f'Error! I could not find/read "{user_file_name}"')
        sys.exit()
    nums = read_file.read()
    print(nums)


if __name__=='__main__':
    main()
