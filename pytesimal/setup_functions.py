#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Define the geometry of planetesimal and set up required empty arrays.

This module allows the user to set up a basic geometry based on parameters
instead of manually defining 'numpy.ndarrays'. It also provides a
`workflow` function which follows a basic default workflow, with parameters
set by an input parameter file, and results saved as a json file and as
compressed numpy arrays. These results files can then be loaded and analysed,
with meteorite results calculated and the results plotted.
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


def workflow(filename, folder_path): # set folder = folder path if you want results saved in same loc as params file
    """
    Still under development

    Saves a results file (json format, .txt) and a results array file (.npz)
    to the folder specified in the parameter file. If you want the results to
    save to the same folder that the parameter file is in, ensure that the
    field "folder" in the json parameter file is the same as `folder_path`.

    Results files will be saved under the `filename` with `_results` and the
    appropriate file extension appended.

    Parameters
    ----------
    filename : str
        The filename of the parameters file to read in, without file extension.
        File must be in json format with a .txt extension. It's recommended to
        generate an example parameters file using the
        `pytesimal.load_plot_save.make_default_param_file(filepath)` function
        and edit the default settings in this file
    folder_path : str
        The absolute path to the directory that holds the parameters file. If
        the "folder" field of the parameters file == `folder_path`, the results
        file will be saved alongside the parameters file.

    """
    import pytesimal.load_plot_save # justmoving these here for now for testing
    import pytesimal.core_function
    import pytesimal.mantle_properties
    import pytesimal.numerical_methods
    import pytesimal.analysis
    filepath = f"{folder_path}/{filename}.txt"
    (run_ID, folder, timestep, r_planet, core_size_factor,
     reg_fraction, max_time, temp_core_melting, olivine_cp,
     olivine_density, cmb_conductivity, core_cp, core_density,
     temp_init, temp_surface, core_temp_init, core_latent_heat,
     kappa_reg, dr, cond_constant, density_constant,
     heat_cap_constant
     ) = pytesimal.load_plot_save.load_params_from_file(filepath)
    pytesimal.load_plot_save.check_folder_exists(folder)
    (r_core,
     radii,
     core_radii,
     reg_thickness,
     where_regolith,
     times,
     mantle_temperature_array,
     core_temperature_array) = set_up(timestep,
                                      r_planet,
                                      core_size_factor,
                                      reg_fraction,
                                      max_time,
                                      dr)
    latent = []

    core_values = pytesimal.core_function.IsothermalEutecticCore(
        temp=core_temp_init,
        melt=temp_core_melting,
        outer_r=r_core,
        inner_r=0,
        rho=core_density,
        cp=core_cp,
        core_latent_heat=core_latent_heat)
    (mantle_conductivity,
     mantle_heatcap,
     mantle_density) = pytesimal.mantle_properties.set_up_mantle_properties(
        cond_constant,
        density_constant,
        heat_cap_constant,
        olivine_density,
        olivine_cp,
        cmb_conductivity, )

    top_mantle_bc = pytesimal.numerical_methods.surface_dirichlet_bc
    bottom_mantle_bc = pytesimal.numerical_methods.cmb_dirichlet_bc

    (mantle_temperature_array,
     core_temperature_array,
     latent,
     ) = pytesimal.numerical_methods.discretisation(
        core_values,
        latent,
        temp_init,
        core_temp_init,
        top_mantle_bc,
        bottom_mantle_bc,
        temp_surface,
        mantle_temperature_array,
        dr,
        core_temperature_array,
        timestep,
        r_core,
        radii,
        times,
        where_regolith,
        kappa_reg,
        mantle_conductivity,
        mantle_heatcap,
        mantle_density)

    (core_frozen,
     times_frozen,
     time_core_frozen,
     fully_frozen) = pytesimal.analysis.core_freezing(core_temperature_array,
                                                      max_time,
                                                      times,
                                                      latent,
                                                      temp_core_melting,
                                                      timestep)
    mantle_cooling_rates = pytesimal.analysis.cooling_rate(
        mantle_temperature_array,
        timestep)
    core_cooling_rates = pytesimal.analysis.cooling_rate(
        core_temperature_array,
        timestep)
    result_filename = f"{filename}_results"
    pytesimal.load_plot_save.save_params_and_results(
        result_filename,
        run_ID,
        folder,
        timestep,
        r_planet,
        core_size_factor,
        reg_fraction,
        max_time,
        temp_core_melting,
        olivine_cp,
        olivine_density,
        cmb_conductivity,
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
        time_core_frozen,
        fully_frozen,)

    pytesimal.load_plot_save.save_result_arrays(
        result_filename,
        folder,
        mantle_temperature_array,
        core_temperature_array,
        mantle_cooling_rates,
        core_cooling_rates)
