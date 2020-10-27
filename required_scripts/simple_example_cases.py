#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 08:26:11 2020

@author: maeve
"""


# Tests to check tidying comments and variable names doesn't throw errors
import modular_cond_cooling as mcc
folder = "setting_up_tests_oct_2020"


run_ID = "simple_test_22oct20_c"
begins_to_freeze, finished_freezing, Esquel_Depth, Esq_timing, Imilac_Depth, Im_timing = mcc.conductive_cooling(run_ID, folder,return_vars = "y",save_param_file = "n")

run_ID = "simple_test_22oct20_v"
vbegins_to_freeze, vfinished_freezing, vEsquel_Depth, vEsq_timing, vImilac_Depth, vIm_timing = mcc.conductive_cooling(run_ID, folder, cond_constant="n",
  density_constant="n",heat_cap_constant = "n",return_vars = "y",save_param_file = "n")

print("Constant!")
print("")
print(begins_to_freeze, finished_freezing, Esquel_Depth, Esq_timing, Imilac_Depth, Im_timing)
print("")
print("***")
print("Variable!")
print("")
print(vbegins_to_freeze, vfinished_freezing, vEsquel_Depth, vEsq_timing, vImilac_Depth, vIm_timing)