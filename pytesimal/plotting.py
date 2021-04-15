#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 20:21:50 2020.

@author: Maeve Murphy Quinlan

Script to load example data stored as a compressed NumPy array and produce a
simple illustrative heatmap.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import matplotlib.ticker as plticker


def read_datafile(data_file):
    """
    Read the contents of a model run into numpy arrays.

    Reads the content of the numpy 'npz' data file representing
    a model run and returns arrays of the mntle temperature,
    core temperature, and cooling rates of the mantle and core.
    """
    with np.load(data_file) as data:
        temperatures = data["temperatures"]  # mantle temperatures in K
        coretemp = data["coretemp"]  # core temperatures in K
        dT_by_dt = data["dT_by_dt"]  # mantle cooling rates in K/1E11 s
        dT_by_dt_core = data["dT_by_dt_core"]  # core cooling rates in K/1E11 s

    return temperatures, coretemp, dT_by_dt, dT_by_dt_core


def get_million_years_formatters(timestep, maxtime):
    """
    Return a matplotlib formatters.

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

    Input temperature in a n-steps by n-depths array "temperatures" for the
    mantle and n-steps by n-depths array "coretemp" for the core. "timestep"
    is the length of a timestep and "maxtime" is the maximum time (both in
    seconds).

    Optional arguments fig and ax can be set to plot on existing matplotlib
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

    Input cooling rate in a n-steps by n-depths array "dT_by_dt" for the
    mantle and n-steps by n-depths array "dT_by_dt_core" for the core.
    "timestep" is the length of a timestep and "maxtime" is the maximum time
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
):
    """
    Return a heat map of depth vs time; colormap shows variation in temp.

    Change save="n" to save="y" when function is called to produce a png image
    named after the data filename

    """
    fig, axs = plt.subplots(2, 1, figsize=(fig_w, fig_h), sharey=True)
    ax, ax2 = axs

    # These probably belong in the data files...
    timestep = 1e11
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
