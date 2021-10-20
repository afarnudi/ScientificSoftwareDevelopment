#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

def main():
    
   try:
       file = open("testfile", "w")
       try:
          file.write("This is my test file for exception handling!!")
       finally:
          print("Going to close the file")
          file.close()
   except Exception as e:
       print("Error:")
       print(e)

if __name__=='__main__':
    main()




   
   
   
   