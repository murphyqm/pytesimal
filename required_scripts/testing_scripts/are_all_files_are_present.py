#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 14:51:52 2020

@author: maeve
"""


# testing that all the required files are present

import modular_cond_cooling as mcc
run_ID = "temp_testing"
folder = "temp_outputs"
mcc.conductive_cooling(run_ID, folder, plotting = "temp",)
