#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 14/04/2021
by murphyqm

"""
import pytest
from context import draft_mainmodule as mainmod
from context import draft_mantle_timestepping_2 as mantle_timestepping
from context import draft_core_functions_2 as core_function

# @pytest.fixture
# def do_something():
#     x = 15
#     y = 12
#     z = x/y
#     return(z)
#
# def test_a_thing(do_something):
#     k = do_something
#     assert k == 1.25


@pytest.fixture(scope="session")  # TODO add (scope="session")
def temperature_timestepping():
    timestep = 100000000000.0
    # r_planet = 250000.0
    # core_size_factor = 0.5
    # reg_fraction = 0.032
    # max_time = 400
    temp_core_melting = 1200.0
    # olivine_cp = 819.0
    # olivine_density = 3341.0
    # cmb_conductivity = 3.0
    core_cp = 850.0
    core_density = 7800.0
    temp_init = 1600.0
    temp_surface = 250.0
    core_temp_init = 1600.0
    core_latent_heat = 270000.0
    kappa_reg = 5e-08
    dr = 1000.0

    (
        r_core,
        radii,
        core_radii,
        reg_thickness,
        where_regolith,
        times,
        mantle_temperature_array,
        core_temperature_array,
    ) = mainmod.set_up()
    latent = []
    core_values = core_function.IsothermalEutecticCore(
        temp=core_temp_init,
        melt=temp_core_melting,
        outer_r=r_core,
        inner_r=0,
        rho=core_density,
        cp=core_cp,
        core_latent_heat=core_latent_heat,
    )

    (
        mantle_temperature_array,
        core_temperature_array,
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
    ) = mantle_timestepping.discretisation(
        core_values,
        latent,
        temp_init,
        core_temp_init,
        temp_core_melting,
        temp_surface,
        mantle_temperature_array,
        dr,
        core_temperature_array,
        timestep,
        core_density,
        core_cp,
        r_core,
        core_latent_heat,
        radii,
        times,
        where_regolith,
        kappa_reg,
    )
    results = {
        "mantle_temperature_array": mantle_temperature_array,
        "core_temperature_array": core_temperature_array,
        "latent": latent,
        "temp_core_melting": 1200,
        "times": times,
    }
    return results
