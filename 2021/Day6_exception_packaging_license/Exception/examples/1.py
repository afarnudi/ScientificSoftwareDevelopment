#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def main():
    user_file_name = input("Please enter file name: ")
    read_file =  open(user_file_name, 'r')
    nums = read_file.read()
    print(nums)


if __name__=='__main__':
    main()