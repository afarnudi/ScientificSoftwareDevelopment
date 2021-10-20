#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  8 17:11:37 2019

@author: alifarnudi
"""
import numpy as np
import matplotlib.pyplot as plt
import sys

filename=str(sys.argv[1])[:-5]
data=np.loadtxt(sys.argv[1])
if filename=='foo':
    plt.plot(np.arange(len(data)),data, 'ro-')
else:
    plt.plot(np.arange(len(data)),data, 'bo-')
plt.xlabel('time (s)')
plt.ylabel('velocity (m/s)')
plt.title(str(sys.argv[1]))
plt.savefig(filename)
