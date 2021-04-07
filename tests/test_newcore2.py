#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 17:01:06 2021

@author: maeve
"""

from context import draft_core_functions as new_core_function
from context import draft_core_functions_2 as new_core_function_2
import numpy as np
import pytest


def test_new_core_function():
    radii = np.arange(10000.0, 50000.0, 1000.0)
    times = np.arange(0, 100 + 0.5 * 1.0, 1.0)
    temperatures = np.zeros((radii.size, times.size))
    core = new_core_function.Core(temp=1000.0,
                                  melt=1200.0,
                                  r=10000.0,
                                  rho=7800.0,
                                  cp=850.0,
                                  maxlh=10000.0,
                                  lat=7000.0)
    core.cooling(temperatures,
                 timestep=1.0,
                 dr=100.0,
                 i=1,
                 cmbk=3.0)
    latent = core.latentlist
    core_lh_extracted = core.latent
    temperature_core = core.temperature
    assert latent == [7000.0]
    assert core_lh_extracted == 7000.0
    assert temperature_core == 1000.0
    print("Success.")

