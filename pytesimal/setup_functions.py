#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Define the geometry of planetesimal and set up required empty arrays.

This module allows the user to set up a basic geometry based on parameters
instead of manually defining 'numpy.ndarrays'.
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
    """
    Define the geometry and set up corresponding arrays.


    Parameters
    ----------
    timestep : float, default 1e11
        A timestep for the numerical discretisation
    r_planet : float, default 250000.0
        The radius of the planetesimal in m
    core_size_factor : float, < 1.0, default 0.5
        The core radius expressed as a fraction of `r_planet`
    reg_fraction : float, <1.0, default 0.032
        The core thickness expressed as a fraction of `r_planet`
    max_time : float, default 400.0
        Total time for model to run, in millions of years
    dr : float, default 1000.0
        Radial step for the numerical discretisation

    Returns
    -------
    r_core : float,
        Radius of the core in m
    radii : numpy.ndarray
        Numpy array of radius values in m for the mantle, with spacing defined
        by `dr`
    core_radii : numpy.ndarray
        Numpy array of radius values in m for the core, with spacing defined by
        `dr`
    reg_thickness : float
        Regolith thickness in m
    where_regolith : numpy.ndarray
        Boolean array with location of regolith
    times : numpy.ndarray
        Numpy array starting at 0 and going to 400 myr, with timestep
        controlling the spacing
    mantle_temperature_array : numpy.ndarray
        Numpy array of zeros to be filled with mantle temperatures
    core_temperature_array : numpy.ndarray
        Numpy array of zeros to be filled with core temperatures

    """
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
