#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 14/04/2021
by murphyqm

"""
import pytest
from context import setup_functions as mainmod
from context import numerical_methods as mantle_timestepping
from context import core_function
from context import mantle_properties


@pytest.fixture(scope="session")
def temperature_timestepping():
    timestep = 100000000000.0
    temp_core_melting = 1200.0
    core_cp = 850.0
    core_density = 7800.0
    temp_init = 1600.0
    temp_surface = 250.0
    core_temp_init = 1600.0
    core_latent_heat = 270000.0
    kappa_reg = 5e-08
    dr = 1000.0
    top_mantle_bc = mantle_timestepping.surface_dirichlet_bc
    bottom_mantle_bc = mantle_timestepping.cmb_dirichlet_bc

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
        initial_temperature=core_temp_init,
        melting_temperature=temp_core_melting,
        outer_r=r_core,
        inner_r=0,
        rho=core_density,
        cp=core_cp,
        core_latent_heat=core_latent_heat,
    )
    (mantle_conductivity,
     mantle_heatcap,
     mantle_density) = mantle_properties.set_up_mantle_properties()
    (
        mantle_temperature_array,
        core_temperature_array,
        latent,
    ) = mantle_timestepping.discretisation(
        core_values,
        latent,
        temp_init,
        core_temp_init,
        top_mantle_bc,
        bottom_mantle_bc,
        temp_surface,
        mantle_temperature_array,
        dr,
        core_temperature_array,
        timestep,
        r_core,
        radii,
        times,
        where_regolith,
        kappa_reg,
        cond=mantle_conductivity,
        heatcap=mantle_heatcap,
        dens=mantle_density,
    )
    results = {
        "mantle_temperature_array": mantle_temperature_array,
        "core_temperature_array": core_temperature_array,
        "latent": latent,
        "temp_core_melting": 1200,
        "times": times,
    }
    return results


@pytest.fixture(scope="session")
def temperature_timestepping_var():
    timestep = 100000000000.0
    temp_core_melting = 1200.0
    core_cp = 850.0
    core_density = 7800.0
    temp_init = 1600.0
    temp_surface = 250.0
    core_temp_init = 1600.0
    core_latent_heat = 270000.0
    kappa_reg = 5e-08
    dr = 1000.0
    top_mantle_bc = mantle_timestepping.surface_dirichlet_bc
    bottom_mantle_bc = mantle_timestepping.cmb_dirichlet_bc

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
        initial_temperature=core_temp_init,
        melting_temperature=temp_core_melting,
        outer_r=r_core,
        inner_r=0,
        rho=core_density,
        cp=core_cp,
        core_latent_heat=core_latent_heat,
    )
    (mantle_conductivity,
     mantle_heatcap,
     mantle_density) = mantle_properties.set_up_mantle_properties(
        cond_constant="n",
        density_constant="n",
        heat_cap_constant="n", )
    (
        mantle_temperature_array,
        core_temperature_array,
        latent,
    ) = mantle_timestepping.discretisation(
        core_values,
        latent,
        temp_init,
        core_temp_init,
        top_mantle_bc,
        bottom_mantle_bc,
        temp_surface,
        mantle_temperature_array,
        dr,
        core_temperature_array,
        timestep,
        r_core,
        radii,
        times,
        where_regolith,
        kappa_reg,
        cond=mantle_conductivity,
        heatcap=mantle_heatcap,
        dens=mantle_density,
    )
    results = {
        "mantle_temperature_array": mantle_temperature_array,
        "core_temperature_array": core_temperature_array,
        "latent": latent,
        "temp_core_melting": 1200,
        "times": times,
    }
    return results