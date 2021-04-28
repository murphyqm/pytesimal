#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
To check that the package has installed, copy this file to a different dir
(outside of the pystesimal git folder) and try to run it from within
the pytesimal conda env (eg >> python3 quick_install_check.py)


Created on 26/04/2021
by murphyqm

"""

import pytesimal.setup_functions as mainmod

def test_small_set_up():
    (
        r_core,
        radii,
        core_radii,
        reg_thickness,
        where_regolith,
        times,
        mantle_temperature_array,
        core_temperature_array,
    ) = mainmod.set_up(
        timestep=2e11,
        r_planet=100000.0,
        core_size_factor=0.2,
        reg_fraction=0.10,
        max_time=100.0,
        dr=1000.0,
    )

    assert r_core == 20000.0
    assert radii.mean() == 59500.0
    assert core_radii.mean() == 9500.0
    assert reg_thickness == 10000.0
    assert where_regolith.size == 80
    assert where_regolith.sum() == 71.0
    assert mantle_temperature_array.shape == (80, 15779)
    assert mantle_temperature_array.sum() == 0.0
    assert core_temperature_array.shape == (20, 15779)
    assert core_temperature_array.sum() == 0.0
    assert times.size == 15779
    print("All assertions passed")


test_small_set_up()
print("Thanks for testing!")