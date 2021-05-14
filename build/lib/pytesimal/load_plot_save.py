#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Load Plot and Save Module

This module contains functions to load parameters and results from files, to
plot results either following a model run or from file, and to save parameters
and results to file following a model run.

Example
-------

A directory and parameter file can be quickly generated::

    folder = 'path/to/folder'
    filename = 'example_param_file.txt'
    filepath=f'{folder}/{filename}'

    check_folder_exists(folder)
    make_default_param_file(filepath=filepath)

This parameters file in json format can then be opened, edited, renamed or
moved, and loaded in to set parameter values for a model run.

Notes
-----

Depending on usage, some functions take a `folder` and `filename` argument and
create an absolute path with these to save or load a file, while some take
a full filepath. Please check which argument is required.

"""

import json
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import matplotlib.ticker as plticker


def check_folder_exists(folder):
    """Check directory exists and make directory if not."""
    if not os.path.isdir(str(folder)):
        os.makedirs(str(folder))


def make_default_param_file(filepath="example_params.txt"):
    """Save an example parameter json file with default parameters."""
    default_variables = {
        "run_ID": "example_default",
        "folder": "example_default",
        "timestep": 1e11,
        "r_planet": 250000.0,
        "core_size_factor": 0.5,
        "reg_fraction": 0.032,
        "max_time": 400,
        "temp_core_melting": 1200.0,
        "mantle_heat_cap_value": 819.0,
        "mantle_density_value": 3341.0,
        "mantle_conductivity_value": 3.0,
        "core_cp": 850.0,
        "core_density": 7800.0,
        "temp_init": 1600.0,
        "temp_surface": 250.0,
        "core_temp_init": 1600.0,
        "core_latent_heat": 270000.0,
        "kappa_reg": 5.0e-8,
        "dr": 1000.0,
        "cond_constant": "y",
        "density_constant": "y",
        "heat_cap_constant": "y",
    }

    with open(filepath, "w") as file:
        json.dump(default_variables, file, indent=4)


def load_params_from_file(filepath="example_params.txt"):
    """Load parameters from a json file and return variable values."""
    with open(filepath) as json_file:
        data = json.load(json_file)
        run_ID = data["run_ID"]
        folder = data["folder"]
        timestep = data["timestep"]
        r_planet = data["r_planet"]
        core_size_factor = data["core_size_factor"]
        reg_fraction = data["reg_fraction"]
        max_time = data["max_time"]
        temp_core_melting = data["temp_core_melting"]
        mantle_heat_cap_value = data["mantle_heat_cap_value"]
        mantle_density_value = data["mantle_density_value"]
        mantle_conductivity_value = data["mantle_conductivity_value"]
        core_cp = data["core_cp"]
        core_density = data["core_density"]
        temp_init = data["temp_init"]
        temp_surface = data["temp_surface"]
        core_temp_init = data["core_temp_init"]
        core_latent_heat = data["core_latent_heat"]
        kappa_reg = data["kappa_reg"]
        dr = data["dr"]
        cond_constant = data["cond_constant"]
        density_constant = data["density_constant"]
        heat_cap_constant = data["heat_cap_constant"]
        return (
            run_ID,
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
        )


def save_params_and_results(
    result_filename,
    run_ID,
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
    time_core_frozen,
    fully_frozen,
    meteorite_results="None given",
    latent_list_len=0,
):
    """
    Save parameters and results from model run to a json file.

    Save the parameters used, core crystallisation timing, and meteorite
    results to a json file. The resulting file can also be read in as a
    parameter file to reproduce the same modelling run.

    Meteorite results can be excluded, or can be passed in as a string, value,
    or dictionary of results.

    Parameters
    ----------
    result_filename : str
        Filename without file suffix; .txt will be appended when the file is
        saved.
    run_ID : str
        Identifier for the specific model run.
    folder : str
        Absolute path to directory where file is to be saved. Existence of
        the directory can be checked with the `check_folder_exists()` function.
    timestep : float
        The timestep used in numerical method.
    r_planet : float
        The radius of the planet in m
    core_size_factor : float
        The core size as a fraction of the total planet radius.
    reg_fraction : float
        The regolith thickness as a fraction of the total planet radius.
    max_time : float
        The total run-time of the model, in millions of years (Myr).
    temp_core_melting : float
        The melting temperature of the core.
    mantle_heat_cap_value: float
        The heat capacity of mantle material.
    mantle_density_value : float
         The density of mantle material.
    mantle_conductivity_value : float
        The conductivity of the mantle.
    core_cp : float
        The heat capacity of the core.
    core_density : float
        The density of the core.
    temp_init : float, list, numpy array
        The initial temperature of the body.
    temp_surface : float
        The surface temperature of the planet.
    core_temp_init : float
        The initial temperature of the core
    core_latent_heat : float
        The latent heat of crystallisation of the core.
    kappa_reg : float
        The regolith constant diffusivity
    dr : float
        The radial step used in the numerical model.
    cond_constant : str
        Flag of `y` or `n` to specify if mantle conductivity is constant.
    density_constant : str
        Flag of `y` or `n` to specify if mantle density is constant.
    heat_cap_constant : str
        Flag of `y` or `n` to specify if mantle heat capacity is constant.
    time_core_frozen : float
        Time when the core begins to freeze in Myr.
    fully_frozen : float
        Time when the core finishes freezing, in Myr.
    meteorite_results : dict, str, float, list, optional
        Depth and timing results of meteorites, can be passed as a dictionary
        of results for different samples, as a list of results, or as a single
        result in the form of a float or string.
    latent_list_len : float, optional
        The length of the latent heat list, needed for further analysis of
        core crystallisation duration at a later point.

    Returns
    -------
    File is saved to `folder`/`result_filename`.txt in the json format.

    """
    myr = 3.1556926e13
    data = {
        "run_ID": run_ID,
        "folder": folder,
        "timestep": timestep,
        "r_planet": r_planet,
        "core_size_factor": core_size_factor,
        "reg_fraction": reg_fraction,
        "max_time": max_time,
        "temp_core_melting": temp_core_melting,
        "mantle_heat_cap_value": mantle_heat_cap_value,
        "mantle_density_value": mantle_density_value,
        "mantle_conductivity_value": mantle_conductivity_value,
        "core_cp": core_cp,
        "core_density": core_density,
        "temp_init": temp_init,
        "temp_surface": temp_surface,
        "core_temp_init": core_temp_init,
        "core_latent_heat": core_latent_heat,
        "kappa_reg": kappa_reg,
        "dr": dr,
        "cond_constant": cond_constant,
        "density_constant": density_constant,
        "heat_cap_constant": heat_cap_constant,
        "core_begins_to_freeze": time_core_frozen / myr,
        "core finishes freezing": fully_frozen / myr,
        "meteorite_results": meteorite_results,
        "latent_list_len": latent_list_len,
    }
    with open(f"{folder}/{result_filename}.txt", "w") as file:
        json.dump(data, file, indent=4)


def save_result_arrays(
    result_filename,
    folder,
    mantle_temperature_array,
    core_temperature_array,
    mantle_cooling_rates,
    core_cooling_rates,
    latent=[],
):
    """
    Save results as a compressed Numpy array (npz).

    Result arrays of temperatures and cooling rates for both the mantle and the
    core (numpy arrays) are saved to a specified file.

    Parameters
    ----------
    result_filename : str
        Filename without file suffix; .npz will be appended when the file is
        saved.
    folder : str
        Absolute path to directory where file is to be saved. Existence of
        the directory can be checked with the `check_folder_exists()` function.
    mantle_temperature_array : numpy.ndarray
        Temperatures in the mantle for all radii through time.
    core_temperature_array : numpy.ndarray
        Temperatures in the core through time.
    mantle_cooling_rates : numpy.ndarray
        Cooling rates in the mantle for all radii through time.
    core_cooling_rates : numpy.ndarray
        Cooling rates in the core through time.
    latent: list, optional
        List of latent heat values for the core; needed to
        calculate timing of core crystallisation.

    Returns
    -------
    File is saved to `folder`/`result_filename`.npz in the compressed Numpy
    array format.

    """
    np.savez_compressed(
        f"{folder}/{result_filename}.npz",
        temperatures=mantle_temperature_array,
        coretemp=core_temperature_array,
        dT_by_dt=mantle_cooling_rates,
        dT_by_dt_core=core_cooling_rates,
        latent_array=np.array(len(latent))
    )


def read_datafile(filepath):
    """
    Read the contents of a model run into numpy arrays.

    Reads the content of the numpy 'npz' data file representing
    a model run and returns arrays of the mantle temperature,
    core temperature, and cooling rates of the mantle and core.
    """
    with np.load(filepath) as data:
        temperatures = data["temperatures"]  # mantle temperatures in K
        coretemp = data["coretemp"]  # core temperatures in K
        dT_by_dt = data["dT_by_dt"]  # mantle cooling rates in K/1E11 s
        dT_by_dt_core = data["dT_by_dt_core"]  # core cooling rates in K/1E11 s

    return temperatures, coretemp, dT_by_dt, dT_by_dt_core


def read_datafile_with_latent(filepath):
    """
    Read contents of a model run into numpy arrays, including latent heat.

    Reads the content of the numpy 'npz' data file representing
    a model run and returns arrays of the mantle temperature,
    core temperature, cooling rates of the mantle and core,
    and the number of timesteps the core was crystallising for.
    """
    with np.load(filepath) as data:
        temperatures = data["temperatures"]  # mantle temperatures in K
        coretemp = data["coretemp"]  # core temperatures in K
        dT_by_dt = data["dT_by_dt"]  # mantle cooling rates in K/1E11 s
        dT_by_dt_core = data["dT_by_dt_core"]  # core cooling rates in K/1E11 s
        latent_array = data["latent_array"]  # tsteps in core crystallisation

    return temperatures, coretemp, dT_by_dt, dT_by_dt_core, latent_array


def get_million_years_formatters(timestep, maxtime):
    """
    Return a matplotlib formatter.

    Creates two matplotlib formatters, one to go from timesteps to myrs and
    one to go from cooling rate per timestep to cooling rate per million years.
    """
    myr = 3.1556926e13  # seconds in a million years

    def million_years(x, pos):
        """
        Tick formatter to go from timesteps to myrs.

        This gets called for each tick value in the plot with the x coordinate
        and a position (which may be None) and returns a string to be used as
        the value to be plotted on the axis of the graph. This retuns a time
        in millions of years, rounded to look nice
        """
        value = (x * timestep) / myr
        value_rounded = round(value, -2)
        value_int = int(value_rounded)
        return value_int

    def cooling_rate(x, pos):
        """Tick formatter to Converting cooling rate to K/myrs."""
        return int(x * myr * -1)

    return million_years, cooling_rate, myr


def plot_temperature_history(
    temperatures,
    coretemp,
    timestep,
    maxtime,
    ax=None,
    fig=None,
    savefile=None,
    fig_w=8,
    fig_h=6,
    show=True,
):
    """
    Generate a heat map of depth vs time; colormap shows variation in temp.

    Input temperature in a n-steps by n-depths array `temperatures` for the
    mantle and n-steps by n-depths array `coretemp` for the core. `timestep`
    is the length of a timestep and `maxtime` is the maximum time (both in
    seconds).

    Optional arguments `fig` and `ax` can be set to plot on existing matplotlib
    figure and axis objects. Passing a string via outfile causes the figure
    to be saved as an image in a file.

    """
    million_years, _, myr = get_million_years_formatters(timestep, maxtime)

    # What if only ax or fig are set? Only need fig for cbar really...
    if (fig is None) and (ax is None):
        fig, ax = plt.subplots(figsize=(fig_w, fig_h))

    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontsize(8)
    formatter = FuncFormatter(million_years)
    ax.xaxis.set_major_formatter(formatter)
    im = ax.imshow(
        np.concatenate(
            (temperatures[-1:0:-1, :], coretemp[-1:0:-1, :]), axis=0
        ),
        aspect="auto",
        cmap="magma",
    )
    ticker_step = (100 * myr) / timestep
    loc = plticker.MultipleLocator(
        base=ticker_step
    )  # this locator puts ticks at regular intervals
    ax.xaxis.set_major_locator(loc)
    ax.set_xlabel("Time (Myr)")
    ax.set_ylabel("Depth (km)")
    ax.xaxis.label.set_size(8)
    ax.yaxis.label.set_size(8)

    ax.set_title(
        "(a) Planetesimal temperatures through time", fontsize=8,
    )

    cb = fig.colorbar(im, ax=ax)
    cb.set_label("Temperature (K)", fontsize=8)
    cb.ax.tick_params(labelsize=8)

    if savefile is not None:
        plt.savefig(savefile, dpi=300, bbox_inches="tight")
    if show:
        plt.show()

    return fig, ax


def plot_coolingrate_history(
    dT_by_dt,
    dT_by_dt_core,
    timestep,
    maxtime,
    ax=None,
    fig=None,
    savefile=None,
    fig_w=8,
    fig_h=6,
    show=True,
):
    """
    Generate a heat map of cooling rate vs time.

    Generate a heat map of cooling rate vs time, with the colormap showing
    variation in cooling rate.

    Input cooling rate in a n-steps by n-depths array `dT_by_dt` for the
    mantle and n-steps by n-depths array `dT_by_dt_core` for the core.
    `timestep` is the length of a timestep and `maxtime` is the maximum time
    (both in seconds).

    Optional arguments fig and ax can be set to plot on existing matplotlib
    figure and axis objects. Passing a string via outfile causes the figure
    to be saved as an image in a file.

    """
    million_years, cooling_rate, myr = get_million_years_formatters(
        timestep, maxtime
    )

    # What if only ax or fig are set? Only need fig for cbar really...
    if (fig is None) and (ax is None):
        fig, ax = plt.subplots(figsize=(fig_w, fig_h))

    im2 = ax.imshow(
        np.concatenate(
            (dT_by_dt[-1:0:-1, :], dT_by_dt_core[-1:0:-1, :]), axis=0
        ),
        aspect="auto",
        vmin=-6e-13,
        cmap="magma",
    )
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontsize(8)
    formatter = FuncFormatter(million_years)
    ax.xaxis.set_major_formatter(formatter)

    ticker_step = (100 * myr) / timestep
    loc = plticker.MultipleLocator(
        base=ticker_step
    )  # this locator puts ticks at regular intervals
    ax.xaxis.set_major_locator(loc)

    ax.set_xlabel("Time (Myr)")
    ax.set_ylabel("Depth (km)")
    ax.xaxis.label.set_size(8)
    ax.yaxis.label.set_size(8)

    ax.set_title("(b) Planetesimal cooling rates through time", fontsize=8)
    fmt1 = plticker.FuncFormatter(cooling_rate)
    cb2 = fig.colorbar(im2, ax=ax, format=fmt1, extend="min")
    cb2.set_label("Cooling Rate (K/Myr)", fontsize=8)
    cb2.ax.tick_params(labelsize=8)
    cb2.ax.invert_yaxis()

    if savefile is not None:
        plt.savefig(savefile, dpi=300, bbox_inches="tight")
    if show:
        plt.show()

    return fig, ax


def two_in_one(
    fig_w,
    fig_h,
    temperatures,
    coretemp,
    dT_by_dt,
    dT_by_dt_core,
    savefile=None,
    timestep=1e11
):
    """
    Return a heat map of depth vs time; colormap shows variation in temp.

    Change save="n" to save="y" when function is called to produce a png
    image named after the data filename

    """
    fig, axs = plt.subplots(2, 1, figsize=(fig_w, fig_h), sharey=True)
    ax, ax2 = axs

    # These probably belong in the data files...
    # timestep = 1e11
    maxtime = 400 * 3.1556926e13

    fig, ax = plot_temperature_history(
        temperatures,
        coretemp,
        timestep,
        maxtime,
        ax=ax,
        fig=fig,
        savefile=None,
        show=False,
    )

    fig, ax2 = plot_coolingrate_history(
        dT_by_dt,
        dT_by_dt_core,
        timestep,
        maxtime,
        ax=ax2,
        fig=fig,
        savefile=None,
        show=True,
    )

    if savefile is not None:
        plt.savefig(savefile, dpi=300, bbox_inches="tight")
    else:
        plt.show()


if __name__ == "__main__":
    import argparse

    # Read and process command line arguments
    parser = argparse.ArgumentParser(
        description="Plot planetesimal cooling history."
    )
    parser.add_argument("datafile", help="Cooling history file name.")
    parser.add_argument(
        "-s",
        "--savefile",
        action="store",
        type=str,
        help="Filename for saving figure as image. "
        + "If not set figure is plotted directly.",
    )
    parser.add_argument(
        "--fig_height", default=9, help="Figure height in inches"
    )
    parser.add_argument(
        "--fig_width", default=6, help="Figure width in inches"
    )
    args = parser.parse_args()
    fig_w = args.fig_width
    fig_h = args.fig_height

    # Read data and make grap
    temperatures, coretemp, dT_by_dt, dT_by_dt_core = read_datafile(
        args.datafile
    )
    two_in_one(
        fig_w,
        fig_h,
        temperatures,
        coretemp,
        dT_by_dt,
        dT_by_dt_core,
        savefile=args.savefile,
    )
