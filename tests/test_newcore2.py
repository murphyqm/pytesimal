#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 17:01:06 2021

@author: maeve
"""


from context import draft_core_functions_2 as new_core_function_2
import numpy as np
import pytest


def test_new_core_function_1():
    radii = np.arange(10000.0, 50000.0, 1000.0)
    times = np.arange(0, 100 + 0.5 * 1.0, 1.0)
    temperatures = np.zeros((radii.size, times.size))
    core = new_core_function_2.IsothermalEutecticCore(temp=1000.0,
                                                      melt=1200.0,
                                                      outer_r=10000.0,
                                                      inner_r = 0,
                                                      rho=7800.0,
                                                      cp=850.0,
                                                      #maxlh=10000.0,
                                                      core_latent_heat=3.060671982536449e-13,
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

def test_new_core_function_2():
    radii = np.arange(10000.0, 50000.0, 1000.0)
    times = np.arange(0, 100 + 0.5 * 1.0, 1.0)
    temperatures = np.zeros((radii.size, times.size))
    cmb_energy = new_core_function_2.EnergyExtractedAcrossCMB(outer_r=10000.0,
                                                          timestep=1.0,
                                                          radius_step=1000.0)

    core = new_core_function_2.IsothermalEutecticCore(temp=1000.0,
                                                      melt=1200.0,
                                                      outer_r=10000.0,
                                                      inner_r = 0,
                                                      rho=7800.0,
                                                      cp=850.0,
                                                      core_latent_heat=3.060671982536449e-13,
                                                      lat=7000.0)
    # core.cooling(temperatures,
    #              timestep=1.0,
    #              dr=100.0,
    #              i=1,
    #              cmbk=3.0)
    energy = cmb_energy.energy_extracted(temperatures,
                                         i=1,
                                         k=3.0)
    core.extract_energy(energy)
    latent = core.latentlist
    core_lh_extracted = core.latent
    temperature_core = core.temperature
    assert latent == [7000.0]
    assert core_lh_extracted == 7000.0
    assert temperature_core == 1000.0
    print("Success.")