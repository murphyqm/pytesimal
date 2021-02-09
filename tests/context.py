#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Context file to allow import of main module.

Created on Tue Feb  2 13:56:32 2021.

@author: maeve
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '../pytesimal/')))
# sys.path.insert(0, os.path.abspath('../pytesimal/'))
import modular_cond_cooling
import modular_temp_timestepping
import draft_mantle_timestepping  # implements new core
import draft_core_functions  # new core
import draft_mantle_properties  # mantle props as methods within a class
