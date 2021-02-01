#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Function to calculate when the core solidifies.

See function docstring. To be incorporated into another module.
"""
import numpy as np
from contracts import contract


@contract(coretemp=np.ndarray,
          max_time=float,
          times=np.ndarray,
          latent=list,
          temp_core_melting='float,>0',
          timestep='float,>0',
          )
def core_freezing(coretemp, max_time, times, latent, temp_core_melting,
                  timestep=1E11):
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
        print('Core freezes after max time')
        time_core_frozen = 0.0
        fully_frozen = 0.0
    else:
        time_core_frozen = times_frozen[0]
        # first time the temperature is less than 1200K
        time_core_frozen = (time_core_frozen)*(timestep)  # convert to seconds

    # find time core finishes freezing, time when latent heat is all
    # gone + time core started to freeze
    fully_frozen = times[len(latent)] + time_core_frozen
    print("core_frozen: " + str(core_frozen) + "; times_frozen: "
          + str(times_frozen) + "; time_core_frozen: " + str(time_core_frozen)
          + "; fully_frozen: " + str(fully_frozen))
    return(core_frozen, times_frozen, time_core_frozen, fully_frozen)
