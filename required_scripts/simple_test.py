#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 08:26:11 2020

@author: maeve
"""


# Tests to check tidying comments and variable names doesn't throw errors
import modular_cond_cooling as mcc
folder = "oct_2020"


run_ID = "simple_test_22oct20_c"
mcc.conductive_cooling(run_ID, folder)

run_ID = "simple_test_22oct20_v"
mcc.conductive_cooling(run_ID, folder, cond_constant="n",
 density_constant="n",heat_cap_constant = "n")

