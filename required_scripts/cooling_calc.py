#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Functions from Yang et al, 2010 to quickly compute the cooling rate of iron or stony iron meteorites, using "cloudy zone" particle diameter or tetrataenite bandwidth in nm.

Returns cooling rate in K/Myr.

Constants from Yang et al., 2010; obtained by comparing cz particles and tetrataenite bandwidth to modelled Ni diffusion in kamacite and taenite.
"""
def cz_cooling(d):
    """
    Cooling rate calculated using cloudy zone particle diameter in nm
    
    Arguments: d, cz particle size in nm
    Returns: cz_rate, the cooling rate in K/Myr
    """
    m = 7620000 #constant
    cz_rate = m / (d**2.9) # in K/Myr
    return(cz_rate)
    
    
def t_cooling(tw):
    """
    Cooling rate calculated using tetrataenite bandwidth in nm
    
    Arguments: tw, tetrataenite bandwidth in nm
    Returns: t_rate, the cooling rate in K/Myr
    """
    k = 14540000 #constant
    t_rate = k / (tw**2.3) # in K/Myr
    return(t_rate)

    
def to_seconds(cooling_rate):
    myr = 3.1556926E13
    new_cooling_rate = cooling_rate/myr #/1000000/365/24/60/60 # fix to myr
    return(new_cooling_rate)