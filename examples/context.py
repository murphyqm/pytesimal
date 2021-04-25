#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 25/04/2021
by murphyqm

Importing modules so package doesn't have to be installed to run examples.
"""
import os
import sys

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../pytesimal/")),
)

import numerical_methods
import core_function
import mantle_properties
import setup_functions
import analysis
import load_plot_save