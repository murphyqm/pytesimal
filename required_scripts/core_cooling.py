#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# editing this to replace 0 with NaN
Created on Tue Feb 26 11:35:18 2019

@author: eememq
"""
import numpy as np

def core_freezing(coretemp, max_time, times, latent,temp_core_melting,timestep=1E11):
    """
    Function to calculate when the core freezes
    
    Takes core temperature and returns boolean array of when the core is 
    below the freezing/melting temperature

    Parameters
    ----------
    coretemp : ARRAY
        Array of temperatures in the core.
    max_time : FLOAT
        Length of time the model runs for.
    times : ARRAY
        DESCRIPTION.
    latent : FLOAT
        DESCRIPTION.
    temp_core_melting : FLOAT
        DESCRIPTION.
    timestep : FLOAT, optional
        DESCRIPTION. The default is 1E11.

    Returns
    -------
    None.

    """
    # finding time where the core starts to freeze
    core_frozen = [coretemp <= temp_core_melting]
    # creates boolean array for temp<=1200
    times_frozen = np.where(core_frozen)[2]
    # np.where outputs indices where temp<=1200

    time_core_frozen = 0.0
    if time_core_frozen >= max_time or len(times_frozen) == 0.0:
        print('Core freezes after max time')
        time_core_frozen = 0.0
        fully_frozen = 0.0
    else:
        time_core_frozen = times_frozen[2]
        # first time the temperature is less than 1200K
        # changed to 2 instead of 0
        time_core_frozen = (time_core_frozen)*(timestep)  # convert to seconds

    # find time core finishes freezing, time when latent heat is all
    # gone + time core started to freeze
    fully_frozen = times[len(latent)] + time_core_frozen
    print("core_frozen: " + str(core_frozen) + "; times_frozen: "
          + str(times_frozen) + "; time_core_frozen: " + str(time_core_frozen)
          + "; fully_frozen: " + str(fully_frozen))
    return(core_frozen, times_frozen, time_core_frozen, fully_frozen)
