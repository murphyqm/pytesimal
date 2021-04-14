#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 14/04/2021
by murphyqm

"""
import pytest

from context import draft_mainmodule as mainmod
from context import draft_mantle_timestepping_2 as mantle_timestepping

def temperature_timestepping():
    (r_core,
     radii,
     core_radii,
     reg_thickness,
     where_regolith,
     times,
     mantle_temperature_array,
     core_temperature_array) = mainmod.set_up()
    latent = []

    (mantle_temperature_array,
    core_temperature_array,
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
    delt_listshal,
    )= mantle_timestepping.discretisation(
        latent,
        1600,
        1600,
        1200,
        250,
        mantle_temperature_array,
        1000,
        core_temperature_array,
        1000,
        7800,
        850,
        r_core,
        270_000.0,
        radii,
        times,
        where_regolith,
        5e-08,)
    return (mantle_temperature_array,
    core_temperature_array,
    latent)

temperature_timestepping()