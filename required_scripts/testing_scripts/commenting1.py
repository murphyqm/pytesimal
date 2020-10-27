#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 08:26:11 2020

@author: maeve
"""


# Tests to check tidying comments and variable names doesn't throw errors
import modular_cond_cooling as mcc
run_ID = "commenting_test2"
folder = "testing_results_folder"

mcc.conductive_cooling(run_ID, folder)
