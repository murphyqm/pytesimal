#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 15:50:11 2020

@author: maeve
"""


# Tests to fix filepath issues
import modular_cond_cooling as mcc
run_ID = "remove_temp_timestepping"
folder = "testing_results_folder"

mcc.conductive_cooling(run_ID, folder)
