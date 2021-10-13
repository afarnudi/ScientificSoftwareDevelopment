#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  8 15:55:55 2019

@author: alifarnudi
"""
import numpy as np
import matplotlib.pyplot as plt

def gen_data(filename, num, length):
    for i in range(num):
        name=filename+str(i)+'.rawdata'
        w_list=np.random.rand(length)
        np.savetxt(name, w_list, delimiter='\n')

gen_data('foo', 3, 10)
gen_data('bar', 3, 10)
