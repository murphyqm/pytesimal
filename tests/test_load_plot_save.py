#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 13/05/2021
by murphyqm

"""
import numpy as np
from context import load_plot_save


def test_default_params(tmpdir):
    filepath = tmpdir.join('abc.txt')
    load_plot_save.make_default_param_file(filepath)
    (run_ID,
     folder,
     timestep,
     r_planet,
     core_size_factor,
     reg_fraction,
     max_time,
     temp_core_melting,
     mantle_heat_cap_value,
     mantle_density_value,
     mantle_conductivity_value,
     core_cp,
     core_density,
     temp_init,
     temp_surface,
     core_temp_init,
     core_latent_heat,
     kappa_reg,
     dr,
     cond_constant,
     density_constant,
     heat_cap_constant,
     ) = load_plot_save.load_params_from_file(filepath)
    # selecting some output to check:
    assert mantle_heat_cap_value == 819.0
    assert timestep == 100000000000.0
    assert cond_constant == 'y'


def test_myr_formatter():
    timestep = 10
    maxtime = 200
    (million_years,
     cooling_rate,
     myr) = load_plot_save.get_million_years_formatters(timestep,
                                                        maxtime)
    assert million_years(3, 2) == 0
    assert cooling_rate(30, 20) == -946707780000000
    assert myr == 31556926000000.0


def test_results_arrays_wlatent(tmpdir):
    result_filename = 'results'
    folder = tmpdir
    mantle_temperature_array = np.array([3, 5, 6, 7, 8])
    core_temperature_array = np.array([3, 5, 6, 7, 8])
    mantle_cooling_rates = np.array([3, 5, 6, 7, 8])
    core_cooling_rates = np.array([3, 5, 6, 7, 8])
    latent = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30]
    load_plot_save.save_result_arrays(
        result_filename,
        folder,
        mantle_temperature_array,
        core_temperature_array,
        mantle_cooling_rates,
        core_cooling_rates,
        latent,
    )
    filepath = str(tmpdir.join(str(result_filename) + '.npz'))
    print(filepath)
    (temperatures,
     coretemp,
     dT_by_dt,
     dT_by_dt_core,
     latent_array) = load_plot_save.read_datafile_with_latent(filepath)
    # check output
    assert latent_array == 12
    assert temperatures.mean() == 5.8
    assert coretemp.mean() == 5.8
    assert dT_by_dt.mean() == 5.8
    assert dT_by_dt_core.mean() == 5.8


def test_results_arrays(tmpdir):
    result_filename = 'results'
    folder = tmpdir
    mantle_temperature_array = np.array([3, 5, 6, 7, 8])
    core_temperature_array = np.array([3, 5, 6, 7, 8])
    mantle_cooling_rates = np.array([3, 5, 6, 7, 8])
    core_cooling_rates = np.array([3, 5, 6, 7, 8])
    load_plot_save.save_result_arrays(
        result_filename,
        folder,
        mantle_temperature_array,
        core_temperature_array,
        mantle_cooling_rates,
        core_cooling_rates,
    )
    filepath = str(tmpdir.join(str(result_filename) + '.npz'))
    print(filepath)
    (temperatures,
     coretemp,
     dT_by_dt,
     dT_by_dt_core) = load_plot_save.read_datafile(filepath)
    assert temperatures.mean() == 5.8
    assert coretemp.mean() == 5.8
    assert dT_by_dt.mean() == 5.8
    assert dT_by_dt_core.mean() == 5.8
