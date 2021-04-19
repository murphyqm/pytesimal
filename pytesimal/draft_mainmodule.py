#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 13/04/2021
by murphyqm

Making a new main module that will include the main functions
of the Pytesimal package:

## Main module
- Set-up function
- timestepping function
- function that manages overall flow

"""
import numpy as np


def set_up(
    timestep=1e11,
    r_planet=250000.0,
    core_size_factor=0.5,
    reg_fraction=0.032,
    max_time=400.0,
    dr=1000.0,
):
    # Set up list of timesteps
    myr = 3.1556926e13  # seconds in a million years
    max_time = max_time * myr  # max time in seconds
    times = np.arange(0, max_time + 0.5 * timestep, timestep)

    # calculate core radius
    r_core = (r_planet) * core_size_factor

    # set up arrays for the core and the mantle
    radii = np.arange(r_core, r_planet, dr)
    core_radii = np.arange(0, r_core - dr + 0.5 * dr, dr)

    # set up regolith
    reg_thickness = (reg_fraction * r_planet) * 1.0
    where_regolith = np.ones_like(radii)
    for i, r in enumerate(radii):
        d = r_planet - r
        if d < reg_thickness:
            where_regolith[i] = 0

    # Set up empty arrays for temperature
    mantle_temperature_array = np.zeros((radii.size, times.size))
    core_temperature_array = np.zeros((core_radii.size, times.size))

    return (
        r_core,
        radii,
        core_radii,
        reg_thickness,
        where_regolith,
        times,
        mantle_temperature_array,
        core_temperature_array,
    )
