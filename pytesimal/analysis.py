#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyse the results of the conductive cooling model for a planetesimal.

This module contains functions to calculate the cooling rates of meteorites
based on the empirical relations suggested by Yang et al. (2010); see full
references in
`Murphy Quinlan et al. (2021) <https://doi.org/10.1029/2020JE006726>`_. It
also contains functions to analyse the temperature arrays produced by the
`pytesimal.numerical_methods` module, allowing estimation of the depth of
genesis of pallasite meteorites, the relative timing of paleomagnetic
recording in meteorites and core dynamo action, and calculation of cooling
rates in the mantle of the planetesimal through time.

"""
import numpy as np


def core_freezing(
    coretemp, max_time, times, latent, temp_core_melting, timestep=1e11
):
    """
    Calculate when the core starts and finishes solidifying.

    Takes core temperature and returns boolean array of when the core is
    below the freezing/melting temperature.

    Parameters
    ----------
    coretemp : numpy.ndarray
        Array of temperatures in the core
    max_time : float
        Length of time the model runs for, in seconds
    times : numpy.ndarray
        Array from 0 to the max time +0.5* the timestep, with a spacing equal
        to the timestep
    latent : list
        List of total latent heat extracted since core began freezing, at each
        timestep
    temp_core_melting : float
        Melting point of core material (in K)
    timestep : float, default 1e11
        Discretisation timestep in seconds.

    Returns
    -------
    core_frozen: boolean array where temperature <= 1200
    times_frozen: array of indices of times where the temp <= 1200
    time_core_frozen: when the core starts to freeze, in seconds
    fully_frozen: when the core finished freezing, in seconds

    """
    # finding time where the core starts to freeze
    core_frozen = [coretemp <= temp_core_melting]
    # creates boolean array for temp<=1200
    times_frozen = np.where(core_frozen)[2]  # 0 and 1 give time = 0.0 Mya
    # np.where outputs indices where temp<=1200

    time_core_frozen = 0.0
    if time_core_frozen >= max_time or len(times_frozen) == 0.0:
        # print("Core freezes after max time")
        time_core_frozen = 0.0
        fully_frozen = 0.0
    else:
        time_core_frozen = times_frozen[0]
        # first time the temperature is less than 1200K
        time_core_frozen = (time_core_frozen) * (
            timestep
        )  # convert to seconds

    # find time core finishes freezing, time when latent heat is all
    # gone + time core started to freeze
    fully_frozen = times[len(latent)] + time_core_frozen
    return (core_frozen, times_frozen, time_core_frozen, fully_frozen)


def cooling_rate(temperature_array, timestep):
    """Calculate an array of cooling rates from temperature array."""
    dTdt = np.gradient(temperature_array, timestep, axis=1)
    return dTdt


def cooling_rate_cloudyzone_diameter(d):
    """
    Cooling rate calculated using cloudy zone particle diameter in nm.

    Constants from Yang et al., 2010; obtained by comparing cz particles and
    tetrataenite bandwidth to modelled Ni diffusion in kamacite and taenite.

    Parameters
    ----------
    d : float
        Cloudy zone particle size in nm

    Returns
    -------
    cz_rate : float
        The cooling rate in K/Myr

    """
    m = 7620000  # constant
    cz_rate = m / (d ** 2.9)  # in K/Myr
    return cz_rate


def cooling_rate_tetra_width(tw):
    """
    Cooling rate calculated using tetrataenite bandwidth in nm.

    Constants from Yang et al., 2010; obtained by comparing cz particles and
    tetrataenite bandwidth to modelled Ni diffusion in kamacite and taenite.

    Parameters
    ----------
    tw : float
        Tetrataenite bandwidth in nm

    Returns
    -------
    t_rate : float
        The cooling rate in K/Myr

    """
    k = 14540000  # constant
    t_rate = k / (tw ** 2.3)  # in K/Myr
    return t_rate


def cooling_rate_to_seconds(cooling_rate):
    """Convert cooling rates to seconds."""
    myr = 3.1556926e13
    new_cooling_rate = cooling_rate / myr  # /1000000/365/24/60/60 # fix to myr
    return new_cooling_rate


def meteorite_depth_and_timing(
    CR,
    temperatures,
    dT_by_dt,
    radii,
    r_planet,
    core_size_factor,
    time_core_frozen,
    fully_frozen,
    dr=1000.0,
    dt=1e11
):
    """
    Find depth of genesis given the cooling rate.

    Function finds the depth, given the cooling rate, and checks if the 593K
    contour crosses this depth during core solidification, implying whether or
    not the meteorite is expected to record core dynamo action.

    Parameters
    ----------
    CR : float
        cooling rate of meteorite
    temperatures : numpy.ndarray
        Array of mantle temperatures
    dT_by_dt : numpy.ndarray
        Array of mantle cooling rates
    radii : numpy.ndarray
        Mantle radii spaced by `dr`
    r_planet : float
        Planetesimal radius, in m
    core_size_factor : float, <1
        Radius of the core, expressed as a fraction of `r_planet`
    time_core_frozen : float
        The time the core begins to freeze
    fully_frozen : float
        The time the core is fully frozen
    dr : float, default 1000.0
        Radial step for numerical discretisation

    Returns
    -------
    depth : float
        Depth of genesis of meteorite
    string : string
        Relative timing of tetrataenite formation and core crystallisation, in
        a string format
    time_core_frozen : float
        The time the core begins to freeze
    Time_of_Crossing : float
        When the meteorite cools through tetrataenite formation temperature
    Critical_Radius : float
        Depth of meteorite genesis given as radius value

    """
    # Define two empty lists
    t_val = []  # for the 800K temperature contour
    dt_val = []  # cooling rate contour
    for ti in range(5, temperatures.shape[1]):

        # Find the index where temperatures are 800K by finding the minimum of
        # (a given temperature-800)
        index_where_800K_ish = np.argmin(
            np.absolute(temperatures[:, ti] - 800)
        )
        if (np.absolute(temperatures[index_where_800K_ish, ti] - 800)) > 10:
            continue

        # Find the index where dT_by_dt = meteorite cooling rate
        index_where_dtbydT = np.argmin(np.absolute(dT_by_dt[:, ti] + CR))
        if (np.absolute(dT_by_dt[index_where_dtbydT, ti] + CR)) > 1e-15:
            continue

        t_val.append(index_where_800K_ish)
        dt_val.append(index_where_dtbydT)

    # Find the points where they cross, this will lead to a depth of formation
    assert len(t_val) == len(
        dt_val
    ), "Contour length error!"  # flags an error if t_val and dt_val are not
    # the same length
    crosses = (
        np.array(t_val) - np.array(dt_val) == 0
    )  # boolean for if the indices of the two arrays are the same
    if not any(crosses):
        # The two lines do not cross
        string = "No cooling rate matched cooling history"
        return None, string, None, None, None

    # finding the depth of formation
    crossing_index2 = np.argmax(
        crosses
    )  # finds the first 'maximum' which is the first TRUE,
    # or the first crossing
    Critical_Radius = radii[
        dt_val[crossing_index2]
    ]  # radius where this first crossing occurs

    t_val2 = []  # for the 593K contour
    d_val = []
    for ti in range(5, temperatures.shape[1]):
        # Find the index where temperatures are 593K by finding the minimum of
        # (a given temperature-593)
        index_where_593K_ish = np.argmin(
            np.absolute(temperatures[:, ti] - 593)
        )
        if (np.absolute(temperatures[index_where_593K_ish, ti] - 593)) > 10:
            pass

        t_val2.append(index_where_593K_ish)
        d_val.append(
            ((Critical_Radius) / dr - ((r_planet / dr) * core_size_factor))
        )  # computes the depth, converts from radius to depth
    crossing = [
        np.array(t_val2) - d_val < 0.00001
    ]  # indices where computed depth crosses temperature contour (593 K)

    crossing_index = np.argmax(
        crossing
    )  # finds the first 'maximum' which is the first TRUE,
    # or the first crossing
    Time_of_Crossing = crossing_index * (dt)  # converts to seconds
    radii_index = int(((d_val)[crossing is True]))

    # check to see if the depth crosses the 593K contour during solidification
    # or before/after
    if time_core_frozen == 0:
        string = "Core Freezes after Max Time"
        depth = ((r_planet) - radii[int(((d_val)[crossing is True]))]) / dr
        return (depth, string, time_core_frozen, Time_of_Crossing)
    else:
        if radii_index > len(radii):
            string = "Core has finished solidifying"
            depth = 0
            return (depth, string, time_core_frozen, Time_of_Crossing)
        else:
            depth = ((r_planet) - radii[int(((d_val)[crossing is True]))]) / dr
            if Time_of_Crossing == 0:
                string = "hmm, see plot"  # lines cross at 0 time, doesn't tell
                # you when it formed
            if Time_of_Crossing < time_core_frozen and Time_of_Crossing != 0:
                string = "Core has not started solidifying yet"
            if time_core_frozen < Time_of_Crossing < fully_frozen:
                string = "Core has started solidifying"
            if Time_of_Crossing > fully_frozen:
                string = "Core has finished solidifying"
            return (
                depth,
                string,
                time_core_frozen,
                Time_of_Crossing,
                Critical_Radius,
            )
