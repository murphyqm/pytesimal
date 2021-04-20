#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 08/04/2021
by murphyqm

Test to check that new core function and mantle are working together correctly
"""

import numpy as np
import pytest
from context import draft_mantle_timestepping_2 as mtt
from context import draft_core_functions_2 as core_functions
from context import draft_mantle_properties as mantle_properties


def test_mtt_discretisation():
    radii = np.arange(100000.0, 200000.0, 1000.0)
    times = np.arange(0, 1000000000 + 0.5 * 1.0, 10000.0)
    core = np.arange(0, 100000.0 - 1000.0 + 0.5 * 1000.0, 1000.0)
    temperatures = np.zeros((radii.size, times.size))
    coretemp = np.zeros((core.size, times.size))
    where_regolith = np.zeros_like(radii)
    top_mantle_bc = mtt.surface_dirichlet_bc
    bottom_mantle_bc = mtt.cmb_dirichlet_bc
    core_values = core_functions.IsothermalEutecticCore(
        temp=1800.0,
        melt=1200.0,
        outer_r=10000.0,
        inner_r=0,
        rho=7800.0,
        cp=850.0,
        core_latent_heat=270000.0,
    )
    (mantle_conductivity,
     mantle_heatcap,
     mantle_density) = mantle_properties.set_up_mantle_properties()
    (
        temperatures,
        coretemp,
        latent,
        # temp_list_mid_mantle,
        # temp_list_shal,
        # temp_list_cmb_5,
        # A_1list,
        # B_1list,
        # C_1list,
        # delt_list,
        # A_1listcmb,
        # B_1listcmb,
        # C_1listcmb,
        # delt_listcmb,
        # A_1listshal,
        # B_1listshal,
        # C_1listshal,
        # delt_listshal,
    ) = mtt.discretisation(
        core_values=core_values,
        latent=[],
        temp_init=1800.0,
        core_temp_init=1800,
        top_mantle_bc=top_mantle_bc,
        bottom_mantle_bc=bottom_mantle_bc,
        temp_surface=100.0,
        temperatures=temperatures,
        dr=1000.0,
        coretemp_array=coretemp,
        timestep=10000.0,
        r_core=10000.0,
        radii=radii,
        times=times,
        where_regolith=where_regolith,
        kappa_reg=1.0,
        cond=mantle_conductivity,
        heatcap=mantle_heatcap,
        dens=mantle_density,
        non_lin_term="y",
    )
    temp_mean = np.mean(temperatures)
    coretemp_mean = np.mean(coretemp)
    # delt_listshal_mean = np.mean(delt_listshal)

    assert temp_mean == pytest.approx(1338.428508059057, 0.0000000001)
    assert coretemp_mean == pytest.approx(1800.0)
    # assert delt_listshal_mean == pytest.approx(0.0034806426277591207)
    print("Success.")


def test_mtt_vardiscretisation():
    radii = np.arange(100000.0, 500000.0, 1000.0)
    times = np.arange(0, 1000000000 + 0.5 * 1.0, 10000.0)
    core = np.arange(0, 100000.0 - 1000.0 + 0.5 * 1000.0, 1000.0)
    temperatures = np.zeros((radii.size, times.size))
    coretemp = np.zeros((core.size, times.size))
    where_regolith = np.zeros_like(radii)
    top_mantle_bc = mtt.surface_dirichlet_bc
    bottom_mantle_bc = mtt.cmb_dirichlet_bc
    core_values = core_functions.IsothermalEutecticCore(
        temp=1800.0,
        melt=1200.0,
        outer_r=10000.0,
        inner_r=0,
        rho=7800.0,
        cp=850.0,
        core_latent_heat=270000.0,
    )
    (mantle_conductivity,
     mantle_heatcap,
     mantle_density) = mantle_properties.set_up_mantle_properties(
                                                cond_constant="n",
                                                density_constant="n",
                                                heat_cap_constant="n",)
    (
        temperatures,
        coretemp,
        latent,
        # temp_list_mid_mantle,
        # temp_list_shal,
        # temp_list_cmb_5,
        # A_1list,
        # B_1list,
        # C_1list,
        # delt_list,
        # A_1listcmb,
        # B_1listcmb,
        # C_1listcmb,
        # delt_listcmb,
        # A_1listshal,
        # B_1listshal,
        # C_1listshal,
        # delt_listshal,
    ) = mtt.discretisation(
        latent=[],
        core_values=core_values,
        temp_init=1800.0,
        core_temp_init=1800,
        top_mantle_bc=top_mantle_bc,
        bottom_mantle_bc=bottom_mantle_bc,
        temp_surface=100.0,
        temperatures=temperatures,
        dr=1000.0,
        coretemp_array=coretemp,
        timestep=10000.0,
        r_core=10000.0,
        radii=radii,
        times=times,
        where_regolith=where_regolith,
        kappa_reg=1.0,
        cond=mantle_conductivity,
        heatcap=mantle_heatcap,
        dens=mantle_density,
        non_lin_term="y",
    )
    temp_mean = np.mean(temperatures)
    coretemp_mean = np.mean(coretemp)
    # delt_listshal_mean = np.mean(delt_listshal)
    assert temp_mean == pytest.approx(1692.134212968852, 0.0000000001)
    assert coretemp_mean == pytest.approx(1800.0)
    # assert delt_listshal_mean == pytest.approx(1.012893130791781e-10)
    print("Success.")


def test_mtt_discretisation_cold_mantle():
    radii = np.arange(100000.0, 200000.0, 1000.0)
    times = np.arange(0, 1000000000 + 0.5 * 1.0, 10000.0)
    core = np.arange(0, 100000.0 - 1000.0 + 0.5 * 1000.0, 1000.0)
    temperatures = np.zeros((radii.size, times.size))
    coretemp = np.zeros((core.size, times.size))
    where_regolith = np.zeros_like(radii)
    top_mantle_bc = mtt.surface_dirichlet_bc
    bottom_mantle_bc = mtt.cmb_dirichlet_bc
    core_values = core_functions.IsothermalEutecticCore(
        temp=1800.0,
        melt=1200.0,
        outer_r=10000.0,
        inner_r=0,
        rho=7800.0,
        cp=850.0,
        core_latent_heat=270000.0,
    )
    (mantle_conductivity,
     mantle_heatcap,
     mantle_density) = mantle_properties.set_up_mantle_properties()
    (
        temperatures,
        coretemp,
        latent,
        # temp_list_mid_mantle,
        # temp_list_shal,
        # temp_list_cmb_5,
        # A_1list,
        # B_1list,
        # C_1list,
        # delt_list,
        # A_1listcmb,
        # B_1listcmb,
        # C_1listcmb,
        # delt_listcmb,
        # A_1listshal,
        # B_1listshal,
        # C_1listshal,
        # delt_listshal,
    ) = mtt.discretisation(
        latent=[],
        core_values=core_values,
        temp_init=1400.0,
        core_temp_init=1800,
        top_mantle_bc=top_mantle_bc,
        bottom_mantle_bc=bottom_mantle_bc,
        temp_surface=100.0,
        temperatures=temperatures,
        dr=1000.0,
        coretemp_array=coretemp,
        timestep=10000.0,
        r_core=10000.0,
        radii=radii,
        times=times,
        where_regolith=where_regolith,
        kappa_reg=1.0,
        cond=mantle_conductivity,
        heatcap=mantle_heatcap,
        dens=mantle_density,
        non_lin_term="y",
    )
    temp_mean = np.mean(temperatures)
    coretemp_mean = np.mean(coretemp)
    # delt_listshal_mean = np.mean(delt_listshal)
    # print(temp_mean, coretemp_mean, delt_listshal_mean)

    assert temp_mean == pytest.approx(1129.0036119517447, 0.0000000001)
    assert coretemp_mean == pytest.approx(1799.9984226292759)
    # assert delt_listshal_mean == pytest.approx(0.0012771823292144018)
    print("Success.")


def test_mtt_vardiscretisation_cold_mantle():
    radii = np.arange(100000.0, 500000.0, 1000.0)
    times = np.arange(0, 100000000 + 0.5 * 1.0, 1000.0)
    core = np.arange(0, 100000.0 - 1000.0 + 0.5 * 1000.0, 1000.0)
    temperatures = np.zeros((radii.size, times.size))
    coretemp = np.zeros((core.size, times.size))
    where_regolith = np.zeros_like(radii)
    top_mantle_bc = mtt.surface_dirichlet_bc
    bottom_mantle_bc = mtt.cmb_dirichlet_bc
    core_values = core_functions.IsothermalEutecticCore(
        temp=1800.0,
        melt=1200.0,
        outer_r=10000.0,
        inner_r=0,
        rho=7800.0,
        cp=850.0,
        core_latent_heat=270000.0,
    )
    (mantle_conductivity,
     mantle_heatcap,
     mantle_density) = mantle_properties.set_up_mantle_properties(
                                                cond_constant="n",
                                                density_constant="n",
                                                heat_cap_constant="n",)
    (
        temperatures,
        coretemp,
        latent,
        # temp_list_mid_mantle,
        # temp_list_shal,
        # temp_list_cmb_5,
        # A_1list,
        # B_1list,
        # C_1list,
        # delt_list,
        # A_1listcmb,
        # B_1listcmb,
        # C_1listcmb,
        # delt_listcmb,
        # A_1listshal,
        # B_1listshal,
        # C_1listshal,
        # delt_listshal,
    ) = mtt.discretisation(
        core_values=core_values,
        latent=[],
        temp_init=1200.0,
        core_temp_init=1800,
        top_mantle_bc=top_mantle_bc,
        bottom_mantle_bc=bottom_mantle_bc,
        temp_surface=100.0,
        temperatures=temperatures,
        dr=1000.0,
        coretemp_array=coretemp,
        timestep=10000.0,
        r_core=10000.0,
        radii=radii,
        times=times,
        where_regolith=where_regolith,
        kappa_reg=1.0,
        cond=mantle_conductivity,
        heatcap=mantle_heatcap,
        dens=mantle_density,
        non_lin_term="y",
    )
    temp_mean = np.mean(temperatures)
    coretemp_mean = np.mean(coretemp)
    # delt_listshal_mean = np.mean(delt_listshal)
    # print(temp_mean, coretemp_mean, delt_listshal_mean)

    assert coretemp_mean == pytest.approx(1799.9985585325398)
    assert temp_mean == pytest.approx(1161.0663997556733, 0.0000000001)
    assert temp_mean == pytest.approx(1161.0663997556733, 0.0000000001)
    # assert delt_listshal_mean == pytest.approx(-7.581142508447556e-06)
    print("Success.")
