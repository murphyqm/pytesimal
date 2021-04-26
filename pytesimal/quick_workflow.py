#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Set up complete runs with a single function call and a parameter file.

This module provides a simple
`workflow` function which follows a basic default workflow, with parameters
set by an input parameter file, and results saved as a json file and as
compressed numpy arrays. These results files can then be loaded and analysed,
with meteorite results calculated and the results plotted.

The function takes two arguments, `filename` which is the name of a parameters
file to be loaded, without the extension (the extension of the file must be
.txt). The location of this input file is given by `folder_path` which should
be the relative or absolute path to the location of the parameters file.
Within this parameters file, the "folder" field defines the path of the
directory where results

"""

from . import setup_functions
from . import load_plot_save
from . import core_function
from . import mantle_properties
from . import numerical_methods
from . import analysis


def workflow(
    filename, folder_path
):  # set folder = folder path if you want results saved in same loc as params file
    """
    Run model in full with parameters set by an input file.

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
    filepath = f"{folder_path}/{filename}.txt"
    (
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
    ) = load_plot_save.load_params_from_file(filepath)
    load_plot_save.check_folder_exists(folder)
    (
        r_core,
        radii,
        core_radii,
        reg_thickness,
        where_regolith,
        times,
        mantle_temperature_array,
        core_temperature_array,
    ) = setup_functions.set_up(
        timestep, r_planet, core_size_factor, reg_fraction, max_time, dr
    )
    latent = []

    core_values = core_function.IsothermalEutecticCore(
        initial_temperature=core_temp_init,
        melting_temperature=temp_core_melting,
        outer_r=r_core,
        inner_r=0,
        rho=core_density,
        cp=core_cp,
        core_latent_heat=core_latent_heat,
    )
    (
        mantle_conductivity,
        mantle_heatcap,
        mantle_density,
    ) = mantle_properties.set_up_mantle_properties(
        cond_constant,
        density_constant,
        heat_cap_constant,
        olivine_density,
        olivine_cp,
        cmb_conductivity,
    )

    top_mantle_bc = numerical_methods.surface_dirichlet_bc
    bottom_mantle_bc = numerical_methods.cmb_dirichlet_bc

    (
        mantle_temperature_array,
        core_temperature_array,
        latent,
    ) = numerical_methods.discretisation(
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
        mantle_density,
    )

    (
        core_frozen,
        times_frozen,
        time_core_frozen,
        fully_frozen,
    ) = analysis.core_freezing(
        core_temperature_array,
        max_time,
        times,
        latent,
        temp_core_melting,
        timestep,
    )
    mantle_cooling_rates = analysis.cooling_rate(
        mantle_temperature_array, timestep
    )
    core_cooling_rates = analysis.cooling_rate(
        core_temperature_array, timestep
    )
    result_filename = f"{filename}_results"
    load_plot_save.save_params_and_results(
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
        fully_frozen,
    )

    load_plot_save.save_result_arrays(
        result_filename,
        folder,
        mantle_temperature_array,
        core_temperature_array,
        mantle_cooling_rates,
        core_cooling_rates,
    )
