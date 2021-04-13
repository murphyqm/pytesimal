#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 17:01:06 2021

@author: maeve
"""

from context import modular_temp_timestepping as mtt
# from pytesimal import modular_temp_timestepping as mtt
import numpy as np
import pytest


def test_mtt_core_cooling():
    radii = np.arange(10000.0, 50000.0, 1000.0)
    times = np.arange(0, 100 + 0.5 * 1.0, 1.0)
    temperatures = np.zeros((radii.size, times.size))
    (latent,
     core_lh_extracted,
     temperature_core) = mtt.core_cooling(latent=[],
                                          i=1,
                                          dr=100.0,
                                          temperature_core=1000.0,
                                          temp_core_melting=1200.0,
                                          core_lh_extracted=7000.0,
                                          max_core_lh=10000.0,
                                          cmb_conductivity=3.0,
                                          temperatures=temperatures,
                                          timestep=1.0,
                                          core_density=7800.0,
                                          core_cp=850.0,
                                          r_core=10000.0,
                                          )
    assert latent == [7000.0]
    assert core_lh_extracted == 7000.0
    assert temperature_core == 1000.0
    print("Success.")


def test_mtt_discretisation():
    radii = np.arange(10000.0, 50000.0, 1000.0)
    times = np.arange(0, 100 + 0.5 * 1.0, 1.0)
    core = np.arange(0, 10000.0 - 1000.0 + 0.5 * 1000.0, 1000.0)
    temperatures = np.zeros((radii.size, times.size))
    coretemp = np.zeros((core.size, times.size))
    kappas = np.ones_like(radii)
    where_regolith = np.zeros_like(radii)
    (temperatures,
        coretemp,
        latent,
        temp_list_mid_mantle,
        temp_list_shal,
        temp_list_cmb_5,
        A_1list,
        B_1list,
        C_1list,
        delt_list,
        A_1listcmb,
        B_1listcmb,
        C_1listcmb,
        delt_listcmb,
        A_1listshal,
        B_1listshal,
        C_1listshal,
        delt_listshal,) = mtt.discretisation(latent=[],
                                             temp_init=1300.0,
                                             temp_core_melting=1200.0,
                                             temp_surface=100.0,
                                             cmb_conductivity=10.0,
                                             p=3000.0,
                                             c=800.0,
                                             temperatures=temperatures,
                                             dr=1000.0,
                                             coretemp=coretemp,
                                             timestep=1.0,
                                             core_density=7800.0,
                                             core_cp=850.0,
                                             r_core=10000.0,
                                             core_latent_heat=270000.0,
                                             radii=radii,
                                             times=times,
                                             kappas=kappas,
                                             where_regolith=where_regolith,
                                             kappa_reg=1.0,
                                             cond_constant="y",
                                             density_constant="y",
                                             heat_cap_constant="y",
                                             non_lin_term="y",
                                             is_a_test="n",
                                             i_choice=126228,
                                             TESTING="n",
                                             )
    temp_mean = np.mean(temperatures)
    coretemp_mean = np.mean(coretemp)
    delt_listshal_mean = np.mean(delt_listshal)
    assert temp_mean == pytest.approx(1270.2955288227372, 0.00001)
    assert coretemp_mean == pytest.approx(1300.0)
    assert delt_listshal_mean == pytest.approx(0.0)
    print("Success.")
