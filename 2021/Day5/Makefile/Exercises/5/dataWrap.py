#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  8 16:51:26 2019

@author: alifarnudi
"""
import numpy as np
import matplotlib.pyplot as plt
import sys

file=sys.argv[1:]

print('\nAha! New data was generated!\n')

mean=np.zeros(np.shape(np.loadtxt(file[0])))
for f in file:
    lis=np.loadtxt(f)
    mean += lis

mean=mean/3
file_name=str(sys.argv[1])[:-9]+'.data'
with open(file_name, 'w') as f:
    np.savetxt(file_name, mean, delimiter='\n')

    
