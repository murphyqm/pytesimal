#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 14/04/2021
by murphyqm

"""
import numpy as np

from context import analysis
import pytest


def test_cloudy_zone():
    d_im = 147  # cz diameter in nm
    d_esq = 158  # cz diameter in nm
    im_cr = analysis.cooling_rate_cloudyzone_diameter(d_im)
    esq_cr = analysis.cooling_rate_cloudyzone_diameter(d_esq)
    assert im_cr == pytest.approx(3.9512517443065804)
    assert esq_cr == pytest.approx(3.2051578229316235)


def test_tetrataenite_bandwidth():
    width = 100
    cooling_rate = analysis.cooling_rate_tetra_width(width)
    assert cooling_rate == pytest.approx(365.22828714149324)


def test_cooling_rate_to_seconds():
    im_cr = 3.95
    esq_cr = 3.21
    im_cr_s = analysis.cooling_rate_to_seconds(im_cr)
    esq_cr_s = analysis.cooling_rate_to_seconds(esq_cr)
    assert im_cr_s == pytest.approx(1.2517062023088055e-13)
    assert esq_cr_s == pytest.approx(1.0172093441547507e-13)


def test_cooling_rate():
    temperatures = np.arange(16, 0, -1).reshape(4, 4)
    timestep = 10.0
    cooling_rates = analysis.cooling_rate(temperatures, timestep)
    comparison = np.full((4, 4), -0.1)
    np.testing.assert_array_almost_equal_nulp(cooling_rates, comparison)


def test_depth_and_timing(temperature_timestepping):
    CR = 1.2517062023088055e-13
    r_core = 125_000.0
    r_planet = 250_000.0
    dr = 1000.0
    dt = 1e11
    data = temperature_timestepping
    temperatures = data["mantle_temperature_array"]
    dT_by_dt = analysis.cooling_rate(temperatures, dt)
    radii = np.arange(r_core, r_planet, dr)
    core_size_factor = 0.5
    time_core_frozen = 5411100000000000.0
    fully_frozen = 7637200000000000.0
    (depth,
     string,
     time_core_frozen,
     Time_of_Crossing,
     Critical_Radius,) = analysis.meteorite_depth_and_timing(
        CR,
        temperatures,
        dT_by_dt,
        radii,
        r_planet,
        core_size_factor,
        time_core_frozen,
        fully_frozen,
        dr=1000.0,
    )
    assert depth == 57.0
    assert string == 'Core has started solidifying'
    assert Critical_Radius == 193000.0
    assert time_core_frozen == 5411100000000000.0
    assert Time_of_Crossing == 5849600000000000


def test_core_freezing(temperature_timestepping):
    myr = 3.1556926e13
    max_time = 400 * myr
    data = temperature_timestepping
    (
        core_frozen,
        times_frozen,
        time_core_frozen,
        fully_frozen,
    ) = analysis.core_freezing(
        coretemp=data["core_temperature_array"],
        max_time=max_time,
        times=data["times"],
        latent=data["latent"],
        temp_core_melting=data["temp_core_melting"],
        timestep=1e11,
    )
    assert time_core_frozen == 5411100000000000.0
    assert fully_frozen == 7637200000000000.0
