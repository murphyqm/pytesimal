#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 17:01:06 2021

@author: maeve
"""

from context import numerical_methods as nm
from context import core_function
import numpy as np


def test_new_core_unit():
    radii = np.arange(10000.0, 50000.0, 1000.0)
    times = np.arange(0, 100 + 0.5 * 1.0, 1.0)
    temperatures = np.zeros((radii.size, times.size))
    cmb_energy = nm.EnergyExtractedAcrossCMB(
        outer_r=10000.0, timestep=1.0, radius_step=1000.0
    )

    core = core_function.IsothermalEutecticCore(
        initial_temperature=1000.0,
        melting_temperature=1200.0,
        outer_r=10000.0,
        inner_r=0,
        rho=7800.0,
        cp=850.0,
        core_latent_heat=3.060671982536449e-13,
        lat=7000.0,
    )
    heat = cmb_energy.power(temperatures, i=1, k=3.0)
    core.extract_heat(heat, timestep=1.0)
    latent = core.latentlist
    core_lh_extracted = core.latent
    temperature_core = core.temperature
    assert latent == [7000.0]
    assert core_lh_extracted == 7000.0
    assert temperature_core == 1000.0
    print("Success.")
