#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 14/04/2021
by murphyqm

"""
import numpy as np


def core_freezing(
    coretemp, max_time, times, latent, temp_core_melting, timestep=1e11
):
    """
    Calculate when the core starts and finishes solidifying.

    Takes core temperature and returns boolean array of when the core is
    below the freezing/melting temperature

    Parameters
    ----------
    coretemp : ARRAY
        Array of temperatures in the core.
    max_time : FLOAT
        Length of time the model runs for.
    times : ARRAY
        Array from 0 to the max time +0.5* the timestep, with a spacing equal
        to the timestep
    latent : LIST
        List of total latent heat extracted since core began freezing, at each
        timestep
    temp_core_melting : FLOAT
        DMelting point of core material (in K)
    timestep : FLOAT, optional
        Discretisation timestep in seconds. The default is 1E11.

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
        print("Core freezes after max time")
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
    print(
        "core_frozen: "
        + str(core_frozen)
        + "; times_frozen: "
        + str(times_frozen)
        + "; time_core_frozen: "
        + str(time_core_frozen)
        + "; fully_frozen: "
        + str(fully_frozen)
    )
    return (core_frozen, times_frozen, time_core_frozen, fully_frozen)


def cooling_rate(temperature_array, timestep):
    dTdt = np.gradient(temperature_array, timestep, axis=1)
    return dTdt


"""
Cooling rate calculation.

Functions from Yang et al, 2010 to quickly compute the cooling rate of iron or
stony iron meteorites, using "cloudy zone" particle diameter or tetrataenite
bandwidth in nm.

Returns cooling rate in K/Myr.

Constants from Yang et al., 2010; obtained by comparing cz particles and
tetrataenite bandwidth to modelled Ni diffusion in kamacite and taenite.
"""


def cooling_rate_cloudyzone_diameter(d):  # TODO add reference
    """
    Cooling rate calculated using cloudy zone particle diameter in nm.

    Arguments: d, cz particle size in nm
    Returns: cz_rate, the cooling rate in K/Myr
    """
    m = 7620000  # constant
    cz_rate = m / (d ** 2.9)  # in K/Myr
    return cz_rate


def cooling_rate_tetra_width(tw):
    """
    Cooling rate calculated using tetrataenite bandwidth in nm.

    Arguments: tw, tetrataenite bandwidth in nm
    Returns: t_rate, the cooling rate in K/Myr
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
    dr=1000,
):
    """
    Find depth of genesis given the cooling rate.

    function finding the depth, given the cooling rate, and checks if the 593K
    contour crosses this depth during core solidification

    Parameters
    ----------
    CR : TYPE
        DESCRIPTION.
    temperatures : TYPE
        DESCRIPTION.
    dT_by_dt : TYPE
        DESCRIPTION.
    radii : TYPE
        DESCRIPTION.
    r_planet : TYPE
        DESCRIPTION.
    core_size_factor : TYPE
        DESCRIPTION.
    time_core_frozen : TYPE
        DESCRIPTION.
    fully_frozen : TYPE
        DESCRIPTION.
    dr : TYPE, optional
        DESCRIPTION. The default is 1000.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    # Define two empty lists
    t_val = []  # for the 800K temperature contour
    dt_val = []  # cooling rate contour
    for ti in range(5, temperatures.shape[1]):  # changing this 5 did not work

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

        t_val.append(
            index_where_800K_ish
        )  # dividing both these by 2 didn't work
        dt_val.append(index_where_dtbydT)  # this one too

    # Find the points where they cross, this will lead to a depth of formation
    assert len(t_val) == len(
        dt_val
    ), "Contour length error!"  # flags an errror if t_val and dt_val are not
    # the same length
    crosses = (
        np.array(t_val) - np.array(dt_val) == 0
    )  # boolean for if the indecies of the two arrays are the same
    if not any(crosses):
        # The two lines do not cross
        x = "No cooling rate matched cooling history"
        return None, x, None, None, None

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
        # print(d_val)
        # added int to line above to try and solve - removing this now and
        # instead changing below line
    crossing = [
        np.array(t_val2) - d_val < 0.00001
    ]  # indicies where computed depth crosses temperature contour (593 K)

    crossing_index = np.argmax(
        crossing
    )  # finds the first 'maximum' which is the first TRUE,
    # or the first crossing
    Time_of_Crossing = crossing_index * (10 ** 11)  # converts to seconds
    radii_index = int(((d_val)[crossing is True]))

    # check to see if the depth crosses the 593K contour during solidification
    # or before/after
    if time_core_frozen == 0:
        x = "Core Freezes after Max Time"
        depth = ((r_planet) - radii[int(((d_val)[crossing is True]))]) / dr
        return (depth, x, time_core_frozen, Time_of_Crossing)
    else:
        if radii_index > len(radii):
            x = "Core has finished solidifying"
            depth = 0
            return (depth, x, time_core_frozen, Time_of_Crossing)
        else:
            depth = ((r_planet) - radii[int(((d_val)[crossing is True]))]) / dr
            if Time_of_Crossing == 0:
                x = "hmm, see plot"  # lines cross at 0 time, but doesn't tell
                # you when it formed
            if Time_of_Crossing < time_core_frozen and Time_of_Crossing != 0:
                x = "Core has not started solidifying yet"
            if time_core_frozen < Time_of_Crossing < fully_frozen:
                x = "Core has started solidifying"
            if Time_of_Crossing > fully_frozen:
                x = "Core has finished solidifying"
            # depth = depth of formation; x = statement on result;
            # time_core_frozen = self explanatory; Time_of_crossing = when the
            # meteorite cools through curie T
            # Critical Radius = radius version of depth
            return (
                depth,
                x,
                time_core_frozen,
                Time_of_Crossing,
                Critical_Radius,
            )
