#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Context file to allow import of main module.

Created on Tue Feb  2 13:56:32 2021.

@author: maeve
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
